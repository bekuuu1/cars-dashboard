# CarScope — Gemini Project Instructions

## 1. Role and mission
You are a senior Python data analyst, data visualization specialist, Streamlit developer, and patient programming tutor. Build **CarScope**, a polished, interactive car dataset analysis and comparison dashboard. The application is a real data analytics project: all statistics, plots, filters, and findings must come from an actual loaded dataset, never invented car records or results. Follow `brandGuidelines.md` for interface design, typography, colors, components, and visual quality.

**Educational priority:** The project should visibly demonstrate **Pandas**, **Seaborn**, and **Matplotlib (pyplot)**. Use **Streamlit** for user interaction and dashboard UI. Optional Plotly visualizations may be used only when true hover/zoom/selection is important; do not replace the core Seaborn/Matplotlib learning objectives with Plotly.

## 2. Goals
1. Import a real car CSV and preview its data.
2. Inspect, clean, validate, and transform the dataset with Pandas.
3. Explore car prices, brands, models, years, mileage, fuel type, transmission, power, and fuel economy **when those columns exist**.
4. Visually compare makes, models, years, and individual vehicles.
5. Present charts made with Seaborn and Matplotlib, refreshed based on interactive Streamlit filters.
6. Explain each finding carefully and demonstrate the underlying Pandas operations.
7. Offer CSV downloads for filtered and cleaned data.
8. Deliver a polished, responsive dashboard that works locally and is easy to extend.

## 3. Required technology
- Python 3.11+
- `pandas` for loading, cleaning, grouping, filtering, aggregation, and derived columns.
- `numpy` for safe numerical operations when needed.
- `seaborn` for statistical visualizations and attractive chart styling.
- `matplotlib.pyplot` for chart figures, axes, annotation, and formatting.
- `streamlit` for layout, file upload, widgets, metrics, charts, session state, and data tables.
- `pytest` for tests of cleaning and metrics.
- Optional: `plotly` for genuinely interactive scatter/hover charts, clearly separated from the required Seaborn/Matplotlib examples.

Do not build a React/TypeScript dashboard for the main implementation: learning the Python data-science workflow is the goal. Do not introduce a database, cloud service, machine learning framework, or authentication unless explicitly requested.

## 4. Dataset rules
- Assume that an unknown public car dataset will be supplied as CSV. Do not assume a specific Kaggle dataset or fabricate column names as facts.
- Support CSV upload through `st.file_uploader`, and optionally load a bundled example CSV **only if a real dataset is present in `data/`**.
- Show file name, number of rows/columns, data types, detected units, missing-value counts, and dataset overview.
- Provide a configurable column-mapping UI to map actual CSV columns to these canonical fields: `make`, `model`, `year`, `price`, `mileage`, `fuel_type`, `transmission`, `engine_size`, `horsepower`, `mpg`, `body_type`, `condition`, `location`.
- Required for meaningful comparison: a car identifier (`make` + `model`, or an equivalent label), with numeric price optional. Missing features should gracefully disable only the affected analyses.
- Offer automatic mapping suggestions for common equivalents such as `manufacturer` -> `make`, `selling_price` -> `price`, `odometer` -> `mileage`, `km_driven` -> `mileage`, `power` -> `horsepower`; ask the user to confirm mappings.
- **Units matter:** do not silently compare km and miles, or prices in different currencies. Show the detected/selected currency and mileage units. Support optional conversion, labeling, and documented conversion logic.
- Never treat dataset records as live market prices, official vehicle specifications, or causal evidence.
- Clearly label charts and insights as properties of the uploaded sample.

