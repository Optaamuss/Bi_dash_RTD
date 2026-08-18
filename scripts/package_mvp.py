import argparse
import shutil
import zipfile
from datetime import datetime
from pathlib import Path

from etl.config import LOCAL_FALLBACK_SOURCE_DIR, PROJECT_ROOT, SOURCE_FILENAMES


PACKAGE_ITEMS = [
    "assets",
    "dashboard",
    "docs",
    "etl",
    "warehouse",
    "README.md",
    "requirements.txt",
]


def copy_item(source: Path, destination: Path) -> None:
    if source.is_dir():
        ignore = shutil.ignore_patterns("__pycache__", ".DS_Store", "*.pyc")
        shutil.copytree(source, destination, ignore=ignore)
    elif source.exists():
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)


def build_package(include_sources: bool) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    build_root = PROJECT_ROOT / "dist" / f"right_to_dream_talent_intelligence_mvp_{timestamp}"
    build_root.mkdir(parents=True, exist_ok=True)

    for item in PACKAGE_ITEMS:
        copy_item(PROJECT_ROOT / item, build_root / item)

    if include_sources:
        source_dir = build_root / "data" / "sources"
        source_dir.mkdir(parents=True, exist_ok=True)
        for filename in SOURCE_FILENAMES.values():
            source_file = LOCAL_FALLBACK_SOURCE_DIR / filename
            if source_file.exists():
                shutil.copy2(source_file, source_dir / filename)

    (build_root / "CLIENT_RUN_INSTRUCTIONS.md").write_text(
        """# Right To Dream Talent Intelligence MVP

## Run Locally

1. Install Python 3.11.
2. Open Terminal in this folder.
3. Run:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m etl.load_raw
python -m etl.run_models
streamlit run dashboard/app.py
```

The dashboard opens at the local URL shown by Streamlit, usually:

```text
http://localhost:8501
```

## Data

If the package includes `data/sources`, the ETL will use those Excel files.
If source files are not included, the existing SQLite warehouse still lets the dashboard open with the packaged snapshot.
""",
        encoding="utf-8",
    )

    zip_path = build_root.with_suffix(".zip")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in build_root.rglob("*"):
            archive.write(path, path.relative_to(build_root.parent))

    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description="Package the dashboard MVP for client delivery.")
    parser.add_argument(
        "--include-sources",
        action="store_true",
        help="Include source Excel workbooks in data/sources. Only use when you are allowed to share them.",
    )
    args = parser.parse_args()

    zip_path = build_package(include_sources=args.include_sources)
    print(zip_path)


if __name__ == "__main__":
    main()
