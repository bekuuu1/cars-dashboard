"""
Data cleaning and transformation module for CarScope.
Applies Pandas transformations defensively, parses messy text/numeric fields,
detects duplicates and outliers, and constructs canonical DataFrames.
"""

from typing import Dict, Optional, Tuple, Any
import pandas as pd
import numpy as np
import re
from datetime import datetime


def extract_numeric(val: Any) -> Optional[float]:
    """
    Safely extract numeric values from strings containing currency, units, or formatting commas.
    Examples: '$24,500' -> 24500.0, '-$5,000' -> -5000.0, '31,000 mi' -> 31000.0, '2.0 L' -> 2.0, '150 hp' -> 150.0
    """
    if pd.isna(val) or val is None:
        return np.nan
    if isinstance(val, (int, float)):
        return float(val)

    s = str(val).strip()
    
    # Check if there is a negative sign before the first digit
    is_negative = False
    digit_match = re.search(r"\d", s)
    if "-" in s and digit_match and s.find("-") < digit_match.start():
        is_negative = True

    match = re.search(r"\d[\d,]*\.?\d*", s)
    if match:
        clean_str = match.group(0).replace(",", "")
        try:
            num = float(clean_str)
            return -num if is_negative else num
        except ValueError:
            return np.nan
    return np.nan


def standardize_text(val: Any) -> Optional[str]:
    """
    Standardize text category string by trimming and preserving proper title casing.
    """
    if pd.isna(val) or val is None:
        return np.nan
    s = str(val).strip()
    if not s or s.lower() in ["nan", "none", "null", "n/a", "unknown"]:
        return np.nan
    # Retain standard capitalization (Title case for brand/model/transmission/fuel)
    return " ".join([word.capitalize() for word in s.split()])


def clean_dataset(
    raw_df: pd.DataFrame,
    col_mapping: Dict[str, Optional[str]],
    drop_duplicates_flag: bool = False,
    exclude_missing_canonical: bool = False
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Clean raw DataFrame according to column mappings and data hygiene rules.

    Returns:
        Tuple of (cleaned_df: pd.DataFrame, cleaning_report: Dict[str, Any])
    """
    # Create an explicit unmutated copy of the mapped fields
    df = pd.DataFrame()
    report = {
        "raw_rows": len(raw_df),
        "exact_duplicates": int(raw_df.duplicated().sum()),
        "removed_duplicates": 0,
        "flagged_outliers": 0,
        "outlier_details": [],
        "missing_counts": {},
        "failed_parses": {}
    }

    # Map raw columns to canonical fields
    for field, raw_col in col_mapping.items():
        if raw_col and raw_col in raw_df.columns:
            df[field] = raw_df[raw_col].copy()
        else:
            df[field] = np.nan

    # 1. Parse Numeric Fields
    numeric_fields = ["year", "price", "mileage", "engine_size", "horsepower", "mpg"]
    for field in numeric_fields:
        if field in df.columns and not df[field].isna().all():
            original_series = df[field].copy()
            df[field] = df[field].apply(extract_numeric)
            failed_count = original_series.notna().sum() - df[field].notna().sum()
            report["failed_parses"][field] = int(failed_count)

    # Convert year to integer where non-null
    if "year" in df.columns:
        df["year"] = pd.to_numeric(df["year"], errors="coerce")

    # 2. Standardize Categorical Fields
    text_fields = ["make", "model", "fuel_type", "transmission", "body_type", "condition", "location"]
    for field in text_fields:
        if field in df.columns:
            df[field] = df[field].apply(standardize_text)

    # 3. Handle Duplicates
    if drop_duplicates_flag:
        initial_len = len(df)
        df = df.drop_duplicates().copy()
        report["removed_duplicates"] = initial_len - len(df)

    # 4. Flag Impossible / Suspicious Outliers
    current_year = datetime.now().year
    outlier_mask = pd.Series(False, index=df.index)

    if "price" in df.columns:
        invalid_price = (df["price"] < 0) | (df["price"] > 10_000_000)
        if invalid_price.any():
            outlier_mask |= invalid_price
            report["outlier_details"].append(f"Price out of range (0 to $10M): {invalid_price.sum()} rows")

    if "mileage" in df.columns:
        invalid_mileage = (df["mileage"] < 0) | (df["mileage"] > 2_000_000)
        if invalid_mileage.any():
            outlier_mask |= invalid_mileage
            report["outlier_details"].append(f"Mileage out of range (0 to 2M): {invalid_mileage.sum()} rows")

    if "year" in df.columns:
        invalid_year = (df["year"] < 1900) | (df["year"] > current_year + 1)
        if invalid_year.any():
            outlier_mask |= invalid_year
            report["outlier_details"].append(f"Year out of range (1900 to {current_year + 1}): {invalid_year.sum()} rows")

    report["flagged_outliers"] = int(outlier_mask.sum())
    df["is_outlier"] = outlier_mask

    # 5. Missing Values Summary
    report["missing_counts"] = df.isna().sum().to_dict()

    # Optional dropping of rows missing mandatory canonical fields (Make and Model)
    if exclude_missing_canonical:
        initial_cnt = len(df)
        df = df.dropna(subset=["make", "model"]).copy()
        report["dropped_missing_canonical"] = initial_cnt - len(df)

    # 6. Generate Stable Unique Row Identifier (car_id)
    # Allows unambiguous vehicle selection even when display names overlap
    car_ids = []
    for idx, row in df.iterrows():
        make_str = str(row["make"]) if pd.notna(row["make"]) else "Unknown Make"
        model_str = str(row["model"]) if pd.notna(row["model"]) else "Unknown Model"
        year_str = str(int(row["year"])) if pd.notna(row["year"]) else "N/A"
        car_ids.append(f"{make_str} {model_str} ({year_str}) [#{idx}]")
    df["car_id"] = car_ids

    report["cleaned_rows"] = len(df)
    return df, report
