class Player:
    def __init__(self, name, health, level, x=0, y=0):
        self.name = name
        self.health = health
        self.level = level
        self.x = x
        self.y = y
        self.inventory = []
        # self.skills = []
        # self.equipment = {}
        # self.experience = 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def is_alive(self):
        return self.health > 0

    def __str__(self):
        return f"Player(name={self.name}, health={self.health}"
    
