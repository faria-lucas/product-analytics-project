## Product Analytics Pipeline (DuckDB + Python)

This project implements a lightweight end-to-end product analytics pipeline, from raw event ingestion to user-level insights.

### What this project does
- Ingests raw product events using Python
- Normalizes and stores data in Parquet
- Builds analytical models in SQL (DuckDB):
  - events (canonical event table)
  - sessions (30-minute inactivity window)
  - users (first seen, signup, activation, last activity)
- Enables product metrics such as activation, retention and engagement

### Key insights from the data
- Anonymous users tend to have very short sessions and do not convert
- Users who sign up activate quickly (≈7 minutes)
- Activated users return the next day, indicating early retention
- The product delivers value post-signup, while pre-signup experience may have friction

### Tech stack
- Python (ingestion & orchestration)
- DuckDB (analytical engine)
- SQL (analytics modeling)
- Streamlit (data exploration)

### How to run
```bash
uv run python -m ingest_pipeline/ingest_events.py
uv run python -m src/run_pipeline.py
streamlit dashboard/run app.py
```
