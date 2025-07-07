from game_classes.face_direction import FaceDirection
from game_classes.techniques import*

import pyglet
import math
import button_class
import random
from game_classes.projectiles import *
from font import *
from game_classes.item import *
from game_classes.id_shuffling import *
#from animations import *

def enemy_grid_to_use(level):
    global grid_entities1 
    global grid_entities2
    global grid_entities3
    global grid_entities4
    if level < 2:
        return grid_entities1
    elif level == 2:
        return grid_entities2
    elif level == 3:
        return grid_entities3
    else:
        return grid_entities4

def check_if_entity_is_on_screen(entity, player, result1, result2):
    if entity == None:
        return result1
    
    if ((entity.x > player.x + 13 or entity.x < player.x - 13) or (entity.y > player.y + 9 or entity.y < player.y - 9)):
        return result1
    else:
        return result2
    
def refresh_all_visuals(entity):
    entity.prevx = entity.x
    entity.prevy = entity.y
    entity.offsetx = 0
    entity.offsety = 0
    entity.initx = entity.x
    entity.inity = entity.y
    entity.health_visual = entity.health
    entity.maxhealth_visual = entity.maxhealth
    if isinstance(entity, Enemy) == False:
        entity.experience_visual = entity.experience
        entity.strength_visual = entity.strength
        entity.defense_visual = entity.defense
    entity.level_visual = entity.level
    entity.paralysis_visual = entity.paralysis_turns
    entity.speed_visual = entity.speed



def create_sprite_enemy(image_grid, index):
    #tex = pyglet.image.Texture.create(16, 16)
    #tex.blit_into(image_grid[index], 0, 0, 0)
    return pyglet.sprite.Sprite(image_grid[index], x=0, y=0)


