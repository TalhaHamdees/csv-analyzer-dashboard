# CSV Analyzer Dashboard

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.54-FF4B4B?logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

A Streamlit web app that lets you upload any CSV file and instantly get insights, visualizations, and summary statistics — no coding required.

<!-- Replace with your deployed app URL after deploying to Streamlit Cloud -->
<!-- [**Try the live demo**](https://your-app-name.streamlit.app) -->

## What It Does

Upload a CSV and the dashboard automatically:

- Detects column types (numeric, categorical, datetime)
- Shows key metrics: row count, missing data, duplicates
- Generates histograms, bar charts, and a correlation heatmap
- Highlights missing data patterns with visual analysis
- Plots time series if date columns are found

You can also filter data, sort columns, build custom scatter plots, and download the results as CSV.

## Features

| Tab | What's inside |
|-----|---------------|
| **Data** | Interactive table with sidebar filters, sorting, CSV export, and column details |
| **Statistics** | Numeric & categorical stats, missing data bar chart and heatmap |
| **Visualizations** | Auto-generated histograms, bar charts, and correlation matrix |
| **Explore** | Custom scatter plot (pick X, Y, color) and time series line chart |

Summary metric cards (rows, columns, missing cells, duplicates) are always visible above the tabs.

## Who This Is For

- **Data analysts** who want a quick look at a new dataset
- **Students** learning about data exploration
- **Non-technical users** who need insights from CSV files without writing code
- **Anyone** who wants a fast, visual summary of tabular data

## Quick Start

### Try it with sample data

A sample CSV is included at `data/sample.csv` with 30 rows of employee data (names, cities, departments, salaries, sales, ratings, and dates) — including some intentional missing values to demonstrate the missing data analysis features.

### Run locally

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

The app opens at `http://localhost:8501`.

### Deploy to Streamlit Cloud

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with GitHub
4. Click **"New app"** and select this repository
5. Set the main file path to `app.py`
6. Click **"Deploy"**

## Tech Stack

- **Python 3.10+**
- **Streamlit** — web app framework
- **Pandas** — data manipulation
- **Plotly** — interactive charts
- **NumPy** — numerical computing

## Project Structure

```
csv-analyzer-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── README.md
├── LICENSE                # MIT License
├── CLAUDE.md              # Development guide
├── .streamlit/
│   └── config.toml        # Theme and server settings
├── data/
│   └── sample.csv         # Sample dataset for testing
└── utils/
    ├── data_profiler.py   # Column type detection, stats, datetime detection
    ├── visualizations.py  # Chart generation (histograms, bar, heatmap, scatter, line)
    └── filters.py         # Dynamic filtering, sorting, CSV export logic
```

## License

This project is licensed under the [MIT License](LICENSE).
