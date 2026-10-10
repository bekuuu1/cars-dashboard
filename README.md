# CarScope — Vehicle Intelligence & Analytics Platform

[![Live Demo](https://img.shields.io/badge/Live_Demo-CarScope_Web_App-1DB954?style=for-the-badge&logo=google-chrome&logoColor=white)](https://bekuuu1.github.io/cars-dashboard/)
[![Dataset](https://img.shields.io/badge/Dataset-Vehicle_Market_Data-00F2FE?style=for-the-badge&logo=kaggle&logoColor=black)](https://github.com/bekuuu1/cars-dashboard)
[![License](https://img.shields.io/badge/License-MIT-8A2BE2?style=for-the-badge)](LICENSE)

> 🚀 **Live Demo Available**: Experience the application instantly at **[https://bekuuu1.github.io/cars-dashboard/](https://bekuuu1.github.io/cars-dashboard/)**

---

CarScope is a senior-level Python data analytics application and interactive dashboard built using **Pandas**, **Seaborn**, **Matplotlib**, and **Streamlit**. It allows data analysts, researchers, and students to import vehicle CSV datasets, dynamically clean and map column schemas, perform statistical visual analytics, execute multi-car side-by-side comparative analyses, and inspect underlying Pandas operations via interactive learning snippets.

---

## 🌟 Key Features

1. **Flexible CSV Ingestion & Automatic Column Mapping**:
   - Upload custom vehicle CSV datasets or explore using the pre-packaged dataset (`data/sample_cars.csv`).
   - Heuristic automatic mapping for common aliases (`manufacturer` -> `make`, `selling_price` -> `price`, `odometer` -> `mileage`, `power` -> `horsepower`, `gearbox` -> `transmission`, etc.).
   - Fallback UI to manually select or adjust field mappings.

2. **Defensive Data Cleaning & Quality Auditing**:
   - Safe parsing of messy numeric values (`$24,500`, `31,000 mi`, `2.0 L`, `150 hp`).
   - Categorical text normalization (Title Case for makes, models, fuel types, transmissions).
   - Identification of exact and listing duplicates.
   - Outlier detection (non-positive prices, negative mileage, unrealistic years).
   - Generates stable, unique vehicle identifiers (`car_id`) to differentiate identical display names.

3. **7 Interactive Analytics Pages**:
   - **Page A — Overview**: Title banner, 5 KPI cards (Total Count, Unique Makes, Median Price, Avg Mileage, Year Range), Seaborn top makes volume chart, Matplotlib price distribution with KDE & mean/median markers, model year histogram, and data health mini-summary.
   - **Page B — Explore Data**: Case-insensitive text search, column sort controls, interactive dataframe display, filter summary, and filtered CSV export.
   - **Page C — Price Analytics**: Mean vs. median price by brand (with minimum sample size threshold), price progression by vehicle year, price vs. mileage scatterplot with linear regression & Pearson correlation label, and price boxplots by transmission or fuel type.
   - **Page D — Compare Cars**: Side-by-side specification table for 2 to 4 selected vehicles, min/max attribute highlighting, and Min-Max normalized (0.0 to 1.0) metric comparative charts.
   - **Page E — Brand & Segment Insights**: Brand volume rankings, brand price tables, transmission & fuel type composition, and two-brand head-to-head comparative analysis.
   - **Page F — Correlations**: Numeric variable selector, Pearson vs. Spearman correlation matrix toggle, Seaborn correlation heatmap with diverging palette, and pairwise scatterplots.
   - **Page G — Data Quality & Methods**: Pipeline audit log (raw vs cleaned counts, missingness bar plot, outlier report), `df.describe()` table, cleaned CSV export, and educational Pandas snippets.

4. **Brand Design Guidelines**:
   - Styled strictly adhering to `brandGuidelines.md` with dark navy canvas (`#0B1220`), surface panels (`#162338`), electric cyan primary accents (`#43C6DB`), tabular numerals, and high-contrast accessible Seaborn palette.

5. **Educational Priority**:
   - Every page includes a **"📘 Pandas Behind the Chart"** expander displaying exact Python code snippets (`.groupby()`, `.agg()`, `.corr()`, `.sort_values()`, boolean index masks) for students learning data science.

---

## 📁 Project Architecture

```text
cars-dashboard/
├── gemini.md                 # Technical prompt and project specifications
├── brandGuidelines.md        # UI design, color system, and visualization standards
├── app.py                    # Main Streamlit dashboard application
├── requirements.txt          # Dependencies (Streamlit, Pandas, Seaborn, Matplotlib, Pytest)
├── README.md                 # Project documentation
├── .gitignore                # Git exclusions
├── .streamlit/
│   └── config.toml           # Streamlit theme configuration (Dark Navy)
├── data/
│   ├── README.md             # Dataset upload documentation & privacy overview
│   └── sample_cars.csv       # Pre-packaged 60-row realistic sample car dataset
├── src/
│   ├── __init__.py           # Source package initializer
│   ├── ui.py                 # Custom CSS, headers, KPI cards & learning snippets
│   ├── data_loader.py        # Safe CSV parsing & metadata extraction
│   ├── column_mapping.py     # Canonical field schema & alias matching heuristics
│   ├── cleaning.py           # Text standardization, numeric parsing & outlier detection
│   ├── analytics.py          # Pandas aggregations, correlations & min-max scaling
│   ├── charts.py             # Seaborn & Matplotlib chart renderers
│   └── filters.py            # Dynamic Streamlit sidebar filters & DataFrame slicing
└── tests/
    ├── test_cleaning.py      # Pytest suite for cleaning & mapping logic
    └── test_analytics.py     # Pytest suite for KPIs, aggregations & comparison math
```

---

## ⚙️ Quickstart & Setup

### 1. Prerequisites
Ensure Python 3.11+ is installed.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Dashboard Locally
```bash
streamlit run app.py
```
CarScope will open automatically in your browser at `http://localhost:8501`.

### 4. Live Demo via GitHub Pages
Experience CarScope live in your browser without local installation:
- 🚀 **[https://bekuuu1.github.io/cars-dashboard/](https://bekuuu1.github.io/cars-dashboard/)**

---

## 🧪 Running Automated Tests

Run the full pytest suite to verify dataset loading, string parsing, duplicate detection, KPI calculations, and vehicle min-max scaling:

```bash
python -m pytest tests/ -v
```

---

## 🛡️ License & Data Ethics
- All dataset operations are performed **100% locally**.
- Observational trends and correlations displayed in CarScope represent sample characteristics and do not imply causal relationships or official market valuations.
