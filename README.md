# CarScope 🚘 — Interactive Vehicle Data Analytics & Comparative Dashboard

> **Explore cars. Compare smarter.**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://cars-dashboard-bekuuu1.streamlit.app)
[![GitHub Repository](https://img.shields.io/badge/GitHub-bekuuu1%2Fcars--dashboard-181717?logo=github)](https://github.com/bekuuu1/cars-dashboard)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)

---

### 🌐 Live Demo
- 🚀 **Live Interactive Demo:** [Launch CarScope on Streamlit Community Cloud](https://cars-dashboard-bekuuu1.streamlit.app)
- 📂 **GitHub Repository:** [https://github.com/bekuuu1/cars-dashboard](https://github.com/bekuuu1/cars-dashboard)

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

### 4. Deploy Live to Streamlit Community Cloud
You can host and share your live CarScope dashboard online for free in under two minutes:
1. Ensure your repository is pushed to GitHub at [bekuuu1/cars-dashboard](https://github.com/bekuuu1/cars-dashboard).
2. Go to [share.streamlit.io](https://share.streamlit.io) and log in with your GitHub account.
3. Click **"New app"** (or **"Create app"**).
4. Fill in the deployment details:
   - **Repository:** `bekuuu1/cars-dashboard`
   - **Branch:** `main`
   - **Main file path:** `app.py`
   - **App URL:** `cars-dashboard-bekuuu1` (or custom name of your choice)
5. Click **"Deploy!"**
Your dashboard will build and be live at `https://cars-dashboard-bekuuu1.streamlit.app`.

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
