from game_classes.face_direction import *
from game_classes.techniques import*
import pyglet
import math
from game_classes.map import Map
import button_class
import random
from game_classes.item import *
from game_classes.projectiles import *
import animations
import turn_logic
import image_handling
from font import *

class Player:
    def __init__(self, name, health, level, experience, sprite, spriteindex, spritegrid, itemgrid, color, animtype, x, y):
        global batch 
        global group_enemies
        self.name = name
        self.health = health
        self.maxhealth = health
        self.level = level
        self.experience = experience
        self.equipment_weapon = None
        self.equipment_shield = None

        #these are for displaying the stats during combat
        self.health_visual = health
        self.maxhealth_visual = health
        self.experience_visual = experience
        self.level_visual = level

        self.x = x # x coords are in 
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y 
        self.offsetx = 0
        self.offsety = 0
        self.inventory = [None]*40
        self.active_projectiles = []
        #self.active_spells = []
        self.direction = FaceDirection.DOWN  # Default direction
        self.technique = Technique.NA
        self.techniquex = 0
        self.techniquey = 0
        self.techniqueitem = None #used if technique uses an item and the object is needed (e.g. throwing)
        self.techniqueframe = 0
        self.techniquefinished = 0
        self.techniquecharges = 0
        self.should_be_deleted = False #unused; do not delete player ever
        self.current_holding = False
        self.strength = 5  # Default strength
        self.maxstrength = 5
        self.strength_visual = 5
        self.maxstrength_visual = 5

        self.defense = 5  # Default defense
        self.maxdefense = 5
        self.defense_visual = 5
        self.maxdefense_visual = 5
        
        self.sprite = sprite  # pyglet.sprite.Sprite
        self.spriteindex = spriteindex #actual index of sprite on tilegrid
        self.spriteindex_prev = -1
        self.grid = spritegrid

        self.sprite_weapon = image_handling.create_sprite(itemgrid, 0)
        self.sprite_shield = image_handling.create_sprite(itemgrid, 0)
        self.sprite_weapon.color = (0, 0, 0, 0)
        self.sprite_shield.color = (0, 0, 0, 0)
        self.itemgrid = itemgrid

        self.sprite_weapon.batch = batch 
        self.sprite_shield.batch = batch
        self.sprite.batch = batch
        self.sprite.group = group_enemies

        self.color = color #4 entry tuple for the sprite to be colored as; white is default
        self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        self.animframe = 0 #what frame of the animation it's on
        self.animmod = 1/16 #a preset animation modifier (e.g. vibration amplitude)
        self.scale = 3

        self.default_speed = 2
        self.speed = 2
        self.turns_left_before_moving = 2
        self.speed_turns = 0
        self.speed_visual = 2
        
        self.paralysis_turns = 0
        self.paralysis_visual = 0
    
    def add_to_inventory(self, item):
        for slot in range(len(self.inventory)):
            print(f"Checking slot {slot} for item {item.name}")
            if self.inventory[slot] is None:
                self.inventory[slot] = item
                return True  # Success
        print("Inventory full. Cannot pick up item.")
        return False  # Inventory was full

    def increase_experience(self, incoming_experience):
        self.experience +=incoming_experience
        new_level = int(self.experience**(1/3))

        while new_level>self.level:
            self.level_up()
            new_level = int (self.experience**(1/3))
    
    def level_up(self):
        self.level+=1
        
        self.maxhealth += 4
        self.health += 4

        self.strength += 1
        self.maxstrength += 1
        

    

    def equip_weapon(self, weapon):
        """Equip a weapon to the player."""
        if weapon in self.inventory:
            self.equipment_weapon = weapon
            #self.strength += weapon.damage  # Increase strength by weapon's damage

    def equip_shield(self, shield):
        """Equip a shield to the player."""
        if shield in self.inventory:
            self.equipment_shield = shield
            #self.defense += shield.defense  # Increase defense by shield's defense
            
    def unequip_weapon(self):
        """Unequip the currently equipped weapon."""
        if self.equipment_weapon != None:
            self.equipment_weapon = None
    
    def unequip_shield(self):
        """Unequip the currently equipped weapon."""
        if self.equipment_shield != None:
            self.equipment_shield = None

    
    def can_move_to(self, x, y, game_map):
        #Detect walls
        if (y,x) not in game_map.valid_tiles:
            print(f"Invalid tile cannot move{x, y}")
            return False
        else:
            for enemy in game_map.all_enemies:
                if enemy.technique == Technique.MOVE and enemy.techniquefinished == 0 and enemy.techniquex == x and enemy.techniquey == y:#x == enemy.x and y == enemy.y:
                    return False
                elif enemy.x == x and enemy.y == y:
                    return False
            return True
        
    
        
    def move(self, dx, dy, game_map): #Move relative to current position
        self.technique = Technique.MOVE
        self.techniquex = self.x + dx
        self.techniquey = self.y + dy

    def hit(self, x, y):
        self.technique = Technique.HIT
        self.techniquex = x
        self.techniquey = y


    def throw(self, x, y):
        item = self.inventory[self.techniqueitem]
        self.inventory[self.techniqueitem] = None  # Remove item from inventory
        self.active_projectiles.append(item)
        item.sprite.color = (255, 255, 255, 0)
        item.x = self.x + 0.5
        item.y = self.y + 0.5
        item.xinit = item.x 
        item.yinit = item.y
        item.xend = x + 0.5
        item.yend = y + 0.5
        item.distance_to_travel = math.sqrt(abs(item.x - item.xend)**2 + abs(item.y - item.yend)**2)
        item.prevx = self.x + 0.5
        item.prevy = self.y + 0.5
        item.entity = self
        self.technique = Technique.THROW
        self.techniquex = x
        self.techniquey = y
        dx = x - self.x 
        dy = y - self.y


    def cast(self, x, y):
        item = self.inventory[self.techniqueitem]
        self.active_projectiles.append(turn_logic.Projectile(item.name, self.techniquecharges, self.x + 0.5, self.y + 0.5, x, y, self))
        self.technique = Technique.THROW
        self.techniquex = x 
        self.techniquey = y
        

    def cast_static(self):
        self.technique = Technique.CAST
        








    def drop_item(self, inv_slot, floor):
        coords_to_check = [[0, 0], [1, 1], [0, 1], [0, -1], [1, 0], [-1, 0], [1, -1], [0, -1], [-1, -1]]
        for coords in coords_to_check:
            x = item.x + coords[0]
            y = item.y + coords[1]
            if self.detect_item(floor.floor_items, x, y) == False and (y,x) in floor.valid_tiles:
                item = self.inventory[inv_slot]
                if item is not None:
                    self.inventory[inv_slot] = None  # Remove item from inventory
                    floor.floor_items.append(item)
                    item.x = self.x
                    item.y = self.y 
            self.technique = Technique.STILL 

    def consume_item(self, inv_slot, list_of_animations):
        item = self.inventory[inv_slot]
        if item is not None:
            self.inventory[inv_slot] = None  
        health_to_restore = item.nutrition_value

        print(health_to_restore, self.maxhealth, self.health, self.maxhealth_visual, self.health_visual)
        if item.name == "Mushrooms":
            self.maxhealth += health_to_restore
            self.maxhealth_visual += health_to_restore

        if (self.health + health_to_restore > self.maxhealth) and item.name != "Durian":
            health_to_restore = self.maxhealth - self.health
        self.health += health_to_restore
        #button_class.create_point_number(self.x, self.y, "+" + str(health_to_restore), (0, 189, 66, 255), self, all_buttons)
        #print("adqwd")
        anim = animations.Animation("+" + str(health_to_restore), 2, 0, (0, 189, 66, 0), 0, 50, self.x, self.y+0.5, self.x, self.y, 0, None, None, self, self, -health_to_restore)
        #when this anim happens...

        list_of_animations.append(anim)

        if item.name == "Starfruit":
            self.speed = 4
            self.speed_turns = 12
            self.technique = Technique.STILL 
        elif item.name == "Dragonfruit":
            #increase a random stat by 1
            rand_result = random.choice([0, 1, 2])
            if rand_result == 0:
                self.maxhealth += 1
                self.health += 1
            elif rand_result == 1:
                self.strength += 1
                self.maxstrength += 1
            elif rand_result == 2:
                self.defense += 1
                self.maxdefense += 1

            self.technique = Technique.STILL
        else:
            self.technique = Technique.STILL 
        del item

    
                





    # returns True if the item is detected at the player's current position
    def detect_item(self, item_list, x, y):
        for i in item_list:
            # Check if the item is at the player's current position
            if i.x == x and i.y == y:
                print(f"Detected item: {i.name} at ({i.x}, {i.y})")
                return True
        return False
    
    # Pick up an item and add it to the player's inventory if there's room
    def pick_up_item(self, item_list):
        """Pick up an item and add it to the player's inventory."""
        for item in item_list:
            if item.x == self.x and item.y == self.y:
                if self.add_to_inventory(item):
                    item_list.remove(item)  # Remove item from the map
                    print(f"Picked up {item.name} at {item.x}, {item.y}")
                    print(f"player{self.x}, {self.y}")
                else:
                    print("Inventory full. Cannot pick up item.")

    
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







    def draw(self, batch, animation_presets, group, group_bg, group_fg):
        
        sprite = self.sprite

        if self.paralysis_visual > 0:
            frame_index = self.direction.value * 8
            paralyze_x = (1 - 2*((self.animframe*4) % 2))/2
        else:
            #print(self.direction)
            frame_index = self.direction.value * 8 + animation_presets[self.animtype][math.floor(self.animframe)]
            paralyze_x = 0

        


        base_x, base_y = 1152/2 -24 + (self.offsetx*16 + paralyze_x)*self.scale, 768/2-24 + self.offsety*16*self.scale #self.get_screen_position()


        # texture = tile.get_texture()
        # sprite.image = texture

        if frame_index != self.spriteindex_prev:
            # tile = self.grid[frame_index]

            # # Get texture and set filtering
            # texture = tile.get_texture()
            # texture.min_filter = pyglet.gl.GL_NEAREST
            # texture.mag_filter = pyglet.gl.GL_NEAREST

            # Assign directly — no blitting, no texture creation

            sprite.image.blit_into(self.grid[self.spriteindex + frame_index], 0, 0, 0)
            self.spriteindex_prev = frame_index




        self.animframe = self.animframe + self.animmod*self.speed_visual
        if self.animframe >= len(animation_presets[self.animtype]):
            self.animframe = 0



        if self.current_holding != False:
            tile2 = self.itemgrid[self.current_holding.spriteindex]
            self.sprite_weapon.image = tile2.get_texture()
            self.sprite_weapon.color = (255, 255, 255, 255)
            self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "staff", "right")
            # self.sprite_weapon.x = base_x - 24
            # self.sprite_weapon.y = base_y
            self.sprite_weapon.scale = self.scale
            self.sprite_weapon.batch = batch

        elif self.equipment_weapon != None:# and self.technique != Technique.CAST:
            tile2 = self.itemgrid[self.equipment_weapon.spriteindex]
            self.sprite_weapon.image = tile2.get_texture()
            self.sprite_weapon.color = (255, 255, 255, 255)
            self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "weapon", "right")
            # self.sprite_weapon.x = base_x - 24
            # self.sprite_weapon.y = base_y
            self.sprite_weapon.scale = self.scale
            self.sprite_weapon.batch = batch
        else:
            self.sprite_weapon.color = (0, 0, 0, 0)

        if self.equipment_shield != None:
            tile3 = self.itemgrid[self.equipment_shield.spriteindex]
            self.sprite_shield.image = tile3.get_texture()
            self.sprite_shield.color = (255, 255, 255, 255)
            self.sprite_shield.x, self.sprite_shield.y, self.sprite_shield.scale_x, self.sprite_shield.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "shield", "left")
            self.sprite_shield.scale = self.scale
            self.sprite_shield.batch = batch
        else:
            self.sprite_shield.color = (0, 0, 0, 0)

        sprite.group = group
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        sprite.color = self.color
        #sprite.color = (int(20*self.animframe), int(20*self.animframe), int(20*self.animframe))
        sprite.z = 40
        sprite.batch = batch


        

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)
    

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