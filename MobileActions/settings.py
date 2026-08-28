from pathlib import Path
import os


MOBILE_ACTION_DIR = Path(os.path.dirname(__file__))

PROJECT_DIR = MOBILE_ACTION_DIR.parent

DATASET_DIR = MOBILE_ACTION_DIR / "Dataset"