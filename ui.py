import customtkinter as ctk
from tkinter import Menu

class MainWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.menu = Menu(self)
        self.configure(menu = self.menu)
        
        self.file_menu = Menu(self.menu, tearoff = False)
        self.menu.add_cascade(label = "File", menu = self.file_menu)
        
        self.file_menu.add_command(label = "New Thought")
        self.file_menu.add_separator()
        self.file_menu.add_command(label = "Exit")
        
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
        
class ThoughtCard(ctk.CTkFrame):
    def __init__ (self, parent, thought_id, thought, date, delete_callback, edit_callback):
        super().__init__(parent)
        
        self.thought_id = thought_id
        self.delete_callback = delete_callback
        self.edit_callback = edit_callback
        
        self.thought_label = ctk.CTkLabel(self, text = thought, anchor = "w", justify = "left", wraplength = 500, font = ("Arial", 12))
        self.thought_label.pack(anchor = "w", padx = 15, pady = (10, 4))
        
        self.date_label = ctk.CTkLabel(self, text = date, text_color = "gray")
        self.date_label.pack(anchor = "w", padx = 15, pady = (0, 10))
        
        self.buttom_frame = ctk.CTkFrame(self, fg_color = "transparent")
        self.buttom_frame.pack(anchor = "e", padx = 15, pady = (0, 10))
        
        self.edit_button = ctk.CTkButton(self.buttom_frame, text = "Edit", width = 70)
        self.edit_button.configure(command = lambda: self.edit_callback(self.thought_id, self.thought_label.cget("text")))
        self.edit_button.pack(side = "left", padx = 5)
        
        self.delete_button = ctk.CTkButton(self.buttom_frame, text = "Delete", width = 70)
        self.delete_button.configure(command = lambda: self.delete_callback(self.thought_id))
        self.delete_button.pack(side = "left")
        
class InputPanel(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.pack(fill = "x", padx = 20)
        
        self.search_entry = ctk.CTkEntry(self, placeholder_text = "Search thoughts...")
        self.search_entry.pack(fill = "x", pady = (0, 10))
        
        self.textbox = ctk.CTkTextbox(self, height = 120)
        
        self.textbox.pack(fill = "x")
        
        self.save_button = ctk.CTkButton(self, text = "Save Thought")
        self.save_button.pack(pady = 15)
        
