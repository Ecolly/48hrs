
import pyglet
from enum import Enum, auto

def create_sprite_item(image_grid, index): #dumb. literally the same as the image handling function
    tex = pyglet.image.Texture.create(16, 16)
    tex.blit_into(image_grid[index], 0, 0, 0)
    return pyglet.sprite.Sprite(tex, x=0, y=0)


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
        self.x = x
        self.y = y
        self.prevx = x #previous x and y coordanites, for animating
        self.prevy = y
        self.quantity = quantity
        self.scale = 3
        self.is_usable = False #default to false
        self.is_equipable = False #default to false
        self.is_consumable = False #default to false
        self.is_piercing = False #default to false


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
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        sprite.group = group
        sprite.batch = batch
    
    def draw_projectiles(self, batch, player, group):
        base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
        base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
        sprite = self.sprite
        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        sprite.group = group
        sprite.batch = batch

    def draw_inventory(self, batch, player, group, invslot, gamestate):
        sprite = self.sprite
        if gamestate == 3: #if in the inventory menu
            base_x = (invslot % 10)*48 + int((1152)/48)*12 #1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
            base_y = (invslot // 10)*48 + int((768)/48)*32 #768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
            sprite.x = base_x
            sprite.y = base_y
            sprite.color = (255, 255, 255, 255)
            sprite.scale = self.scale
            sprite.group = group
            sprite.batch = batch
        else:
            sprite.color = (0, 0, 0, 0)
            sprite.batch = batch

class Weapon(Item):
    def __init__(self, name, grid_items, sprite_locs, x=0, y=0, quantity=1, damage=0, durability=0, is_equipable = True):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*10+ sprite_locs)
        self.damage = damage
        self.durability = durability  # Default durability
        self.damage_type = "slashing"  # Default damage type
        self.is_equipable = is_equipable

class Consumable(Item):
    def __init__(self, name, grid_items, sprite_locs, temp_hp_enabled=False, x=0, y=0, quantity=1, nutrition_value=0):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*6+ sprite_locs)
        self.nutrition_value = nutrition_value
        self.health_restored = 5  # Default health restored
        self.is_consumable = True
        self.temp_hp_enabled = temp_hp_enabled

class Shield (Item):
    def __init__(self, name, grid_items, sprite_locs, x=0, y=0, quantity=1, defense=0, is_equipable = True):
        super().__init__(name, grid_items, sprite_locs, x, y, quantity)
        self.sprite = create_sprite_item(grid_items, 29*8+ sprite_locs)
        self.defense = defense  # Default defense value
        self.is_equipable = is_equipable

# class Staff(Item):


# class Potion(Item):















