import customtkinter as ctk

class StatusBar(ctk.CTkFrame):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.container = ctk.CTkFrame(self, fg_color = "transparent")
        self.container.pack(fill = "x", padx = 10, pady = 5)
        
        self.label = ctk.CTkLabel(self.container, text = "Ready")
        
        self.label.pack(side = "left")
        
        self.undo_button = ctk.CTkButton(self.container, text = "Undo", width = 70)
        self.undo_button.pack(side = "right")
        self.undo_button.pack_forget()
        
        self.pack(fill = "x", side = "bottom")
        
    def set_status(self, text):
        self.label.configure(text = text)
        
    def flash(self, text, duration = 2000):
        self.set_status(text)
        
        self.after(duration, lambda: self.set_status("Ready"))
        
    def show_undo(self, command):
        self.undo_button.configure(command = command)
        self.undo_button.pack(side = "right")
        
    def hide_undo(self):
        self.undo_button.pack_forget()
        
        