import pygame
from .scene import Scene

class SettingsMenu(Scene):
    def __init__(self, back_scene=None, title="SETTINGS"):
        super().__init__()
        self.back_scene = back_scene
        self.title = title
        self.selected = 0
        
        self.options = [
            {"name": "Fullscreen", "key": "fullscreen", "category": "video", "type": "bool", "value": False},
            {"name": "VSync", "key": "vsync", "category": "video", "type": "bool", "value": True},
            {"name": "FPS Limit", "key": "fps", "category": "video", "type": "int_range", "value": 60, "min": 30, "max": 300, "step": 10},
            {"name": "Master Volume", "key": "master_volume", "category": "audio", "type": "float_range", "value": 1.0, "min": 0.0, "max": 1.0, "step": 0.1},
            {"name": "Music Volume", "key": "music_volume", "category": "audio", "type": "float_range", "value": 0.7, "min": 0.0, "max": 1.0, "step": 0.1},
            {"name": "SFX Volume", "key": "sfx_volume", "category": "audio", "type": "float_range", "value": 1.0, "min": 0.0, "max": 1.0, "step": 0.1},
            {"name": "Show FPS", "key": "show_fps", "category": "gameplay", "type": "bool", "value": False},
            {"name": "Language", "key": "language", "category": "gameplay", "type": "choice", "value": "en", "choices": ["en", "uk", "pl"]},
        ]
        
        try:
            from .settings import Settings
            s = Settings()
            for opt in self.options:
                val = s.get(opt["category"], opt["key"])
                if val is not None: opt["value"] = val
        except: pass
    
    def _save(self):
        try:
            from .settings import Settings
            s = Settings()
            for opt in self.options:
                s.set(opt["category"], opt["key"], opt["value"])
        except: pass
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._save()
                if self.back_scene: self.game.set_scene(self.back_scene())
                else: self.game.quit()
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self._change(-1)
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self._change(1)
            elif event.key == pygame.K_RETURN:
                opt = self.options[self.selected]
                if opt["type"] == "bool":
                    opt["value"] = not opt["value"]
                elif opt["type"] == "choice":
                    choices = opt.get("choices", [])
                    idx = choices.index(opt["value"]) if opt["value"] in choices else 0
                    opt["value"] = choices[(idx+1) % len(choices)]
    
    def _change(self, direction):
        opt = self.options[self.selected]
        if opt["type"] in ("int_range", "float_range"):
            opt["value"] += direction * opt.get("step", 1)
            opt["value"] = max(opt.get("min", 0), min(opt.get("max", 999), opt["value"]))
            if opt["type"] == "float_range":
                opt["value"] = round(opt["value"], 2)
        elif opt["type"] == "choice":
            choices = opt.get("choices", [])
            idx = choices.index(opt["value"]) if opt["value"] in choices else 0
            opt["value"] = choices[(idx+direction) % len(choices)]
    
    def draw(self, screen):
        screen.fill((20, 20, 35))
        
        font_title = pygame.font.Font(None, 56)
        font_opt = pygame.font.Font(None, 30)
        font_val = pygame.font.Font(None, 26)
        font_hint = pygame.font.Font(None, 18)
        
        title = font_title.render(self.title, True, (255,255,255))
        screen.blit(title, (self.game.width//2 - title.get_width()//2, 40))
        pygame.draw.line(screen, (100,100,150), (80, 75), (self.game.width-80, 75), 1)
        
        for i, opt in enumerate(self.options):
            y = 110 + i * 42
            if y < 80 or y > self.game.height-60: continue
            
            if i == self.selected:
                pygame.draw.rect(screen, (40,40,70), (70, y-3, self.game.width-140, 32))
                pygame.draw.rect(screen, (0,200,100), (70, y-3, self.game.width-140, 32), 1)
            
            name_color = (255,255,255) if i == self.selected else (200,200,200)
            name = font_opt.render(opt["name"], True, name_color)
            screen.blit(name, (85, y))
            
            val_str = self._format(opt)
            if i == self.selected: val_str = f"< {val_str} >"
            val = font_val.render(val_str, True, (150,200,150) if i == self.selected else (150,150,150))
            screen.blit(val, (self.game.width - val.get_width() - 85, y))
        
        hints = ["Arrows/WASD: Navigate | Left/Right: Change | Enter: Toggle | ESC: Back & Save"]
        for i, h in enumerate(hints):
            hs = font_hint.render(h, True, (120,120,120))
            screen.blit(hs, (self.game.width//2 - hs.get_width()//2, self.game.height-35))
    
    def _format(self, opt):
        if opt["type"] == "bool": return "ON" if opt["value"] else "OFF"
        elif "volume" in opt["key"]: return f"{int(opt['value']*100)}%"
        elif opt["type"] == "choice": return str(opt["value"]).upper()
        return str(opt["value"])