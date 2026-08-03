import subprocess
import sys
from pathlib import Path

TASK_NAME = "ThoughtInbox Reminder"

BASE_DIR = Path(__file__).resolve().parent.parent
NOTIFIER_PATH = BASE_DIR / "reminders" / "notifier.py"

def register_task():
    command = [
        "schtasks",
        "/Create",
        "/TN",
        TASK_NAME,
        "/TR",
        f'"{sys.executable} {NOTIFIER_PATH}"',
        "/SC",
        "MINUTE",
        "/MO",
        "1",
        "/F"
    ]
    
    subprocess.run(command, check = True)
    
def remove_task():
    command = [
        "schtasks",
        "/Delete",
        "/TN",
        TASK_NAME,
        "/F"
    ]
    
    subprocess.run(command, check = True)