import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.label = ctk.CTkLabel(self, text = "Ready", anchor = "w")
        
        self.label.pack(fill = "x", padx = 10, pady = 5)
        
        self.pack(fill = "x", side = "bottom")
        
    def set_status(self, text):
        self.label.configure(text = text)
        
    def flash(self, text, duration = 2000):
        self.set_status(text)
        
        self.after(duration, lambda: self.set_status("Ready"))
        
        