"""
CarScope — Vehicle Data Analytics & Comparative Dashboard
Main Streamlit Application File.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configure Streamlit page layout and theme title
st.set_page_config(
    page_title="CarScope — Vehicle Data Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

from src.ui import (
    apply_custom_css, render_header, render_kpi_card,
    render_empty_state, render_pandas_snippet,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_POSITIVE, COLOR_WARNING, COLOR_DANGER
)
from src.data_loader import load_dataset, get_dataset_metadata
from src.column_mapping import render_mapping_sidebar
from src.cleaning import clean_dataset
from src.filters import render_sidebar_filters
from src.analytics import (
    compute_overview_kpis, compute_top_makes, compute_price_by_make,
    compute_price_vs_year, compute_correlation_matrix, compute_car_comparison
)
from src.charts import (
    plot_top_makes, plot_price_distribution, plot_year_distribution,
    plot_price_by_make, plot_price_vs_year, plot_price_vs_mileage,
    plot_price_by_category, plot_car_comparison_normalized,
    plot_correlation_heatmap, plot_missingness
)

# Apply minimal light theme CSS
apply_custom_css()


def main():
    # Sidebar Header & File Upload
    st.sidebar.markdown("# CarScope")
    st.sidebar.markdown("---")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Car Dataset (CSV)",
        type=["csv"],
        help="Upload your own vehicle CSV or use the bundled sample dataset."
    )

    # Determine data source
    sample_path = "data/sample_cars.csv"
    raw_df = None
    dataset_name = "Sample Dataset"

    if uploaded_file is not None:
        try:
            raw_df, dataset_name = load_dataset(uploaded_file)
            st.sidebar.success(f"Loaded: {dataset_name}")
        except Exception as e:
            st.sidebar.error(f"Failed to load uploaded CSV: {e}")
            st.stop()
    elif os.path.exists(sample_path):
        try:
            raw_df, dataset_name = load_dataset(sample_path)
            st.sidebar.info("Using bundled sample dataset (`data/sample_cars.csv`)")
        except Exception as e:
            st.sidebar.error(f"Failed to load sample dataset: {e}")
            st.stop()
    else:
        st.error("No dataset available. Please upload a vehicle CSV file in the sidebar.")
        st.stop()

    # Column Mapping UI
    col_mapping = render_mapping_sidebar(raw_df)

    # Cleaning Options Sidebar
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Cleaning Options")
    drop_dup = st.sidebar.checkbox("Drop Exact Duplicates", value=False)
    exclude_missing_canon = st.sidebar.checkbox("Exclude Missing Make/Model", value=False)

    # Clean Dataset
    cleaned_df, clean_report = clean_dataset(
        raw_df,
        col_mapping,
        drop_duplicates_flag=drop_dup,
        exclude_missing_canonical=exclude_missing_canon
    )

    # Sidebar Interactive Filters
    filtered_df = render_sidebar_filters(cleaned_df)

    # Minimal Top Header
    render_header(
        dataset_name=dataset_name,
        total_rows=len(filtered_df),
        status_text="Filtered" if len(filtered_df) != len(cleaned_df) else "Complete"
    )

    # Main Dashboard Page Navigation
    page = st.sidebar.radio(
        "Navigation",
        options=[
            "Page A — Overview",
            "Page B — Explore Data",
            "Page C — Price Analytics",
            "Page D — Compare Cars",
            "Page E — Brand & Segment Insights",
            "Page F — Correlations",
            "Page G — Data Quality & Methods"
        ],
        index=0
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("CarScope v1.0 • Built with Pandas, Seaborn & Streamlit")

    # =========================================================================
    # PAGE A — OVERVIEW
    # =========================================================================
    if page == "Page A — Overview":
        st.markdown("### Dataset Overview & Key Metrics")

        if filtered_df.empty:
            render_empty_state()
            return

        kpis = compute_overview_kpis(filtered_df)

        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            render_kpi_card("Total Vehicles", f"{kpis['total_vehicles']:,}", "Active filtered count")
        with col2:
            render_kpi_card("Unique Makes", f"{kpis['unique_makes']}", "Distinct brands")
        with col3:
            med_price_str = f"${kpis['median_price']:,.0f}" if kpis['median_price'] else "N/A"
            render_kpi_card("Median Price", med_price_str, "50th percentile price")
        with col4:
            mean_mil_str = f"{kpis['mean_mileage']:,.0f} mi" if kpis['mean_mileage'] else "N/A"
            render_kpi_card("Avg Mileage", mean_mil_str, "Mean odometer reading")
        with col5:
            yr_str = f"{kpis['year_min']}–{kpis['year_max']}" if kpis['year_min'] else "N/A"
            render_kpi_card("Year Range", yr_str, "Production span")

        # Top Visualizations Row
        c1, c2 = st.columns(2)
        with c1:
            fig_makes = plot_top_makes(filtered_df, top_n=10)
            if fig_makes:
                st.pyplot(fig_makes, clear_figure=True)
                plt.close(fig_makes)
            else:
                st.info("Make information unavailable for plotting.")

        with c2:
            fig_price_dist = plot_price_distribution(filtered_df)
            if fig_price_dist:
                st.pyplot(fig_price_dist, clear_figure=True)
                plt.close(fig_price_dist)
            else:
                st.info("Price distribution unavailable (missing numeric price column).")

        c3, c4 = st.columns(2)
        with c3:
            fig_yr_dist = plot_year_distribution(filtered_df)
            if fig_yr_dist:
                st.pyplot(fig_yr_dist, clear_figure=True)
                plt.close(fig_yr_dist)
            else:
                st.info("Year distribution unavailable.")

        with c4:
            st.markdown("#### Data Health Summary")
            meta = get_dataset_metadata(filtered_df)
            st.write(f"- **Filtered Records:** `{meta['rows']:,}` rows × `{meta['columns']}` columns")
            st.write(f"- **Missing Value Ratio:** `{meta['missing_percentage']}%` missing cells")
            st.write(f"- **Flagged Outliers:** `{clean_report['flagged_outliers']}` suspicious rows")
            st.write(f"- **Usable Complete Rows:** `{len(filtered_df.dropna(subset=['make', 'price'])):,}` rows")

        render_pandas_snippet(
            title="Overview KPIs and Aggregations",
            code_snippet="""
