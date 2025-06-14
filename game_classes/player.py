from game_classes.face_direction import *

from game_classes.face_direction import *

class Player:
    def __init__(self, name, health, level, sprite, color, animtype, animframe, animmod, x, y):
        self.name = name
        self.health = health
        self.level = level
        self.x = x # x coords are in 
        self.y = y
        self.inventory = []
        self.direction = FaceDirection.DOWN  # Default direction
        
        self.sprite = sprite  # pyglet.sprite.Sprite
        self.color = color #4 entry tuple for the sprite to be colored as; white is default
        self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        self.animframe = 0 #what frame of the animation it's on
        self.animmod = animmod #a preset animation modifier (e.g. vibration amplitude)
        self.scale = 2
        # self.skills = []
        # self.equipment = {}
        # self.experience = 0

    def get_screen_position(self):
        return self.x*32-16, self.y*32-16

    def draw(self, batch):
        base_x, base_y = self.get_screen_position()
        sprite = self.sprite
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        sprite.color = self.color
        sprite.batch = batch
        sprite.z = 40

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
    
    def move(self, dx, dy): #Move relative to current position
        self.x += dx
        self.y += dy

    def is_alive(self):
        return self.health > 0
    
    def set_face_direction(self, direction):
        if isinstance(direction, FaceDirection):
            self.direction = direction
        else:
            raise ValueError("Invalid direction. Use 'up', 'down', 'left', or 'right'.")

    def __str__(self):
        return f"Player(name={self.name}, health={self.health}"
    
    def enemy_collison(self, enemy_list):
        """Check if an enemy is nearby in a 3x3 around the player."""
        directions = [(-1, -1), (-1, 0), (-1, 1),
                (0, -1),          (0, 1),
                (1, -1),  (1, 0), (1, 1)]
        for dx, dy in directions:
            x, y = self.x + dx, self.y + dy
            for enemy in enemy_list:
                if enemy.x == x and enemy.y == y:
                    return True
            return False

    def __str__(self):
        return f"Player(name={self.name}, health={self.health}"
    
