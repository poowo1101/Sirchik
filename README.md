markdown
# 🎮 Sirchik Engine

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/poowo1101/Sirchik)
[![Python](https://img.shields.io/badge/Python-3.8+-yellow.svg)](https://python.org)
[![Pygame-CE](https://img.shields.io/badge/Pygame--CE-latest-green.svg)](https://pyga.me)
[![License](https://img.shields.io/badge/license-MIT-red.svg)](LICENSE)

> **Простий 2D-рушій на Python для тих, хто хоче робити ігри, а не налаштовувати тулчейн.**

---

## 🚀 Встановлення

```bash
pip install pygame-ce
git clone https://github.com/poowo1101/Sirchik
cd Sirchik
⚡ 30 секунд до першої гри
python
from sirchik.core.game import Game
from sirchik.core.scene import Scene

class MyGame(Scene):
    def draw(self, screen):
        screen.fill((20, 20, 30))

game = Game(width=800, height=600, title="Моя гра", fps=60)
game.run(MyGame())
Все. Вікно відкрито. Можеш малювати.

🧩 Що вміє
Компонент	Опис
🎯 Game	Головний цикл, вікно, FPS, дельта-тайм
🎬 Scene	Сцени з on_enter, update, draw, handle_event
📷 Camera	2D камера з плавним слідкуванням
⚡ PhysicsBody	Фізика з прискоренням, тертям, максимальною швидкістю
💥 Collision	AABB, коло, точка в прямокутнику, вирішення колізій
❤️ Health	HP, шкода, лікування, респавн
💀 DeathScreen	Екран смерті з можливістю респавну
🖥️ Console	Консоль розробника (Shift + ~)
⏳ LoadingScreen	Екран завантаження з прогрес-баром
⚙️ Settings	JSON-налаштування з авто-збереженням
🎛️ SettingsMenu	Готове меню налаштувань
🎥 Камера
python
camera = Camera(width=800, height=600, world_width=2000, world_height=2000)
camera.smoothness = 0.08  # 0 = миттєво, 0.1 = плавно

camera.set_target(player_x, player_y)
camera.update(dt)

screen_x, screen_y = camera.apply(world_x, world_y)
⚡ Фізика
python
body = PhysicsBody(x=400, y=300, width=40, height=40,
                   max_speed=400, acceleration=1500, friction=1000)

body.apply_movement(move_x, move_y, dt)  # -1, 0, або 1

# body.x, body.y — позиція
# body.vx, body.vy — швидкість
💥 Колізії
python
# Перевірка
Collision.aabb(x1, y1, w1, h1, x2, y2, w2, h2)  # -> bool
Collision.circle(x1, y1, r1, x2, y2, r2)        # -> bool

# Вирішення (виштовхування зі стін)
x, y, vx, vy = Collision.check_and_resolve(
    x, y, w, h, vx, vy, blocks  # blocks = [[x, y, w, h], ...]
)
🖥️ Консоль
Shift + ~ відкриває консоль. Вбудовані команди:

text
sr_fps        # показати FPS
sr_fps 144    # встановити FPS
sr_hp         # показати HP
sr_hp 50      # встановити HP
sr_heal 20    # лікування
sr_damage 30  # шкода
sr_kill       # вбити гравця
sr_quit       # вийти
sr_status     # статус движка
sr_meow       # діагностика
Свої команди:

python
game.console.register_command("money", lambda: f"Gold: {gold}")
game.console.register_command("give", my_give_func)
❤️ Здоров'я
python
hp = Health(max_hp=100)
hp.take_damage(25)   # -25 HP
hp.heal(15)          # +15 HP
hp.is_alive()        # -> bool
hp.get_ratio()       # -> float (для HP бару)
hp.revive()          # воскресити
💀 Екран смерті
python
from sirchik.core.death_screen import DeathScreen

game.set_scene(DeathScreen(
    reason="Вас вбив дракон!",
    respawn_scene=GameScene,  # SPACE для респавну
    bg_color=(80, 0, 0),
    text_color=(255, 50, 50)
))
⚙️ Налаштування
python
settings = Settings("config.json")
settings.set("audio", "volume", 0.8)      # авто-збереження
volume = settings.get("audio", "volume", 1.0)
📂 Структура
text
Sirchik/
├── sirchik/
│   ├── __init__.py
│   └── core/
│       ├── game.py
│       ├── scene.py
│       ├── camera.py
│       ├── physics.py
│       ├── collision.py
│       ├── health.py
│       ├── death_screen.py
│       ├── console.py
│       ├── loading_screen.py
│       ├── settings.py
│       └── settings_menu.py
├── examples/
│   └── full_example.py
├── README.md
└── LICENSE
🎮 Повний приклад
python
import pygame
from sirchik.core.game import Game
from sirchik.core.scene import Scene
from sirchik.core.physics import PhysicsBody
from sirchik.core.collision import Collision
from sirchik.core.camera import Camera

class GameScene(Scene):
    def __init__(self):
        super().__init__()
        self.player = PhysicsBody(400, 300, 40, 40, max_speed=400)
        self.camera = Camera(800, 600, 2000, 2000)
        self.camera.smoothness = 0.08
        self.blocks = [[300, 300, 200, 30], [600, 400, 30, 200]]

    def update(self, dt):
        keys = pygame.key.get_pressed()
        mx = keys[pygame.K_d] - keys[pygame.K_a]
        my = keys[pygame.K_s] - keys[pygame.K_w]
        self.player.apply_movement(mx, my, dt)
        
        self.player.x, self.player.y, _, _ = Collision.check_and_resolve(
            self.player.x, self.player.y, 40, 40,
            self.player.vx, self.player.vy, self.blocks
        )
        
        self.camera.set_target(self.player.x + 20, self.player.y + 20)
        self.camera.update(dt)

    def draw(self, screen):
        screen.fill((20, 20, 30))
        for b in self.blocks:
            bx, by = self.camera.apply(b[0], b[1])
            pygame.draw.rect(screen, (100, 80, 60), (bx, by, b[2], b[3]))
        px, py = self.camera.apply(self.player.x, self.player.y)
        pygame.draw.rect(screen, (0, 255, 0), (px, py, 40, 40))

if __name__ == "__main__":
    game = Game(800, 600, "Гра на Sirchik Engine", 60)
    game.run(GameScene())
📄 Ліцензія
MIT © Poowo1101

⭐ Підтримка
Постав зірочку якщо рушій тобі сподобався. Кожна ⭐ гріє душу розробнику.

"Я навіть не знаю скільки я робив движок і документацію" — Poowo1101

Декілька слів від пуву

"Я просто назвав цей движок в честь мого кота Сірчика" 