# Compute basic summary metrics using Pandas
total_count = df.shape[0]
unique_makes = df['make'].nunique()
median_price = df['price'].median()
mean_mileage = df['mileage'].mean()

# Top 10 makes by listing frequency
top_makes = df['make'].value_counts().head(10)
            """,
            explanation="Overview statistics use `.shape[0]`, `.nunique()`, `.median()`, `.mean()`, and `.value_counts()`."
        )

    # =========================================================================
    # PAGE B — EXPLORE DATA
    # =========================================================================
    elif page == "Page B — Explore Data":
        st.markdown("### Searchable & Sortable Data Table")

        if filtered_df.empty:
            render_empty_state()
            return

        c_search, c_sort, c_order = st.columns([2, 1, 1])
        with c_search:
            search_query = st.text_input("Search by Make or Model", value="", placeholder="e.g. Toyota or Civic")
        with c_sort:
            sort_col = st.selectbox("Sort By Column", options=[c for c in filtered_df.columns if c != "car_id"], index=0)
        with c_order:
            sort_order = st.radio("Order", options=["Ascending", "Descending"], horizontal=True)

        display_df = filtered_df.copy()
        if search_query:
            query = search_query.lower()
            mask = display_df["make"].astype(str).str.lower().str.contains(query) | display_df["model"].astype(str).str.lower().str.contains(query)
            display_df = display_df[mask]

        display_df = display_df.sort_values(by=sort_col, ascending=(sort_order == "Ascending"))

        st.caption(f"Displaying **{len(display_df):,}** of **{len(cleaned_df):,}** cleaned vehicle records.")
        st.dataframe(display_df.drop(columns=["is_outlier"], errors="ignore"), use_container_width=True, height=400)

        # Download Filtered Data Button
        csv_data = display_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download Filtered Dataset (CSV)",
            data=csv_data,
            file_name="carscope_filtered_data.csv",
            mime="text/csv",
            type="primary"
        )

        st.markdown("#### Summary of Categorical & Numeric Attributes")
        tab_num, tab_cat = st.tabs(["Numeric Summary", "Categorical Summary"])

        with tab_num:
            num_cols = display_df.select_dtypes(include=[np.number]).columns.tolist()
            if num_cols:
                st.dataframe(display_df[num_cols].describe().T, use_container_width=True)
            else:
                st.info("No numeric columns available.")

        with tab_cat:
            cat_cols = display_df.select_dtypes(include=["object", "category"]).columns.tolist()
            if cat_cols:
                cat_summary = []
                for c in cat_cols:
                    if c != "car_id":
                        cat_summary.append({
                            "column": c,
                            "unique_values": display_df[c].nunique(),
                            "top_category": display_df[c].mode()[0] if not display_df[c].dropna().empty else "N/A",
                            "top_frequency": display_df[c].value_counts().iloc[0] if not display_df[c].dropna().empty else 0
                        })
                st.dataframe(pd.DataFrame(cat_summary), use_container_width=True)

        render_pandas_snippet(
            title="Filtering, Sorting & Text Search",
            code_snippet="""
