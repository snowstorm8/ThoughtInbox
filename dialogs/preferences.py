from base_dialog import BaseDialog
import customtkinter as ctk

class PreferencesDialog(BaseDialog):
    def __init__(self, parent):
        super().__init__(parent, "Preferences", 650, 450)
        
        self.tabs = ctk.CTkTabview(self)
        
        self.tabs.pack(fill = "both", expand = True, padx = 20, pady = 20)
        
        appearance = self.tabs.add("Appearance")
        ctk.CTkLabel(appearance, text = "Theme", font = ("Arial", 20)).pack(anchor = "w", pady = (15, 10), padx = 20)
        self.theme = ctk.StringVar(value = parent.settings.get("theme"))
        ctk.CTkRadioButton(appearance, text = "Light", variable = self.theme, value = "Light").pack(anchor = "w", padx = 35)
        ctk.CTkRadioButton(appearance, text = "Dark", variable = self.theme, value = "Dark").pack(anchor = "w", padx = 35)
        ctk.CTkRadioButton(appearance, text = "System", variable = self.theme, value = "System").pack(anchor = "w", padx = 35)
        
        bottom = ctk.CTkFrame(self, fg_color = "transparent")
        bottom.pack(fill = "x", pady = (0, 20))
        ctk.CTkButton(bottom, text = "Cancel", command = self.destroy).pack(side = "right", padx = 10)
        ctk.CTkButton(bottom, text = "Save", command = self.save).pack(side = "right")
        
        general = self.tabs.add("General")
        editor = self.tabs.add("Editor")
        
    def save(self):
        theme = self.theme.get()
        
        self.master.settings.set("theme", theme)
        
        ctk.set_appearance_mode(theme)
        
        self.master.status_bar.flash("Preferences Saved")
        
        self.destroy()