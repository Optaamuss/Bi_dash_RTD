# Client Delivery Guide

## Recommended MVP Package

Deliver a ZIP created by:

```bash
python -m scripts.package_mvp
```

This includes:

- Streamlit dashboard
- ETL and transformation code
- SQLite warehouse snapshot
- Right to Dream logo asset
- Documentation
- Python requirements
- Client run instructions

## Data-Sharing Decision

There are two delivery modes.

### Snapshot Package

Use:

```bash
python -m scripts.package_mvp
```

This includes the built SQLite warehouse but not the raw Excel workbooks. It is best when the client only needs to review the dashboard MVP.

### Rebuildable Package

Use:

```bash
python -m scripts.package_mvp --include-sources
```

This includes the Excel source workbooks in `data/sources/`, so the client can reload and rebuild the warehouse. Use this only when you have permission to share the underlying player data.

## What The Client Needs

- Python 3.11
- Terminal access
- Internet access for the first `pip install`

## Client Run Command

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m etl.load_raw
python -m etl.run_models
streamlit run dashboard/app.py
```

## Better Hosted MVP Option

For a smoother client experience, host the dashboard on a small internal server or Streamlit-compatible hosting. The local ZIP is useful for handoff, review, and reproducibility, but non-technical clients usually prefer a URL.