# Case-insensitive text search on Make/Model
query = "toyota"
mask = df['make'].str.lower().str.contains(query) | df['model'].str.lower().str.contains(query)
filtered_df = df[mask]

# Sort values by specified column
sorted_df = filtered_df.sort_values(by='price', ascending=False)
            """,
            explanation="Defensive filtering uses boolean masks (`.str.contains`) and sorting (`.sort_values`)."
        )

    # =========================================================================
    # PAGE C — PRICE ANALYTICS
    # =========================================================================
    elif page == "Page C — Price Analytics":
        st.markdown("### Price Analytics & Valuation Trends")

        if filtered_df.empty:
            render_empty_state()
            return

        # 1. Price by Make
        st.markdown("#### Price Comparison by Brand")
        min_samples = st.slider("Minimum listings per make to display", min_value=1, max_value=10, value=2)
        df_price_make = compute_price_by_make(filtered_df, min_group_size=min_samples)

        if not df_price_make.empty:
            fig_pm = plot_price_by_make(df_price_make)
            if fig_pm:
                st.pyplot(fig_pm, clear_figure=True)
                plt.close(fig_pm)
        else:
            st.info(f"No make has at least {min_samples} valid listings.")

        # 2. Price by Production Year & Price vs Mileage
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("#### Price by Production Year")
            df_price_yr = compute_price_vs_year(filtered_df)
            if not df_price_yr.empty:
                fig_py = plot_price_vs_year(df_price_yr)
                if fig_py:
                    st.pyplot(fig_py, clear_figure=True)
                    plt.close(fig_py)
            else:
                st.info("Year & Price data unavailable.")

        with col_right:
            st.markdown("#### Price vs. Mileage")
            show_reg = st.toggle("Show Linear Regression Line", value=True)
            fig_pmil = plot_price_vs_mileage(filtered_df, show_regression=show_reg)
            if fig_pmil:
                st.pyplot(fig_pmil, clear_figure=True)
                plt.close(fig_pmil)
            else:
                st.info("Mileage & Price data unavailable.")

        # 3. Price Distribution across Segments
        st.markdown("#### Price Distribution by Transmission / Fuel Type")
        segment_col = st.radio("Segment Column", options=["transmission", "fuel_type", "body_type"], horizontal=True)
        fig_seg = plot_price_by_category(filtered_df, segment_col)
        if fig_seg:
            st.pyplot(fig_seg, clear_figure=True)
            plt.close(fig_seg)
        else:
            st.info(f"Column '{segment_col}' is unavailable or has missing values.")

        st.warning("Observational Disclaimer: Relationships in observational data (e.g. price vs. mileage) describe sample trends and do not prove direct causal effects or guarantee future market value.")

        render_pandas_snippet(
            title="Groupby Aggregation & Pearson Correlation",
            code_snippet="""
# Calculate Mean and Median price grouped by Make
price_stats = df.groupby('make')['price'].agg(['mean', 'median', 'count'])

# Filter by minimum sample size
price_stats_filtered = price_stats[price_stats['count'] >= 2]

# Compute Pearson correlation coefficient between price and mileage
corr = df['price'].corr(df['mileage'], method='pearson')
            """,
            explanation="Pandas `.groupby()`, `.agg()`, and `.corr()` enable statistical aggregations."
        )

    # =========================================================================
    # PAGE D — COMPARE CARS
    # =========================================================================
    elif page == "Page D — Compare Cars":
        st.markdown("### Side-by-Side Vehicle Comparison")
        st.caption("Select 2 to 4 vehicles from the current dataset to evaluate specifications and normalized performance metrics.")

        if filtered_df.empty or "car_id" not in filtered_df.columns:
            render_empty_state()
            return

        available_cars = filtered_df["car_id"].unique().tolist()
        default_selection = available_cars[:2] if len(available_cars) >= 2 else available_cars

        selected_car_ids = st.multiselect(
            "Select Vehicles to Compare (2 to 4 cars)",
            options=available_cars,
            default=default_selection,
            max_selections=4
        )

        if len(selected_car_ids) < 2:
            st.info("Please select at least 2 vehicles to generate comparison tables and charts.")
            return

        raw_specs, normalized_df = compute_car_comparison(filtered_df, selected_car_ids)

        st.markdown("#### Attribute Specification Matrix")
        st.dataframe(raw_specs, use_container_width=True)

        st.markdown("#### Normalized Metric Scores (Min-Max Scaled 0.0 to 1.0)")
        fig_comp = plot_car_comparison_normalized(normalized_df)
        if fig_comp:
            st.pyplot(fig_comp, clear_figure=True)
            plt.close(fig_comp)

        st.info("Normalization Note: Min-Max scaling normalizes metrics within the selected group (0.0 = minimum among selection, 1.0 = maximum). This enables comparison across distinct units (e.g. Price vs. Horsepower).")

        render_pandas_snippet(
            title="Vehicle Comparison & Min-Max Scaling",
            code_snippet="""
