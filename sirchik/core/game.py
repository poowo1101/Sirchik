import pygame
import sys
import random
from typing import Optional
from .console import Console

class Game:
    STATUS_OK = 0
    STATUS_BROKEN = 1
    STATUS_GUTTED = 2
    
    def __init__(self, width: int = 800, height: int = 600, title: str = "Sirchik Game", fps: int = 60):
        pygame.init()
        
        self.width = width
        self.height = height
        self.title = title
        self.fps = fps
        
        self.screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        pygame.display.set_caption(title)
        
        self.clock = pygame.time.Clock()
        self.running = False
        self.scene: Optional["Scene"] = None
        self.delta_time: float = 0.0
        self.console = Console()
        
        self._engine_status = self.STATUS_OK
        self._error_count = 0
        self._missing_modules = []
        self._check_engine_integrity()
        self._register_default_commands()
    
    def _check_engine_integrity(self):
        try: from . import camera
        except ImportError: self._missing_modules.append("camera")
        try: from . import console
        except ImportError: self._missing_modules.append("console")
        try: from . import scene
        except ImportError: self._missing_modules.append("scene")
        try: from . import collision
        except ImportError: self._missing_modules.append("collision")
        
        if len(self._missing_modules) > 2:
            self._engine_status = self.STATUS_GUTTED
        elif len(self._missing_modules) > 0:
            self._engine_status = self.STATUS_BROKEN
    
    def report_error(self):
        self._error_count += 1
        if self._engine_status == self.STATUS_OK:
            self._engine_status = self.STATUS_BROKEN
    
    def _register_default_commands(self):
        self.console.register_command("sr_meow", self._cmd_meow)
        self.console.register_command("sr_fps", self._cmd_fps)
        self.console.register_command("sr_quit", self._cmd_quit)
        self.console.register_command("sr_status", self._cmd_status)
        self.console.register_command("sr_help", self._cmd_sr_help)
        self.console.register_command("sr_kill", self._cmd_sr_kill)
        self.console.register_command("sr_hp", self._cmd_sr_hp)
        self.console.register_command("sr_maxhp", self._cmd_sr_maxhp)
        self.console.register_command("sr_heal", self._cmd_sr_heal)
        self.console.register_command("sr_damage", self._cmd_sr_damage)
    
    def _get_scene_player_health(self):
        if not self.scene: return None
        if hasattr(self.scene, 'health'): return self.scene.health
        if hasattr(self.scene, 'player'):
            if hasattr(self.scene.player, 'health'): return self.scene.player.health
        return None
    
    def _cmd_meow(self, *args):
        if self._engine_status == self.STATUS_OK: return "Meow! ^_^"
        elif self._engine_status == self.STATUS_BROKEN: return "mEoW1!1"
        elif self._engine_status == self.STATUS_GUTTED: return "meow..."
        return "?"
    
    def _cmd_status(self, *args):
        names = {0: "OK", 1: "BROKEN (running)", 2: "GUTTED (modules missing)"}
        return f"Sirchik v1.0.0 | {names[self._engine_status]} | Errors: {self._error_count}"
    
    def _cmd_fps(self, *args):
        if args:
            try:
                self.fps = int(args[0])
                return f"FPS set to {self.fps}"
            except: return "Usage: sr_fps <number>"
        return f"FPS: {self.clock.get_fps():.0f}/{self.fps}"
    
    def _cmd_quit(self, *args):
        self.quit()
    
    def _cmd_sr_help(self, *args):
        return "sr_meow | sr_fps | sr_quit | sr_status | sr_kill | sr_hp | sr_maxhp | sr_heal | sr_damage"
    
    def _cmd_sr_kill(self, *args):
        health = self._get_scene_player_health()
        if health:
            health.hp = 0
            health.alive = False
            if hasattr(self.scene, 'on_death'): self.scene.on_death("sr_kill")
            return "💀 Killed!"
        return "No health found"
    
    def _cmd_sr_hp(self, *args):
        health = self._get_scene_player_health()
        if not health: return "No health found"
        if args:
            try:
                health.hp = max(0, min(health.max_hp, int(args[0])))
                return f"HP: {health.hp}/{health.max_hp}"
            except: return "Usage: sr_hp <number>"
        return f"HP: {health.hp}/{health.max_hp}"
    
    def _cmd_sr_maxhp(self, *args):
        health = self._get_scene_player_health()
        if not health: return "No health found"
        if args:
            try:
                v = int(args[0])
                if v < 1: return "Must be > 0"
                health.max_hp = v
                if health.hp > v: health.hp = v
                return f"Max HP: {v}"
            except: return "Usage: sr_maxhp <number>"
        return f"Max HP: {health.max_hp}"
    
    def _cmd_sr_heal(self, *args):
        health = self._get_scene_player_health()
        if not health: return "No health found"
        if not health.alive: return "Already dead"
        amt = int(args[0]) if args else 100
        old = health.hp
        health.heal(amt)
        return f"+{health.hp - old} HP → {health.hp}/{health.max_hp}"
    
    def _cmd_sr_damage(self, *args):
        health = self._get_scene_player_health()
        if not health: return "No health found"
        if not health.alive: return "Already dead"
        amt = int(args[0]) if args else 10
        health.take_damage(amt)
        if not health.alive:
            if hasattr(self.scene, 'on_death'): self.scene.on_death(f"sr_damage {amt}")
            return f"💀 -{amt} HP → DEAD"
        return f"-{amt} HP → {health.hp}/{health.max_hp}"
    
    def set_scene(self, scene: "Scene"):
        if self.scene: self.scene.on_exit()
        self.scene = scene
        scene.game = self
        scene.on_enter()
    
    def run(self, start_scene: "Scene"):
        self.set_scene(start_scene)
        self.running = True
        
        while self.running:
            self.delta_time = self.clock.tick(self.fps) / 1000.0
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.VIDEORESIZE:
                    self.width, self.height = event.w, event.h
                    self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
                
                if not self.console.handle_event(event):
                    if self.scene:
                        try: self.scene.handle_event(event)
                        except Exception as e:
                            self.report_error()
                            print(f"[Sirchik] Event error: {e}")
            
            if self.scene:
                try: self.scene.update(self.delta_time)
                except Exception as e:
                    self.report_error()
                    print(f"[Sirchik] Update error: {e}")
            
            self.console.update(self.delta_time)
            
            self.screen.fill((0, 0, 0))
            if self.scene:
                try: self.scene.draw(self.screen)
                except Exception as e:
                    self.report_error()
                    print(f"[Sirchik] Draw error: {e}")
            
            self.console.draw(self.screen)
            pygame.display.flip()
        
        pygame.quit()
    
    def quit(self):
        if self.scene: self.scene.on_exit()
        self.running = False