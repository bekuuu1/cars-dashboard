"""
Visualization module for CarScope.
Generates Seaborn and Matplotlib figures styled in a clean light-mode theme.
Ensures memory management by closing figures after Streamlit rendering.
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Optional, List
from src.ui import (
    COLOR_BACKGROUND, COLOR_SURFACE, COLOR_BORDER,
    COLOR_TEXT_PRIMARY, COLOR_TEXT_SECONDARY,
    COLOR_PRIMARY, COLOR_SECONDARY, COLOR_POSITIVE,
    COLOR_WARNING, COLOR_DANGER, CHART_PALETTE
)


def apply_chart_style(fig: plt.Figure, ax: plt.Axes):
    """
    Apply clean light-mode styling to Matplotlib figure and axes without line clutter.
    """
    fig.patch.set_facecolor(COLOR_SURFACE)
    ax.set_facecolor(COLOR_SURFACE)

    # Remove top and right spines to reduce line clutter
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#CBD5E1")
    ax.spines["bottom"].set_color("#CBD5E1")

    # Ticks and tick labels
    ax.tick_params(colors=COLOR_TEXT_SECONDARY, labelsize=10)
    ax.xaxis.label.set_color(COLOR_TEXT_PRIMARY)
    ax.yaxis.label.set_color(COLOR_TEXT_PRIMARY)
    ax.xaxis.label.set_size(11)
    ax.yaxis.label.set_size(11)
    ax.title.set_color(COLOR_TEXT_PRIMARY)
    ax.title.set_size(13)
    ax.title.set_weight("bold")

    # Subtle gridlines
    ax.grid(True, color="#F1F5F9", linestyle="--", alpha=0.7)


def plot_top_makes(df: pd.DataFrame, top_n: int = 10) -> Optional[plt.Figure]:
    """
    Render Seaborn horizontal bar plot of top vehicle makes by listing count.
    """
    if df.empty or "make" not in df.columns:
        return None

    counts = df["make"].value_counts().head(top_n).reset_index()
    counts.columns = ["make", "count"]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    apply_chart_style(fig, ax)

    sns.barplot(
        data=counts,
        y="make",
        x="count",
        hue="make",
        legend=False,
        ax=ax,
        palette=[COLOR_PRIMARY] * len(counts),
        edgecolor=COLOR_BORDER
    )

    ax.set_title(f"Top {top_n} Makes by Listing Volume", pad=12)
    ax.set_xlabel("Number of Listings")
    ax.set_ylabel("Make")

    # Value annotations on bars
    for p in ax.patches:
        width = p.get_width()
        ax.annotate(
            f"{int(width):,}",
            (width, p.get_y() + p.get_height() / 2.0),
            ha="left", va="center",
            xytext=(6, 0),
            textcoords="offset points",
            color=COLOR_TEXT_PRIMARY,
            fontsize=9.5,
            weight="bold"
        )

    ax.set_xlim(0, counts["count"].max() * 1.15)
    plt.tight_layout()
    return fig


def plot_price_distribution(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Render Matplotlib histogram with optional Seaborn KDE curve and mean/median markers.
    """
    if df.empty or "price" not in df.columns:
        return None

    valid = df["price"].dropna()
    if valid.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4.5))
    apply_chart_style(fig, ax)

    sns.histplot(
        valid,
        kde=True,
        ax=ax,
        color=COLOR_PRIMARY,
        edgecolor=COLOR_BORDER,
        alpha=0.6,
        line_kws={"color": COLOR_SECONDARY, "linewidth": 2.5}
    )

    mean_val = valid.mean()
    median_val = valid.median()

    ax.axvline(mean_val, color=COLOR_DANGER, linestyle="--", linewidth=2, label=f"Mean: ${mean_val:,.0f}")
    ax.axvline(median_val, color=COLOR_POSITIVE, linestyle="-", linewidth=2, label=f"Median: ${median_val:,.0f}")

    ax.set_title("Price Distribution & Density Estimation", pad=12)
    ax.set_xlabel("Price ($)")
    ax.set_ylabel("Frequency / Count")
    ax.legend(facecolor=COLOR_SURFACE, edgecolor=COLOR_BORDER, labelcolor=COLOR_TEXT_PRIMARY)

    plt.tight_layout()
    return fig