# Min-Max normalization score formula for attribute x:
# score = (x - min(x)) / (max(x) - min(x))

selected_df = df[df['car_id'].isin(selected_ids)]
min_val = selected_df['price'].min()
max_val = selected_df['price'].max()
norm_price = (selected_df['price'] - min_val) / (max_val - min_val)
            """,
            explanation="Normalization rescales numeric columns to a 0.0 to 1.0 range for cross-metric comparison."
        )

    # =========================================================================
    # PAGE E — BRAND & SEGMENT INSIGHTS
    # =========================================================================
    elif page == "Page E — Brand & Segment Insights":
        st.markdown("### Brand & Market Segment Analysis")

        if filtered_df.empty:
            render_empty_state()
            return

        c_b1, c_b2 = st.columns(2)
        with c_b1:
            st.markdown("#### Brand Market Share (Listing Frequency)")
            makes_df = compute_top_makes(filtered_df, top_n=15)
            st.dataframe(makes_df, use_container_width=True)

        with c_b2:
            st.markdown("#### Median Price by Brand")
            price_make_df = compute_price_by_make(filtered_df, min_group_size=1)
            st.dataframe(price_make_df, use_container_width=True)

        st.markdown("#### Brand Head-to-Head Comparison")
        all_makes = sorted(filtered_df["make"].dropna().unique().tolist()) if "make" in filtered_df.columns else []

        if len(all_makes) >= 2:
            bm1, bm2 = st.columns(2)
            with bm1:
                brand1 = st.selectbox("Select Brand 1", options=all_makes, index=0)
            with bm2:
                brand2 = st.selectbox("Select Brand 2", options=all_makes, index=1 if len(all_makes) > 1 else 0)

            df_b1 = filtered_df[filtered_df["make"] == brand1]
            df_b2 = filtered_df[filtered_df["make"] == brand2]

            kpi1 = compute_overview_kpis(df_b1)
            kpi2 = compute_overview_kpis(df_b2)

            comp_records = [
                {"Metric": "Total Listings", brand1: kpi1["total_vehicles"], brand2: kpi2["total_vehicles"]},
                {"Metric": "Median Price", brand1: f"${kpi1['median_price']:,.0f}" if kpi1['median_price'] else "N/A", brand2: f"${kpi2['median_price']:,.0f}" if kpi2['median_price'] else "N/A"},
                {"Metric": "Mean Price", brand1: f"${kpi1['mean_price']:,.0f}" if kpi1['mean_price'] else "N/A", brand2: f"${kpi2['mean_price']:,.0f}" if kpi2['mean_price'] else "N/A"},
                {"Metric": "Avg Mileage", brand1: f"{kpi1['mean_mileage']:,.0f} mi" if kpi1['mean_mileage'] else "N/A", brand2: f"{kpi2['mean_mileage']:,.0f} mi" if kpi2['mean_mileage'] else "N/A"},
                {"Metric": "Year Span", brand1: f"{kpi1['year_min']}–{kpi1['year_max']}" if kpi1['year_min'] else "N/A", brand2: f"{kpi2['year_min']}–{kpi2['year_max']}" if kpi2['year_min'] else "N/A"},
            ]
            st.dataframe(pd.DataFrame(comp_records), use_container_width=True)

        render_pandas_snippet(
            title="Subsetting Data for Brand Comparison",
            code_snippet="""
# Filter DataFrame for specific brands
brand1_df = df[df['make'] == 'Toyota']
brand2_df = df[df['make'] == 'Honda']

