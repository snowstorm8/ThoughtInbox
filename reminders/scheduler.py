import subprocess
import sys
from pathlib import Path

TASK_NAME = "ThoughtInbox Reminder"

BASE_DIR = Path(__file__).resolve().parent.parent
NOTIFIER_PATH = BASE_DIR / "reminders" / "notifier.py"

def register_task():
    pythonw_path = Path(sys.executable).with_name("pythonw.exe")
    
    command = [
        "schtasks",
        "/Create",
        "/TN",
        TASK_NAME,
        "/TR",
        f'"{pythonw_path}" "{NOTIFIER_PATH}"',
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
    
    
if __name__ == "__main__":
    remove_task()