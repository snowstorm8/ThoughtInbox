import sys
import sqlite3
from pathlib import Path
from tkinter import messagebox
import tkinter as tk

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE_PATH = BASE_DIR / "thoughts.db"

def get_due_reminders():
    connection = sqlite3.connect(DATABASE_PATH)
    
    cursor = connection.cursor()
    
    cursor.execute("""
        SELECT 
            reminders.id, 
            thoughts.text 
            
        FROM reminders 
        JOIN thoughts on thoughts.id = reminders.thought_id 
        
        WHERE reminders.triggerred = 0 AND reminders.reminder_time <= datetime('now')
        
        """)
    
    reminders = cursor.fetchall()
    
    connection.close()
    
    return reminders

def mark_triggered(reminder_id):
    connection = sqlite3.connect(DATABASE_PATH)
    
    cursor = connection.cursor()
    
    cursor.execute("""
        UPDATE reminders 
        SET triggerred = 1 
        WHERE id = ?
        """, (reminder_id,))
    
    connection.commit()
    
    connection.close()
    
def main():
    reminders = get_due_reminders()
    
    if not reminders:
        return
    
    root = tk.Tk()
    root.withdraw()
    
    for reminder_id, text in reminders:
        preview = text.strip()
        
        if len(preview) > 150:
            preview = preview[:150] + "..."
            
        messagebox.showinfo("ThoughtInbox Reminder", f"Reminder: {preview}")
        
        mark_triggered(reminder_id)
        
    root.destroy()
    
    
if __name__ == "__main__":
    main()