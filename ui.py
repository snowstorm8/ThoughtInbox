import customtkinter as ctk
from tkinter import Menu
import tkinter as tk
from PIL import Image
from datetime import datetime

class MainWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.iconbitmap("assets/inbox.ico")
        
        self.menu = Menu(self)
        self.configure(menu = self.menu)
        
        self.file_menu = Menu(self.menu, tearoff = False)
        
        self.file_menu.add_command(label = "New Thought", accelerator = "Ctrl+N")
        self.file_menu.add_command(label = "Save Thought", accelerator = "Ctrl+S")
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Export...")
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Restore Backup...")
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Exit")
        
        self.menu.add_cascade(label = "File", menu = self.file_menu)
        
        self.edit_menu = Menu(self.menu, tearoff = False)
        
        self.edit_menu.add_command(label = "Find", accelerator = "Ctrl+F")
        self.edit_menu.add_command(label = "Clear Search")
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label = "Preferences...")
        
        self.menu.add_cascade(label = "Edit", menu = self.edit_menu)
        
        self.view_menu = Menu(self.menu, tearoff = False)
        
        self.view_menu.add_command(label = "Light Mode")
        self.view_menu.add_command(label = "Dark Mode")
        self.view_menu.add_command(label = "System Mode")
        self.view_menu.add_separator()
        self.show_favorites = tk.BooleanVar(value = False)
        self.view_menu.add_checkbutton(label = "Show Favorites", variable = self.show_favorites)
        self.view_menu.add_separator()
        self.view_menu.add_command(label = "Refresh")
        
        self.menu.add_cascade(label = "View", menu = self.view_menu)
        
        self.help_menu = Menu(self.menu, tearoff = False)
        
        self.help_menu.add_command(label = "Keyboard Shortcuts")
        self.help_menu.add_separator()
        self.help_menu.add_command(label = "About ThoughtInbox")
        
        self.menu.add_cascade(label = "Help", menu = self.help_menu)
        
        self.title("Thought Inbox")
        self.geometry("700x500")
        
        # ------- Title ------- #
        self.title_label = ctk.CTkLabel(self, text="Thought Inbox", font=("Arial", 24, "bold"))
        self.title_label.pack(pady=(20,10))
        
        # ------- Input Panel ------- #
        self.input_panel = InputPanel(self)
        self.input_panel.pack(fill = "x", padx = 20)
        
        # ------- Recent Thoughts ------- #
        self.thought_label = ctk.CTkLabel(self, text="Recent Thoughts", font=("Arial", 18, "bold"))
        self.thought_label.pack(pady = (10, 5))
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, width = 620, height = 250)
        self.scroll_frame.pack(fill = "both", expand = True, padx = 20, pady = (0, 20))
        
    def set_new_thought_command(self, command):
        self.file_menu.entryconfigure("New Thought", command = command)
        
    def set_exit_command(self, command):
        self.file_menu.entryconfigure("Exit", command = command)
        
