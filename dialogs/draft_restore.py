import customtkinter as ctk
from dialogs.base_dialog import BaseDialog


class RestoreDialog(BaseDialog):

    def __init__(self, parent, title, message):

        super().__init__(parent, title, 420, 200)

        self.result = False

        ctk.CTkLabel(self, text = message, font = ("Segoe UI", 15), justify = "center", wraplength = 360).pack(pady = (25, 20), padx = 20)

        button_frame = ctk.CTkFrame(self, fg_color = "transparent")
        button_frame.pack(pady = 5)

        ctk.CTkButton(button_frame, text = "Restore Draft", width = 120, command = self.restore).pack(side = "left", padx = 10)
        ctk.CTkButton(button_frame, text = "Discard", width = 120, fg_color = "#C0392B", hover_color = "#922B21", command = self.discard).pack(side = "left", padx = 10)
        
        self.force_center()

    def discard(self):
        self.result = False
        self.destroy()

    def restore(self):
        self.result = True
        self.destroy()