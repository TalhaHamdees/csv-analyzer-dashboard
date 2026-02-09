# CLAUDE.md — CSV Analyzer Dashboard

## Project Overview

A Streamlit web app that lets users upload any CSV file and auto-generates insights, visualizations, and summary statistics. Built for portfolio and Fiverr gig potential.

**Tech stack:** Python 3.10+ · Streamlit · Pandas · Plotly · NumPy

## Development Approach

This project is being built **step-by-step for learning purposes**. The developer is a beginner learning Python data tools alongside building.

**IMPORTANT:**
- Only implement what is explicitly asked for in the current step. Do NOT build ahead or add features from future steps.
- After writing code, **explain what the code does** in simple terms — line by line for new concepts, block-level for familiar ones.
- When introducing a new library or function for the first time, explain **what it is, why we use it, and how it works**.
- If there are multiple ways to do something, briefly mention the alternative and why we chose this approach.
- Flag any "gotchas" or common beginner mistakes related to the code being written.

## Project Structure

```
csv-analyzer/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies with versions
├── .gitignore
├── README.md
├── CLAUDE.md              # This file
└── utils/                 # Helper modules (added in later steps)
    ├── data_profiler.py   # Column type detection, stats
    ├── visualizations.py  # Chart generation functions
    └── filters.py         # Dynamic filtering logic
```

## Commands

- `streamlit run app.py` — Run the app locally
- `pip install -r requirements.txt` — Install dependencies
- `pip freeze > requirements.txt` — Update dependency list

## Development Steps

The project follows 10 sequential steps. Reference `project-plan.md` for the full breakdown if needed.

1. Project setup & hello world
2. CSV upload & data preview
3. Summary statistics & data profiling
4. Automated visualizations
5. Interactive scatter plot & user controls
6. Filtering, sorting & data export
7. Missing data analysis & time series
8. Polish, layout & UX
9. Deploy to Streamlit Cloud
10. Document & portfolio-ify

## Code Style

- Use clear, descriptive variable names (prefer `filtered_dataframe` over `df2`)
- Add inline comments explaining "why", not "what"
- Keep functions small and single-purpose
- Use `st.cache_data` for any expensive computation
- Use Plotly Express (`px`) over Plotly Graph Objects unless custom layout is needed
- Handle errors gracefully with `try/except` and show user-friendly messages via `st.error()`

## Streamlit Conventions

- Use `st.set_page_config()` as the first Streamlit call
- Use `st.sidebar` for controls and filters
- Use `st.tabs()` to organize sections (from Step 8 onward)
- Persist data across reruns with `st.session_state` when needed
- Never use `st.experimental_*` deprecated APIs

## Common Pitfalls to Watch For

- `st.file_uploader` returns `None` on first load — always check before processing
- `pd.read_csv()` can fail on encoding — use `encoding='utf-8'` with fallback to `'latin-1'`
- Plotly charts need `st.plotly_chart(fig, use_container_width=True)` to render properly
- Streamlit reruns the entire script on every interaction — keep expensive ops cached
- `df.describe()` only includes numeric columns by default — pass `include='all'` for full stats
