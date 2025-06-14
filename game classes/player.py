from face_direction import FaceDirection

class Player:
    def __init__(self, name, health, level, x=0, y=0):
        self.name = name
        self.health = health
        self.level = level
        self.x = x
        self.y = y
        self.inventory = []
        self.direction = FaceDirection.DOWN  # Default direction
        
        # self.skills = []
        # self.equipment = {}
        # self.experience = 0

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
    
