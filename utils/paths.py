from pathlib import Path
import os


APP_NAME = "ThoughtInbox"


def get_data_dir():
    appdata = os.getenv("APPDATA")

    if appdata:
        data_dir = Path(appdata) / APP_NAME
    else:
        # Fallback for unusual environments
        data_dir = Path.home() / f".{APP_NAME}"

    data_dir.mkdir(parents=True, exist_ok=True)

    return data_dir


DATA_DIR = get_data_dir()

DATABASE_PATH = DATA_DIR / "thoughts.db"
SETTINGS_PATH = DATA_DIR / "settings.json"
DRAFT_PATH = DATA_DIR / "drafts.txt"