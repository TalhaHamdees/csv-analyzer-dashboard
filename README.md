# CSV Analyzer Dashboard

A Streamlit web app that lets you upload any CSV file and instantly get insights, visualizations, and summary statistics — no coding required.

## Features

- **CSV Upload** — drag and drop any CSV file, with automatic encoding detection
- **Data Preview** — interactive table with filtering, sorting, and CSV export
- **Summary Statistics** — row/column counts, missing data, duplicates, per-column profiling
- **Automated Visualizations** — histograms, bar charts, and correlation heatmaps generated automatically
- **Interactive Scatter Plot** — choose X, Y, and color columns to explore relationships
- **Missing Data Analysis** — visual bar chart and heatmap showing where gaps are
- **Time Series** — auto-detects date columns and plots trends over time
- **Tabbed Layout** — organized into Data, Statistics, Visualizations, and Explore tabs

## Tech Stack

- **Python 3.10+**
- **Streamlit** — web app framework
- **Pandas** — data manipulation
- **Plotly** — interactive charts
- **NumPy** — numerical computing

## Run Locally

```bash
# Clone the repo
git clone https://github.com/TalhaHamdees/csv-analyzer-dashboard.git
cd csv-analyzer-dashboard

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click "New app" and select this repository
5. Set the main file path to `app.py`
6. Click "Deploy"

## Project Structure

```
csv-analyzer-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md
├── CLAUDE.md              # Development instructions
├── .gitignore
├── .streamlit/
│   └── config.toml        # Theme and server settings
└── utils/
    ├── data_profiler.py   # Column type detection, stats
    ├── visualizations.py  # Chart generation functions
    └── filters.py         # Dynamic filtering logic
```
