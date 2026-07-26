import customtkinter as ctk
from dialogs.base_dialog import BaseDialog


class AboutDialog(BaseDialog):

    def __init__(self, parent):
        super().__init__(parent, "About ThoughtInbox", 350, 260)
        
        ctk.CTkLabel(self, text = "ThoughtInbox", font = ("Arial", 20)).pack(pady = (20, 5))
        ctk.CTkLabel(self, text = "Version 0.1").pack()
        ctk.CTkLabel(self, text = "Capture ideas before they disappear...", wraplength = 250, justify = "center").pack(pady = 15)
        
        ctk.CTkButton(self, text = "Close", command = self.destroy).pack()
    