# Compare median prices
med1 = brand1_df['price'].median()
med2 = brand2_df['price'].median()
            """,
            explanation="Pandas comparison uses boolean filtering to separate subset DataFrames."
        )

    # =========================================================================
    # PAGE F — CORRELATIONS
    # =========================================================================
    elif page == "Page F — Correlations":
        st.markdown("### Numeric Correlations")

        if filtered_df.empty:
            render_empty_state()
            return

        numeric_cols = filtered_df.select_dtypes(include=[np.number]).columns.tolist()
        numeric_cols = [c for c in numeric_cols if c != "is_outlier"]

        if len(numeric_cols) < 2:
            st.warning("Insufficient numeric variables available for correlation matrix.")
            return

        c_corr1, c_corr2 = st.columns([3, 1])
        with c_corr1:
            selected_num = st.multiselect("Select Numeric Columns for Correlation", options=numeric_cols, default=numeric_cols)
        with c_corr2:
            corr_method = st.radio("Correlation Method", options=["pearson", "spearman"])

        if len(selected_num) >= 2:
            corr_df, valid_cols = compute_correlation_matrix(filtered_df, selected_num, method=corr_method)
            if not corr_df.empty:
                fig_corr = plot_correlation_heatmap(corr_df)
                if fig_corr:
                    st.pyplot(fig_corr, clear_figure=True)
                    plt.close(fig_corr)
            else:
                st.warning("Selected numeric variables contain constant values or zero variance.")
        else:
            st.info("Select at least 2 numeric variables.")

        st.warning("Statistical Reminder: A high correlation coefficient (r) measures linear association, but does not prove causation.")

        render_pandas_snippet(
            title="Correlation Matrix Computation",
            code_snippet="""
# Compute Pearson or Spearman correlation matrix on numeric columns
numeric_df = df[['price', 'mileage', 'horsepower', 'year']]
corr_matrix = numeric_df.corr(method='pearson')
            """,
            explanation="`.corr()` ignores NaN cells automatically when calculating pairwise correlation."
        )

    # =========================================================================
    # PAGE G — DATA QUALITY & METHODS
    # =========================================================================
    elif page == "Page G — Data Quality & Methods":
        st.markdown("### Data Quality Audit & Methods")

        st.markdown("#### Record Count Pipeline Summary")
        q1, q2, q3, q4 = st.columns(4)
        with q1:
            render_kpi_card("Raw CSV Rows", f"{clean_report['raw_rows']:,}")
        with q2:
            render_kpi_card("Duplicates Found", f"{clean_report['exact_duplicates']:,}")
        with q3:
            render_kpi_card("Outliers Flagged", f"{clean_report['flagged_outliers']:,}")
        with q4:
            render_kpi_card("Cleaned Rows", f"{clean_report['cleaned_rows']:,}")

        c_qleft, c_qright = st.columns(2)
        with c_qleft:
            st.markdown("#### Missing Data Percentage by Column")
            fig_miss = plot_missingness(cleaned_df)
            if fig_miss:
                st.pyplot(fig_miss, clear_figure=True)
                plt.close(fig_miss)

        with c_qright:
            st.markdown("#### Data Cleaning Decision Log")
            st.write(f"- **Raw File Records:** `{clean_report['raw_rows']:,}` rows")
            st.write(f"- **Exact Duplicates:** `{clean_report['exact_duplicates']}` rows identified")
            st.write(f"- **Removed Duplicates:** `{clean_report['removed_duplicates']}` rows dropped")
            st.write(f"- **Flagged Outliers:** `{clean_report['flagged_outliers']}` rows flagged with `is_outlier=True`")

            if clean_report["outlier_details"]:
                st.write("**Outlier Flags:**")
                for d in clean_report["outlier_details"]:
                    st.write(f"  • {d}")

        # Cleaned CSV Export
        csv_cleaned = cleaned_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Export Full Cleaned Dataset (CSV)",
            data=csv_cleaned,
            file_name="carscope_cleaned_data.csv",
            mime="text/csv",
            type="primary"
        )

        st.markdown("#### Summary Statistics via DataFrame.describe()")
        st.dataframe(cleaned_df.describe().T, use_container_width=True)

        render_pandas_snippet(
            title="Data Quality & Missingness Auditing",
            code_snippet="""
# Calculate null counts per column
missing_counts = df.isna().sum()

# Calculate missing percentage per column
missing_pct = (df.isna().sum() / len(df)) * 100

# Summary descriptive statistics for numeric columns
summary_stats = df.describe()
            """,
            explanation="Data quality checks use `.isna().sum()` and `.describe()` to inspect completeness and distributions."
        )


if __name__ == "__main__":
    main()
