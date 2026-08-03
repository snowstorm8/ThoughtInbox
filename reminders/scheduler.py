import subprocess

TASK_NAME = "ThoughtInbox Reminder"

def register_task():
    command = [
        "schtasks",
        "/Create",
        "/TN",
        TASK_NAME,
        "/TR",
        "python reminders/notifier.py",
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