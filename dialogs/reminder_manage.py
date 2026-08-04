import customtkinter as ctk
from datetime import datetime, timezone
from tkinter import messagebox
from dialogs.base_dialog import BaseDialog


class ReminderManageDialog(BaseDialog):
    def __init__(self, parent, reminder_time_utc):
        super().__init__(parent, "Reminder", 420, 270)

        self.result = None

        utc_time = datetime.fromisoformat(reminder_time_utc)
        local_time = utc_time.astimezone()
        display_time = local_time.strftime("%Y-%m-%d %H:%M")

        ctk.CTkLabel(self, text="Reminder", font=("Segoe UI", 17, "bold")).pack(pady=(25, 8))
        ctk.CTkLabel(self, text="Date and time", font=("Segoe UI", 12)).pack(pady=(0, 5))

        self.entry = ctk.CTkEntry(self, width=280)
        self.entry.insert(0, display_time)
        self.entry.pack(pady=(0, 20))

        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.pack()

        ctk.CTkButton(button_frame, text="Delete", width=90, fg_color="#C0392B", hover_color="#922B21", command=self.delete).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Cancel", width=90, command=self.cancel).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Save", width=90, command=self.save).pack(side="left", padx=5)

    def save(self):
        value = self.entry.get().strip()

        try:
            local_time = datetime.strptime(value, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Date", "Please use YYYY-MM-DD HH:MM.")
            return

        local_time = local_time.astimezone()
        utc_time = local_time.astimezone(timezone.utc)
        self.result = ("update", utc_time.isoformat())
        self.destroy()

    def delete(self):
        self.result = ("delete",)
        self.destroy()

    def cancel(self):
        self.result = None
        self.destroy()