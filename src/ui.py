"""
UI helper module for CarScope.
Applies clean, minimal light-mode CSS with soft elevation shadows,
no heavy outline borders, a minimal header, and guarantees sidebar navigation buttons stay visible.
"""

import streamlit as st

# Color Palette Constants (Clean Minimal Light Mode)
COLOR_BACKGROUND = "#F8FAFC"
COLOR_SIDEBAR = "#F1F5F9"
COLOR_SURFACE = "#FFFFFF"
COLOR_BORDER = "#E2E8F0"
COLOR_TEXT_PRIMARY = "#0F172A"
COLOR_TEXT_SECONDARY = "#475569"
COLOR_PRIMARY = "#0284C7"
COLOR_SECONDARY = "#6366F1"
COLOR_POSITIVE = "#10B981"
COLOR_WARNING = "#F59E0B"
COLOR_DANGER = "#EF4444"

# Seaborn / Matplotlib palette sequence
CHART_PALETTE = [
    "#0284C7", "#6366F1", "#10B981", "#F59E0B",
    "#EF4444", "#8B5CF6", "#06B6D4", "#84CC16"
]


def apply_custom_css():
    """Inject minimal light-mode CSS with soft card shadows, clean typography, visible sidebar toggle, and no line clutter."""
    css = f"""
    <style>
        /* Force Root & Main Canvas Background */
        html, body, .stApp, [data-testid="stAppViewContainer"], .stMain {{
            background-color: {COLOR_BACKGROUND} !important;
            color: {COLOR_TEXT_PRIMARY} !important;
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
        }}

        /* Header Bar Background */
        [data-testid="stHeader"] {{
            background-color: {COLOR_BACKGROUND} !important;
        }}

        /* Hide ONLY Streamlit Deploy Button */
        [data-testid="stDeployButton"],
        [data-testid="stAppDeployButton"],
        .stDeployButton,
        .stAppDeployButton,
        button[title*="Deploy"] {{
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            pointer-events: none !important;
        }}

        /* Explicitly keep Sidebar Expand / Collapse Toggle Button visible & styled at all times */
        [data-testid="stCollapsedControl"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stSidebarExpandButton"],
        [data-testid="stHeaderSidebarToggle"],
        button[data-testid="stSidebarCollapseButton"],
        button[data-testid="stSidebarExpandButton"],
        button[data-testid="stHeaderSidebarToggle"],
        button[aria-label*="sidebar" i],
        button[title*="sidebar" i],
        button[aria-label*="Sidebar" i],
        button[title*="Sidebar" i] {{
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            color: {COLOR_TEXT_PRIMARY} !important;
            background-color: {COLOR_SURFACE} !important;
            border: 1px solid {COLOR_BORDER} !important;
            border-radius: 8px !important;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.08) !important;
            z-index: 999999 !important;
            transition: background-color 0.15s ease, border-color 0.15s ease !important;
        }}

        [data-testid="stCollapsedControl"]:hover,
        [data-testid="stSidebarCollapseButton"]:hover,
        [data-testid="stSidebarExpandButton"]:hover,
        [data-testid="stHeaderSidebarToggle"]:hover,
        button[aria-label*="sidebar" i]:hover {{
            background-color: #F1F5F9 !important;
            border-color: {COLOR_PRIMARY} !important;
        }}

        /* SVG icons inside sidebar toggle buttons */
        [data-testid="stCollapsedControl"] svg,
        [data-testid="stSidebarCollapseButton"] svg,
        [data-testid="stSidebarExpandButton"] svg,
        [data-testid="stHeaderSidebarToggle"] svg,
        button[data-testid="stHeaderSidebarToggle"] svg,
        button[aria-label*="sidebar" i] svg,
        button[title*="sidebar" i] svg {{
            color: {COLOR_TEXT_PRIMARY} !important;
            fill: {COLOR_TEXT_PRIMARY} !important;
            stroke: {COLOR_TEXT_PRIMARY} !important;
            width: 1.25rem !important;
            height: 1.25rem !important;
            display: block !important;
            visibility: visible !important;
            opacity: 1 !important;
        }}

        [data-testid="stCollapsedControl"] svg path,
        [data-testid="stSidebarCollapseButton"] svg path,
        [data-testid="stSidebarExpandButton"] svg path,
        [data-testid="stHeaderSidebarToggle"] svg path,
        button[aria-label*="sidebar" i] svg path {{
            fill: {COLOR_TEXT_PRIMARY} !important;
            stroke: {COLOR_TEXT_PRIMARY} !important;
        }}

        /* Keep Three-Dots menu visible */
        [data-testid="stMainMenu"],
        [data-testid="stMainMenu"] button,
        header button[aria-label="Main menu"] {{
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }}

        /* Sidebar Styling */
        section[data-testid="stSidebar"], [data-testid="stSidebarNav"] {{
            background-color: {COLOR_SIDEBAR} !important;
            border-right: 1px solid {COLOR_BORDER} !important;
        }}

        /* Sidebar Navigation Radio Options Styling */
        div[data-testid="stRadio"] label {{
            font-weight: 500 !important;
            color: {COLOR_TEXT_PRIMARY} !important;
            padding: 0.35rem 0.6rem !important;
            border-radius: 6px !important;
            transition: background-color 0.15s ease !important;
        }}
        div[data-testid="stRadio"] label:hover {{
            background-color: rgba(2, 132, 199, 0.08) !important;
            color: {COLOR_PRIMARY} !important;
        }}

        /* Typography Color Overrides */
        h1, h2, h3, h4, h5, h6, p, span, label, div, li, small {{
            color: {COLOR_TEXT_PRIMARY} !important;
        }}
        .stCaption, [data-testid="stCaptionContainer"] p {{
            color: {COLOR_TEXT_SECONDARY} !important;
        }}

        /* Minimal Header Container */
        .carscope-header {{
            margin-bottom: 1.25rem;
            padding-bottom: 0.75rem;
        }}
        .carscope-title {{
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.02em;
            color: {COLOR_TEXT_PRIMARY} !important;
            margin: 0;
        }}
        .carscope-title span {{
            color: {COLOR_PRIMARY} !important;
        }}

        /* Soft Highlight KPI Cards */
        .kpi-card {{
            background-color: {COLOR_SURFACE} !important;
            border: none !important;
            border-radius: 12px;
            padding: 1.25rem 1.4rem;
            margin-bottom: 1rem;
            box-shadow: 0 4px 14px rgba(15, 23, 42, 0.05) !important;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
        }}
        .kpi-card:hover {{
            box-shadow: 0 6px 18px rgba(2, 132, 199, 0.1) !important;
        }}
        .kpi-label {{
            font-size: 0.8rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: {COLOR_TEXT_SECONDARY} !important;
            margin-bottom: 0.4rem;
        }}
        .kpi-value {{
            font-size: 1.85rem;
            font-weight: 700;
            color: {COLOR_TEXT_PRIMARY} !important;
            font-feature-settings: "tnum";
            font-variant-numeric: tabular-nums;
            line-height: 1.1;
        }}
        .kpi-subtext {{
            font-size: 0.78rem;
            color: {COLOR_TEXT_SECONDARY} !important;
            margin-top: 0.35rem;
        }}

        /* Soft Highlighted Cards for Containers & Plot Cards */
        [data-testid="stVerticalBlockBorderWrapper"] {{
            background-color: {COLOR_SURFACE} !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 1.25rem !important;
            margin-bottom: 1.25rem !important;
            box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05) !important;
        }}

        [data-testid="stImage"] {{
            background-color: {COLOR_SURFACE} !important;
            border: none !important;
            border-radius: 10px !important;
            padding: 0.4rem !important;
        }}

        /* Status Badge */
        .status-badge {{
            display: inline-flex;
            align-items: center;
            padding: 0.35rem 0.85rem;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: 600;
            background-color: rgba(2, 132, 199, 0.08) !important;
            color: {COLOR_PRIMARY} !important;
            border: 1px solid rgba(2, 132, 199, 0.2) !important;
        }}

        /* Expander & Code Box */
        [data-testid="stExpander"] {{
            background-color: {COLOR_SURFACE} !important;
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 2px 8px rgba(15, 23, 42, 0.04) !important;
        }}

        /* Buttons Styling */
        .stButton button, .stDownloadButton button {{
            background-color: {COLOR_PRIMARY} !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            border: none !important;
            box-shadow: 0 2px 4px rgba(2, 132, 199, 0.2) !important;
        }}
        .stButton button:hover, .stDownloadButton button:hover {{
            background-color: #0369A1 !important;
        }}

        /* Form Controls & Dropdowns */
        div[data-baseweb="select"] > div {{
            background-color: {COLOR_SURFACE} !important;
            border-color: {COLOR_BORDER} !important;
            color: {COLOR_TEXT_PRIMARY} !important;
            border-radius: 8px !important;
        }}
        input[type="text"] {{
            background-color: {COLOR_SURFACE} !important;
            color: {COLOR_TEXT_PRIMARY} !important;
            border-color: {COLOR_BORDER} !important;
            border-radius: 8px !important;
        }}

        /* Dataframe & Table Card Container */
        [data-testid="stDataFrame"], div[data-testid="stTable"] {{
            background-color: {COLOR_SURFACE} !important;
            border: none !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.04) !important;
        }}

        /* Empty state notification box */
        .empty-state-box {{
            background-color: {COLOR_SURFACE} !important;
            border: 1px dashed {COLOR_BORDER} !important;
            border-radius: 10px;
            padding: 2rem;
            text-align: center;
            color: {COLOR_TEXT_SECONDARY} !important;
            margin: 1.5rem 0;
            box-shadow: 0 2px 6px rgba(15, 23, 42, 0.03);
        }}
        .empty-state-title {{
            font-size: 1.1rem;
            font-weight: 600;
            color: {COLOR_TEXT_PRIMARY} !important;
            margin-bottom: 0.5rem;
        }}

        /* Section headers */
        .section-header {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {COLOR_TEXT_PRIMARY} !important;
            margin-top: 1.5rem;
            margin-bottom: 0.8rem;
        }}

        /* Clean Streamlit tab styling override */
        button[data-baseweb="tab"] {{
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def render_header(dataset_name: str, total_rows: int, status_text: str = "Active"):
    """Render minimal CarScope title header without tagline or subtitle."""
    st.markdown(
        f"""
        <div class="carscope-header">
            <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem;">
                <div>
                    <h1 class="carscope-title">Car<span>Scope</span></h1>
                </div>
                <div>
                    <div class="status-badge">
                        {dataset_name} ({total_rows:,} rows)
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_kpi_card(label: str, value: str, subtext: str = ""):
    """Render a clean light-mode KPI card with soft shadow highlight."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-label">{label}</div>
            <div class="kpi-value">{value}</div>
            {f'<div class="kpi-subtext">{subtext}</div>' if subtext else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_empty_state(title: str = "No vehicles match the selected filters", message: str = "Try adjusting your sidebar filter choices or resetting all filters."):
    """Render minimal empty state feedback box."""
    st.markdown(
        f"""
        <div class="empty-state-box">
            <div class="empty-state-title">{title}</div>
            <div>{message}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pandas_snippet(title: str, code_snippet: str, explanation: str = ""):
    """Render a clean learning expander with Pandas code snippet."""
    with st.expander(f"Pandas Behind the Chart — {title}"):
        if explanation:
            st.markdown(f"*{explanation}*")
        st.code(code_snippet.strip(), language="python")
