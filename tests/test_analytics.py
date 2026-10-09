"""
Unit tests for analytics, KPI calculations, correlations, and car comparison metrics in CarScope.
"""

import pytest
import pandas as pd
import numpy as np
from src.analytics import (
    compute_overview_kpis, compute_price_by_make,
    compute_correlation_matrix, compute_car_comparison
)


def test_compute_overview_kpis():
    df = pd.DataFrame({
        "make": ["Toyota", "Toyota", "Honda"],
        "price": [20000.0, 30000.0, 25000.0],
        "mileage": [10000.0, 20000.0, 15000.0],
        "year": [2020, 2022, 2021]
    })

    kpis = compute_overview_kpis(df)
    assert kpis["total_vehicles"] == 3
    assert kpis["unique_makes"] == 2
    assert kpis["median_price"] == 25000.0
    assert kpis["mean_price"] == 25000.0
    assert kpis["year_min"] == 2020
    assert kpis["year_max"] == 2022


def test_compute_overview_kpis_empty():
    kpis = compute_overview_kpis(pd.DataFrame())
    assert kpis["total_vehicles"] == 0
    assert kpis["unique_makes"] == 0
    assert kpis["median_price"] is None


def test_compute_price_by_make():
    df = pd.DataFrame({
        "make": ["Toyota", "Toyota", "Honda", "BMW"],
        "price": [20000.0, 30000.0, 22000.0, 50000.0]
    })

    # Minimum group size 2 should exclude Honda and BMW
    result = compute_price_by_make(df, min_group_size=2)
    assert len(result) == 1
    assert result["make"].iloc[0] == "Toyota"
    assert result["median_price"].iloc[0] == 25000.0


def test_compute_correlation_matrix():
    df = pd.DataFrame({
        "price": [20000, 30000, 40000, 50000],
        "mileage": [50000, 40000, 30000, 20000],
        "constant_col": [5, 5, 5, 5]
    })

    corr_df, valid_cols = compute_correlation_matrix(df, ["price", "mileage", "constant_col"])
    assert "constant_col" not in valid_cols
    assert "price" in valid_cols
    assert "mileage" in valid_cols
    # Price vs mileage should have negative correlation -1.0
    assert pytest.approx(corr_df.loc["price", "mileage"], 0.01) == -1.0


def test_compute_car_comparison():
    df = pd.DataFrame({
        "car_id": ["Car A", "Car B"],
        "make": ["Toyota", "Honda"],
        "model": ["Camry", "Civic"],
        "year": [2021, 2022],
        "price": [24000.0, 20000.0],
        "horsepower": [200.0, 150.0]
    })

    raw_specs, norm_df = compute_car_comparison(df, ["Car A", "Car B"])
    assert not raw_specs.empty
    assert not norm_df.empty
    
    # Check min-max normalization values: Car A price 24000 should have norm score 1.0, Car B price 20000 should have 0.0
    price_norm_a = norm_df[(norm_df["car_id"] == "Car A") & (norm_df["metric"] == "Price")]["normalized_score"].values[0]
    price_norm_b = norm_df[(norm_df["car_id"] == "Car B") & (norm_df["metric"] == "Price")]["normalized_score"].values[0]
    
    assert price_norm_a == 1.0
    assert price_norm_b == 0.0
