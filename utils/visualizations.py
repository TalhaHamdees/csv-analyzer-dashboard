"""Chart generation functions using Plotly Express.

Each function takes a DataFrame and returns a Plotly figure (or None when
there is no applicable data). No Streamlit imports — keeps visualization
logic separate from the UI layer.
"""

import pandas as pd
import plotly.express as px


def create_histogram(df, column_name):
    """Create a histogram showing the distribution of a single numeric column.

    Returns a Plotly figure.
    """
    fig = px.histogram(
        df,
        x=column_name,
        title=f"Distribution of {column_name}",
        labels={column_name: column_name, "count": "Count"},
    )
    # Clean up the layout — remove clutter, keep it readable
    fig.update_layout(bargap=0.1, showlegend=False)
    return fig


def create_bar_chart(df, column_name, max_categories=10):
    """Create a bar chart showing the most common values in a categorical column.

    Caps at max_categories to keep the chart readable.
    Returns None if the column has no non-null values.
    """
    # Drop missing values before counting
    value_counts = df[column_name].dropna().value_counts().head(max_categories)

    if value_counts.empty:
        return None

    # Decide title based on whether we're showing all values or just the top N
    total_unique = df[column_name].nunique()
    if total_unique > max_categories:
        title = f"Top {max_categories} values in {column_name}"
    else:
        title = f"Value counts for {column_name}"

    fig = px.bar(
        x=value_counts.index.astype(str),
        y=value_counts.values,
        title=title,
        labels={"x": column_name, "y": "Count"},
    )
    fig.update_layout(showlegend=False)
    return fig


def create_correlation_heatmap(df):
    """Create a heatmap showing correlations between all numeric columns.

    Returns None if fewer than 2 numeric columns exist (no meaningful correlation).
    """
    numeric_df = df.select_dtypes(include="number")

    if numeric_df.shape[1] < 2:
        return None

    correlation_matrix = numeric_df.corr()

    fig = px.imshow(
        correlation_matrix,
        text_auto=".2f",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1,
        aspect="auto",
        title="Correlation Matrix",
    )
    return fig


def create_scatter_plot(df, x_col, y_col, color_col=None):
    """Create a scatter plot comparing two numeric columns.

    Optionally color points by a third column (numeric or categorical).
    Returns None if either x_col or y_col is missing from the DataFrame.
    """
    if x_col not in df.columns or y_col not in df.columns:
        return None

    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        title=f"{y_col} vs {x_col}",
        labels={x_col: x_col, y_col: y_col},
    )
    # Only show legend when color grouping is active
    fig.update_layout(showlegend=color_col is not None)
    return fig


def create_missing_bar_chart(df):
    """Create a horizontal bar chart showing missing data percentage per column.

    Only includes columns that have at least one missing value.
    Returns None if no columns have missing data.
    """
    missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
    # Keep only columns with missing data, sorted worst-to-best
    missing_pct = missing_pct[missing_pct > 0].sort_values(ascending=True)

    if missing_pct.empty:
        return None

    fig = px.bar(
        x=missing_pct.values,
        y=missing_pct.index,
        orientation="h",
        title="Missing Data by Column",
        labels={"x": "Missing %", "y": ""},
    )
    fig.update_layout(showlegend=False)
    return fig


def create_missing_heatmap(df, max_rows=100):
    """Create a heatmap showing where missing values are located.

    Caps at max_rows to avoid performance issues with large datasets.
    Only shows columns that have at least one missing value.
    Returns None if no columns have missing data.
    """
    # Find columns that actually have missing data
    cols_with_missing = [col for col in df.columns if df[col].isnull().any()]

    if not cols_with_missing:
        return None

    # Cap rows for performance and build a binary matrix (1 = missing, 0 = present)
    capped_df = df[cols_with_missing].head(max_rows)
    actual_rows = len(capped_df)
    missing_matrix = capped_df.isnull().astype(int)

    fig = px.imshow(
        missing_matrix.T,
        color_continuous_scale=["#2196F3", "#FF5722"],
        aspect="auto",
        title=f"Missing Data Pattern (first {actual_rows} rows)",
        labels={"x": "Row", "y": "Column", "color": "Missing"},
    )
    return fig


def create_line_chart(df, date_col, value_col):
    """Create a line chart showing a numeric value over time.

    Parses the date column, drops unparseable rows, and sorts by date.
    Returns None if either column is missing from the DataFrame.
    """
    if date_col not in df.columns or value_col not in df.columns:
        return None

    # Work on a copy to avoid modifying the original
    plot_df = df[[date_col, value_col]].copy()
    plot_df[date_col] = pd.to_datetime(plot_df[date_col], errors="coerce")

    # Drop rows where the date couldn't be parsed
    plot_df = plot_df.dropna(subset=[date_col])

    if plot_df.empty:
        return None

    # Sort chronologically for a clean line
    plot_df = plot_df.sort_values(by=date_col)

    fig = px.line(
        plot_df,
        x=date_col,
        y=value_col,
        title=f"{value_col} over {date_col}",
    )
    return fig
