import customtkinter as ctk
from dialogs.base_dialog import BaseDialog


class ConfirmDialog(BaseDialog):

    def __init__(self, parent, title, message):

        super().__init__(parent, title, 420, 190)

        self.result = False

        ctk.CTkLabel(self, text = message, font = ("Segoe UI", 15), justify = "center", wraplength = 360).pack(pady = (25, 20), padx = 20)

        button_frame = ctk.CTkFrame(self, fg_color = "transparent")
        button_frame.pack(pady = (0, 20))

        ctk.CTkButton(button_frame, text = "Cancel", width = 120, command = self.cancel).pack(side = "left", padx = 10)
        ctk.CTkButton(button_frame, text = "Delete", width = 120, fg_color = "#C0392B", hover_color = "#922B21", command = self.confirm).pack(side = "left", padx = 10)

    def cancel(self):
        self.result = False
        self.destroy()

    def confirm(self):
        self.result = True
        self.destroy()