def generate_enemy(name, level, x, y, grid, floor, player):

    if (name in player.enemies_remaining) == False and name != "HAMSTER" and name != "DEBT COLLECTOR" and name != "EXECUTIVE":
        return False

    global grid_items
    enemy_names = ["DAMIEN", "LEAFALOTTA", "CHLOROSPORE", "GOOSE", "FOX", "S'MORE", "HAMSTER", "DRAGON", "CHROME DOME", "TETRAHEDRON", "SCORPION", "TURTLE", "CULTIST", "JUJUBE", "DEMON CORE", "DEBT COLLECTOR", "VITRIOLIVE", "EXECUTIVE", "DODECAHEDRON", "MONITAUR"]
    enemy_hps = [20, 9, 5, 8, 9, 12, 20, 30, 18, 10, 12, 6, 12, 24, 23, 100, 20, 20, 50, 25]
    enemy_strength = [0, 8, 5, 9, 8, 12, 9, 18, 17, 15, 12, 1, 1, 1, 1, 70, 10, 5, 8, 8]
    enemy_defense = [0, 2, 2, 1, 2, 1, 1, 4, 8, 3, 6, 30, 2, 1, 4, 70, 2, 1, 10, 3]
    enemy_sprites = [23*64, 21*64, 20*64, 19*64, 18*64, 17*64, 9*64, 11*64, 6*64, 12*64, 15*64, 10*64, 2*64, 5*64, 8*64, 1*64, 14*64, 0, 13*64, 16*64]
    enemy_animtypes = [1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1]
    enemy_animmods = [1/16, 1/16, 1/16, 1/16, 1/16, 1/16, 1/16, 1/16, 1/16, 1/8, 1/8, 1/16, 1/16, 1/16, 1/16, 1/16, 1/16, 1/16, 1/8, 1/16]
    enemy_exp = [0, 6, 7, 7, 10, 30, 1, 100, 60, 60, 30, 2, 60, 4, 40, 1, 45, 1, 90, 45]
    enemy_speeds = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4, 2, 1, 2, 2, 1, 4, 2, 2, 2, 2] #1 - slow, 2 - default speed, 4 - fast (this should eventually be per-level)
    if level == 1:
        enemy_drops = [None, "Leaves", "Mushrooms", "Poultry", None, "Candy", "Apple", "15 Gold", "Rapier", None, None, None, "Staff of Mana", "Candy", None, "60 Gold", "Leaves", None, None]
    elif level == 2:
        enemy_drops = [None, "Lettuce", "Mushrooms", "Poultry", None, "Candy", "Apple", "15 Gold", "Rapier", None, None, None, "Staff of Mana", "Candy", None, "60 Gold", "Lettuce", None, None]
    elif level == 3:
        enemy_drops = [None, "Kale", "Mushrooms", "Poultry", None, "Candy", "Apple", "60 Gold", "Rapier", None, None, None, "Staff of Mana", "Candy", None, "60 Gold", "Kale", None, None]
    else:
        enemy_drops = [None, "Kale", "Mushrooms", "Poultry", None, "Candy", "Apple", "60 Gold", "Rapier", None, None, None, "Staff of Mana", "Candy", None, "60 Gold", "Kale", None, None]
    
    
    enemy_drop_odds = [0, 0.5, 0.5, 0.5, 0, 0.25, 0.1, 0.2, 1, 0, 0, 0, 0.2, 0.2, 0, 1, 0.1, 0, 0, 0]
    enemy_type = ["Human", "Plant", "Plant", None, None, "Food", None, None, "Robotic", "Abstract", None, None, "Abstract", "Food", "Robotic", "Human", "Food", "Human", "Abstract", "Robotic"]
    id = enemy_names.index(name)


    enemy = Enemy(
        name = name,
        health = enemy_hps[id],
        strength = enemy_strength[id],
        defense = enemy_defense[id],
        level = level,
        #sprite = create_sprite_enemy(grid, enemy_sprites[id]), #this SUCKS
        spriteindex = enemy_sprites[id],
        color = (255, 255, 255, 255),
        animtype = enemy_animtypes[id],
        animmod = enemy_animmods[id],
        animframe = 0,
        x = x,
        y = y,
        experience = enemy_exp[id]*(level)*(level),
        speed = enemy_speeds[id],
        type = enemy_type[id]
    ) 

    if random.uniform(0, 1) < enemy_drop_odds[id]:
        enemy.current_holding = floor.create_item(enemy_drops[id], grid_items)  
    elif random.uniform(0, 1) < 0.33:
        enemy.current_holding = floor.create_item("3 Gold", grid_items)
    elif random.uniform(0, 1) < 0.02:
        enemy.current_holding = floor.create_item("15 Gold", grid_items)
    elif random.uniform(0, 1) < 0.005:
        enemy.current_holding = floor.create_item("60 Gold", grid_items)

    return enemy



