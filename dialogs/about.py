import customtkinter as ctk

class AboutDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("About")
        self.geometry("350x260")
        self.resizable(False, False)
        
        self.grab_set()
        
        ctk.CTkLabel(self, text = "ThoughtInbox", font = ("Arial", 20)).pack(pady = (20, 5))
        ctk.CTkLabel(self, text = "Version 0.1").pack()
        ctk.CTkLabel(self, text = "Capture ideas before they disappear...", wraplength = 250, justify = "center").pack(pady = 15)
        
        ctk.CTkButton(self, text = "Close", command = self.destroy).pack()
    