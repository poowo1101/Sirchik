import pygame
from .scene import Scene

class DeathScreen(Scene):
    def __init__(self, reason: str = "You died", respawn_scene=None, bg_color=(80,0,0), text_color=(255,50,50)):
        super().__init__()
        self.reason = reason
        self.respawn_scene = respawn_scene
        self.bg_color = bg_color
        self.text_color = text_color
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and self.respawn_scene:
                self.game.set_scene(self.respawn_scene())
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()
    
    def draw(self, screen):
        screen.fill(self.bg_color)
        
        font_big = pygame.font.Font(None, 100)
        font_small = pygame.font.Font(None, 36)
        font_tiny = pygame.font.Font(None, 20)
        
        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500.0
        
        # Тінь
        shadow = font_big.render("YOU DIED", True, (0, 0, 0))
        sr = shadow.get_rect(center=(self.game.width//2+3, self.game.height//2-53))
        screen.blit(shadow, sr)
        
        # Текст
        death = font_big.render("YOU DIED", True, self.text_color)
        dr = death.get_rect(center=(self.game.width//2, self.game.height//2-50))
        screen.blit(death, dr)
        
        # Причина
        reason = font_small.render(self.reason, True, (255, 180, 180))
        rr = reason.get_rect(center=(self.game.width//2, self.game.height//2+20))
        screen.blit(reason, rr)
        
        # Підказки
        y = self.game.height//2 + 60
        if self.respawn_scene:
            hint = font_small.render("SPACE = Respawn", True, (200,200,200))
            screen.blit(hint, (self.game.width//2 - hint.get_width()//2, y))
            y += 30
        hint2 = font_small.render("ESC = Quit", True, (200,200,200))
        screen.blit(hint2, (self.game.width//2 - hint2.get_width()//2, y))
        
        # Sirchik
        powered = font_tiny.render("Death Screen (c) Sirchik Engine by Poowo1101", True, (100,100,100))
        screen.blit(powered, (self.game.width//2 - powered.get_width()//2, self.game.height-25))