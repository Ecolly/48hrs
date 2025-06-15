from game_classes.face_direction import *
import pyglet
import math

class Player:
    def __init__(self, name, health, level, experience, sprite, spriteindex, spritegrid, color, animtype, animframe, animmod, x, y):
        self.name = name
        self.health = health
        self.level = level
        self.experience = experience
        self.x = x # x coords are in 
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y 
        self.inventory = []
        self.direction = FaceDirection.DOWN  # Default direction
        self.technique = 0
        
        self.sprite = sprite  # pyglet.sprite.Sprite
        self.spriteindex = spriteindex #actual index of sprite on tilegrid
        self.grid = spritegrid
        self.color = color #4 entry tuple for the sprite to be colored as; white is default
        self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        self.animframe = 0 #what frame of the animation it's on
        self.animmod = animmod #a preset animation modifier (e.g. vibration amplitude)
        self.scale = 3


        # self.skills = []
        # self.equipment = {}
        # self.experience = 0

    # def get_screen_position(self):
    #     return self.scale*(self.prevx*16-8), self.scale*(self.prevy*16-8)

    # def is_mouse_over(self, mouse_x, mouse_y):
    #     """Check if a point is within this object's interactive bounds."""
    #     base_x, base_y = self.get_screen_position()
    #     #print(mouse_x, mouse_y, base_x, base_y)
    #     return (base_x <= mouse_x <= base_x + self.width*self.scale and
    #             base_y <= mouse_y <= base_y + self.height*self.scale)
    
    def process_turn(self, current_entity_turn):
        #print("a")
        if self.x != self.prevx:
            self.prevx = self.prevx + (abs(self.x - self.prevx)/(self.x - self.prevx))/8
        if self.y != self.prevy:
            self.prevy = self.prevy + (abs(self.y - self.prevy)/(self.y - self.prevy))/8

        #print(self.x, self.y, self.prevx, self.prevy)

        if self.y == self.prevy and self.x == self.prevx:
            return current_entity_turn + 1
        else:
            return current_entity_turn
            





    def draw(self, batch, animation_presets):
        base_x, base_y = 1152/2 -24, 768/2-24 #self.get_screen_position()
        sprite = self.sprite

        frame_index = self.spriteindex + self.direction.value * 8 + animation_presets[self.animtype][int(self.animframe)]
        tile = self.grid[frame_index]

        # Get texture and set filtering
        texture = tile.get_texture()
        texture.min_filter = pyglet.gl.GL_NEAREST
        texture.mag_filter = pyglet.gl.GL_NEAREST

        # Assign directly — no blitting, no texture creation
        sprite.image = texture

        self.animframe = self.animframe + self.animmod
        if self.animframe >= len(animation_presets[self.animtype]):
            self.animframe = 0

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

        #adjust rotation state (gross)
        if dx == 1:
            if dy == 1:
                self.direction = FaceDirection.UP_RIGHT
            elif dy == -1:
                self.direction = FaceDirection.DOWN_RIGHT
            else:
                self.direction = FaceDirection.RIGHT
        elif dx == -1:
            if dy == 1:
                self.direction = FaceDirection.UP_LEFT
            elif dy == -1:
                self.direction = FaceDirection.DOWN_LEFT
            else:
                self.direction = FaceDirection.LEFT
        else:
            if dy == 1:
                self.direction = FaceDirection.UP
            elif dy == -1:
                self.direction = FaceDirection.DOWN
        
        








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
    
