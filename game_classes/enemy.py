from game_classes.face_direction import FaceDirection
from game_classes.techniques import*

import pyglet
import math
import button_class
import random

def create_sprite_enemy(image_grid, index):
    tex = pyglet.image.Texture.create(16, 16)
    tex.blit_into(image_grid[index], 0, 0, 0)
    return pyglet.sprite.Sprite(tex, x=0, y=0)


def generate_enemy(name, level, x, y, grid):

    enemy_names = ["DAMIEN", "LEAFALOTTA", "CHLOROSPORE", "GOOSE", "FOX", "S'MORE", "HAMSTER"]
    enemy_hps = [20, 15, 18, 8, 10, 12, 20]
    enemy_sprites = [20*64, 18*64, 17*64, 16*64, 15*64, 14*64, 6*64]
    enemy_animtypes = [1, 1, 1, 1, 2, 1, 1]
    enemy_animmods = [1/8, 1/8, 1/8, 1/8, 1/8, 1/8,1/8]
    enemy_exp = [0, 10, 10, 10, 10, 6, 35, 2]

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
        experience = enemy_exp[id],
    ) 

    return enemy



class Enemy:
    def __init__(self, name, health, level, sprite, spriteindex, spritegrid, color, animtype, animframe, animmod, x, y, experience):
        self.name = name
        self.health = health
        self.maxhealth = health
        self.strength = 10  # Default strength
        self.maxstrength = 10
        self.defense = 5  # Default defense
        self.maxdefense = 5
        self.level = level

        #these are for displaying the stats during combat
        self.health_visual = health
        self.maxhealth_visual = health
        self.level_visual = level


        self.x = x # x coords are in 
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y 
        self.offsetx = 0
        self.offsety = 0
        self.inventory = []
        self.direction = FaceDirection.DOWN  # Default direction
        self.technique = Technique.NA
        self.techniquex = 0
        self.techniquey = 0
        self.techniqueframe = 0
        self.techniquefinished = 0
        self.equipment_weapon = None
        self.equipment_shield = None
        self.should_be_deleted = False
        
        self.sprite = sprite  # pyglet.sprite.Sprite
        self.spriteindex = spriteindex #actual index of sprite on tilegrid
        self.grid = spritegrid
        self.color = color #4 entry tuple for the sprite to be colored as; white is default
        self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        self.animframe = animframe #what frame of the animation it's on
        self.animmod = animmod #a preset animation modifier (e.g. vibration amplitude)
        self.scale = 3
        self.loot = None #drop when dead
        self.experience = experience #Drop when dead
    
    def sign(self, x):
        return (x > 0) - (x < 0)  # returns 1, 0, or -1

    def do_AI(self, all_enemies, player, game_map):

        xtochk = player.x
        ytochk = player.y

        if self.name == "FOX":

            #always run away when sees the player, in sscared mode 
            if self.can_see_player(player=player, vision_range=5):
                dx = self.sign(self.x - xtochk)
                dy = self.sign(self.y - ytochk)
                new_x = self.x + dx
                new_y = self.y + dy
                return Technique.MOVE, self.x, new_y    

            else:
                idle_action = random.choice([Technique.MOVE, Technique.STILL])
                if idle_action == Technique.MOVE:
                    dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                    new_x = self.x + dx
                    new_y = self.y + dy
                    if self.can_move_to(new_x, new_y, game_map):
                        return Technique.MOVE, new_x, new_y
                # If not moving or can't move, stay still
                return Technique.STILL, self.x, self.y
                    
        elif self.name == "GOOSE":
            if abs(xtochk-self.x) < 2 and abs(ytochk-self.y) < 2:
                return Technique.HIT, xtochk, ytochk
            else:
                new_x = self.x + self.sign(xtochk - self.x)
                new_y = self.y + self.sign(ytochk - self.y)
                return Technique.MOVE, new_x, new_y    

                
        elif self.name == "LEAFALOTTA":
            if abs(player.x-self.x) < 2 and abs(player.y-self.y) < 2:
                return Technique.HIT, player.x, player.y
            else:
                new_x = self.x + self.sign(player.x - self.x)
                new_y = self.y + self.sign(player.y - self.y)
                return Technique.MOVE, new_x, new_y    
                
        elif self.name == "CHLOROSPORE":
            if abs(player.x-self.x) < 2 and abs(player.y-self.y) < 2:
                return Technique.HIT, player.x, player.y
            else:
                new_x = self.x + self.sign(player.x - self.x)
                new_y = self.y + self.sign(player.y - self.y)
                return Technique.MOVE, new_x, new_y    

                
        elif self.name == "S'MORE":
            print(self.x, self.y)
            
            #tries to hunt other player + entities down as soon as they spawn on the map
            if abs(xtochk-self.x) < 2 and abs(ytochk-self.y) < 2:
                print("The smore is hitting player")
                return Technique.HIT, xtochk, ytochk
            for enemy in game_map.all_enemies:
                if enemy is not self:
                    if abs(enemy.x-self.x) < 2 and abs(enemy.y-self.y) < 2:
                        print("The smore is hitting others")
                        return Technique.HIT, enemy.x, enemy.y

            #Otherwise check if  can see the player
            if self.can_see_player(player,8):
                return self.movement_to_entity(player, game_map)

            nearest_enemy = None
            min_dist = float('inf')
            for enemy in game_map.all_enemies:
                if enemy is not self:
                    dist = abs(enemy.x - self.x) + abs(enemy.y - self.y)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_enemy = enemy
            if nearest_enemy:
                return self.movement_to_entity(nearest_enemy, game_map)
            #once a player is in certain range, turn targets
        return Technique.STILL, self.x, self.y 
        

    def drop_item(self, game_map):
        item = random.choice(self.loot)
        game_map.floor_items.append(item)
        item.x = self.x
        item.y = self.y    
        self.technique = Technique.STILL 
        #maybe randomize a loot table

    def movement_to_entity(self, target, game_map):
        dx = self.sign(target.x - self.x)
        dy = self.sign(target.y- self.y)
        new_x = self.x + dx
        new_y = self.y + dy
        return Technique.MOVE, new_x, new_y    

    
    def can_move_to(self, x, y, game_map):
        #Detect walls
        if (y,x) not in game_map.valid_tiles:
            #print(f"Invalid tile cannot move{x, y}")
            return False
        else:
            for enemy in game_map.all_enemies:
                if enemy.technique == Technique.MOVE and enemy.techniquefinished == 0 and enemy.techniquex == x and enemy.techniquey == y:#x == enemy.x and y == enemy.y:
                    return False
                elif enemy.x == x and enemy.y == y:
                    return False
            return True


    def draw(self, batch, animation_presets, player, group):
        base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.prevx*16 + 8)*self.scale + self.offsetx*16*self.scale
        base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.prevy*16 + 8)*self.scale + self.offsety*16*self.scale



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

        sprite.group = group
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        sprite.color = self.color
        sprite.batch = batch
        sprite.z = 40




    def process_turn(self, all_enemies, player, all_buttons, game_map):
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
                        damage = 0
                        if self.equipment_weapon != None:
                            damage += self.equipment_weapon.damage
                        damage += self.strength
                        if enemy.equipment_shield != None:
                            damage -= enemy.equipment_shield.defense
                        damage -= enemy.defense
                        if damage < 1:
                            damage = 1
                        enemy.health = enemy.health - damage
                        if enemy.is_alive() is False:
                            enemy.should_be_deleted = True
                            self.level_up()

                        button_class.create_point_number(enemy.x, enemy.y, "-" + str(damage), (255, 0, 0, 255), player, all_buttons)
                        break 
                
                if player.x == self.techniquex and player.y == self.techniquey:
                    damage = 0
                    if self.equipment_weapon != None:
                        damage += self.equipment_weapon.damage
                    damage += self.strength
                    if player.equipment_shield != None:
                        damage -= player.equipment_shield.defense
                    damage -= player.defense
                    if damage < 1:
                        damage = 1
                    player.health = player.health - damage
                    if player.is_alive() is False:
                        print("gg loser you lost")


                    
                    
                    button_class.create_point_number(player.x, player.y, "-" + str(damage), (255, 0, 0, 255), player, all_buttons)

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
    
    def level_scale(self): #depending what level they are their stats will change
        level = self.level
        self.maxhealth = level*self.maxhealth
        self.defense = level*self.defense
        self.strength = level*self.strength
    
    def level_up(self):
        #more can be added later
        self.level += 1
        if self.name == "S'MORE":
            self.maxhealth += 5  # You can scale this however you want
            self.health = self.maxhealth  # Heal to full on level up
            self.strength += 2
            self.defense += 1
    
    
    def can_see_player(self, player, vision_range=5):
        ex, ey = self.x, self.y
        px, py = player.x, player.y
        distance = ((ex - px) ** 2 + (ey - py) ** 2) ** 0.5
        return distance <= vision_range




