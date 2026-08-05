import json
from pathlib import Path

SETTINGS_FILE = Path("config/settings.json")

class Settings:
    DEFAULTS = {
        "theme": "System",
        "window_width": 900,
        "window_height": 700,
        "window_x": 250,
        "window_y": 120,
        "autosave": True,
        "autosave_delay": 1000
    }
    
    def __init__(self):
        SETTINGS_FILE.parent.mkdir(exist_ok = True)
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE) as f:
                self.data = json.load(f)
                
        else:
            self.data = self.DEFAULTS.copy()
            self.save()
            
    def save(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.data, f, indent = 4)
            
    def get(self, key):
        return self.data.get(key, self.DEFAULTS[key])
        
    def set(self, key, value):
        self.data[key] = value
        self.save()