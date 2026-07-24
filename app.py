from database import Database
from ui import MainWindow, ThoughtCard

class ThoughtInbox(MainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        
        self.save_button.configure(command = self.save_thought)
        
        self.refresh()
        
    def save_thought(self):
        
        text = self.textbox.get("1.0", "end").strip()
        
        if text == "": 
            return
        
        self.db.add_thought(text)
        
        self.textbox.delete("1.0", "end")
        
        self.refresh()
        
    def refresh(self):
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        thoughts = self.db.get_thoughts()
        
        for _, text, date, in thoughts:
            card = ThoughtCard(self.scroll_frame, text, date)
            card.pack(fill = "x", padx = 6, pady = 6)