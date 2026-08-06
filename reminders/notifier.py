import sqlite3
from datetime import datetime, timezone
from tkinter import messagebox

from utils.paths import DATABASE_PATH


def get_due_reminders():
    connection = sqlite3.connect(DATABASE_PATH)
    cursor = connection.cursor()
    
    now = datetime.now(timezone.utc).isoformat()
    
    cursor.execute("""
        SELECT 
            reminders.id,
            reminders.thought_id,
            reminders.reminder_time_utc, 
            thoughts.text 
        FROM reminders 
        
        JOIN thoughts on thoughts.id = reminders.thought_id 
        
        WHERE reminders.triggered = 0 AND reminders.reminder_time_utc <= ?
        
        """, (now,))
    
    reminders = cursor.fetchall()
    
    connection.close()
    
    return reminders

def mark_triggered(reminder_id):
    connection = sqlite3.connect(DATABASE_PATH)
    
    cursor = connection.cursor()
    
    cursor.execute("""
        UPDATE reminders 
        SET triggered = 1 
        WHERE id = ?
        """, (reminder_id,))
    
    connection.commit()
    
    connection.close()
    
def show_notification(text):
    preview = text.strip()
    
    if len(preview) > 150:
        preview = preview[:150] + "..."

    messagebox.showinfo(
        "ThoughtInbox Reminder",
        preview
    )

def main():
    reminders = get_due_reminders()
    
    if not reminders:
        return
    
    for reminder in reminders:
        reminder_id = reminder[0]
        text = reminder[3]
        
        show_notification(text)
        
        mark_triggered(reminder_id)

    
if __name__ == "__main__":
    main()