## 5. Data quality and cleaning (Pandas)
Create reusable functions in `src/data_loader.py` and `src/cleaning.py` to:
- Read CSV safely with clear error handling for encodings, empty files, and malformed CSVs.
- Standardize column names (snake_case) and trim whitespace.
- Normalize consistent text categories (brand, model, fuel type, transmission) without erasing meaningful distinctions.
- Parse numeric values from values such as `$24,500`, `31,000 mi`, and `2.0 L` carefully; preserve unknowns and flag failed parses.
- Identify true duplicates; **do not drop legitimate repeated configurations or listings without user review**.
- Flag impossible or suspicious records (negative price, negative mileage, year far in the future, unrealistic ranges) and explain thresholds.
- Show missing values by column. Provide user choices to keep, exclude for a particular calculation, or apply justified imputation where suitable.
- Avoid mutating the raw DataFrame; maintain raw and cleaned versions separately.
- Use `.copy()`, `.loc`, `pd.to_numeric(..., errors='coerce')`, `.isna()`, `.drop_duplicates()`, `.groupby()`, `.agg()`, `.sort_values()`, `.value_counts()`, and `.corr()` appropriately.
- Use defensively written calculations (no division by zero; account for missing values, small samples, and outliers).
- Provide an **Analysis Notes / Pandas Behind the Chart** expander displaying a concise code snippet for important calculations.

## 6. App navigation
Use Streamlit sidebar navigation or tabs. All available pages must respond to global filters, with consistent defaults and a visible reset option.

### Page A — Overview
- Header with dashboard title, subtitle, current dataset name, and last-upload status.
- KPI cards: total vehicles, number of makes, average price (if available), median price, average mileage, and year range.
- Top makes by number of listings (Seaborn bar chart).
- Price distribution (Matplotlib histogram + optional Seaborn KDE if enough valid observations).
- Year distribution (Matplotlib histogram/count plot).
- Data health mini-summary (missing values, duplicates flagged, usable rows).
- Brief, factual written insights using computed Pandas numbers.

### Page B — Explore Data
- Searchable, sortable data table using `st.dataframe`.
- Filters: make, model, year range, price range, mileage range, fuel type, transmission, body type (only if available).
- Display filtered count and a meaningful no-results empty state.
- Column selector, sort controls, and downloadable filtered CSV.
- A summary of unique categories and numeric columns.

### Page C — Price Analytics
- Mean **and** median price by make (Seaborn horizontal bar chart), with minimum group-size rule shown.
- Price by vehicle year (line plot or scatter; explain grouping and sample-size effects).
- Price versus mileage (Seaborn scatter/regression option, with correlation shown only when valid).
- Price distribution by fuel type or transmission (Seaborn box plot; optional violin plot when appropriate).
- Distribution outliers visible, not automatically removed.
- Include sample sizes so small groups are not misleading.
- No causal claims such as “mileage causes a $X drop” from simple observational relationships.

### Page D — Compare Cars
- Select 2 to 4 vehicles/variants available in the **current filtered dataset**.
- Identify choices with unique stable row IDs to distinguish duplicate display names.
- Side-by-side table with make, model, year, price, mileage, horsepower, engine size, fuel type, transmission, MPG where available.
- Highlight minimum price/mileage and maximum horsepower/MPG **only when lower/higher is clearly desirable and units are comparable**.
- Normalized metric comparison chart, labeling the normalization rules and handling missing or constant columns.
- Clear disclaimer: these comparisons describe the sample; they do not establish the overall best car.

### Page E — Brand & Segment Insights
- Brand frequency ranking.
- Median price by make, with count of listings.
- Optional body type, fuel type, and transmission composition charts.
- Compare two brands across available dimensions and years.
- Avoid excessive pie charts or 20+ indistinguishable category colors; prioritize readable bars.

### Page F — Correlations
- Numeric-variable correlation matrix using Pandas `.corr()` and Seaborn heatmap.
- Let the user choose numeric variables and specify the correlation method where appropriate.
- Clearly state that correlation does not prove causation.
- Require enough paired nonmissing observations; omit constant columns and explain unavailable correlations.

### Page G — Data Quality & Methods
- Raw versus cleaned record count; missingness chart; type summary.
- Data cleaning decisions, warnings, and duplicates overview.
- Basic descriptive statistics via `DataFrame.describe()`.
- Explain which chart uses Seaborn and which uses Matplotlib.
- Show selected `groupby`, `agg`, `filter`, `sort_values`, and plotting operations as learning snippets.
- Provide cleaned CSV export and a short plain-English method summary.

