"""
Column mapping module for CarScope.
Provides canonical schema definitions, alias matching heuristics,
unit tagging, and interactive mapping state controls.
"""

from typing import Dict, List, Optional
import streamlit as st
import pandas as pd

# Canonical field definitions with labels, descriptions, and alias heuristics
CANONICAL_FIELDS = {
    "make": {
        "label": "Make / Brand",
        "required": True,
        "aliases": ["make", "manufacturer", "brand", "company", "car_make"],
        "unit": None
    },
    "model": {
        "label": "Model",
        "required": True,
        "aliases": ["model", "car_model", "model_name", "vehicle_model", "trim"],
        "unit": None
    },
    "year": {
        "label": "Year",
        "required": False,
        "aliases": ["year", "model_year", "prod_year", "reg_year", "registration_year"],
        "unit": "Year"
    },
    "price": {
        "label": "Price",
        "required": False,
        "aliases": ["price", "selling_price", "cost", "msrp", "value", "price_usd", "amount"],
        "unit": "$"
    },
    "mileage": {
        "label": "Mileage",
        "required": False,
        "aliases": ["mileage", "odometer", "km_driven", "distance", "miles", "kms_driven"],
        "unit": "mi"
    },
    "fuel_type": {
        "label": "Fuel Type",
        "required": False,
        "aliases": ["fuel_type", "fuel", "fueltype", "engine_fuel", "fuel_category"],
        "unit": None
    },
    "transmission": {
        "label": "Transmission",
        "required": False,
        "aliases": ["transmission", "gearbox", "gear_type", "trans", "transmission_type"],
        "unit": None
    },
    "engine_size": {
        "label": "Engine Size",
        "required": False,
        "aliases": ["engine_size", "engine", "displacement", "vol_cc", "engine_capacity", "engine_l"],
        "unit": "L"
    },
    "horsepower": {
        "label": "Horsepower",
        "required": False,
        "aliases": ["horsepower", "power", "hp", "max_power", "engine_hp", "bhp"],
        "unit": "hp"
    },
    "mpg": {
        "label": "Fuel Economy (MPG)",
        "required": False,
        "aliases": ["mpg", "fuel_economy", "consumption", "kml", "l_per_100km"],
        "unit": "mpg"
    },
    "body_type": {
        "label": "Body Type",
        "required": False,
        "aliases": ["body_type", "body", "vehicle_type", "car_type", "style", "category"],
        "unit": None
    },
    "condition": {
        "label": "Condition",
        "required": False,
        "aliases": ["condition", "status", "usage", "state_desc"],
        "unit": None
    },
    "location": {
        "label": "Location",
        "required": False,
        "aliases": ["location", "city", "state", "region", "zip_code"],
        "unit": None
    },
}


def auto_suggest_mappings(raw_columns: List[str]) -> Dict[str, Optional[str]]:
    """
    Suggest canonical mapping from raw dataset columns based on case-insensitive alias matching.
    """
    mapped = {field: None for field in CANONICAL_FIELDS}
    normalized_raw = {col.lower().strip().replace(" ", "_"): col for col in raw_columns}

    for field, info in CANONICAL_FIELDS.items():
        for alias in info["aliases"]:
            if alias in normalized_raw:
                mapped[field] = normalized_raw[alias]
                break

    return mapped


def render_mapping_sidebar(df: pd.DataFrame) -> Dict[str, Optional[str]]:
    """
    Render column mapping UI in Streamlit sidebar expander.
    Stores and returns active mappings in st.session_state.
    """
    if "column_mapping" not in st.session_state:
        st.session_state.column_mapping = auto_suggest_mappings(df.columns.tolist())

    raw_cols = ["-- Unmapped --"] + df.columns.tolist()

    with st.sidebar.expander("Dataset Column Mapping", expanded=False):
        st.caption("Map raw dataset columns to CarScope canonical fields:")
        
        current_map = {}
        for field, info in CANONICAL_FIELDS.items():
            suggested = st.session_state.column_mapping.get(field)
            default_index = raw_cols.index(suggested) if suggested in raw_cols else 0
            
            selected = st.selectbox(
                f"{info['label']} {'*' if info['required'] else ''}",
                options=raw_cols,
                index=default_index,
                key=f"map_select_{field}"
            )
            
            current_map[field] = None if selected == "-- Unmapped --" else selected
            
        st.session_state.column_mapping = current_map
        
        if st.button("Auto-Detect Aliases", use_container_width=True):
            st.session_state.column_mapping = auto_suggest_mappings(df.columns.tolist())
            st.rerun()

    return st.session_state.column_mapping