class Enemy:
    def __init__(self, name, health, strength, defense, level, spriteindex, color, animtype, animframe, animmod, x, y, experience, speed, type):
        global batch#, batch, batch, batch, batch
        global group_enemies
        global grid_items

        if level < 2:
            self.grid =  grid_entities1
        elif level == 2:
            self.grid =  grid_entities2
        elif level == 3:
            self.grid =  grid_entities3
        else:
            self.grid =  grid_entities4
        
        self.name = name
        self.health = health*level
        self.maxhealth = health*level
        self.level = level

        #these are for displaying the stats during combat
        self.health_visual = health*level
        self.maxhealth_visual = health*level
        self.level_visual = level
  # Default strength
        self.strength = strength*level
        self.maxstrength = strength*level
        self.strength_visual = strength*level
        self.maxstrength_visual = strength*level

        self.defense = defense*level  # Default defense
        self.maxdefense = defense*level
        self.defense_visual = defense*level
        self.maxdefense_visual = defense*level

        #these stats are the base stats that are used to scale stats when increasing a level
        self.basehealth = health
        self.basestrength = strength
        self.basedefense = defense
        self.has_been_resurrected = 0
        self.is_inked = False



        self.creaturetype = type
        self.x = x # x coords are in 
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y 
        self.offsetx = 0
        self.offsety = 0
        self.initx = x
        self.inity = y
        self.inventory = []
        self.active_projectiles = []
        self.direction = FaceDirection.DOWN  # Default direction
        self.technique = Technique.NA
        self.techniquex = 0
        self.techniquey = 0
        self.techniqueframe = 0
        self.techniquefinished = 0
        self.techniquecharges = 0
        self.techniqueitem = None
        self.equipment_weapon = None
        self.equipment_shield = None
        self.should_be_deleted = False
        
        self.current_holding = None
        self.has_been_hit = False #for enemies that only hit if you retaliate
        

        self.sprite_weapon = image_handling.create_sprite(grid_items, 0)

        #self.sprite_shield = image_handling.create_sprite(itemgrid, 0)
        self.sprite_weapon.color = (0, 0, 0, 0)
        #self.sprite_shield.color = (0, 0, 0, 0)
        self.itemgrid = grid_items
        self.sprite_weapon.batch = batch



        self.spriteindex_prev = -1
        self.spriteindex = spriteindex #actual index of sprite on tilegrid

        self.sprite = create_sprite_enemy(self.grid, self.spriteindex)  # Create the sprite from the grid

        # self.spriteset = []

        # i = 0
        # while i < 64:
        #     self.spriteset.append(self.grid[self.spriteindex + i].get_texture())
        #     i = i + 1

        self.sprite.group = group_enemies

        # if level == 1:
        #     self.sprite.batch = batch
        # elif level == 2:
        #     self.sprite.batch = batch
        # elif level == 3:
        #     self.sprite.batch = batch
        # elif level == 4:
        self.sprite.batch = batch

        self.color = color #4 entry tuple for the sprite to be colored as; white is default
        self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        self.animframe = animframe #what frame of the animation it's on
        self.animmod = animmod #a preset animation modifier (e.g. vibration amplitude)
        self.scale = 3
        self.loot = None #drop when dead
        self.experience = experience #Drop when dead

        self.speed = speed
        self.default_speed = speed
        self.turns_left_before_moving = speed
        self.speed_turns = 0
        self.speed_visual = speed

        self.paralysis_turns = 0
        self.paralysis_visual = 0

        self.flee_ai_turns = 0
        self.rage_ai_turns = 0

        self.invisible_frames = 0
        #self.translucent_frames = 0

    def sign(self, x):
        return (x > 0) - (x < 0)  # returns 1, 0, or -1



    def technique_filter_for_sanctuaries(self, technique, x, y, floor):
        try:
            if floor.map_grid[floor.height-1-y][x] == "S":
                return Technique.STILL, x, y
            else:
                return technique, x, y
        except:
            return Technique.STILL, x, y

    def do_AI(self, all_enemies, player, game_map):
        global grid_items
        if self.paralysis_turns > 0:
            return Technique.STILL, self.x, self.y
        xtochk = player.x
        ytochk = player.y
        if self.name == "HAMSTER" or self.name == "TURTLE" or self.name == "EXECUTIVE" or self.flee_ai_turns > 0:
            #always run away when sees the player, in sscared mode 
            if self.can_see_player(player=player, vision_range=5):
                dx = self.sign(self.x - xtochk)
                dy = self.sign(self.y - ytochk)
                new_x = self.x + dx
                new_y = self.y + dy
                return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)    
            else:
                idle_action = random.choice([Technique.MOVE, Technique.STILL])
                if idle_action == Technique.MOVE:
                    dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                    new_x = self.x + dx
                    new_y = self.y + dy
                    if self.can_move_to(new_x, new_y, game_map):
                        return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)
                # If not moving or can't move, stay still
                return Technique.STILL, self.x, self.y
                    
        elif self.rage_ai_turns > 0 or self.name == "JUJUBE" or self.name == "DODECAHEDRON" or self.name == "MONITAUR" or self.name == "LEAFALOTTA" or self.name == "FOX" or self.name == "GOOSE" or self.name == "TETRAHEDRON" or self.name == "SCORPION":
            if abs(xtochk-self.x) < 2 and abs(ytochk-self.y) < 2:
                return self.technique_filter_for_sanctuaries(Technique.HIT, xtochk, ytochk, game_map)    
            else:
                new_x = self.x + self.sign(xtochk - self.x)
                new_y = self.y + self.sign(ytochk - self.y)
                return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)    



        elif self.name == "DEBT COLLECTOR":
            if player.gold < 0 or game_map.level < 1:
                if abs(xtochk-self.x) < 2 and abs(ytochk-self.y) < 2:
                    
                    return Technique.HIT, xtochk, ytochk
                else:
                    new_x = self.x + self.sign(xtochk - self.x)
                    new_y = self.y + self.sign(ytochk - self.y)
                    return Technique.MOVE, new_x, new_y
            else:
                dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                new_x = self.x + dx
                new_y = self.y + dy
                if self.can_move_to(new_x, new_y, game_map):
                    return Technique.MOVE, new_x, new_y
        elif self.name == "DEMON CORE" or self.name == "VITRIOLIVE":
            #distance to approximate:
            dist_target = 3
            current_dist = math.floor(math.sqrt((self.x - player.x)**2 + (self.y - player.y)**2))

            if current_dist < dist_target:
                new_x = self.x + self.sign(-player.x + self.x)
                new_y = self.y + self.sign(-player.y + self.y)
            elif current_dist > dist_target:
                new_x = self.x + self.sign(player.x - self.x)
                new_y = self.y + self.sign(player.y - self.y)
            else:
                dx, dy = random.choice([(1,0), (-1,0), (0,1), (0,-1)])
                new_x = self.x + dx
                new_y = self.y + dy
            return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)    
        

        elif self.name == "CHLOROSPORE":
            if abs(player.x-self.x) < 2 and abs(player.y-self.y) < 2:
                return self.technique_filter_for_sanctuaries(Technique.HIT, player.x, player.y, game_map)   
            elif abs(player.x-self.x) < 5 and abs(player.y-self.y) < 5 and random.randint(0, 1) == 1:
                if self.level == 2:
                    self.active_projectiles.append(Projectile("Spores 2", 0, self.x, self.y, player.x, player.y, self, self.name + " exhaled spores."))
                elif self.level == 3:
                    self.active_projectiles.append(Projectile("Spores 3", 0, self.x, self.y, player.x, player.y, self, self.name + " exhaled spores."))
                elif self.level == 4:
                    self.active_projectiles.append(Projectile("Spores 4", 0, self.x, self.y, player.x, player.y, self, self.name + " exhaled spores."))
                else:
                    self.active_projectiles.append(Projectile("Spores", 0, self.x, self.y, player.x, player.y, self, self.name + " exhaled spores."))
                return Technique.THROW, player.x, player.y 
            else:
                new_x = self.x + self.sign(player.x - self.x)
                new_y = self.y + self.sign(player.y - self.y)
                return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)      

        elif self.name == "DRAGON":
            if abs(player.x-self.x) < 2 and abs(player.y-self.y) < 2:
                return self.technique_filter_for_sanctuaries(Technique.HIT, player.x, player.y, game_map)   
            elif abs(player.x-self.x) < 8 and abs(player.y-self.y) < 8 and random.randint(0, 4) == 1:
                if self.level == 2:
                    self.active_projectiles.append(Projectile("Dragon Fire 2", 10*self.level, self.x, self.y, player.x, player.y, self, self.name + " breathed fire."))
                elif self.level == 3:
                    self.active_projectiles.append(Projectile("Dragon Fire 3", 10*self.level, self.x, self.y, player.x, player.y, self, self.name + " breathed fire."))
                elif self.level == 4:
                    self.active_projectiles.append(Projectile("Dragon Fire 4", 10*self.level, self.x, self.y, player.x, player.y, self, self.name + " breathed fire."))
                else:
                    self.active_projectiles.append(Projectile("Dragon Fire", 10*self.level, self.x, self.y, player.x, player.y, self, self.name + " breathed fire."))

                
                return Technique.THROW, player.x, player.y
            else:
                new_x = self.x + self.sign(player.x - self.x)
                new_y = self.y + self.sign(player.y - self.y)
                return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)     
        elif self.name == "CHROME DOME":
            if (self.current_holding.name == "Rapier" and abs(xtochk-self.x) < 3 and abs(ytochk-self.y) < 3):
                self.techniqueitem = game_map.create_item("Rapier", grid_items)
                return self.technique_filter_for_sanctuaries(Technique.HIT, xtochk, ytochk, game_map)
            elif (abs(xtochk-self.x) < 3 and abs(ytochk-self.y) < 3):
                return self.technique_filter_for_sanctuaries(Technique.HIT, xtochk, ytochk, game_map)
            else:
                new_x = self.x + self.sign(xtochk - self.x)
                new_y = self.y + self.sign(ytochk - self.y)
                return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)    
        elif self.name == "CULTIST":

            if abs(player.x-self.x) < 2 and abs(player.y-self.y) < 2:
                if random.randint(0, 3) != 1 or self.defense < 0:
                    if self.is_inked == True:
                        self.techniqueitem = game_map.create_item("Staff of Mana", grid_items) #suboptimal, this item is only being generated so the enemy looks like its holding something
                        name_desc = get_display_name(self.techniqueitem)
                        self.active_projectiles.append(Projectile("Staff of Mana", 2, self.x, self.y, player.x, player.y, self, str(self.name)+" swung the " + name_desc + "!"))
                        self.techniquecharges = 2*self.level
                        return Technique.THROW, player.x, player.y
                    
                    else:
                        if self.level == 1:
                            self.techniqueitem = game_map.create_item("Summoning Tome", grid_items)
                        else:
                            if player.extinction_state == 1 and self.level > 2 and random.randint(0, 2) == 1:
                                self.techniqueitem = game_map.create_item("Tome of Resurrection", grid_items)
                            elif self.health > self.maxhealth/2 or random.randint(0, 2) == 1 or self.defense < 0:
                                self.techniqueitem = game_map.create_item("Summoning Tome", grid_items)
                            elif self.level == 2 or self.level == 3:
                                self.techniqueitem = game_map.create_item("Tome of Promotion", grid_items)
                            else:
                                self.techniqueitem = game_map.create_item("Paperskin Tome", grid_items)
                        return Technique.CAST, 0, 0
                else:
                    self.techniqueitem = game_map.create_item("Staff of Mana", grid_items) #suboptimal, this item is only being generated so the enemy looks like its holding something
                    name_desc = get_display_name(self.techniqueitem)
                    self.active_projectiles.append(Projectile("Staff of Mana", 2, self.x, self.y, player.x, player.y, self, str(self.name)+" swung the " + name_desc + "!"))
                    self.techniquecharges = 2*self.level
                    return Technique.THROW, player.x, player.y
            elif abs(player.x-self.x) < 6 and abs(player.y-self.y) < 6 and random.randint(0, 3) == 1:
                if self.level == 1:
                    self.techniqueitem = game_map.create_item("Staff of Swapping", grid_items)
                    name_desc = get_display_name(self.techniqueitem)
                    self.active_projectiles.append(Projectile("Staff of Swapping", 2, self.x, self.y, player.x, player.y, self, str(self.name)+" swung the " + name_desc + "!"))
                else:
                    if random.randint(0, 3) == 1:
                        self.techniqueitem = game_map.create_item("Staff of Lethargy", grid_items)
                        name_desc = get_display_name(self.techniqueitem)
                        self.active_projectiles.append(Projectile("Staff of Lethargy", 2, self.x, self.y, player.x, player.y, self, str(self.name)+" swung the " + name_desc + "!"))
                    else:
                        self.techniqueitem = game_map.create_item("Staff of Division", grid_items)
                        name_desc = get_display_name(self.techniqueitem)
                        self.active_projectiles.append(Projectile("Staff of Division", 2, self.x, self.y, player.x, player.y, self, str(self.name)+" swung the " + name_desc + "!"))
                self.techniquecharges = 2
                return Technique.THROW, player.x, player.y
            else:
                new_x = self.x + self.sign(player.x - self.x)
                new_y = self.y + self.sign(player.y - self.y)
                return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map)   
            



        elif self.name == "S'MORE":
            print(self.x, self.y)
            

            #tries to hunt other player + entities down as soon as they spawn on the map
            if abs(xtochk-self.x) < 2 and abs(ytochk-self.y) < 2:
                print("The smore is hitting player")
                return self.technique_filter_for_sanctuaries(Technique.HIT, xtochk, ytochk, game_map)
            elif self.can_see_player(player,8):
                return self.movement_to_entity(player, game_map)
            for enemy in game_map.all_enemies:
                if enemy is not self and enemy.should_be_deleted == False:
                    if abs(enemy.x-self.x) < 2 and abs(enemy.y-self.y) < 2:
                        print("The smore is hitting others")
                        return self.technique_filter_for_sanctuaries(Technique.HIT, enemy.x, enemy.y, game_map)

            #Otherwise check if  can see the player
            
            nearest_enemy = None
            min_dist = float('inf')
            for enemy in game_map.all_enemies:
                if enemy is not self and enemy.should_be_deleted == False:
                    dist = abs(enemy.x - self.x) + abs(enemy.y - self.y)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_enemy = enemy
            if nearest_enemy:
                return self.movement_to_entity(nearest_enemy, game_map)
            #once a player is in certain range, turn targets
        return Technique.STILL, self.x, self.y 
        

    # def drop_item(self, game_map):
    #     item = random.choice(self.loot)
    #     game_map.floor_items.append(item)
    #     item.x = self.x
    #     item.y = self.y    
    #     self.technique = Technique.STILL 
        #maybe randomize a loot table


    # returns True if the item is detected at x and y location
    def detect_item(self, item_list, x, y):
        for i in item_list:
            print(f"Checking item {i.name} at ({i.x}, {i.y}) against ({x}, {y})")
            if i.x == x and i.y == y:
                print(f"Detected item: {i.name} at ({i.x}, {i.y})")
                return True
        return False
    

    def drop_item(self, item, floor):
        #What is happening good lord
        if item is None:
            return
        #self.technique = Technique.STILL 
        coords_to_check = [[0, 0], [1, 1], [0, 1], [0, -1], [1, 0], [-1, 0], [1, -1], [-1, 1], [-1, -1]]
        for coords in coords_to_check:
            x = self.x + coords[0]
            y = self.y + coords[1]
            if self.detect_item(floor.floor_items, x, y) == False and (y,x) in floor.valid_tiles:
                if item is not None:
                    item.x = self.x + coords[0]
                    item.y = self.y + coords[1]
                    #self.del_item_from_inventory(item) # Remove item from inventory
                    floor.floor_items.append(item)
                    
                    break
                 # Exit after dropping the item in the first available spot
            #self.technique = Technique.STILL 


    def movement_to_entity(self, target, game_map):
        dx = self.sign(target.x - self.x)
        dy = self.sign(target.y- self.y)
        new_x = self.x + dx
        new_y = self.y + dy
        return self.technique_filter_for_sanctuaries(Technique.MOVE, new_x, new_y, game_map) 

    
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


    def draw(self, animation_presets, player, group, group_bg, group_fg, list_of_animations, floor):
        sprite = self.sprite
        self.grid = enemy_grid_to_use(self.level_visual)
        if self.paralysis_visual > 0:
            frame_index = self.direction.value * 8
            paralyze_x = (1 - 2*((self.animframe*4) % 2))/2
        else:
            frame_index = self.direction.value * 8 + animation_presets[self.animtype][math.floor(self.animframe)]
            paralyze_x = 0

        base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.prevx*16 + 8)*self.scale + (self.offsetx*16 + paralyze_x)*self.scale
        base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.prevy*16 + 8)*self.scale + self.offsety*16*self.scale

        if frame_index != self.spriteindex_prev:
            self.sprite.image = self.grid[self.spriteindex + frame_index]

            #sprite.image.blit_into(self.grid[self.spriteindex + frame_index], 0, 0, 0)
            
            self.spriteindex_prev = frame_index


        # if random.randint(0, 8) == 1: 
        #     item = floor.liquid_grid[floor.height-1-self.y][self.x]
        #     #if splashing a flask...
        #     if item == "W":
        #         spr = 2*29 + 16
        #     elif item == "D":
        #         spr = 2*29 + 12
        #     elif item == "A":
        #         spr = 2*29 
        #     elif item == "M":
        #         spr = 2*29 + 24
        #     elif item == "S":
        #         spr = 2*29 + 4
        #     elif item == "C":
        #         spr = 2*29 + 8
        #     elif item == "P":
        #         spr = 2*29 + 20
        #     elif item == "I":
        #         spr = 2*29 + 20
            
        #     if ((self.x > player.x + 13 or self.x < player.x - 13) or (self.y > player.y + 9 or self.y < player.y - 9)) or item == "#":
        #         pass
        #     else:
        #         list_of_animations.append(animations.Animation("", spr, 9, 5, (255, 255, 255, 0), 0, 8, self.x, self.y, sel.x, self.y, item, None, None, None, None, 0, None))


        self.sprite_weapon.scale = self.scale

        self.animframe = self.animframe + self.animmod*self.speed_visual
        if self.animframe >= len(animation_presets[self.animtype]):
            self.animframe = 0

        #sprite.group = group
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        sprite.color = self.color
        if self.invisible_frames > 0:
            sprite.color = (0, 0, 0, 0)
            self.sprite_weapon.color = (0, 0, 0, 0)
        else:
            if self.techniqueitem != None:
                if self.sprite_weapon.color != (255, 255, 255, 255):
                    self.sprite_weapon.image = self.itemgrid[self.techniqueitem.spriteindex]
                    self.sprite_weapon.color = (255, 255, 255, 255)
                    self.sprite_weapon.batch = batch

                if isinstance(self.techniqueitem, Weapon):
                    self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "weapon", "right")
                else:
                    self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "staff", "right")
            elif self.current_holding != None and isinstance(self.current_holding, Consumable) == False and ("Gold" in self.current_holding.name) == False :
                if self.sprite_weapon.color != (255, 255, 255, 255):
                    self.sprite_weapon.image = self.itemgrid[self.current_holding.spriteindex]
                    self.sprite_weapon.color = (255, 255, 255, 255)
                    self.sprite_weapon.batch = batch

                if isinstance(self.current_holding, Weapon):
                    self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "weapon", "right")
                else:
                    self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "staff", "right")
                
                #self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, self.current_holding_type, "right")
            else:
                if self.sprite_weapon.color != (0, 0, 0, 0):
                    self.sprite_weapon.color = (0, 0, 0, 0)
                    self.sprite_weapon.batch = None
        self.invisible_frames += -1

        if check_if_entity_is_on_screen(self, player, False, True) == False:
            sprite.batch = None 
        elif sprite.batch != batch:
            sprite.batch = batch
        #sprite.z = 40






    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def is_alive(self):
        return self.health > 0
    
    def level_scale(self): #depending what level they are their stats will change
        level = self.level
        self.maxhealth = level*self.maxhealth
        self.defense = level*self.defense
        self.strength = level*self.strength
    

    #str, hp, def need to be scaled
    def level_up(self):
        self.level += 1
        if self.level > 4:
            self.level = 4
        self.health = self.basehealth*self.level
        self.maxhealth = self.basehealth*self.level
        self.strength = self.basestrength*self.level  # Default strength
        self.maxstrength = self.basestrength*self.level
        self.defense = self.basedefense*self.level  # Default defense
        self.maxdefense = self.basedefense*self.level

        

    #str, hp, def need to be scaled
    def level_down(self):
        self.level -= 1
        if self.level < 1:
            self.level = 1
        self.health = self.basehealth*self.level
        self.maxhealth = self.basehealth*self.level
        self.strength = self.basestrength*self.level  # Default strength
        self.maxstrength = self.basestrength*self.level
        self.defense = self.basedefense*self.level  # Default defense
        self.maxdefense = self.basedefense*self.level
    
    
    def can_see_player(self, player, vision_range=5):
        ex, ey = self.x, self.y
        px, py = player.x, player.y
        distance = ((ex - px) ** 2 + (ey - py) ** 2) ** 0.5
        return distance <= vision_range
    
    #duplicate of the player's version
    def get_helditem_coordanites(self, base_x, base_y, frame_index, group_bg, group_fg, type, hand):
        coordlist = [[4, 4, 13, 4], [5, 4, 14, 4], [5, 4, 14, 5], [3, 4, 12, 4], [3, 5, 12, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
        [5, 4, 12, 4], [4, 4, 13, 4], [4, 4, 14, 4], [8, 4, 11, 4], [8, 4, 10, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
        [8, 3, 8, 3], [7, 4, 9, 4], [6, 3, 11, 3], [9, 4, 7, 4], [11, 4, 6, 3], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
        [12, 4, 5, 4], [13, 4, 4, 4], [14, 4, 4, 4], [11, 4, 8, 4], [10, 4, 8, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
        [13, 4, 4, 4], [14, 4, 3, 4], [15, 5, 3, 4], [14, 4, 3, 4], [14, 4, 2, 5], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
        [12, 4, 5, 4], [13, 4, 4, 4], [14, 4, 4, 4], [11, 4, 8, 4], [10, 4, 8, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
        [9, 3, 9, 3], [8, 4, 10, 4], [7, 3, 12, 3], [10, 4, 8, 4], [12, 3, 6, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
        [5, 4, 12, 4], [4, 4, 13, 4], [4, 4, 14, 4], [8, 4, 11, 4], [8, 4, 10, 4], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

        
        coords_on_player = coordlist[frame_index]

        if type == "weapon":
            item_coords = [5, 5, 12, 5]
        elif type == "shield":
            item_coords = [8, 7, 8, 7]
        else: #staff coords:
            item_coords = [6, 4, 11, 4]

        if hand == "right":
            if self.direction == FaceDirection.DOWN:
                scale = -1
                group = group_fg
            elif self.direction == FaceDirection.DOWN_RIGHT:
                scale = 1
                group = group_fg
            elif self.direction == FaceDirection.RIGHT:
                scale = 1
                group = group_fg
            elif self.direction == FaceDirection.UP_RIGHT:
                scale = 1
                group = group_fg
            elif self.direction == FaceDirection.UP:
                scale = 1
                group = group_bg
            elif self.direction == FaceDirection.UP_LEFT:
                scale = -1
                group = group_bg
            elif self.direction == FaceDirection.LEFT:
                scale = -1
                group = group_bg
            else: #down left
                scale = -1
                group = group_bg
            if scale == 1:
                coords = [-item_coords[0] + coords_on_player[0], -item_coords[1] + coords_on_player[1]]
            else:
                coords = [-item_coords[2] + coords_on_player[0] + 16, -item_coords[3] + coords_on_player[1]]
        else:
            if self.direction == FaceDirection.DOWN:
                scale = 1
                group = group_fg
            elif self.direction == FaceDirection.DOWN_RIGHT:
                scale = 1
                group = group_bg
            elif self.direction == FaceDirection.RIGHT:
                scale = 1
                group = group_bg
            elif self.direction == FaceDirection.UP_RIGHT:
                scale = -1
                group = group_bg
            elif self.direction == FaceDirection.UP:
                scale = -1
                group = group_bg
            elif self.direction == FaceDirection.UP_LEFT:
                scale = -1
                group = group_fg
            elif self.direction == FaceDirection.LEFT:
                scale = -1
                group = group_fg
            else: #down left
                scale = 1
                group = group_fg
            if scale == 1:
                coords = [-item_coords[0] + coords_on_player[2], -item_coords[1] + coords_on_player[3]]
            else:
                coords = [-item_coords[2] + coords_on_player[2] + 16, -item_coords[3] + coords_on_player[3]]






        return base_x + coords[0]*self.scale, base_y + coords[1]*self.scale, scale, group




