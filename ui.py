import customtkinter as ctk

class MainWindow(ctk.CTk):
    
    def __init__(self):
        super().__init__()
        
        self.title("Thought Inbox")
        self.geometry("700x500")
        
        # ------- Title ------- #
        self.title_label = ctk.CTkLabel(self, text="Thought Inbox", font=("Arial", 24, "bold"))
        
        self.title_label.pack(pady=(20,10))
        
        # ------- Thought Entry ------- #
        self.textbox = ctk.CTkTextbox(self, width = 600, height = 120)
        
        self.textbox.pack()
        
        # ------- Save Button ------- #
        self.save_button = ctk.CTkButton(self, text="Save Thought")
        
        self.save_button.pack(pady = 15)
        
        # ------- Recent Thoughts ------- #
        self.thought_label = ctk.CTkLabel(self, text="Recent Thoughts", font=("Arial", 18, "bold"))
        
        self.thought_label.pack(pady = (10, 5))
        
        self.scroll_frame = ctk.CTkScrollableFrame(self, width = 620, height = 250)
        
        self.scroll_frame.pack(fill = "both", expand = True, padx = 20, pady = (0, 20))