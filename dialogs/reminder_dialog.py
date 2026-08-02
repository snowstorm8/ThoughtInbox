import customtkinter as ctk
from datetime import datetime, date, time
from tkinter import messagebox
from dialogs.base_dialog import BaseDialog


class ReminderDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Reminders", 400, 250)
        
        self.result = None
        
        ctk.CTkLabel(self, text = "Reminder date and time").pack(pady = (25, 10))
        ctk.CtkLabel(self, text = "Format: YYYY-MM-DD HH:MM").pack(pady = (0, 8))
        
        self.entry = ctk.CTkEntry(self, width = 280, placeholder_text = datetime.combine(date.today(), time(18, 0)).strftime("%Y-%m-%d %H:%M"))
        self.entry.pack(pady = (0, 20))
        
        button_frame = ctk.CTkFrame(self, fg_color = "transparent")
        button_frame.pack()
        
        ctk.CTkButton(button_frame, text = "Cancel", command = self.cancel).pack(side = "left", padx = 8)
        ctk.CTkButton(button_frame, text = "Set Reminder", command = self.save).pack(side = "left", padx = 8)
        
    def save(self):
        value = self.entry.get().strip()
        
        try:
            datetime.strptime(value, "%Y-%m-%d %H:%M")
            
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid date and time in the format YYYY-MM-DD HH:MM.")
            return
        
        self.result = value
        self.destroy()
        
    def cancel(self):
        self.result = None
        self.destroy()        
