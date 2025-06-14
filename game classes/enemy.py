from player import Player
from face_direction import FaceDirection

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
    def attack(self, player:Player):
        # Implement attack logic here
        pass
    
    def can_see_player(self, player:Player, vision_range=5):
        ex, ey = self.x, self.y
        px, py = player.x, player.y
        # Calculate the distance between the enemy and the player
        # Using Euclidean distance for simplicity
        distance = ((ex - px) ** 2 + (ey - py) ** 2) ** 0.5
        return distance <= vision_range

class Goblin(Enemy):
    def __init__(self, x=0, y=0, level=1):
        super().__init__(name="Goblin", health=30, x=x, y=y, level=level)
        self.attack_power = 5


