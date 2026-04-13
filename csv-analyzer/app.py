import streamlit as st
import pandas as pd
from utils.data_profiler import get_column_info, get_numeric_stats, get_categorical_stats
from utils.visualizations import create_histogram, create_bar_chart, create_correlation_heatmap, create_scatter_plot
from utils.filters import get_filterable_columns, apply_filters, sort_dataframe, convert_df_to_csv


# --- Cached wrappers ---
# These thin functions keep Streamlit caching out of data_profiler.py
# so the profiler stays a pure-pandas module we can test independently.
@st.cache_data
def cached_column_info(df):
    return get_column_info(df)


@st.cache_data
def cached_numeric_stats(df):
    return get_numeric_stats(df)


@st.cache_data
def cached_categorical_stats(df):
    return get_categorical_stats(df)


@st.cache_data
def cached_histogram(df, column_name):
    return create_histogram(df, column_name)


@st.cache_data
def cached_bar_chart(df, column_name):
    return create_bar_chart(df, column_name)


@st.cache_data
def cached_correlation_heatmap(df):
    return create_correlation_heatmap(df)


@st.cache_data
def cached_scatter_plot(df, x_col, y_col, color_col=None):
    return create_scatter_plot(df, x_col, y_col, color_col)


@st.cache_data
def cached_filterable_columns(df):
    return get_filterable_columns(df)


@st.cache_data
def cached_convert_csv(df):
    return convert_df_to_csv(df)


# Page configuration — must be the first Streamlit command
st.set_page_config(
    page_title="CSV Analyzer Dashboard",
    page_icon="📊",
    layout="wide"
)

# Main heading
st.title("CSV Analyzer Dashboard")

# Subtitle
st.subheader("Upload any CSV file and get instant insights")

# Description
st.write("This tool helps you explore, analyze, and visualize your data — no coding required.")

# --- CSV Upload ---
uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])

