
import pyglet
from enum import Enum, auto
import pyglet
import image_handling
from font import grid_font, letter_order


def create_sprite_item(image_grid, index): #dumb. literally the same as the image handling function
    tex = pyglet.image.Texture.create(16, 16)
    tex.blit_into(image_grid[index], 0, 0, 0)
    return pyglet.sprite.Sprite(tex, x=0, y=0)

spr3 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles("E", grid_font, letter_order), 8, 8, 2))


class Item:
    #very basics item class cause we dono what items there are
    def __init__(self, name, grid_items, sprite_locs, x, y, quantity):
        # item_names = ["Kitchen Knife", "Machete", "Scimitar", "Screwdriver", "Sickle"]
        # item_fakenames = ["Kitchen Knife", "Machete", "Scimitar", "Screwdriver", "Sickle"]
        item_spritelocs = [29*10, 29*10+1, 29*10+2, 29*10+3, 29*10+4]

        self.name = name
        # self.index = item_names.index(name)
        # self.fakename = item_fakenames[self.index]
        self.sprite = create_sprite_item(grid_items, 29*10+ sprite_locs)
        #self.equppedsprite
        self.spriteindex = 29*10+sprite_locs
        self.color = (255, 255, 255, 255)
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
        self.should_be_deleted = False
        self.num_of_bounces = 0
        self.num_of_pierces = 0

    def use(self, target):
        pass

    def get_screen_position(self): #unused?
        if self.inventory_slot == -1:
            return self.scale*(self.prevx*16-8), self.scale*(self.prevy*16-8)
    
    def is_mouse_over(self, mouse_x, mouse_y):
        """Check if a point is within this object's interactive bounds."""
        base_x, base_y = self.get_screen_position()
        #print(mouse_x, mouse_y, base_x, base_y)
        return (base_x <= mouse_x <= base_x + self.width*self.scale and
                base_y <= mouse_y <= base_y + self.height*self.scale)
    
    def draw(self, batch, player, group):
        
        base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
        base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
        
        sprite = self.sprite
        if self.color == None:
            self.color = (255, 255, 255, 255)
        sprite.color = self.color
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        sprite.group = group
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

    def draw_inventory(self, batch, player, group, invslot, gamestate):
        spacing = 9 #spacing between items in the inventory
        if self is not None:
            sprite = self.sprite
            if gamestate == 3: #if in the inventory menu
                base_x = (invslot % 10)*(48+spacing) + int((1152)/48)*12 + 9 #1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y = -(invslot // 10)*(48+spacing)+ spacing + int((768)/48)*32 -10#768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
                sprite.x = base_x
                sprite.y = base_y
                sprite.color = (255, 255, 255, 255)
                sprite.scale = self.scale
                sprite.group = group
                sprite.batch = batch
                if self is player.equipment_weapon or self is player.equipment_shield:
                    e_sprite = spr3
                    e_sprite.x = base_x + 2
                    e_sprite.y = base_y + 30
                    e_sprite.color = (255, 255, 0, 255)
                    e_sprite.scale = 3  # Adjust as needed
                    e_sprite.group = group  # Or use a higher group if you want it on top
                    e_sprite.batch = batch
            else:
                sprite.color = (0, 0, 0, 0)
                sprite.batch = batch       

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
    def __init__(self, name, grid_items, sprite_locs, x=0, y=0, quantity=1, damage=0, durability=0, is_equipable = True):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*10+ sprite_locs)
        self.spriteindex = 29*10+sprite_locs
        self.damage = damage
        self.durability = durability  # Default durability
        self.damage_type = "slashing"  # Default damage type
        self.is_equipable = is_equipable
        self.bonus = 0
        
class Staff(Item):
    def __init__(self, name, grid_items, sprite_locs, projectile, x=0, y=0, quantity=1, damage=0, charges=30):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*9+ sprite_locs)
        self.spriteindex = 29*9+sprite_locs
        self.damage = damage
        self.charges = charges-1 #number of uses
        self.maxcharges = charges
        self.damage_type = "slashing"  # Default damage type
        self.is_castable = True
        self.is_castable_projectile = projectile
        #self.is_equipable = is_equipable

class Consumable(Item):
    def __init__(self, name, grid_items, sprite_locs, nutrition_value, x=0, y=0, quantity=1):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*6+ sprite_locs)
        self.spriteindex = 29*6+sprite_locs
        self.nutrition_value = nutrition_value
        self.is_consumable = True


class Shield (Item):
    def __init__(self, name, grid_items, sprite_locs, x=0, y=0, quantity=1, defense=0, is_equipable = True):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*8+ sprite_locs)
        self.spriteindex = 29*8+sprite_locs
        self.defense = defense  # Default defense value
        self.is_equipable = is_equipable
        self.bonus = 0

class Miscellanious(Item):
    def __init__(self, name, grid_items, sprite_locs, description, x=0, y=0, quantity=1):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*7+ sprite_locs)
        self.spriteindex = 29*7+sprite_locs
        self.description = description
        #self.defense = defense  # Default defense value
        #self.is_equipable = is_equipable

# class Staff(Item):


# class Potion(Item):















