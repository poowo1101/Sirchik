class Camera:
    def __init__(self, width: int, height: int, world_width: int = 2000, world_height: int = 2000):
        self.width = width
        self.height = height
        self.world_width = world_width
        self.world_height = world_height
        self.x = world_width / 2
        self.y = world_height / 2
        self.target_x = self.x
        self.target_y = self.y
        self.smoothness = 0.1
    
    def set_target(self, x: float, y: float):
        self.target_x = x
        self.target_y = y
    
    def update(self, dt: float):
        self.x += (self.target_x - self.x) * self.smoothness * (dt * 60)
        self.y += (self.target_y - self.y) * self.smoothness * (dt * 60)
        self.x = max(self.width/2, min(self.world_width - self.width/2, self.x))
        self.y = max(self.height/2, min(self.world_height - self.height/2, self.y))
    
    def apply(self, x: float, y: float):
        return (x - self.x + self.width/2, y - self.y + self.height/2)
    
    def get_offset(self):
        return (self.width/2 - self.x, self.height/2 - self.y)