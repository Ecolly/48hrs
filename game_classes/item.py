
import pyglet
from enum import Enum, auto
import pyglet
import image_handling
from font import *
import random
import gc

def check_if_on_screen(x, y, player):
    if ((x > player.x + 13 or x < player.x - 13) or (y > player.y + 9 or y < player.y - 9)):
        return False
    else:
        return True
    


def create_sprite_item(image_grid, index): #dumb. literally the same as the image handling function
    # tex = pyglet.image.Texture.create(16, 16)
    # tex.blit_into(image_grid[index], 0, 0, 0)
    #print("a")
    #print(sum(1 for obj in gc.get_objects() if isinstance(obj, pyglet.image.Texture)))
    spr = pyglet.sprite.Sprite(image_grid[index], x=0, y=0)
    
    #print(sum(1 for obj in gc.get_objects() if isinstance(obj, pyglet.image.Texture)))
    return spr

spr3 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles("E", grid_font, letter_order), 8, 8, 2))
spr4 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles("E", grid_font, letter_order), 8, 8, 2))


class Item:
    #very basics item class cause we dono what items there are
    def __init__(self, name, sprite_locs, x, y, quantity, description=""):
        #global group_items
        # item_names = ["Kitchen Knife", "Machete", "Scimitar", "Screwdriver", "Sickle"]
        # item_fakenames = ["Kitchen Knife", "Machete", "Scimitar", "Screwdriver", "Sickle"]
        #item_spritelocs = [29*10, 29*10+1, 29*10+2, 29*10+3, 29*10+4]

        self.name = name
        #self.name_visual = self.name
        # self.index = item_names.index(name)
        # self.fakename = item_fakenames[self.index]
        self.sprite_locs = sprite_locs #for tome and spell color mechanics
        self.spriteindex = 29*10+sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        #self.sprite.group = group_items
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)
        self.grid = grid_items
        #self.equppedsprite
        
        self.color = (255, 255, 255, 255)
        self.magic_color = sprite_locs #for tome and spell color mechanics
        self.x = x
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y
        self.xinit = x 
        self.yinit = y
        self.distance_to_travel = 0
        self.xend = x
        self.yend = y
        self.entity = None
        self.chron_offset = 0
        self.friendly_fire = False 
        self.quantity = quantity
        self.scale = 3
        self.is_usable = False #default to false
        self.is_equipable = False #default to false
        self.is_consumable = False #default to false
        self.is_castable = False
        self.is_piercing = False #default to false
        self.is_readable = False
        self.should_be_deleted = False
        self.num_of_bounces = 0
        self.num_of_pierces = 0
        self.description = description
        self.is_hovered = False
        self.reverse = ""
        self.price = 0
        self.rarity = 0
        


    def get_screen_position(self): #unused?
        if self.inventory_slot == -1:
            return self.scale*(self.prevx*16-8), self.scale*(self.prevy*16-8)
    
    def is_mouse_over(self, mouse_x, mouse_y):
        """Check if a point is within this object's interactive bounds."""
        base_x, base_y = self.get_screen_position()
        #print(mouse_x, mouse_y, base_x, base_y)
        return (base_x <= mouse_x <= base_x + self.width*self.scale and
                base_y <= mouse_y <= base_y + self.height*self.scale)
    
    def draw(self, player, group):
        global batch
        base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
        base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
        
        sprite = self.sprite
        if self.color == None:
            self.color = (255, 255, 255, 255)
        sprite.color = self.color
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        if sprite.group != group:
            sprite.group = group

        if check_if_on_screen(self.x, self.y, player) == False:
            sprite.batch = None 
        elif sprite.batch != batch:
            sprite.batch = batch
        
    
    
    # def draw_projectiles(self, batch, player, group):
    #     base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
    #     base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
    #     sprite = self.sprite
    #     sprite.x = base_x
    #     sprite.y = base_y
    #     sprite.scale = self.scale
    #     sprite.group = group
    #     sprite.batch = batch

    #Dont look at this oml
    

    def wrap_text(text, max_chars_per_line):
        words = text.split(' ')
        lines = []
        current_line = ""
        for word in words:
            if len(current_line) + len(word) + (1 if current_line else 0) <= max_chars_per_line:
                if current_line:
                    current_line += " "
                current_line += word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines
    

    def test_hovering(self, mouse_x, mouse_y, invslot, gamestate):
        spacing = 9
        if self is not None:
            if gamestate == 3: #if in the inventory menu
                #print(f"Testing hovering for item: {self.name} at slot {invslot}")
                base_x = (invslot % 10)*(48+spacing) + int((1152)/48)*12 + 9 #1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y = -(invslot // 10)*(48+spacing)+ spacing + int((768)/48)*32 -10#768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
                return (base_x <= mouse_x <= base_x + 48) and (base_y <= mouse_y <= base_y + 48)
        return False
    
    def draw_inventory(self, player, group, invslot, gamestate):
        global batch
        spacing = 9 #spacing between items in the inventory
        if self is not None:
            sprite = self.sprite
            e_weapon_equip = spr3
            e_shield_equip = spr4
            if gamestate == 3: #if in the inventory menu
                base_x = (invslot % 10)*(48+spacing) + int((1152)/48)*12 + 9 #1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y = -(invslot // 10)*(48+spacing)+ spacing + int((768)/48)*32 -10#768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
                
                sprite.x = base_x
                sprite.y = base_y
                #text = self.draw_description(batch, group2, invslot, gamestate) #draw the description text if it exists
                
                sprite.color = (255, 255, 255, 255)
                sprite.scale = self.scale

                if sprite.group != group or sprite.batch != batch:
                    sprite.group = group
                    sprite.batch = batch

                #this code here is a disgrace to humanity, but it works
                if self is player.equipment_weapon:
                    e_weapon_equip.x = base_x + 2
                    e_weapon_equip.y = base_y + 30
                    e_weapon_equip.color = (255, 255, 0, 0)
                    e_weapon_equip.scale = 3  # Adjust as needed
                    #do not use E for weapons anymore, only shields
                    #e_weapon_equip.group = group  # Or use a higher group if you want it on top
                    #e_weapon_equip.batch = batch
                if self is player.equipment_shield:
                    e_shield_equip.x = base_x + 2
                    e_shield_equip.y = base_y + 30
                    e_shield_equip.color = (255, 255, 0, 255)
                    e_shield_equip.scale = 3  # Adjust as needed
                    if e_shield_equip.group != group or e_shield_equip.batch != batch:
                        e_shield_equip.group = group  # Or use a higher group if you want it on top
                        e_shield_equip.batch = batch
            else:
                e_shield_equip.batch = None
                e_weapon_equip.batch = None
                sprite.batch = None    
                  

    # if self.type == 'equip sword':
    #                 sprite.group = group6
    #                 if player.equipment_weapon == None:
    #                     sprite.color = (0, 189, 66, 0)
    #                 else:
    #                     sprite.color = (0, 189, 66, 255)
    #                     id = player.inventory.index(player.equipment_weapon)
    #                     inventory_x = id % 10
    #                     inventory_y = id // 10
    #                     self.x = inventory_x*48 + int(1152/48)*12
    #                     self.y = -inventory_y*48 + int(768/48)*32 - 1   