# Only process when a file is actually uploaded (None on first page load)
if uploaded_file is not None:
    # Try UTF-8 first, fall back to Latin-1 for files with special characters
    try:
        dataframe = pd.read_csv(uploaded_file, encoding="utf-8")
    except UnicodeDecodeError:
        uploaded_file.seek(0)  # Reset file pointer before re-reading
        dataframe = pd.read_csv(uploaded_file, encoding="latin-1")

    rows, columns = dataframe.shape
    st.success(f"Loaded **{rows}** rows and **{columns}** columns.")

    # --- Data Filters (Step 6) ---
    st.sidebar.header("Data Filters")

    # Find which columns are eligible for filtering
    filterable = cached_filterable_columns(dataframe)
    all_filterable = filterable["numeric"] + filterable["categorical"]

    # Let the user pick which columns to filter on
    selected_filter_columns = st.sidebar.multiselect(
        "Choose columns to filter",
        options=all_filterable,
        default=[],
    )

    # Build filter widgets for each selected column
    numeric_filters = {}
    categorical_filters = {}

    for col in selected_filter_columns:
        if col in filterable["numeric"]:
            min_val = float(dataframe[col].min())
            max_val = float(dataframe[col].max())
            # Skip slider if column has only one unique value (slider would error)
            if min_val < max_val:
                selected_range = st.sidebar.slider(
                    f"{col} range",
                    min_value=min_val,
                    max_value=max_val,
                    value=(min_val, max_val),
                    key=f"filter_{col}",
                )
                numeric_filters[col] = selected_range
        elif col in filterable["categorical"]:
            unique_values = dataframe[col].dropna().unique().tolist()
            selected_values = st.sidebar.multiselect(
                f"{col} values",
                options=unique_values,
                default=[],
                key=f"filter_{col}",
            )
            categorical_filters[col] = selected_values

    # Apply all active filters to get the filtered view
    filtered_dataframe = apply_filters(dataframe, numeric_filters, categorical_filters)

    # --- Data Preview with sorting and export (Step 6) ---
    st.subheader("Data Preview")
    st.write(f"Showing **{len(filtered_dataframe):,}** of **{rows:,}** rows")

    # Sorting controls
    sort_col1, sort_col2 = st.columns([3, 1])
    with sort_col1:
        sort_column = st.selectbox(
            "Sort by",
            options=["None"] + dataframe.columns.tolist(),
            index=0,
        )
    with sort_col2:
        sort_direction = st.radio(
            "Direction",
            options=["Ascending", "Descending"],
            horizontal=True,
        )

    # Apply sorting
    sort_by = None if sort_column == "None" else sort_column
    ascending = sort_direction == "Ascending"
    display_dataframe = sort_dataframe(filtered_dataframe, sort_by, ascending)

    # Show the filtered and sorted table
    if len(display_dataframe) == 0:
        st.warning("No rows match the current filters.")
    st.dataframe(display_dataframe, use_container_width=True)

    # Download button for filtered data
    csv_bytes = cached_convert_csv(display_dataframe)
    st.download_button(
        label="Download filtered data as CSV",
        data=csv_bytes,
        file_name="filtered_data.csv",
        mime="text/csv",
    )

    # Collapsible section for a quick peek at the first 5 rows
    with st.expander("Show raw data (first 5 rows)"):
        st.table(dataframe.head())

    # --- Summary Statistics (Step 3) ---

    # -- Metric cards --
    st.subheader("Summary Statistics")
    try:
        total_missing = dataframe.isnull().sum().sum()
        total_cells = rows * columns
        # Guard against division by zero when the DataFrame has no cells
        missing_percent = (total_missing / total_cells * 100) if total_cells > 0 else 0
        duplicate_rows = dataframe.duplicated().sum()

        # Four side-by-side cards for the key numbers
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Rows", f"{rows:,}")
        col2.metric("Columns", f"{columns:,}")
        col3.metric("Missing Cells", f"{total_missing:,} ({missing_percent:.1f}%)")
        col4.metric("Duplicate Rows", f"{duplicate_rows:,}")
    except Exception as error:
        st.error(f"Could not calculate summary metrics: {error}")

    # -- Column Details --
    st.subheader("Column Details")
    try:
        column_info = cached_column_info(dataframe)
        st.dataframe(column_info, use_container_width=True)
    except Exception as error:
        st.error(f"Could not generate column details: {error}")

    # -- Numeric Column Statistics --
    st.subheader("Numeric Column Statistics")
    try:
        numeric_stats = cached_numeric_stats(dataframe)
        if numeric_stats is not None:
            st.dataframe(numeric_stats, use_container_width=True)
        else:
            st.info("No numeric columns found in this dataset.")
    except Exception as error:
        st.error(f"Could not calculate numeric statistics: {error}")

    # -- Categorical Column Statistics --
    st.subheader("Categorical Column Statistics")
    try:
        categorical_stats = cached_categorical_stats(dataframe)
        if categorical_stats is not None:
            st.dataframe(categorical_stats, use_container_width=True)
        else:
            st.info("No categorical columns found in this dataset.")
    except Exception as error:
        st.error(f"Could not calculate categorical statistics: {error}")

    # --- Automated Visualizations (Step 4) ---
    st.subheader("Automated Visualizations")

    # -- Histograms for numeric columns --
    numeric_columns = dataframe.select_dtypes(include="number").columns.tolist()

    if numeric_columns:
        st.markdown("#### Distributions")
        # Display histograms two per row for a clean grid layout
        for i in range(0, len(numeric_columns), 2):
            chart_cols = st.columns(2)
            for j, chart_col in enumerate(chart_cols):
                if i + j < len(numeric_columns):
                    column_name = numeric_columns[i + j]
                    try:
                        fig = cached_histogram(dataframe, column_name)
                        chart_col.plotly_chart(fig, use_container_width=True)
                    except Exception as error:
                        chart_col.error(f"Could not create histogram for {column_name}: {error}")

    # -- Bar charts for categorical columns --
    categorical_columns = dataframe.select_dtypes(exclude="number").columns.tolist()

    if categorical_columns:
        st.markdown("#### Value Counts")
        for i in range(0, len(categorical_columns), 2):
            chart_cols = st.columns(2)
            for j, chart_col in enumerate(chart_cols):
                if i + j < len(categorical_columns):
                    column_name = categorical_columns[i + j]
                    try:
                        fig = cached_bar_chart(dataframe, column_name)
                        if fig is not None:
                            chart_col.plotly_chart(fig, use_container_width=True)
                    except Exception as error:
                        chart_col.error(f"Could not create bar chart for {column_name}: {error}")

    # -- Correlation heatmap --
    try:
        heatmap_fig = cached_correlation_heatmap(dataframe)
        if heatmap_fig is not None:
            st.markdown("#### Correlation Matrix")
            st.plotly_chart(heatmap_fig, use_container_width=True)
    except Exception as error:
        st.error(f"Could not create correlation heatmap: {error}")

    # --- Interactive Scatter Plot (Step 5) ---

    # Only show if there are at least 2 numeric columns to compare
    if len(numeric_columns) >= 2:
        st.subheader("Interactive Scatter Plot")

        # Sidebar controls — grouped under a header for clarity
        st.sidebar.header("Scatter Plot Controls")

        x_axis = st.sidebar.selectbox(
            "X-axis",
            options=numeric_columns,
            index=0,
        )
        y_axis = st.sidebar.selectbox(
            "Y-axis",
            options=numeric_columns,
            index=1,
        )

        # Color-by is optional and can use any column (numeric or categorical)
        all_columns = dataframe.columns.tolist()
        color_option = st.sidebar.selectbox(
            "Color by",
            options=["None"] + all_columns,
            index=0,
        )
        # Convert the string "None" to Python None for the function call
        color_column = None if color_option == "None" else color_option

        try:
            scatter_fig = cached_scatter_plot(dataframe, x_axis, y_axis, color_column)
            if scatter_fig is not None:
                st.plotly_chart(scatter_fig, use_container_width=True)
            else:
                st.warning("Could not create scatter plot with the selected columns.")
        except Exception as error:
            st.error(f"Could not create scatter plot: {error}")
