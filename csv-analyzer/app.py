import streamlit as st
import pandas as pd

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
