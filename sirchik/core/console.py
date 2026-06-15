import pygame
from typing import Callable

class Console:
    def __init__(self):
        self.visible = False
        self.text = ""
        self.history = []
        self.commands = {}
        self.cursor_visible = True
        self.cursor_timer = 0.0
        self.font = pygame.font.Font(None, 24)
        self.max_lines = 10
    
    def register_command(self, name: str, callback: Callable):
        self.commands[name.lower()] = callback
    
    def toggle(self):
        self.visible = not self.visible
        if self.visible: self.text = ""
    
    def handle_event(self, event: pygame.event.Event):
        if not self.visible:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKQUOTE:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    self.toggle()
                    return True
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.execute(self.text)
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key in (pygame.K_ESCAPE, pygame.K_BACKQUOTE):
                self.visible = False
            elif event.unicode and event.unicode.isprintable():
                self.text += event.unicode
            return True
        return False
    
    def execute(self, text: str):
        text = text.strip()
        if not text: return
        self.history.append(f"] {text}")
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:]
        if cmd in self.commands:
            try:
                result = self.commands[cmd](*args)
                if result: self.history.append(str(result))
            except Exception as e:
                self.history.append(f"Error: {e}")
        else:
            self.history.append(f"Unknown: {cmd}")
        while len(self.history) > self.max_lines:
            self.history.pop(0)
    
    def update(self, dt: float):
        self.cursor_timer += dt
        if self.cursor_timer > 0.5:
            self.cursor_timer = 0.0
            self.cursor_visible = not self.cursor_visible
    
    def draw(self, screen: pygame.Surface):
        if not self.visible: return
        bg = pygame.Surface((screen.get_width(), screen.get_height()//2))
        bg.set_alpha(200)
        bg.fill((20, 20, 30))
        screen.blit(bg, (0, 0))
        
        y = 10
        for line in self.history:
            s = self.font.render(line, True, (200, 200, 200))
            screen.blit(s, (10, y))
            y += 25
        
        cur = "_" if self.cursor_visible else " "
        inp = self.font.render(f"] {self.text}{cur}", True, (255, 255, 255))
        screen.blit(inp, (10, y))