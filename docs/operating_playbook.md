# Operating Playbook

## Daily Local Run

```bash
python -m etl.load_raw
python -m etl.run_models
streamlit run dashboard/app.py
```

## Add A New Source

1. Put the source workbook somewhere stable.
2. Add it to `SOURCE_WORKBOOKS` in `etl/config.py`.
3. Run the loader.
4. Extend the transformation logic in `etl/run_models.py`.
5. Add charts or filters to `dashboard/app.py`.

## Data Quality Checks To Add

- Primary keys are unique.
- Player names are consistently spelled across workbooks.
- Required player fields are not null.
- Latitude and longitude are present for heatmap records.
- Dates are valid and not unexpectedly in the future.
- Joins do not create duplicate player records.

## Dashboard Design Rules

- Use mart tables only.
- Keep core metrics visible at the top.
- Add filters that match how the business thinks.
- Prefer trend, comparison, and contribution views.
- Keep drill-down tables available for auditability.
