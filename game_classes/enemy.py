from game_classes.player import Player
from game_classes.face_direction import FaceDirection
import pyglet
import math

def create_sprite_enemy(image_grid, index):
    tex = pyglet.image.Texture.create(16, 16)
    tex.blit_into(image_grid[index], 0, 0, 0)
    return pyglet.sprite.Sprite(tex, x=0, y=0)


def generate_enemy(name, level, x, y, grid):

    enemy_names = ["DAMIEN", "LEAFALOTTA", "CHLOROSPORE", "GOOSE", "FOX", "S'MORE"]
    enemy_hps = [20, 15, 18, 8, 10, 12]
    enemy_sprites = [20*64, 18*64, 17*64, 16*64, 15*64, 14*64]
    enemy_animtypes = [1, 1, 1, 1, 2, 1]
    enemy_animmods = [1/8, 1/8, 1/8, 1/8, 1/8]

    id = enemy_names.index(name)
    enemy = Enemy(
        name = name,
        health = enemy_hps[id],
        level = level,
        sprite = create_sprite_enemy(grid, enemy_sprites[id]), #this SUCKS
        spriteindex = enemy_sprites[id],
        spritegrid = grid,
        color = (255, 255, 255, 255),
        animtype = enemy_animtypes[id],
        animmod = enemy_animmods[id],
        animframe = 0,
        x = x,
        y = y,


    ) 

    return enemy



class Enemy:
    def __init__(self, name, health, level, sprite, spriteindex, spritegrid, color, animtype, animframe, animmod, x, y):
        self.name = name
        self.health = health
        self.level = level
        self.x = x # x coords are in 
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y 
        self.inventory = []
        self.direction = FaceDirection.DOWN  # Default direction
        self.technique = "n/a"
        self.techniquex = 0
        self.techniquey = 0
        self.techniqueframe = 0
        self.techniquefinished = 0

        self.sprite = sprite  # pyglet.sprite.Sprite
        self.spriteindex = spriteindex #actual index of sprite on tilegrid
        self.grid = spritegrid
        self.color = color #4 entry tuple for the sprite to be colored as; white is default
        self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        self.animframe = animframe #what frame of the animation it's on
        self.animmod = animmod #a preset animation modifier (e.g. vibration amplitude)
        self.scale = 3


    def do_AI(self, all_enemies, player):
        if self.name == "FOX":
            return "move", self.x, self.y+1
        elif self.name == "GOOSE":
            if abs(player.x-self.x) < 2 and abs(player.y-self.y) < 2:
                return "hit", player.x, player.y
            else:
                return "move", self.x + round(abs(player.x-self.x)/((player.x-self.x)+0.01)), self.y + round(abs(player.y-self.y)/((player.y-self.y)+0.01))




    def draw(self, batch, animation_presets, player):
        base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.prevx*16 + 8)*self.scale
        base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.prevy*16 + 8)*self.scale



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




    def process_turn(self):
        #print("a")
        self.techniqueframe = self.techniqueframe + 1

        if self.technique == "move":
            if self.techniquex != self.prevx:
                self.prevx = self.prevx + round((abs(self.techniquex - self.prevx)/(self.techniquex - self.prevx+0.01)))/8
            if self.techniquey != self.prevy:
                self.prevy = self.prevy + round((abs(self.techniquey - self.prevy)/(self.techniquey - self.prevy+0.01)))/8

            if self.techniquey == self.prevy and self.techniquex == self.prevx:
                self.x = self.prevx
                self.y = self.prevy
                self.technique = "move"
                self.techniquefinished = 1
        elif self.technique == "hit":
            #animate the "hit movement"
            self.prevx = self.prevx + round((abs(self.techniquex - self.prevx)/(self.techniquex - self.prevx + 0.01)))/4
            self.prevy = self.prevy + round((abs(self.techniquey - self.prevy)/(self.techniquey - self.prevy + 0.01)))/4


            #if hit is finished, find entity at the target square and deduct hp
            if self.techniqueframe == 4:
                self.prevx = self.x
                self.prevy = self.y
                self.techniquex = self.x - 6
                self.techniquey = self.y - 6
                self.technique = "move"
                self.techniquefinished = 1


        else:
            self.technique = "move"
            self.techniquefinished = 1







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




