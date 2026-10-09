"""
Interactive filter controls module for CarScope.
Generates Streamlit sidebar filter widgets and defensively filters
working DataFrames using Pandas.
"""

from typing import Dict, Any
import streamlit as st
import pandas as pd
import numpy as np


def render_sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    """
    Render interactive filter controls in Streamlit sidebar and apply
    the filter criteria to derive a filtered DataFrame.
    """
    if df.empty:
        return df

    st.sidebar.markdown("### Global Filters")

    if st.sidebar.button("Reset All Filters", use_container_width=True):
        for key in list(st.session_state.keys()):
            if key.startswith("filter_"):
                del st.session_state[key]
        st.rerun()

    filtered_df = df.copy()

    # 1. Make Filter
    if "make" in df.columns and df["make"].notna().any():
        all_makes = sorted(df["make"].dropna().unique().tolist())
        selected_makes = st.sidebar.multiselect(
            "Make / Brand",
            options=all_makes,
            default=[],
            key="filter_make",
            help="Select one or more vehicle brands"
        )
        if selected_makes:
            filtered_df = filtered_df[filtered_df["make"].isin(selected_makes)]

    # 2. Model Filter (Dependent on selected makes)
    if "model" in filtered_df.columns and filtered_df["model"].notna().any():
        all_models = sorted(filtered_df["model"].dropna().unique().tolist())
        selected_models = st.sidebar.multiselect(
            "Model",
            options=all_models,
            default=[],
            key="filter_model",
            help="Select specific vehicle models"
        )
        if selected_models:
            filtered_df = filtered_df[filtered_df["model"].isin(selected_models)]

    # 3. Year Range Slider
    if "year" in df.columns and df["year"].notna().any():
        valid_years = df["year"].dropna().astype(int)
        min_yr = int(valid_years.min())
        max_yr = int(valid_years.max())

        if min_yr < max_yr:
            year_range = st.sidebar.slider(
                "Model Year",
                min_value=min_yr,
                max_value=max_yr,
                value=(min_yr, max_yr),
                key="filter_year"
            )
            filtered_df = filtered_df[
                (filtered_df["year"].isna()) |
                ((filtered_df["year"] >= year_range[0]) & (filtered_df["year"] <= year_range[1]))
            ]

    # 4. Price Range Slider
    if "price" in df.columns and df["price"].notna().any():
        valid_prices = df["price"].dropna()
        min_p = float(valid_prices.min())
        max_p = float(valid_prices.max())

        if min_p < max_p:
            price_range = st.sidebar.slider(
                "Price ($)",
                min_value=float(min_p),
                max_value=float(max_p),
                value=(float(min_p), float(max_p)),
                format="$%.0f",
                key="filter_price"
            )
            filtered_df = filtered_df[
                (filtered_df["price"].isna()) |
                ((filtered_df["price"] >= price_range[0]) & (filtered_df["price"] <= price_range[1]))
            ]

    # 5. Mileage Range Slider
    if "mileage" in df.columns and df["mileage"].notna().any():
        valid_miles = df["mileage"].dropna()
        min_m = float(valid_miles.min())
        max_m = float(valid_miles.max())

        if min_m < max_m:
            mileage_range = st.sidebar.slider(
                "Mileage",
                min_value=float(min_m),
                max_value=float(max_m),
                value=(float(min_m), float(max_m)),
                key="filter_mileage"
            )
            filtered_df = filtered_df[
                (filtered_df["mileage"].isna()) |
                ((filtered_df["mileage"] >= mileage_range[0]) & (filtered_df["mileage"] <= mileage_range[1]))
            ]

    # 6. Fuel Type Multiselect
    if "fuel_type" in df.columns and df["fuel_type"].notna().any():
        fuels = sorted(df["fuel_type"].dropna().unique().tolist())
        selected_fuels = st.sidebar.multiselect(
            "Fuel Type",
            options=fuels,
            default=[],
            key="filter_fuel"
        )
        if selected_fuels:
            filtered_df = filtered_df[filtered_df["fuel_type"].isin(selected_fuels)]

    # 7. Transmission Multiselect
    if "transmission" in df.columns and df["transmission"].notna().any():
        transmissions = sorted(df["transmission"].dropna().unique().tolist())
        selected_trans = st.sidebar.multiselect(
            "Transmission",
            options=transmissions,
            default=[],
            key="filter_transmission"
        )
        if selected_trans:
            filtered_df = filtered_df[filtered_df["transmission"].isin(selected_trans)]

    return filtered_df
