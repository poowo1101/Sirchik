import json
import os

class Settings:
    def __init__(self, filename: str = "sirchik_settings.json"):
        self.filename = filename
        self.data = {
            "video": {"fullscreen": False, "vsync": True, "width": 800, "height": 600, "fps": 60},
            "audio": {"master_volume": 1.0, "music_volume": 0.7, "sfx_volume": 1.0},
            "gameplay": {"camera_smoothness": 0.08, "show_fps": False, "language": "en"},
            "controls": {"up": "W", "down": "S", "left": "A", "right": "D", "pause": "ESCAPE", "console": "GRAVE"}
        }
        self.load()
    
    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    saved = json.load(f)
                    for cat in self.data:
                        if cat in saved:
                            self.data[cat].update(saved[cat])
            except: pass
    
    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.data, f, indent=4)
        except: pass
    
    def get(self, category: str, key: str, default=None):
        return self.data.get(category, {}).get(key, default)
    
    def set(self, category: str, key: str, value):
        if category in self.data:
            self.data[category][key] = value
            self.save()