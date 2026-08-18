import sqlite3

import pandas as pd

from etl.config import SOURCE_WORKBOOKS, WAREHOUSE_DIR, WAREHOUSE_PATH


def clean_column_name(column: object) -> str:
    cleaned = str(column).strip().lower()
    for old, new in {
        " ": "_",
        "@": "at",
        "=": "",
        "-": "_",
        "/": "_",
    }.items():
        cleaned = cleaned.replace(old, new)
    return "_".join(part for part in cleaned.split("_") if part)


def main() -> None:
    WAREHOUSE_DIR.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(WAREHOUSE_PATH) as con:
        for table_name, workbook_path in SOURCE_WORKBOOKS.items():
            if not workbook_path.exists():
                raise FileNotFoundError(f"Missing source workbook: {workbook_path}")

            df = pd.read_excel(workbook_path)
            df.columns = [clean_column_name(column) for column in df.columns]
            df["source_file"] = workbook_path.name
            df.to_sql(table_name, con, if_exists="replace", index=False)
            print(f"Loaded {table_name}: {len(df)} rows from {workbook_path.name}")


if __name__ == "__main__":
    main()
