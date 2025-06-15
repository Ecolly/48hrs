from game_classes.face_direction import FaceDirection
from game_classes.techniques import*

import pyglet
import math
import button_class

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
        self.technique = Technique.NA
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
    
    def sign(self, x):
        return (x > 0) - (x < 0)  # returns 1, 0, or -1

    def do_AI(self, all_enemies, player, game_map):
        if self.name == "FOX":
            return Technique.MOVE, self.x, self.y+1
        elif self.name == "GOOSE":
            if abs(player.x-self.x) < 2 and abs(player.y-self.y) < 2:
                return Technique.HIT, player.x, player.y
            else:
                new_x = self.x + self.sign(player.x - self.x)
                new_y = self.y + self.sign(player.y - self.y)
                # new_x = self.x + round(abs(player.x - self.x) / ((player.x - self.x) + 0.01))
                # new_y = self.y + round(abs(player.y - self.y) / ((player.y - self.y) + 0.01))
                print(self.x, self.y, new_x, new_y, (new_x, new_y) in game_map.valid_tiles)
                if self.can_move_to(new_x, new_y, game_map):
                    return Technique.MOVE, new_x, new_y    
                else:
                    return Technique.STILL, self.x, self.y 
    
    def can_move_to(self, x, y, game_map):
        #Detect walls
        if (y,x) not in game_map.valid_tiles:
            print(f"Invalid tile cannot move{x, y}")
            return False
        elif any(x== enemy.x and enemy.y for enemy in game_map.all_enemies):
            print("Enemy cannot move")
            return False
        else: 
            return True
    
    


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




    def process_turn(self, all_enemies, player):
        #print("a")
        self.techniqueframe = self.techniqueframe + 1

        if self.technique == Technique.MOVE:
            if self.techniquex != self.prevx:
                self.prevx = self.prevx + round((abs(self.techniquex - self.prevx)/(self.techniquex - self.prevx+0.01)))/8
            if self.techniquey != self.prevy:
                self.prevy = self.prevy + round((abs(self.techniquey - self.prevy)/(self.techniquey - self.prevy+0.01)))/8

            if self.techniquey == self.prevy and self.techniquex == self.prevx:
                self.x = self.prevx
                self.y = self.prevy
                self.technique = Technique.MOVE
                self.techniquefinished = 1
        elif self.technique == Technique.HIT:
            #animate the "hit movement"



            quartic_eq = (-0.19*(0.25*self.techniqueframe)**4 + (0.25*self.techniqueframe)**3 - (0.25*self.techniqueframe)**2)/2.5
            #print(quartic_eq)

            self.prevx = self.x + round((abs(self.techniquex - self.x)/(self.techniquex - self.x + 0.01)))*quartic_eq
            self.prevy = self.y + round((abs(self.techniquey - self.y)/(self.techniquey - self.y + 0.01)))*quartic_eq


            #if hit is finished, find entity at the target square and deduct hp
            if self.techniqueframe == 16:
                
                for enemy in all_enemies:
                    if enemy.x == self.techniquex and enemy.y == self.techniquey:
                        enemy.health = enemy.health - 1
                        #button_class.create_point_number(enemy.x, enemy.y, 1, (255, 0, 0), player)
                        break 
                
                if player.x == self.techniquex and player.y == self.techniquey:
                    player.health = player.health - 1
                    #button_class.create_point_number(player.x, player.y, 1, (255, 0, 0), player)

                self.prevx = self.x
                self.prevy = self.y
                self.techniquex = self.x
                self.techniquey = self.y
                self.technique = Technique.MOVE
                self.techniquefinished = 1



        else:
            #self.technique = Technique.MOVE
            self.techniquefinished = 1







    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def is_alive(self):
        return self.health > 0
    
    #TODO
    def attack(self, player):
        # Implement attack logic here
        pass
    
    def can_see_player(self, player, vision_range=5):
        ex, ey = self.x, self.y
        px, py = player.x, player.y
        # Calculate the distance between the enemy and the player
        # Using Euclidean distance for simplicity
        distance = ((ex - px) ** 2 + (ey - py) ** 2) ** 0.5
        return distance <= vision_range




