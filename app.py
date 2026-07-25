from database import Database
from ui import MainWindow, ThoughtCard
from tkinter import messagebox
import customtkinter as ctk

class ThoughtInbox(MainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        
        self.input_panel.save_button.configure(command = self.save_thought)
        
        self.editing_id = None
        
        self.configure_menu(
            new = self.new_thought,
            save = self.save_thought,
            export = self.export_thoughts,
            exit = self.destroy,
            find = self.focus_search,
            clear_search = self.clear_search,
            preferences = self.open_preferences,
            light = self.light_theme,
            dark = self.dark_theme,
            system = self.system_theme,
            refresh = self.refresh,
            shortcuts = self.show_shortcuts,
            about = self.show_about
        )
        
        self.input_panel.search_entry.bind("<KeyRelease>", self.on_search)
        
        # ------- Keyboard Shortcuts ------- #
        self.bind("<Control-n>", lambda e: self.new_thought())
        self.bind("<Control-f>", lambda e: self.focus_search())
        self.bind("<Control-s>", lambda e: self.save_thought())
        self.bind("<Escape>", lambda e: self.cancel_edit())
        

        self.refresh()
        
    def new_thought(self):
        self.editing_id = None
        
        self.input_panel.textbox.delete("1.0", "end")
        self.input_panel.save_button.configure(text = "Save Thought")
        
        self.input_panel.textbox.focus()
        
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
        
    def export_thoughts(self):
        print("Coming soon")
        
    def focus_search(self):
        self.input_panel.search_entry.focus()
    
    def clear_search(self):
        self.input_panel.search_entry.delete(0, "end")
        self.refresh()
        
    def open_preferences(self):
        print("Coming soon")
        
    def light_theme(self):
        ctk.set_appearance_mode("Light")
        
    def dark_theme(self):
        ctk.set_appearance_mode("Dark")
        
    def system_theme(self):
        ctk.set_appearance_mode("System")
        
    def show_shortcuts(self):
        messagebox.showinfo("Keyboard Shortcuts", ("New Thought: Ctrl+N\nSave: Ctrl+S\nFind: Ctrl+F\n\nExit Edit Mode: Esc"))
        
    def show_about(self):
        messagebox.showinfo("About ThoughtInbox", ("ThoughtInbox\n\n Version 0.1\n\n Built with Python \n ~Nihar Sreeram"))
        
    def cancel_edit(self):
        self.editing_id = None
        
        self.input_panel.textbox.delete("1.0", "end")
        
        self.input_panel.save_button.configure(text = "Save Thought")
        
        self.refresh()
        
    def refresh(self):
            
        thoughts = self.get_current_thoughts()
            
        self.display_thoughts(thoughts)
    
    def display_thoughts(self, thoughts):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()
            
        for text_id, text, date, in thoughts:
            card = ThoughtCard(self.scroll_frame, text_id,text, date, self.delete_thought, self.edit_thought)
            card.pack(fill = "x", padx = 6, pady = 6) 
            
    def get_current_thoughts(self):
        query = self.input_panel.search_entry.get().strip()    
        
        if query:
            return self.db.search(query)
        
        return self.db.get_thoughts()
        
            
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
        
    def configure_menu(self, **commands):
        self.file_menu.entryconfigure(
            "New Thought",
            command=commands["new"]
        )

        self.file_menu.entryconfigure(
            "Save Thought",
            command=commands["save"]
        )

        self.file_menu.entryconfigure(
            "Export...",
            command=commands["export"]
        )

        self.file_menu.entryconfigure(
            "Exit",
            command=commands["exit"]
        )

        self.edit_menu.entryconfigure(
            "Find",
            command=commands["find"]
        )

        self.edit_menu.entryconfigure(
            "Clear Search",
            command=commands["clear_search"]
        )

        self.edit_menu.entryconfigure(
            "Preferences...",
            command=commands["preferences"]
        )

        self.view_menu.entryconfigure(
            "Light Mode",
            command=commands["light"]
        )

        self.view_menu.entryconfigure(
            "Dark Mode",
            command=commands["dark"]
        )

        self.view_menu.entryconfigure(
            "System Mode",
            command=commands["system"]
        )

        self.view_menu.entryconfigure(
            "Refresh",
            command=commands["refresh"]
        )

        self.help_menu.entryconfigure(
            "Keyboard Shortcuts",
            command=commands["shortcuts"]
        )

        self.help_menu.entryconfigure(
            "About ThoughtInbox",
            command=commands["about"]
        )