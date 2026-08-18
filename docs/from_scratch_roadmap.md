# From-Scratch BI Roadmap

This project now uses your RTD Excel workbooks as the first real data sources. The first goal is to prove the full BI flow locally, then improve data quality and dashboard usefulness step by step.

## Phase 1: Learn The Shape

Build a working local system:

1. Load the RTD Excel workbooks into a warehouse.
2. Transform raw tables into clean reporting tables.
3. Build a dashboard from trusted mart tables.
4. Learn what each layer owns.
5. Identify missing fields, duplicates, and business definitions.

## Phase 2: Define The First Dashboard Questions

Choose the first questions the dashboard should answer:

- Where are players from?
- Which regions, pathways, and squads have the most players?
- Which players have market value data?
- How have squads changed over time?
- Which Black Queens players are linked to clubs and regions?

Start narrow. A BI system becomes useful when one workflow is trustworthy, not when every possible data source is connected.

## Phase 3: Improve The Source Layer

Useful next sources:

- Updated Excel or CSV exports from tools you already use
- Google Sheets
- Academy databases
- Scouting systems
- Player management systems
- Public datasets

Keep the same pattern:

```text
source -> raw table -> SQL model -> mart table -> dashboard
```

## Phase 4: Add Trust

Add checks before relying on dashboards:

- Are player names unique enough to join between files?
- Are required fields present?
- Do row counts match the source workbooks?
- Are important joins causing duplicates?
- Are dates, regions, and coordinates consistent?

## Phase 5: Automate

Only automate after the manual version is correct:

- Schedule ingestion.
- Add alerts for failed loads.
- Store historical snapshots.
- Add access control if others will use it.
