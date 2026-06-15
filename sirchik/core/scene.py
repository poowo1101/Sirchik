import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .game import Game

class Scene:
    """
    Базова сцена. Успадковуй від неї для створення своїх сцен
    (меню, гра, налаштування, game over тощо).
    """
    def __init__(self):
        self.game: "Game" = None
    
    def on_enter(self):
        """Викликається коли сцена стає активною"""
        pass
    
    def on_exit(self):
        """Викликається коли сцена змінюється на іншу"""
        pass
    
    def handle_event(self, event: pygame.event.Event):
        """Обробка подій (клавіші, миша і т.д.)"""
        pass
    
    def update(self, dt: float):
        """Оновлення логіки. dt — дельта-тайм у секундах"""
        pass
    
    def draw(self, screen: pygame.Surface):
        """Малювання сцени"""
        pass