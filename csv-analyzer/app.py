import streamlit as st
import pandas as pd
from utils.data_profiler import get_column_info, get_numeric_stats, get_categorical_stats


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

    # Interactive table — users can sort and scroll
    st.subheader("Data Preview")
    st.dataframe(dataframe)

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
