from database import Database
from ui import MainWindow

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
        
        self.thoughts_list.configure(state = "normal")
        
        self.thoughts_list.delete("1.0", "end")
        
        thoughts = self.db.get_thoughts()
        
        for _, text, date in thoughts:
            self.thoughts_list.insert("end", f"{date}\n{text}\n\n")
            
        self.thoughts_list.configure(state = "disabled")