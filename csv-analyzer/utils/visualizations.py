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
