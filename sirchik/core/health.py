class Health:
    def __init__(self, max_hp: int = 100):
        self.max_hp = max_hp
        self.hp = max_hp
        self.alive = True
    
    def take_damage(self, amount: int) -> int:
        if not self.alive: return 0
        self.hp -= amount
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
        return self.hp
    
    def heal(self, amount: int) -> int:
        if not self.alive: return 0
        self.hp += amount
        if self.hp > self.max_hp: self.hp = self.max_hp
        return self.hp
    
    def revive(self, hp: int = None):
        self.alive = True
        self.hp = hp if hp is not None else self.max_hp
    
    def is_alive(self) -> bool:
        return self.alive
    
    def get_ratio(self) -> float:
        return self.hp / self.max_hp if self.max_hp > 0 else 0