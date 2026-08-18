# BI System Architecture

## Layers

### Source Layer

This is where business data originates. Current sources are the four RTD Excel workbooks. Later sources can include:

- Operational databases
- SaaS APIs
- Scouting systems
- Player management systems
- Google Sheets
- Public datasets

### Raw Layer

Raw tables preserve source data as closely as possible. The goal is traceability, not cleanliness.

Naming pattern:

```text
raw_<source_name>
```

### Transformation Layer

The Python transformation layer in `etl/run_models.py` cleans, joins, renames, type-casts, and applies business rules.

Good model habits:

- Use clear table and column names.
- Keep business definitions in one place.
- Avoid dashboard-only calculations when the metric should be reusable.
- Make important assumptions visible in code and documentation.

### Mart Layer

Marts are trusted tables designed for reporting and analysis.

Examples:

- `dim_player`
- `fact_squad_movement`
- `dim_squad`
- `dim_date`
- `dim_geography`
- `mart_source_effectiveness`
- `mart_dashboard_summary`
- `mart_black_queens`

### Visualization Layer

The dashboard should use mart tables, not raw tables. This keeps charts fast and business logic consistent.

## Next Capabilities To Add

- Data quality checks
- Incremental loads
- API connectors
- Authentication
- Scheduled jobs
- Semantic metric definitions
- Row-level security
