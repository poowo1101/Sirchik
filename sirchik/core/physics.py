class PhysicsBody:
    def __init__(self, x=0, y=0, width=32, height=32, max_speed=300, acceleration=1500, friction=1000):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vx = 0.0
        self.vy = 0.0
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.friction = friction
        self.current_speed = 0.0
    
    def apply_movement(self, move_x, move_y, dt):
        if move_x != 0 and move_y != 0:
            move_x *= 0.7071
            move_y *= 0.7071
        
        if move_x != 0 or move_y != 0:
            self.current_speed += self.acceleration * dt
            if self.current_speed > self.max_speed:
                self.current_speed = self.max_speed
        else:
            self.current_speed -= self.friction * dt
            if self.current_speed < 0:
                self.current_speed = 0
        
        self.vx = move_x * self.current_speed
        self.vy = move_y * self.current_speed
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def stop(self):
        self.vx = 0
        self.vy = 0
        self.current_speed = 0