from database import Database
from ui import MainWindow, ThoughtCard

class ThoughtInbox(MainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        
        self.input_panel.save_button.configure(command = self.save_thought)
        
        self.editing_id = None
        
        self.input_panel.search_entry.bind("<KeyRelease>", self.on_search)
        
        self.refresh()
        
    def save_thought(self):
        
        text = self.input_panel.textbox.get("1.0", "end").strip()
        
        if text == "": 
            return
        
        if self.editing_id is None:
            self.db.add_thought(text)
            
        else:
            self.db.update(self.editing_id, text)
            
            self.editing_id = None
            
            self.input_panel.save_button.configure(text = "Save Thought")
        
        self.input_panel.textbox.delete("1.0", "end")
        
        self.refresh()
        
    def refresh(self):
        
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        query = self.input_panel.search_entry.get().strip()    
        
        if query:
            thoughts = self.db.search(query)
        else:    
            thoughts = self.db.get_thoughts()
        
        for text_id, text, date, in thoughts:
            card = ThoughtCard(self.scroll_frame, text_id,text, date, self.delete_thought, self.edit_thought)
            card.pack(fill = "x", padx = 6, pady = 6)
            
            
    def delete_thought(self, thought_id):
        self.db.delete(thought_id)
        self.refresh()
        
    def edit_thought(self, thought_id, text):
        self.editing_id = thought_id
        
        self.input_panel.textbox.delete("1.0", "end")
        self.input_panel.textbox.insert("1.0", text)
        
        self.input_panel.save_button.configure(text = "Update Thought")
        
    def on_search(self, event):
        self.refresh()