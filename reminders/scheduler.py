import subprocess
import sys
from pathlib import Path
from . import notifier

TASK_NAME = "ThoughtInbox Reminder"


def register_task():

    exe_path = Path(sys.executable)

    command = [
        "schtasks",
        "/Create",
        "/TN",
        TASK_NAME,
        "/TR",
        f'"{exe_path}" --reminder',
        "/SC",
        "MINUTE",
        "/MO",
        "1",
        "/F"
    ]

    subprocess.run(
        command,
        check=True
    )


def remove_task():

    command = [
        "schtasks",
        "/Delete",
        "/TN",
        TASK_NAME,
        "/F"
    ]

    subprocess.run(
        command,
        check=True
    )


if __name__ == "__main__":
    remove_task()