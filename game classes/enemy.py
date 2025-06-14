from player import Player

class Enemy:
    def __init__(self, name, health=50, x=0, y=0, level=1):
        self.name = name
        self.health = health
        self.x = x
        self.y = y
        self.level = level  # Default level for all enemies

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def is_alive(self):
        return self.health > 0
    
    #TODO
    def attack(self, player):
        # Implement attack logic here
        pass
    def detect_player(self, player):
        # Implement player detection logic here
        pass 

class Goblin(Enemy):
    def __init__(self, x=0, y=0, level=1):
        super().__init__(name="Goblin", health=30, x=x, y=y, level=level)
        self.attack_power = 5


