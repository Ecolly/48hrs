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
from game_classes.id_shuffling import *
from font import *

class Player:
    def __init__(self, name, health, level, experience, spriteindex, animtype, x, y):
        global batch, batch
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
        self.grid = grid_entities1

        self.creaturetype = None
        self.x = x # x coords are in 
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y 
        self.offsetx = 0
        self.offsety = 0
        self.initx = x
        self.inity = y
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
        
        self.gold = 0
        self.spriteindex = spriteindex #actual index of sprite on tilegrid
        self.spriteindex_prev = -1
        self.grid = grid_entities1
        self.credit_score = 1 #if 1, you can pick up items from shop and get negative gold. if 0, you can no longer do this
        self.extinction_state = 0 #0 - all enemies remain, 1 - boss mode
        self.enemies_remaining = ["LEAFALOTTA", "CHLOROSPORE", "GOOSE", "FOX", "S'MORE", "DRAGON", "CHROME DOME", "TETRAHEDRON", "SCORPION", "TURTLE", "CULTIST", "JUJUBE", "DEMON CORE", "VITRIOLIVE", "DODECAHEDRON", "MONITAUR"]
        self.has_been_resurrected = 0

        self.sprite = create_sprite(grid_entities1, spriteindex)
        self.sprite_weapon = image_handling.create_sprite(grid_items, 0)
        self.sprite_shield = image_handling.create_sprite(grid_items, 0)

        self.sprite_weapon.color = (0, 0, 0, 0)
        self.sprite_shield.color = (0, 0, 0, 0)

        self.sprite_weapon.batch = batch
        self.sprite_shield.batch = batch
        self.sprite.batch = batch
        self.sprite.group = group_enemies

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

        self.flee_ai_turns = 0
        self.rage_ai_turns = 0

        self.is_shopping = False
        self.haswon = False
        
    
    def add_to_inventory(self, item):
        if item.name == "3 Gold":
            self.gold += 3
            return True 
        elif item.name == "15 Gold":
            self.gold += 15
            return True
        elif item.name == "60 Gold":
            self.gold += 50
            return True
        
        for slot in range(len(self.inventory)):
            #print(f"Checking slot {slot} for item {item.name}")
            if self.inventory[slot] is None:
                self.inventory[slot] = item
                return True  # Success
        #print("Inventory full. Cannot pick up item.")
        return False  # Inventory was full

    def increase_experience(self, incoming_experience):
        #can handle negative numbers
        self.experience +=incoming_experience
        new_level = int(self.experience**(1/3))
        if new_level>self.level:
            while new_level>self.level:
                self.level_up()
                new_level = int(self.experience**(1/3)) #unneeded?
        elif new_level<self.level:
            while new_level<self.level:
                self.level_down()
                new_level = int(self.experience**(1/3)) #unneeded?

    def level_up(self):
        self.level+=1
        
        self.maxhealth += 4
        self.health += 4

        self.strength += 1
        self.maxstrength += 1
        
    def level_down(self):
        self.level-=1
        
        self.maxhealth -= 4
        self.health -= 4

        self.strength -= 1
        self.maxstrength -= 1
    

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
        # item = self.inventory[self.techniqueitem]
        # self.inventory[self.techniqueitem] = None  # Remove item from inventory
        item = self.techniqueitem
        self.del_item_from_inventory(item)
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
        item = self.techniqueitem
        name_desc = get_display_name(item)
        self.active_projectiles.append(turn_logic.Projectile(item.name, self.techniquecharges, self.x + 0.5, self.y + 0.5, x, y, self, str(self.name)+" swung the " + name_desc + "!"))
        self.technique = Technique.THROW
        self.techniquex = x 
        self.techniquey = y
        

    def cast_static(self):
        self.technique = Technique.CAST
        

    def splash(self, x, y):
        item = self.techniqueitem
        name_desc = get_display_name(item)
        self.active_projectiles.append(turn_logic.Projectile(item.name, item.charges, self.x + 0.5, self.y + 0.5, x, y, self, str(self.name)+" emptied the " + name_desc + "!"))
        self.technique = Technique.THROW
        self.techniquex = x 
        self.techniquey = y

    def del_item_from_inventory(self, item):
        for i in range(len(self.inventory)):
            if self.inventory[i] == item:
                item.hotbar_sprite.visible = False
                print(f"Deleting item {item.name} from inventory slot {i}")
                self.inventory[i] = None

    def drop_item(self, item, floor, adventure_log):

        #What is happening good lord
        if item is None:
            return
        name_desc = get_display_name_and_description(item)
            
        

        self.technique = Technique.STILL 
        coords_to_check = [[0, 0], [1, 1], [0, 1], [0, -1], [1, 0], [-1, 0], [1, -1], [-1, 1], [-1, -1]]
        for coords in coords_to_check:
            x = self.x + coords[0]
            y = self.y + coords[1]
            if self.detect_item(floor.floor_items, x, y) == False and (y,x) in floor.valid_tiles:
                if item is not None:
                    item.x = self.x + coords[0]
                    item.y = self.y + coords[1]
                    self.del_item_from_inventory(item) # Remove item from inventory
                    floor.floor_items.append(item)
                    if floor.map_grid[floor.height-1-self.y][self.x] == "S":
                        self.gold += item.price
                        adventure_log.append(str(self.name) + " sold " + name_desc[0] + " for " + str(item.price) + " gold.")
                        item.price = max(item.price+1, 1) #increase price by 1 after selling.
                    else:
                        adventure_log.append(str(self.name) + " dropped " + name_desc[0] + ".")
                    break
                 # Exit after dropping the item in the first available spot
            self.technique = Technique.STILL 



                    #             if floor.map_grid[floor.height-1-self.y][self.x] == "S":
                    #     self.gold += -item.price
                    #     item.price = max(item.price-1, 1) #after buying an item, reduce its price by 1.
                    #     adventure_log.append(str(self.name) + " purchased " + name_desc + " for " + str(item.price) + " gold.")
                    #     if self.gold < 0:
                    #         adventure_log.append(str(self.name) + " is now in debt.")
                    # else:


                    #     adventure_log.append(str(self.name) + " picked up " + name_desc + ".")

    

    def consume_item(self, item, list_of_animations):
        self.del_item_from_inventory(item)

            
        health_to_restore = item.nutrition_value

        #print(health_to_restore, self.maxhealth, self.health, self.maxhealth_visual, self.health_visual)
        if item.name == "Mushrooms" or item.name == "Beet":
            self.maxhealth += health_to_restore
            self.maxhealth_visual += health_to_restore

        if item.name == "Leaves":
            health_to_restore = math.ceil(self.maxhealth*0.05)
        elif item.name == "Kale":
            health_to_restore = math.ceil(self.maxhealth*0.30)
        elif item.name == "Lettuce":
            health_to_restore = math.ceil(self.maxhealth*0.15)
        
            
        if self.health > self.maxhealth and item.name != "Durian": 
            health_to_restore = 0
        elif (self.health + health_to_restore > self.maxhealth) and item.name != "Durian":
            health_to_restore = self.maxhealth - self.health
        self.health += health_to_restore

        anim = animations.Animation(str(self.name) + " ate the " + str(item.name) + ".", "+" + str(health_to_restore), 2, 0, (0, 189, 66, 0), 0, 50, self.x, self.y+0.5, self.x, self.y, 0, None, None, self, self, -health_to_restore)
        list_of_animations.append(anim)

        if item.name == "Starfruit":
            self.speed = 4
            self.speed_turns = 12
            self.technique = Technique.STILL 
        elif item.name == "Dragonfruit":
            self.increase_experience(((self.level + 1)**3) - self.experience) 
            list_of_animations.append(animations.Animation(str(self.name) + " grew to level " + str(self.level) + "!", 0*29 + 24, 6, 4, (255, 255, 255, 0), 1, 50, self.x, self.y, self.x, self.y, 0, None, None, None, None, None))
            self.technique = Technique.STILL
        elif item.name == "Lemon":
            self.maxhealth = self.health
            self.paralysis_turns = 3
            self.paralysis_visual = 3
            list_of_animations.append(animations.Animation(str(self.name) + "'s max HP was changed to match HP.", 0*29 + 24, 6, 4, (255, 255, 255, 0), 1, 50, self.x, self.y, self.x, self.y, 0, None, None, None, None, None))
            list_of_animations.append(animations.Animation(str(self.name) + "was paralyzed by the sourness of the Lemon.", 0*29 + 24, 6, 4, (255, 255, 255, 0), 2, 50, self.x, self.y, self.x, self.y, 0, None, None, None, None, None))
            self.technique = Technique.STILL
        else:
            self.technique = Technique.STILL 
        del item

    
                





    # returns True if the item is detected at x and y location
    def detect_item(self, item_list, x, y):
        for i in item_list:
            print(f"Checking item {i.name} at ({i.x}, {i.y}) against ({x}, {y})")
            if i.x == x and i.y == y:
                print(f"Detected item: {i.name} at ({i.x}, {i.y})")
                return True
        return False
    
    # Pick up an item and add it to the player's inventory if there's room
    def pick_up_item(self, floor_item_list, adventure_log, floor):
        """Pick up an item and add it to the player's inventory."""
        for item in floor_item_list:
            if item.x == self.x and item.y == self.y and item is not None:
                name_desc = get_display_name(item)
                
                if floor.map_grid[floor.height-1-self.y][self.x] == "S" and self.gold-item.price < 0 and self.credit_score == 0:
                    adventure_log.append(str(self.name) + " can't afford the item.")
                else: 
                    if self.add_to_inventory(item) == True:
                        
                        floor_item_list.remove(item)  # Remove item from the map 

                        if floor.map_grid[floor.height-1-self.y][self.x] == "S":
                            self.gold += -item.price
                            adventure_log.append(str(self.name) + " purchased " + name_desc + " for " + str(item.price) + " gold.")
                            if self.gold < 0 and self.gold + item.price > -1:
                                adventure_log.append(str(self.name) + " is now in debt.")
                            item.price = max(item.price-1, 1) #after buying an item, reduce its price by 1.
                        else:


                            adventure_log.append(str(self.name) + " picked up " + name_desc + ".")
                    else:
                        adventure_log.append(str(self.name) + "'s inventory was too full to pick up " + name_desc + ".")
                        #inventory was full
                
            else:
                pass  # Item not at player's position, do nothing

    
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







    def draw(self, animation_presets, group, group_bg, group_fg, held_item):
        global batch
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
            sprite.image = self.grid[self.spriteindex + frame_index] #.blit_into(self.grid[self.spriteindex + frame_index], 0, 0, 0)
            self.spriteindex_prev = frame_index




        self.animframe = self.animframe + self.animmod*self.speed_visual
        if self.animframe >= len(animation_presets[self.animtype]):
            self.animframe = 0



        if held_item != None and held_item != self.equipment_shield:
            if self.sprite_weapon.image != grid_items[held_item.spriteindex]:
                self.sprite_weapon.image = grid_items[held_item.spriteindex]#.blit_into(self.itemgrid[held_item.spriteindex], 0, 0, 0)
                self.sprite_weapon.color = (255, 255, 255, 255)
                self.sprite_weapon.batch = batch

                if isinstance(held_item, Weapon):
                    self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "weapon", "right")
                else:
                    self.sprite_weapon.x, self.sprite_weapon.y, self.sprite_weapon.scale_x, self.sprite_weapon.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "staff", "right")
                self.sprite_weapon.scale = self.scale
                
        else:
            if self.sprite_weapon.color != (0, 0, 0, 0):
                self.sprite_weapon.color = (0, 0, 0, 0)
                self.sprite_weapon.batch = None

        if self.equipment_shield != None:
            if self.sprite_shield.image != grid_items[self.equipment_shield.spriteindex]:
                self.sprite_shield.image = grid_items[self.equipment_shield.spriteindex]#.blit_into(tile3, 0, 0, 0)
                self.sprite_shield.color = (255, 255, 255, 255)
                self.sprite_shield.batch = batch
            self.sprite_shield.x, self.sprite_shield.y, self.sprite_shield.scale_x, self.sprite_shield.group = self.get_helditem_coordanites(base_x, base_y, frame_index, group_bg, group_fg, "shield", "left")
            self.sprite_shield.scale = self.scale
            
        else:
            if self.sprite_shield.color != (0, 0, 0, 0):
                self.sprite_shield.color = (0, 0, 0, 0)
                self.sprite_shield.batch = None


        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        #sprite.z = 40



        

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