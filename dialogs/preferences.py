from dialogs.base_dialog import BaseDialog
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
        ctk.CTkLabel(general, text = "Window", font = ("Arial", 20)).pack(anchor = "w", pady = (15, 10), padx = 20)
        window_frame = ctk.CTkFrame(general, fg_color = "transparent")
        window_frame.pack(fill = "x", padx = 20)
        ctk.CTkLabel(window_frame, text = "Window Size is saved automatically", font = ("Arial", 16)).pack(anchor = "w")
        
        editor = self.tabs.add("Editor")
        ctk.CTkLabel(editor, text = "Autosave", font = ("Arial", 20)).pack(anchor = "w", pady = (15, 10), padx = 20)
        autosave_frame = ctk.CTkFrame(editor, fg_color = "transparent")
        autosave_frame.pack(fill = "x", padx = 20)
        ctk.CTkLabel(autosave_frame, text = "Enable Autosave", font = ("Arial", 16)).pack(anchor = "w")
        self.autosave_switch = ctk.CTkSwitch(autosave_frame, text = "")
        self.autosave_switch.pack(side = "right")
        if self.master.settings.get("autosave", True):
            self.autosave_switch.select()
        else:
            self.autosave_switch.deselect()
        delay_frame = ctk.CTkFrame(editor, fg_color = "transparent")
        delay_frame.pack(fill = "x", padx = 20)
        
        ctk.CTkLabel(delay_frame, text = "Autosave Delay (milliseconds)", font = ("Arial", 16)).pack(anchor = "w")
        self.delay_entry = ctk.CTkEntry(delay_frame)
        current_delay = self.master.settings.get("autosave_delay", 1000)
        self.delay_entry.insert(0, str(current_delay))
        self.delay_entry.pack(side = "right")
        
    def save(self):
        theme = self.theme.get()
        
        self.master.settings.set("theme", theme)
        
        if self.autosave_switch.get() == 1:
            self.master.settings.set("autosave", True)
            self.master.settings.set("autosave_delay", int(self.delay_entry.get()))
        else:
            self.master.settings.set("autosave", False)
            self.master.settings.set("autosave_delay", 0)
        
        ctk.set_appearance_mode(theme)
        
        self.master.status_bar.flash("Preferences Saved")
        
        self.destroy()