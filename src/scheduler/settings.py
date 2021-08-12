import os
from pathlib import Path

_CSV_REPOSITORY_FOLDER = os.environ.get("CSV_REPOSITORY_FOLDER", None)
CSV_REPOSITORY_FOLDER = (
    Path(_CSV_REPOSITORY_FOLDER) if _CSV_REPOSITORY_FOLDER else Path(__file__).resolve().parent.parent.parent / "data"
)
