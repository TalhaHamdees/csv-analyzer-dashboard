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
csv-analyzer-dashboard/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies (direct only)
├── .gitignore
├── README.md
├── CLAUDE.md              # This file
├── .streamlit/
│   └── config.toml        # Theme and server settings
└── utils/                 # Helper modules
    ├── data_profiler.py   # Column type detection, stats, datetime detection
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
- Plotly charts need `st.plotly_chart(fig, use_container_width=True)` for responsive layout
- `df.describe()` only covers numeric columns by default — use `include='all'` for full profile
- Large CSVs can slow down reruns — wrap parsing in `st.cache_data`

## Progress Tracker

Tracks what has been completed so far. Update after each step.

- [x] Step 1 — Project setup & hello world
- [x] Step 2 — CSV upload & data preview
- [x] Step 3 — Summary statistics & data profiling
- [x] Step 4 — Automated visualizations
- [x] Step 5 — Interactive scatter plot & user controls
- [x] Step 6 — Filtering, sorting & data export
- [x] Step 7 — Missing data analysis & time series
- [x] Step 8 — Polish, layout & UX
- [x] Step 9 — Deploy to Streamlit Cloud
- [ ] Step 10 — Document & portfolio-ify

## Helper Module Guidelines

- Keep utility functions **pure** (no Streamlit imports inside `utils/` files) — this makes them testable independently
- Add `st.cache_data` wrappers in `app.py`, not in the utility modules
- Each utility file should focus on one responsibility (profiling, charts, filters)
- Return `None` from helper functions when there's no data to process (e.g., no numeric columns) — let `app.py` decide how to display the empty state
