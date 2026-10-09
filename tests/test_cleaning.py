"""
Unit tests for data loader, column mapping, and cleaning functions in CarScope.
"""

import pytest
import pandas as pd
import numpy as np
from src.cleaning import extract_numeric, standardize_text, clean_dataset
from src.column_mapping import auto_suggest_mappings


def test_extract_numeric():
    assert extract_numeric("$24,500") == 24500.0
    assert extract_numeric("31,000 mi") == 31000.0
    assert extract_numeric("2.0 L") == 2.0
    assert extract_numeric("150 hp") == 150.0
    assert extract_numeric("15.5") == 15.5
    assert extract_numeric(100) == 100.0
    assert np.isnan(extract_numeric(None))
    assert np.isnan(extract_numeric("N/A"))
    assert np.isnan(extract_numeric("unknown"))


def test_standardize_text():
    assert standardize_text("  toyota ") == "Toyota"
    assert standardize_text("HONDA civic ") == "Honda Civic"
    assert standardize_text(None) is np.nan
    assert standardize_text("n/a") is np.nan


def test_auto_suggest_mappings():
    raw_cols = ["Manufacturer", "Selling_Price", "Odometer", "Year", "Fuel_Type", "Power"]
    suggestions = auto_suggest_mappings(raw_cols)

    assert suggestions["make"] == "Manufacturer"
    assert suggestions["price"] == "Selling_Price"
    assert suggestions["mileage"] == "Odometer"
    assert suggestions["year"] == "Year"
    assert suggestions["fuel_type"] == "Fuel_Type"
    assert suggestions["horsepower"] == "Power"


def test_clean_dataset():
    raw_df = pd.DataFrame({
        "Manufacturer": ["Toyota", "Toyota", "Honda", "Ford"],
        "Model": ["Camry", "Camry", "Civic", "Mustang"],
        "Year": [2021, 2021, 2022, 2020],
        "Price": ["$24,500", "$24,500", "$22,000", "-$5,000"],  # Note suspicious negative price
        "Odometer": ["28,000 mi", "28,000 mi", "15,000 mi", "30,000 mi"]
    })

    col_mapping = auto_suggest_mappings(raw_df.columns.tolist())
    cleaned_df, report = clean_dataset(raw_df, col_mapping, drop_duplicates_flag=True)

    assert report["raw_rows"] == 4
    assert report["removed_duplicates"] == 1
    assert len(cleaned_df) == 3
    assert "car_id" in cleaned_df.columns
    assert cleaned_df["price"].iloc[0] == 24500.0
    assert cleaned_df["mileage"].iloc[0] == 28000.0
    # Negative price should be flagged as outlier
    assert report["flagged_outliers"] >= 1
