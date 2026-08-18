import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
SOURCE_DATA_DIR = Path(os.environ.get("RTD_SOURCE_DATA_DIR", PROJECT_ROOT / "data" / "sources"))
WAREHOUSE_DIR = PROJECT_ROOT / "warehouse"
WAREHOUSE_PATH = WAREHOUSE_DIR / "bi_system.sqlite"
MODELS_DIR = PROJECT_ROOT / "models"

SOURCE_FILENAMES = {
    "raw_black_queens": "Black_Queens (2).xlsx",
    "raw_ghana_heatmap": "Ghana Heatmap (2).xlsx",
    "raw_ghana_rtd_players": "Ghana_RTD_Players (3).xlsx",
    "raw_squad_movement": "Squad_Movement (2).xlsx",
}

LOCAL_FALLBACK_SOURCE_DIR = Path("/Users/MussaYousef/Downloads/RTD NAMEs")

SOURCE_WORKBOOKS = {
    table_name: (
        SOURCE_DATA_DIR / filename
        if (SOURCE_DATA_DIR / filename).exists()
        else LOCAL_FALLBACK_SOURCE_DIR / filename
    )
    for table_name, filename in SOURCE_FILENAMES.items()
}
