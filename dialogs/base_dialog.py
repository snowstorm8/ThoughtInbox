import customtkinter as ctk


class BaseDialog(ctk.CTkToplevel):

    def __init__(self, parent, title, width = 400, height = 250):
        super().__init__(parent)

        self.title(title)
        self.geometry(f"{width}x{height}")
        self.resizable(False, False)

        # Make modal
        self.transient(parent)
        self.grab_set()
        self.focus_force()
        self.protocol("WM_DELETE_WINDOW", self.destroy)

        self.after_idle(self.center)

    def center(self):
        self.update_idletasks()

        parent = self.master
        
        x = (parent.winfo_rootx() + (parent.winfo_width() - self.winfo_width()) // 2)

        y = (parent.winfo_rooty() + (parent.winfo_height() - self.winfo_height()) // 2)

        self.geometry(f"+{x}+{y}")
        
    def force_center(self):
        self.update_idletasks()
        
        width = self.winfo_width()
        height = self.winfo_height()
        
        screenwidth = self.winfo_screenwidth()
        screenheight = self.winfo_screenheight()
        
        x = (screenwidth - (width // 2)) // 2
        y = (screenheight - (height // 2)) // 2
        
        self.geometry(f"{width}x{height}+{x}+{y}")