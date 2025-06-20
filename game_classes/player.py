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

class Player:
    def __init__(self, name, health, level, experience, sprite, spriteindex, spritegrid, color, animtype, animframe, animmod, x, y):
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
        self.inventory = []
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
        
        self.strength = 10  # Default strength
        self.maxstrength = 10

        self.defense = 5  # Default defense
        self.maxdefense = 5
        
        self.sprite = sprite  # pyglet.sprite.Sprite
        self.spriteindex = spriteindex #actual index of sprite on tilegrid
        self.grid = spritegrid
        self.color = color #4 entry tuple for the sprite to be colored as; white is default
        self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        self.animframe = 0 #what frame of the animation it's on
        self.animmod = animmod #a preset animation modifier (e.g. vibration amplitude)
        self.scale = 3

        self.default_speed = 1
        self.speed = 1
        self.turns_left_before_moving = 1
        self.speed_turns = 0


    # def get_screen_position(self):
    #     return self.scale*(self.prevx*16-8), self.scale*(self.prevy*16-8)

    # def is_mouse_over(self, mouse_x, mouse_y):
    #     """Check if a point is within this object's interactive bounds."""
    #     base_x, base_y = self.get_screen_position()
    #     #print(mouse_x, mouse_y, base_x, base_y)
    #     return (base_x <= mouse_x <= base_x + self.width*self.scale and
    #             base_y <= mouse_y <= base_y + self.height*self.scale)

    def increase_experience(self, incoming_experience):
        self.experience +=incoming_experience
        new_level = int(self.experience**(1/3))

        while new_level>self.level:
            self.level_up()
            new_level = int (self.experience**(1/3))
    
    def level_up(self):
        self.level+=1
        self.maxhealth +=3
        

    

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
        item = self.inventory.pop(self.techniqueitem)
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
        self.technique = Technique.THROW
        self.techniquex = x
        self.techniquey = y
        dx = x - self.x 
        dy = y - self.y


    def cast(self, x, y):
        item = self.inventory[self.techniqueitem]
        self.active_projectiles.append(turn_logic.Projectile(item.name, 0, self.x + 0.5, self.y + 0.5, x, y))
        self.technique = Technique.THROW
        self.techniquex = x 
        self.techniquey = y

    def cast_static(self):
        self.technique = Technique.CAST
        

    # def spellcasting(self, inv_slot, all_enemies, all_buttons, has_won, floor, sound_magic, gamestate):
        
    #     item = self.inventory[inv_slot]
    #     name = item.name
    #     if isinstance(item, Staff) == True:
    #         if name == "Red Staff": #Cuts an enemy's HP in half
    #             pass
    #         elif name == "Orange Staff": #Deducts 10 from HP of all enemies in floor (including you)
    #             self.health = self.health - 10
    #             button_class.create_point_number(self.x, self.y, "-15", (255, 0, 0, 255), self, all_buttons)
    #             button_class.create_graphical_effect(self.x, self.y, 0, self, all_buttons)
    #             for enemy in all_enemies:
    #                 enemy.health = enemy.health - 10
    #                 button_class.create_point_number(enemy.x, enemy.y, "-15", (255, 0, 0, 255), self, all_buttons)
    #                 button_class.create_graphical_effect(enemy.x, enemy.y, 0, self, all_buttons)
    #                 if not enemy.is_alive():
    #                     enemy.sprite.delete()
    #                     del enemy.sprite
    #                     floor.all_enemies.remove(enemy)
    #             sound_magic.play()
    #             self.inventory.remove(item)
    #             del item
    #         elif name == "Gold Staff": #average all stats together (could be a consumable)
    #             total_stats = math.floor((self.health + self.strength + self.defense)/3)

    #             self.maxhealth = total_stats
    #             self.health = total_stats

    #             self.maxstrength = total_stats
    #             self.strength = total_stats

    #             self.maxdefense = total_stats
    #             self.defense = total_stats
    #             sound_magic.play()
    #             self.inventory.remove(item)
    #             del item
    #         elif name == "Green Staff": #wand of teleporting
    #             random_location = random.choice(floor.valid_entity_tiles)
    #             y, x = random_location
    #             self.x, self.y = x, y
    #             self.prevx, self.prevy = x, y
    #             sound_magic.play()
    #             self.inventory.remove(item)
    #             del item
    #             pass
    #         elif name == "Teal Staff": 
    #             self.health = self.maxhealth
    #             sound_magic.play()
    #             self.inventory.remove(item)
    #             del item
    #         elif name == "Blue Staff": #+1 to Sword and Shield.
    #             if self.equipment_shield != None:
    #                 self.equipment_shield.defense += 1
    #             if self.equipment_weapon != None:
    #                 self.equipment_weapon.damage += 1
    #             sound_magic.play()
    #             self.inventory.remove(item)
    #             del item
    #         elif name == "Light Blue Staff": #Multiplies Sword & Shield strength by 1.2x
    #             if self.equipment_shield != None:
    #                 self.equipment_shield.defense = math.floor(self.equipment_shield.defense*1.2)
    #             if self.equipment_weapon != None:
    #                 self.equipment_weapon.damage = math.floor(self.equipment_sheild.damage*1.2)
    #             sound_magic.play()
    #             self.inventory.remove(item)
    #             del item
    #         elif name == "Magenta Staff":
    #             sound_magic.play()
    #             has_won = 1
    #             self.inventory.remove(item)
    #             del item
    #         elif name == "Black Staff":
    #             self.maxhealth = self.maxhealth + 1
    #             sound_magic.play()
    #             self.inventory.remove(item)
    #             del item
    #             pass
            
    #         self.technique = Technique.STILL
    #         return has_won


    # def cast_projectile(self, x, y):
    #     projectile = Spell("spell", sprite_locs=4)
    #     self.active_spells.append(projectile)
    #     projectile.x = self.x
    #     projectile.y = self.y   
    #     projectile.prevx = self.x 
    #     projectile.prevy = self.y
    #     self.technique = Technique.CAST

    #     self.techniquex = x
    #     self.techniquey = y
    #     dx = x - self.x 
    #     dy = y - self.y

    #     #adjust rotation state (gross)
    #     if dx == 1:
    #         if dy == 1:
    #             self.direction = FaceDirection.UP_RIGHT
    #         elif dy == -1:
    #             self.direction = FaceDirection.DOWN_RIGHT
    #         else:
    #             self.direction = FaceDirection.RIGHT
    #     elif dx == -1:
    #         if dy == 1:
    #             self.direction = FaceDirection.UP_LEFT
    #         elif dy == -1:
    #             self.direction = FaceDirection.DOWN_LEFT
    #         else:
    #             self.direction = FaceDirection.LEFT
    #     else:
    #         if dy == 1:
    #             self.direction = FaceDirection.UP
    #         elif dy == -1:
    #             self.direction = FaceDirection.DOWN













    def drop_item(self, inv_slot, floor_items):
        if self.detect_item(floor_items) == False:
            item = self.inventory.pop(inv_slot)
            floor_items.append(item)
            item.x = self.x
            item.y = self.y    
        self.technique = Technique.STILL 

    def consume_item(self, inv_slot, list_of_animations):
        item = self.inventory.pop(inv_slot)
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
            self.speed = 2
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
    def detect_item(self, item_list):
        for i in item_list:
            # Check if the item is at the player's current position
            if i.x == self.x and i.y == self.y:
                print(f"Detected item: {i.name} at ({i.x}, {i.y})")
                return True
        return False
    
    # Pick up an item and add it to the player's inventory if there's room
    def pick_up_item(self, item_list):
        """Pick up an item and add it to the player's inventory."""
        for item in item_list:
            if item.x == self.x and item.y == self.y:
                if len(self.inventory) < 30:  # Arbitrary limit for inventory size
                    self.inventory.append(item)
                    item_list.remove(item)  # Remove item from the map
                    print(f"Picked up {item.name} at {item.x}, {item.y}")
                    print(f"player{self.x}, {self.y}")
                    print(f"inventory: {[i.name for i in self.inventory]}")
                else:
                    print("Inventory full. Cannot pick up item.")





    def draw(self, batch, animation_presets, group):
        base_x, base_y = 1152/2 -24 + self.offsetx*16*self.scale, 768/2-24 + self.offsety*16*self.scale #self.get_screen_position()
        sprite = self.sprite

        frame_index = self.spriteindex + self.direction.value * 8 + animation_presets[self.animtype][int(self.animframe)]
        tile = self.grid[frame_index]

        # Get texture and set filtering
        texture = tile.get_texture()
        pyglet.gl.glBindTexture(pyglet.gl.GL_TEXTURE_2D, texture.id)
        texture.min_filter = pyglet.gl.GL_NEAREST
        texture.mag_filter = pyglet.gl.GL_NEAREST
        
        # Assign directly — no blitting, no texture creation
        sprite.image = texture

        self.animframe = self.animframe + self.animmod*self.speed
        if self.animframe >= len(animation_presets[self.animtype]):
            self.animframe = 0

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