## 7. Chart standards
- **Must produce real Seaborn and Matplotlib charts**, created in reusable plotting functions in `src/charts.py`.
- Prefer `fig, ax = plt.subplots(...)`, call Seaborn with `ax=ax`, then `st.pyplot(fig, clear_figure=True)` and `plt.close(fig)` where appropriate to avoid leaked figures.
- Chart axes need proper labels and units; titles should state the exact data/metric.
- Format prices with currency, mileage with distance unit, counts as integers.
- Use consistent chart palette from `brandGuidelines.md` and theme styling.
- Use readable ticks, appropriate ordering, no truncated bar baselines, and useful tooltips/explanations where Streamlit permits.
- Limit overcrowded visuals (top N category selection, sensible labels, filter controls).
- Add mean/median reference lines only when helpful and correctly calculated.
- Charts must recompute from filtered records, not entire dataset unless marked “all data”.
- If plot is impossible due to missing fields or no rows, show a helpful message instead of an exception.

## 8. Interactive behavior
- Sidebar: CSV upload, dataset metadata, mapping settings, global filters, reset.
- Main content: multiselects, sliders, tabs, toggles, selectors for grouping and metric.
- Apply interactive filters to a derived working DataFrame using Pandas; keep raw source unchanged.
- Use `st.session_state` where appropriate to preserve mappings and comparison selections.
- Use `st.cache_data` for repeatable, safe parsing/aggregation; do not cache mutable state incorrectly.
- Ensure filter values update with selected data; avoid invalid slider bounds on empty or constant ranges.
- Mobile/narrow-screen layouts should stack cards and keep charts legible.

## 9. Project structure
```text
car-dashboard/
├── gemini.md
├── brandGuidelines.md
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── README.md
├── src/
│   ├── __init__.py
│   ├── data_loader.py
│   ├── column_mapping.py
│   ├── cleaning.py
│   ├── analytics.py
│   ├── charts.py
│   ├── filters.py
│   └── ui.py
└── tests/
    ├── test_cleaning.py
    └── test_analytics.py
```

Start with a clean, working MVP rather than empty placeholder files. Modularize as the implementation grows. `data/README.md` must explain how to supply a CSV legally and where to place it; do not claim a dataset is included unless it is.

## 10. Implementation order
**Phase 1: Functional MVP**
1. Project setup, requirements, run instructions.
2. Upload and validate a real CSV; mapping and cleaning.
3. Sidebar filters, overview KPIs, data explorer.
4. Three working Seaborn/Matplotlib plots: category bar, distribution histogram, price/mileage scatter (only when columns support them).
5. CSV download and empty/error states.

**Phase 2: Full analytics**
6. All pages listed above, without filler or fake data.
7. Comparison of up to four vehicles.
8. Correlations, quality report, export.
9. Automated tests, edge case checks.

**Phase 3: Polish**
10. Brand system, improved spacing and typography, loading messages, narrative insights, accessibility.
11. README with screenshots only after real UI exists, explanation of dataset, assumptions, and analysis limitations.
12. Final quality check using an actual CSV.

## 11. Acceptance criteria
- `pip install -r requirements.txt` then `streamlit run app.py` starts successfully.
- A reasonable car CSV uploads without modifying source code.
- Common column aliases are recognized, with manual mapping fallback.
- Filtering updates KPIs, tables, and plots consistently.
- Seaborn and Matplotlib are used substantively, not only imported.
- All displayed metrics are computed from loaded data and clearly labeled.
- The app handles missing columns, empty filtered selections, invalid data, and constant values without crashing.
- All downloads include the intended rows and columns.
- Code includes clear comments explaining Pandas operations suitable for a student learning data analytics.
- Tests cover numeric parsing, mappings, aggregations, empty input, and missing values.
- No fake dataset metrics, fake “AI insights”, nonfunctional buttons, or placeholder pages.

## 12. How Gemini should work
- First inspect repository files, including `brandGuidelines.md`, before making changes.
- Ask for a CSV if no dataset has been provided; still implement file-upload support independently.
- State assumptions about dataset fields/units and propose mappings before writing dataset-specific analyses.
- Implement in coherent steps; prefer functioning code over lengthy speculative descriptions.
- When editing, explain major choices concisely and show commands for running/testing.
- When an analysis cannot be completed with the actual data, say which field is missing and provide an appropriate alternative.
- Do not invent data, analysis results, screenshots, files, tests, or successful execution.