class ThoughtCard(ctk.CTkFrame):
    def __init__ (self, parent, thought_id, thought, date, favorite, tags, reminder, delete_callback, edit_callback, favorite_callback, reminder_callback, tag_callback = None):
        super().__init__(parent)
        
        self.thought_id = thought_id
        self.favorite = favorite
        self.tag = tags
        self.reminder = reminder
        self.favorite_callback = favorite_callback
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        self.reminder_callback = reminder_callback
        self.tag_callback = tag_callback
        
        tag_frame = ctk.CTkFrame(self, fg_color = "transparent")
        tag_frame.pack(anchor = "w", padx = 15, pady = (4, 2))
        
        for tag in tags:
            tag_button = ctk.CTkButton(tag_frame, text = f"#{tag}", width = 60, height = 24, fg_color = "transparent", hover_color = ("gray85", "gray25"), text_color = ("gray30", "gray75"), command = lambda t = tag: self.tag_callback(t))
            tag_button.pack(side = "left", padx = 1)
        
        self.edit_icon = ctk.CTkImage(light_image = Image.open("assets/edit_icon.png"), dark_image = Image.open("assets/edit_icon.png"), size = (18, 18))
        self.delete_icon = ctk.CTkImage(light_image = Image.open("assets/delete_icon.png"), dark_image = Image.open("assets/delete_icon.png"), size = (18, 18))
        
        self.thought_label = ctk.CTkLabel(self, text = thought, anchor = "w", justify = "left", wraplength = 500, font = ("Arial", 12))
        self.thought_label.pack(anchor = "w", padx = 15, pady = (10, 4))
        
        self.date_label = ctk.CTkLabel(self, text = date, text_color = "gray")
        self.date_label.pack(anchor = "w", padx = 15, pady = (0, 10))
        
        if self.reminder:
            reminder_time = datetime.fromisoformat(self.reminder[1]).astimezone()
            reminder_text = reminder_time.strftime("%b %d, %Y at %I:%M %p")
            
            ctk.CTkLabel(self, text = reminder_text).pack(anchor = "w", padx = 15, pady = (0, 5))
        
        self.button_frame = ctk.CTkFrame(self, fg_color = "transparent")
        self.button_frame.pack(anchor = "e", padx = 15, pady = (0, 10))
        
        self.favorite_on = ctk.CTkImage(light_image = Image.open("assets/star_filled.png"), dark_image = Image.open("assets/star_filled.png"), size = (18, 18))
        self.favorite_off = ctk.CTkImage(light_image = Image.open("assets/star_empty.png"), dark_image = Image.open("assets/star_empty.png"), size = (18, 18))
        
        self.favorite_button = ctk.CTkButton(self.button_frame, image = self.favorite_on if favorite else self.favorite_off, text = "", width = 35, command = self.toggle_favorite)
        self.favorite_button.pack(side = "left", padx = (0, 5))
        
        self.bell_icon = ctk.CTkImage(light_image = Image.open("assets/bell.png"), dark_image = Image.open("assets/bell.png"), size = (18, 18))
        
        self.reminder_button = ctk.CTkButton(self.button_frame, image = self.bell_icon, text = "", width = 35, command = lambda: self.reminder_callback(self.thought_id))
        self.reminder_button.pack(side = "left", padx = (0, 5))
        
        self.edit_button = ctk.CTkButton(self.button_frame, text = "Edit", width = 70)
        self.edit_button.configure(command = lambda: self.edit_callback(self.thought_id, self.thought_label.cget("text")))
        self.edit_button.configure(image = self.edit_icon, compound = "left")
        self.edit_button.pack(side = "left", padx = 5)
        
        self.delete_button = ctk.CTkButton(self.button_frame, text = "Delete", width = 70)
        self.delete_button.configure(command = lambda: self.delete_callback(self.thought_id))
        self.delete_button.configure(image = self.delete_icon, compound = "left")
        self.delete_button.pack(side = "left")
        
    def toggle_favorite(self):
        self.favorite = not self.favorite
        self.favorite_button.configure(image = self.favorite_on if self.favorite else self.favorite_off)
        self.favorite_callback(self.thought_id)
        
    def set_reminder(self):
        self.reminder_callback(self.thought_id)
        
class InputPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pack(fill = "x", padx = 20)
        
        self.search_icon = ctk.CTkImage(light_image = Image.open("assets/search_icon.png"), dark_image = Image.open("assets/search_icon.png"), size = (18, 18))
        
        self.search_entry = ctk.CTkEntry(self, placeholder_text = "Search thoughts...")
        self.search_entry.pack(fill = "x", pady = (0, 10))
        
        self.textbox = ctk.CTkTextbox(self, height = 120)
        
        self.textbox.pack(fill = "x")
        
        self.save_icon = ctk.CTkImage(light_image = Image.open("assets/save_icon.png"), dark_image = Image.open("assets/save_icon.png"), size = (18, 18))
        
        self.save_button = ctk.CTkButton(self, text = "Save Thought")
        self.save_button.pack(pady = 15)
        self.save_button.configure(image = self.save_icon, compound = "left")
        
