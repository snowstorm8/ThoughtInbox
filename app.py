from database import Database
from ui import MainWindow, ThoughtCard
from tkinter import messagebox
import customtkinter as ctk
from widgets.statusbar import StatusBar
from dialogs.confirm import ConfirmDialog
from dialogs.about import AboutDialog
from dialogs.preferences import PreferencesDialog
from settings import Settings
from tkinter import filedialog
from utils.exporter import Exporter
from pathlib import Path
from utils.backups import BackupManager
from shutil import copy2

class ThoughtInbox(MainWindow):
    
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        self.status_bar = StatusBar(self)
        self.settings = Settings()
        
        width = self.settings.get("window_width")
        height = self.settings.get("window_height")
        x = self.settings.get("window_x")
        y = self.settings.get("window_y")
        
        self.geometry(f"{width}x{height}+{x}+{y}")
        
        ctk.set_appearance_mode(self.settings.get("theme"))
        
        self.input_panel.save_button.configure(command = self.save_thought)
        
        self.editing_id = None
        
        self.configure_menu(
            new = self.new_thought,
            save = self.save_thought,
            export = self.export_thoughts,
            restore = self.restore_thoughts,
            exit = self.close_application,
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
        
        self.protocol("WM_DELETE_WINDOW", self.close_application)

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
            
            self.status_bar.flash("✓ Thought Saved")
        
        self.input_panel.textbox.delete("1.0", "end")
        
        self.refresh()
        
    def export_thoughts(self):
        thoughts = self.db.get_thoughts()
        
        if not thoughts:
            self.status_bar.flash("No thoughts to export")
            return
        
        path = filedialog.asksaveasfilename(title = "Export Thoughts", defaultextension = ".md", filetypes = [("Markdown", "*.md"), ("JSON", "*.json"), ("Text", "*.txt")])
        
        if not path:
            return
        
        suffix = Path(path).suffix.lower()
        
        if suffix == ".txt":
            Exporter.export_txt(path, thoughts)
        elif suffix == ".json":
            Exporter.export_json(path, thoughts)
        else:
            Exporter.export_markdown(path, thoughts)
            
        self.status_bar.flash("Thoughts exported successfully.")
        
    def restore_thoughts(self):
        backup = filedialog.askopenfilename(title = "Restore Backup", initialdir = "backups", filetypes = [("Database", "*.db")])
        
        if not backup:
            return
        
        dialog = ConfirmDialog(self, "Restore Backup", "This will replace your current database.\nContinue?")
        
        self.wait_window(dialog)
        
        if not dialog.result:
            return
        
        self.db.close()
        
        copy2(backup, "thoughts.db")
        
        self.db = Database()
        
        self.refresh()
        
        self.status_bar.flash("Backup restored successfully.")

    def focus_search(self):
        self.input_panel.search_entry.focus()
    
    def clear_search(self):
        self.input_panel.search_entry.delete(0, "end")
        self.refresh()
        
    def open_preferences(self):
        PreferencesDialog(self)
        
    def light_theme(self):
        ctk.set_appearance_mode("Light")
        
        self.settings.set("theme", "Light")
        
    def dark_theme(self):
        ctk.set_appearance_mode("Dark")
        
        self.settings.set("theme", "Dark")
        
    def system_theme(self):
        ctk.set_appearance_mode("System")
        
        self.settings.set("theme", "System")
        
    def show_shortcuts(self):
        messagebox.showinfo("Keyboard Shortcuts", ("New Thought: Ctrl+N\nSave: Ctrl+S\nFind: Ctrl+F\n\nExit Edit Mode: Esc"))
        
    def show_about(self):
        if hasattr(self, "_about_dialog"):
            if self._about_dialog.winfo_exists():
                self._about_dialog.focus()
                return

        self._about_dialog = AboutDialog(self)
        
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
            thoughts = self.db.search(query)
            self.status_bar.set_status(f"{len(thoughts)} thoughts")
            return thoughts
        
        self.status_bar.set_status("Ready")
        return self.db.get_thoughts()
        
            
    def delete_thought(self, thought_id):
        dialog = ConfirmDialog(self, "Delete Thought", "Delete this thought permanently?")
        self.wait_window(dialog)
        
        if dialog.result:
            self.db.delete(thought_id)
            self.status_bar.flash("🗑 Thought Deleted")
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
            "Restore Backup...",
            command=commands["restore"]
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
        
    def save_window_geometry(self):
        self.settings.set("window_width", self.winfo_width())
        self.settings.set("window_height", self.winfo_height())
        self.settings.set("window_x", self.winfo_x())
        self.settings.set("window_y", self.winfo_y())
        
    def close_application(self):
        self.save_window_geometry()
        BackupManager.create_backup()
        self.destroy()