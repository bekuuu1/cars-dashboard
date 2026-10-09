"""
Analytics and Aggregation module for CarScope.
Defensively calculates summary KPIs, grouped metrics, correlations,
and vehicle comparative normalization using Pandas.
"""

from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
import numpy as np


def compute_overview_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate summary statistics for KPI cards.
    Handles empty DataFrames and missing numeric columns gracefully.
    """
    if df.empty:
        return {
            "total_vehicles": 0,
            "unique_makes": 0,
            "mean_price": None,
            "median_price": None,
            "mean_mileage": None,
            "year_min": None,
            "year_max": None,
        }

    total_vehicles = len(df)
    unique_makes = df["make"].nunique(dropna=True) if "make" in df.columns else 0

    mean_price = df["price"].mean() if "price" in df.columns and df["price"].notna().any() else None
    median_price = df["price"].median() if "price" in df.columns and df["price"].notna().any() else None
    mean_mileage = df["mileage"].mean() if "mileage" in df.columns and df["mileage"].notna().any() else None

    year_min, year_max = None, None
    if "year" in df.columns and df["year"].notna().any():
        year_min = int(df["year"].min())
        year_max = int(df["year"].max())

    return {
        "total_vehicles": total_vehicles,
        "unique_makes": unique_makes,
        "mean_price": round(mean_price, 2) if mean_price is not None and not np.isnan(mean_price) else None,
        "median_price": round(median_price, 2) if median_price is not None and not np.isnan(median_price) else None,
        "mean_mileage": round(mean_mileage, 0) if mean_mileage is not None and not np.isnan(mean_mileage) else None,
        "year_min": year_min,
        "year_max": year_max,
    }


def compute_top_makes(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Return top N makes ordered by listing count.
    """
    if df.empty or "make" not in df.columns:
        return pd.DataFrame(columns=["make", "count"])

    counts = df["make"].value_counts().reset_index()
    counts.columns = ["make", "count"]
    return counts.head(top_n)


def compute_price_by_make(df: pd.DataFrame, min_group_size: int = 2) -> pd.DataFrame:
    """
    Compute mean and median price by make, filtering out small sample groups.
    """
    if df.empty or "make" not in df.columns or "price" not in df.columns:
        return pd.DataFrame(columns=["make", "mean_price", "median_price", "count"])

    valid = df.dropna(subset=["make", "price"])
    if valid.empty:
        return pd.DataFrame(columns=["make", "mean_price", "median_price", "count"])

    grouped = (
        valid.groupby("make")["price"]
        .agg(["mean", "median", "count"])
        .reset_index()
    )
    grouped.rename(columns={"mean": "mean_price", "median": "median_price"}, inplace=True)
    
    # Filter by minimum sample threshold
    filtered = grouped[grouped["count"] >= min_group_size].sort_values("median_price", ascending=False)
    return filtered


def compute_price_vs_year(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute mean and median price per vehicle production year.
    """
    if df.empty or "year" not in df.columns or "price" not in df.columns:
        return pd.DataFrame(columns=["year", "mean_price", "median_price", "count"])

    valid = df.dropna(subset=["year", "price"])
    if valid.empty:
        return pd.DataFrame(columns=["year", "mean_price", "median_price", "count"])

    grouped = (
        valid.groupby("year")["price"]
        .agg(["mean", "median", "count"])
        .reset_index()
    )
    grouped.rename(columns={"mean": "mean_price", "median": "median_price"}, inplace=True)
    return grouped.sort_values("year")


def compute_correlation_matrix(
    df: pd.DataFrame,
    selected_cols: List[str],
    method: str = "pearson"
) -> Tuple[pd.DataFrame, List[str]]:
    """
    Compute correlation matrix for selected numeric columns.
    Omits constant columns or columns with insufficient paired data.

    Returns:
        Tuple of (corr_df: pd.DataFrame, valid_numeric_cols: List[str])
    """
    valid_cols = []
    for col in selected_cols:
        if col in df.columns and pd.api.types.is_numeric_dtype(df[col]):
            # Verify column is non-constant and has non-null entries
            non_null = df[col].dropna()
            if len(non_null) > 1 and non_null.nunique() > 1:
                valid_cols.append(col)

    if len(valid_cols) < 2:
        return pd.DataFrame(), valid_cols

    corr_df = df[valid_cols].corr(method=method)
    return corr_df, valid_cols


def compute_car_comparison(df: pd.DataFrame, selected_car_ids: List[str]) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Extract side-by-side comparative table for selected car IDs and calculate
    0-to-1 min-max normalized metric scores for multi-attribute comparison plotting.

    Returns:
        Tuple of (raw_specs_df: pd.DataFrame, normalized_df: pd.DataFrame)
    """
    if df.empty or not selected_car_ids or "car_id" not in df.columns:
        return pd.DataFrame(), pd.DataFrame()

    selected_df = df[df["car_id"].isin(selected_car_ids)].copy()
    if selected_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    # Raw Specs Table formatted as clean string representations
    cols_to_show = ["car_id", "make", "model", "year", "price", "mileage", "horsepower", "engine_size", "fuel_type", "transmission", "mpg"]
    avail_cols = [c for c in cols_to_show if c in selected_df.columns]
    formatted_df = selected_df[avail_cols].copy()
    for col in avail_cols:
        if col == "price":
            formatted_df[col] = formatted_df[col].apply(lambda x: f"${x:,.0f}" if pd.notna(x) else "N/A")
        elif col == "mileage":
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.0f} mi" if pd.notna(x) else "N/A")
        elif col in ["year", "horsepower", "mpg"]:
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{int(x)}" if pd.notna(x) else "N/A")
        elif col == "engine_size":
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.1f} L" if pd.notna(x) else "N/A")
        else:
            formatted_df[col] = formatted_df[col].astype(str)

    raw_specs = formatted_df.set_index("car_id").T

    # Calculate Min-Max Normalization (0.0 to 1.0) across selected numeric metrics
    numeric_metrics = ["price", "mileage", "horsepower", "engine_size", "mpg", "year"]
    avail_metrics = [m for m in numeric_metrics if m in selected_df.columns and selected_df[m].notna().any()]

    normalized_records = []
    for metric in avail_metrics:
        s = selected_df[metric].astype(float)
        min_val = s.min()
        max_val = s.max()
        val_range = max_val - min_val

        for car_id, val in zip(selected_df["car_id"], s):
            if pd.isna(val):
                norm_score = np.nan
            elif val_range == 0:
                norm_score = 0.5  # Constant value baseline
            else:
                norm_score = (val - min_val) / val_range

            normalized_records.append({
                "car_id": car_id,
                "metric": metric.replace("_", " ").title(),
                "raw_value": val,
                "normalized_score": norm_score
            })

    normalized_df = pd.DataFrame(normalized_records)
    return raw_specs, normalized_df
