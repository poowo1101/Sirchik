import pygame
import math
from .scene import Scene

class LoadingScreen(Scene):
    def __init__(self, load_func, text: str = "Loading...", bg_color=(10,10,20), bar_color=(0,200,100)):
        super().__init__()
        self.load_func = load_func
        self.text = text
        self.bg_color = bg_color
        self.bar_color = bar_color
        self.progress = 0.0
        self.loaded = False
        self.next_scene = None
        self.timer = 0.0
    
    def update(self, dt):
        self.timer += dt
        
        if not self.loaded:
            self.progress += dt * 0.4
            if self.progress >= 0.7:
                try:
                    self.next_scene = self.load_func()
                    self.loaded = True
                    self.progress = 1.0
                except Exception as e:
                    print(f"[Sirchik] Loading error: {e}")
                    self.loaded = True
                    self.progress = 0.0
        
        if self.loaded and self.timer > 0.5:
            if self.next_scene:
                self.game.set_scene(self.next_scene)
    
    def draw(self, screen):
        screen.fill(self.bg_color)
        cx, cy = self.game.width//2, self.game.height//2
        
        # Спінер
        for i in range(8):
            angle = math.radians(self.timer * 360 + i * 45)
            sx = cx + math.cos(angle) * 35
            sy = cy - 70 + math.sin(angle) * 35
            alpha = 255 - i * 28
            pygame.draw.circle(screen, self.bar_color, (int(sx), int(sy)), 4)
        
        # Текст
        font = pygame.font.Font(None, 36)
        text = font.render(self.text, True, (255,255,255))
        screen.blit(text, (cx - text.get_width()//2, cy - 15))
        
        # Прогрес-бар
        bw, bh = 350, 18
        bx, by = cx - bw//2, cy + 25
        pygame.draw.rect(screen, (40,40,50), (bx, by, bw, bh))
        if self.progress > 0:
            pygame.draw.rect(screen, self.bar_color, (bx, by, int(bw*self.progress), bh))
        pygame.draw.rect(screen, (100,100,120), (bx, by, bw, bh), 2)
        
        # %
        font_pct = pygame.font.Font(None, 22)
        pct = font_pct.render(f"{int(self.progress*100)}%", True, (255,255,255))
        screen.blit(pct, (cx - pct.get_width()//2, by + bh + 8))
        
        # Sirchik
        font_tiny = pygame.font.Font(None, 18)
        ver = font_tiny.render("Sirchik Engine v1.0.0 | Poowo1101", True, (100,100,100))
        screen.blit(ver, (cx - ver.get_width()//2, self.game.height-22))