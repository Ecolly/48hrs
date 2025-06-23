#just a superdeduper small class for non-item projectiles


import math 

class Projectile:
    def __init__(self, name, damage, x, y, xend, yend, entity, chron=0):
        self.name = name
        self.damage = damage
        self.x = math.floor(x)
        self.y = math.floor(y)
        self.xend = xend + 0.5
        self.yend = yend + 0.5
        self.distance_to_travel = math.sqrt(abs(self.x - xend)**2 + abs(self.y - yend)**2)
        self.xinit = math.floor(x)
        self.yinit = math.floor(y)
        self.chron_offset = chron
        self.entity = entity
        self.num_of_bounces = 0
        self.num_of_pierces = 0
        self.friendly_fire = False
        if name == "Spores":
            self.spriteindex = 29 + 8
        elif name == "Dragon Fire":
            self.spriteindex = 2*29
            self.num_of_pierces = 4
        else:
            self.spriteindex = 4*29

        if name == "Green Staff":
           self.num_of_bounces = damage
        elif name == "Magenta Staff":
            self.num_of_pierces = damage








            
# import pyglet
# import math
# from enum import Enum, auto

# sprite_items = pyglet.image.load('items_and_fx.png')
# columns_items = sprite_items.width // 16
# rows_items = sprite_items.height // 16
# grid_items = pyglet.image.ImageGrid(sprite_items, rows_items, columns_items)

# def create_sprite_item(image_grid, index): #dumb. literally the same as the image handling function
#     tex = pyglet.image.Texture.create(16, 16)
#     tex.blit_into(image_grid[index], 0, 0, 0)
#     return pyglet.sprite.Sprite(tex, x=0, y=0)


# class Spell:
#     #very basics item class cause we dono what items there are
#     def __init__(self, name, sprite_locs, x=0, y=0):
#         global grid_items
#         self.name = name
#         self.grid = grid_items
#         # self.index = item_names.index(name)
#         # self.fakename = item_fakenames[self.index]
#         self.sprite = create_sprite_item(grid_items, 29*4+ sprite_locs)
#         self.spriteindex = 29*4+ sprite_locs
#         self.x = x
#         self.y = y
#         self.animframe = 0
#         self.prevx = x #previous x and y coordanites, for animating
#         self.prevy = y
#         self.scale = 3

#     def draw(self, batch, player, group):
#         base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
#         base_y = 768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
#         sprite = self.sprite
#         self.animframe += 1

#         frame_index = self.spriteindex + math.floor(self.animframe/8) % 4
        
#         tile = self.grid[frame_index]

#         # Get texture and set filtering
#         texture = tile.get_texture()
#         texture.min_filter = pyglet.gl.GL_NEAREST
#         texture.mag_filter = pyglet.gl.GL_NEAREST

#         # Assign directly — no blitting, no texture creation
#         sprite.image = texture
#         sprite.x = base_x
#         sprite.y = base_y
#         sprite.scale = self.scale
#         sprite.group = group
#         sprite.batch = batch