def plot_year_distribution(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Render Matplotlib/Seaborn distribution plot of vehicle manufacture years.
    """
    if df.empty or "year" not in df.columns:
        return None

    valid = df["year"].dropna()
    if valid.empty:
        return None

    fig, ax = plt.subplots(figsize=(8, 4.5))
    apply_chart_style(fig, ax)

    sns.histplot(
        valid,
        discrete=True,
        ax=ax,
        color=COLOR_SECONDARY,
        edgecolor=COLOR_BORDER,
        alpha=0.8
    )

    ax.set_title("Vehicle Distribution by Model Year", pad=12)
    ax.set_xlabel("Model Year")
    ax.set_ylabel("Count")

    plt.tight_layout()
    return fig


def plot_price_by_make(df_price_by_make: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Render Seaborn horizontal bar chart comparing mean vs median price by make.
    """
    if df_price_by_make.empty:
        return None

    top_df = df_price_by_make.head(12)

    fig, ax = plt.subplots(figsize=(9, 5.5))
    apply_chart_style(fig, ax)

    y_indices = np.arange(len(top_df))
    bar_height = 0.38

    ax.barh(y_indices - bar_height / 2, top_df["median_price"], height=bar_height, label="Median Price", color=COLOR_PRIMARY, edgecolor=COLOR_BORDER)
    ax.barh(y_indices + bar_height / 2, top_df["mean_price"], height=bar_height, label="Mean Price", color=COLOR_SECONDARY, edgecolor=COLOR_BORDER, alpha=0.7)

    ax.set_yticks(y_indices)
    ax.set_yticklabels(top_df["make"])
    ax.invert_yaxis()

    ax.set_title("Mean vs. Median Price by Make", pad=12)
    ax.set_xlabel("Price ($)")
    ax.legend(facecolor=COLOR_SURFACE, edgecolor=COLOR_BORDER, labelcolor=COLOR_TEXT_PRIMARY)

    plt.tight_layout()
    return fig


def plot_price_vs_year(df_price_vs_year: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Render Matplotlib line plot illustrating average and median price progression over years.
    """
    if df_price_vs_year.empty:
        return None

    fig, ax = plt.subplots(figsize=(9, 4.8))
    apply_chart_style(fig, ax)

    ax.plot(df_price_vs_year["year"], df_price_vs_year["median_price"], marker="o", color=COLOR_PRIMARY, linewidth=2.5, label="Median Price")
    ax.plot(df_price_vs_year["year"], df_price_vs_year["mean_price"], marker="s", color=COLOR_SECONDARY, linewidth=2.0, linestyle="--", label="Mean Price")

    ax.set_title("Vehicle Price Progression by Production Year", pad=12)
    ax.set_xlabel("Production Year")
    ax.set_ylabel("Price ($)")
    ax.legend(facecolor=COLOR_SURFACE, edgecolor=COLOR_BORDER, labelcolor=COLOR_TEXT_PRIMARY)

    plt.tight_layout()
    return fig


def plot_price_vs_mileage(df: pd.DataFrame, show_regression: bool = True) -> Optional[plt.Figure]:
    """
    Render Seaborn scatter plot of Price vs. Mileage with linear regression option.
    """
    if df.empty or "price" not in df.columns or "mileage" not in df.columns:
        return None

    valid = df.dropna(subset=["price", "mileage"])
    if valid.empty:
        return None

    fig, ax = plt.subplots(figsize=(8.5, 5))
    apply_chart_style(fig, ax)

    if show_regression:
        sns.regplot(
            data=valid,
            x="mileage",
            y="price",
            ax=ax,
            scatter_kws={"color": COLOR_PRIMARY, "alpha": 0.6, "s": 35},
            line_kws={"color": COLOR_DANGER, "linewidth": 2}
        )
    else:
        sns.scatterplot(
            data=valid,
            x="mileage",
            y="price",
            ax=ax,
            color=COLOR_PRIMARY,
            alpha=0.6,
            s=35
        )

    corr_val = valid["price"].corr(valid["mileage"])
    if pd.notna(corr_val):
        ax.text(
            0.95, 0.92,
            f"Pearson r = {corr_val:.2f}",
            transform=ax.transAxes,
            ha="right", va="top",
            bbox=dict(boxstyle="round,pad=0.4", facecolor=COLOR_SURFACE, edgecolor=COLOR_BORDER),
            color=COLOR_TEXT_PRIMARY,
            fontsize=10, weight="bold"
        )

    ax.set_title("Vehicle Price vs. Mileage", pad=12)
    ax.set_xlabel("Mileage")
    ax.set_ylabel("Price ($)")

    plt.tight_layout()
    return fig


def plot_price_by_category(df: pd.DataFrame, category_col: str) -> Optional[plt.Figure]:
    """
    Render Seaborn boxplot illustrating price distributions across categorical segments.
    """
    if df.empty or "price" not in df.columns or category_col not in df.columns:
        return None

    valid = df.dropna(subset=["price", category_col])
    if valid.empty:
        return None

    fig, ax = plt.subplots(figsize=(8.5, 5))
    apply_chart_style(fig, ax)

    n_cats = valid[category_col].nunique()
    palette_use = (CHART_PALETTE * ((n_cats // len(CHART_PALETTE)) + 1))[:n_cats]

    sns.boxplot(
        data=valid,
        x=category_col,
        y="price",
        hue=category_col,
        legend=False,
        ax=ax,
        palette=palette_use,
        boxprops=dict(edgecolor=COLOR_TEXT_PRIMARY),
        medianprops=dict(color=COLOR_TEXT_PRIMARY, linewidth=2.5),
        flierprops=dict(marker="o", color=COLOR_DANGER, alpha=0.5)
    )

    ax.set_title(f"Price Distribution by {category_col.replace('_', ' ').title()}", pad=12)
    ax.set_xlabel(category_col.replace('_', ' ').title())
    ax.set_ylabel("Price ($)")
    plt.xticks(rotation=15)

    plt.tight_layout()
    return fig


def plot_car_comparison_normalized(normalized_df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Render Seaborn horizontal grouped bar chart showing 0-to-1 min-max normalized scores.
    """
    if normalized_df.empty:
        return None

    fig, ax = plt.subplots(figsize=(9, 5.5))
    apply_chart_style(fig, ax)

    n_cars = normalized_df["car_id"].nunique()
    palette_use = (CHART_PALETTE * ((n_cars // len(CHART_PALETTE)) + 1))[:n_cars]

    sns.barplot(
        data=normalized_df,
        y="metric",
        x="normalized_score",
        hue="car_id",
        ax=ax,
        palette=palette_use,
        edgecolor=COLOR_BORDER
    )

    ax.set_title("Normalized Metric Comparison (0.0 = Min, 1.0 = Max in Selection)", pad=12)
    ax.set_xlabel("Relative Score (Min-Max Scaled)")
    ax.set_ylabel("Metric")
    ax.set_xlim(0, 1.1)

    ax.legend(
        facecolor=COLOR_SURFACE,
        edgecolor=COLOR_BORDER,
        labelcolor=COLOR_TEXT_PRIMARY,
        title="Vehicle",
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.tight_layout()
    return fig


def plot_correlation_heatmap(corr_df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Render Seaborn correlation heatmap centered at zero using a clean palette.
    """
    if corr_df.empty:
        return None

    fig, ax = plt.subplots(figsize=(7.5, 6))
    apply_chart_style(fig, ax)

    sns.heatmap(
        corr_df,
        annot=True,
        fmt=".2f",
        cmap="Blues",
        center=0,
        vmin=-1.0,
        vmax=1.0,
        ax=ax,
        cbar_kws={"label": "Correlation Coefficient"},
        square=True,
        linewidths=1,
        linecolor=COLOR_BORDER
    )

    ax.set_title("Numeric Variable Correlation Matrix", pad=12)
    plt.xticks(rotation=45, ha="right")
    plt.yticks(rotation=0)

    plt.tight_layout()
    return fig


def plot_missingness(df: pd.DataFrame) -> Optional[plt.Figure]:
    """
    Render horizontal bar plot showing missing cell percentage per canonical field.
    """
    if df.empty:
        return None

    missing_pct = (df.isna().sum() / len(df) * 100).sort_values(ascending=True)
    missing_df = missing_pct.reset_index()
    missing_df.columns = ["field", "missing_pct"]

    fig, ax = plt.subplots(figsize=(8, 4.5))
    apply_chart_style(fig, ax)

    sns.barplot(
        data=missing_df,
        y="field",
        x="missing_pct",
        hue="field",
        legend=False,
        ax=ax,
        palette=[COLOR_WARNING if p > 0 else COLOR_PRIMARY for p in missing_df["missing_pct"]],
        edgecolor=COLOR_BORDER
    )

    ax.set_title("Missing Data Percentage by Field", pad=12)
    ax.set_xlabel("Missing Percentage (%)")
    ax.set_ylabel("Canonical Field")
    ax.set_xlim(0, max(100, missing_df["missing_pct"].max() * 1.15))

    for p in ax.patches:
        width = p.get_width()
        ax.annotate(
            f"{width:.1f}%",
            (width, p.get_y() + p.get_height() / 2.0),
            ha="left", va="center",
            xytext=(6, 0),
            textcoords="offset points",
            color=COLOR_TEXT_PRIMARY,
            fontsize=9.5
        )

    plt.tight_layout()
    return fig