class Weapon(Item):
    def __init__(self, name, sprite_locs, x=0, y=0, quantity=1, damage=0, durability=0, is_equipable = True, description="", price=0):
        super().__init__(name, sprite_locs, x, y, quantity, description)

        self.spriteindex = 29*11+sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)

        self.damage = damage
        self.durability = durability  # Default durability
        self.damage_type = "slashing"  # Default damage type
        self.is_equipable = is_equipable
        self.bonus = 0
        self.price = price
        
class Staff(Item):
    def __init__(self, name, reverse, sprite_locs, projectile, x=0, y=0, quantity=1, damage=0, charges=7, description="", rarity=0):
        super().__init__(name, sprite_locs, x, y, quantity, description)
        self.spriteindex = 29*10+sprite_locs
        self.magic_color = sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)
        self.damage = damage
        self.charges = charges-random.randint(0, 3) #number of uses
        self.maxcharges = charges
        self.damage_type = "slashing"  # Default damage type
        self.is_castable = True
        self.is_castable_projectile = projectile
        self.reverse = reverse
        self.rarity = rarity
        self.price = 10 + rarity*5 + self.charges
        #self.is_equipable = is_equipable

class Tome(Item):
    def __init__(self, name, reverse, sprite_locs, projectile, x=0, y=0, quantity=1, damage=0, charges=30, description="", price=0):
        super().__init__(name, sprite_locs, x, y, quantity, description)
        self.spriteindex = 29*5+sprite_locs
        self.magic_color = sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)
        self.damage = damage
        self.charges = 1 #number of uses
        self.maxcharges = 1 #um
        self.damage_type = "slashing"  #???
        self.is_castable = False
        self.is_castable_projectile = False
        self.is_readable = True
        self.to_be_converted = None
        self.reverse = reverse
        self.price = price

class Flask(Item):
    def __init__(self, name, reverse, evaporation_rate, liquid, product, sprite_locs, x=0, y=0, quantity=1, damage=0, description="", price=0):
        super().__init__(name, sprite_locs, x, y, quantity, description)
        self.spriteindex = 29*6+sprite_locs
        self.magic_color = sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)

        self.evaporation_rate = evaporation_rate 
        self.liquid = liquid 
        self.product = product 
        
        self.charges = 15 #number of liquid tiles to make
        self.maxcharges = 15 #um...

        self.damage_type = "slashing"  #???
        self.is_castable = False
        self.is_castable_projectile = False
        self.is_readable = True
        self.to_be_converted = None
        self.reverse = reverse
        self.price = price

class Consumable(Item):
    def __init__(self, name, sprite_locs, nutrition_value, x=0, y=0, quantity=1, description="", price=0):
        super().__init__(name, sprite_locs, x, y, quantity, description)
        self.spriteindex = 29*7+sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)
        self.nutrition_value = nutrition_value
        self.is_consumable = True
        self.price = price




class Shield (Item):
    def __init__(self, name, sprite_locs, x=0, y=0, quantity=1, defense=0, is_equipable = True, description="", price=0):
        super().__init__(name, sprite_locs, x, y, quantity, description)
        self.spriteindex = 29*9+sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)
        self.defense = defense  # Default defense value
        self.is_equipable = is_equipable
        self.bonus = 0
        self.price = price

class Miscellanious(Item):
    def __init__(self, name, sprite_locs, x=0, y=0, quantity=1, description="", price=0):
        super().__init__(name, sprite_locs, x, y, quantity)
        self.spriteindex = 29*8+sprite_locs
        self.sprite = create_sprite_item(grid_items, self.spriteindex)
        self.hotbar_sprite = create_sprite_item(grid_items, self.spriteindex)
        self.price = price
        self.description = description
        #self.description = "wqde"
        #self.defense = defense  # Default defense value
        #self.is_equipable = is_equipable

# class Staff(Item):


# class Potion(Item):















