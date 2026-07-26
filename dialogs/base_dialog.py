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

        self.center()

    def center(self):
        self.update_idletasks()

        parent = self.master
        
        x = (parent.winfo_x() + (parent.winfo_width() // 2) - (self.winfo_width() // 2))

        y = (parent.winfo_y()+ (parent.winfo_height() // 2)- (self.winfo_height() // 2))

        self.geometry(f"+{x}+{y}")