
import pyglet
import image_handling
import math
import random
from game_classes.techniques import *
from enum import Enum, auto
from game_classes.item import *

# def create_sprite_item(image_grid, index): #dumb. literally the same as the image handling function
#     tex = pyglet.image.Texture.create(16, 16)
#     tex.blit_into(image_grid[index], 0, 0, 0)
#     return pyglet.sprite.Sprite(tex, x=0, y=0)
sprite_items = pyglet.image.load('items_and_fx.png')
columns_items = sprite_items.width // 16
rows_items = sprite_items.height // 16
grid_items = pyglet.image.ImageGrid(sprite_items, rows_items, columns_items)

sprite_font = pyglet.image.load('font.png')
columns_font = sprite_font.width // 8
rows_font = sprite_font.height // 8
grid_font = pyglet.image.ImageGrid(sprite_font, rows_font, columns_font)


class Animation:
    def __init__(self, spriteindex, animtype, animspeed, color, start_time, duration, startx, starty, endx, endy, rot, associated_object, technique, attacker, target, damage, item=None):
        global grid_items
        global grid_font
        # 1. move player
        # 2. move enemy
        # 3. move item (aka throw)
        # 4. move effect (aka cast)
        # 5. damage number
        # 6. strike effect
        # 7. smoke effect for magic
        # 8. splash effect for 'wave' attacks

        #3, 4, 5, 6, 7, 8 are all the same. give them a
        # sprite index/color
        # animation type  
        # animation speed
        # duration
        # starting x/y
        # ending x/y
        
        #for 1, 2, simply link to the object, and give them a
        # duration
        # starting x/y (same as their x/y)
        # ending x/y
        # animation type (0 = interpolate from starting x/y to ending x/y, 1 = use quartic formula to do striking anim)
        self.scale = 3 
        self.color = (color[0], color[1], color[2], 0)
        self.spriteindex = spriteindex
        self.animtype = animtype 
        self.animspeed = animspeed
        self.start_time = start_time
        self.duration = duration
        self.current_time = 0
        self.startx = startx
        self.starty = starty
        self.endx = endx 
        self.endy = endy 
        self.rot = rot
        self.x = startx 
        self.y = starty
        self.associated_object = associated_object
        self.should_be_deleted = False
        self.technique = technique
        self.attacker = attacker 
        self.target = target
        self.damage = damage
        self.item = item
        self.proceed = False #if this is true for all animations, game will switch back to gamestate 1. useful for damage nums

        self.spriteindex = spriteindex
        if self.spriteindex != None:
            if type(self.spriteindex) == str: #if it's a string, use the grid_font & generate the sprite using text handling
                self.sprite = image_handling.create_sprite_text_simple(grid_font, spriteindex)
                self.grid = grid_font
            else:
                self.sprite = image_handling.create_sprite(grid_items, spriteindex)
                self.grid = grid_items

    def draw(self, batch, player, group, floor):
        self.current_time += 1
        if self.current_time > self.start_time:
            frame = self.current_time - self.start_time
            if self.associated_object != None and self.technique != Technique.THROW:
                obj = self.associated_object
                obj.direction = self.rot
                if self.animtype == 1:
                    quartic_eq = (-0.19*(0.25*frame)**4 + (0.25*frame)**3 - (0.25*frame)**2)/2.5
                    if obj == player:
                        obj.offsetx = round((abs(obj.techniquex - obj.x)/(obj.techniquex - obj.x + 0.01)))*quartic_eq
                        obj.offsety = round((abs(obj.techniquey - obj.y)/(obj.techniquey - obj.y + 0.01)))*quartic_eq
                    else:
                        obj.prevx = obj.x + round((abs(obj.techniquex - obj.x)/(obj.techniquex - obj.x + 0.01)))*quartic_eq
                        obj.prevy = obj.y + round((abs(obj.techniquey - obj.y)/(obj.techniquey - obj.y + 0.01)))*quartic_eq
                else:
                    obj.prevx = obj.prevx + round((abs(obj.techniquex - obj.prevx)/(obj.techniquex - obj.prevx+0.01)))/8
                    obj.prevy = obj.prevy + round((abs(obj.techniquey - obj.prevy)/(obj.techniquey - obj.prevy+0.01)))/8



                    if self.associated_object == player and frame > self.duration:
                        player.pick_up_item(floor.floor_items)
            else:
                self.color = (self.color[0], self.color[1], self.color[2], 255)




                base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y =  768/2-24-(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #+768/2-24?

                
                if self.animtype == 1 or self.animtype == 4:

                    
                    tile = self.grid[self.spriteindex+(math.floor(self.current_time/self.animspeed) % 4)]
                    # Get texture and set filtering
                    texture = tile.get_texture()
                    texture.min_filter = pyglet.gl.GL_NEAREST
                    texture.mag_filter = pyglet.gl.GL_NEAREST
                    # Assign directly — no blitting, no texture creation
                    self.sprite.image = texture


                elif self.animtype == 2: #point numbers
                    #print("dwqdwdw")
                    #base_y =  -(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #for some reason, base y alignment is different for letters
                    self.y += 1/32
                    
                    if frame == 6:
                        self.proceed = True
                        if self.attacker != None:
                            #check if a death was caused
                            is_dead = 0
                            if self.target.should_be_deleted == True:
                                self.target.color = (255, 255, 255, 0)
                                self.target.sprite.color = (255, 255, 255, 0)
                                is_dead = 1
                            if self.attacker == player:
                                #if the player attacked something and it died, update the UI to reflect their new experience amounts
                                if is_dead == 1:
                                    self.attacker.experience_visual += self.target.experience
                                    new_level = int(self.attacker.experience_visual**(1/3))
                                    while new_level>self.attacker.level_visual:
                                        self.attacker.level_visual+= 1
                                        self.attacker.maxhealth_visual += 3
                            else:
                                if is_dead == 1:
                                    pass
                                    #update attacker sprite to reflect current level
                            self.target.health_visual = self.target.health_visual - self.damage
                            

                    elif frame > 20:
                        self.color = (self.color[0], self.color[1], self.color[2], random.choice([0, 255]))
                
                
                if self.animtype == 3 or self.animtype == 4: #projectiles
                    
                    self.color = (self.color[0], self.color[1], self.color[2], 255)           
                    distance_x = self.endx - self.startx
                    distance_y = self.endy - self.starty
                    distance_total = math.sqrt(distance_x*distance_x + distance_y*distance_y)

                    distance_x_normalized = distance_x/(distance_total*5)
                    distance_y_normalized = distance_y/(distance_total*5)
                    
                    self.x = self.x + distance_x_normalized
                    self.y = self.y + distance_y_normalized
                    
                    
                
                


                sprite = self.sprite
                sprite.color = self.color
                sprite.x = base_x
                sprite.y = base_y
                sprite.scale = self.scale
                sprite.group = group
                sprite.batch = batch
            if frame > self.duration:
                #delete self
                if self.associated_object != None and self.technique != Technique.THROW:
                    obj.prevx = obj.x 
                    obj.prevy = obj.y 
                    obj.offsetx = 0 
                    obj.offsety = 0
                else:
                    self.color = (self.color[0], self.color[1], self.color[2], 0) #turn transparent
                    sprite = self.sprite
                    sprite.color = self.color
                    sprite.group = group
                    sprite.batch = batch
                    if self.item != None:
                        if isinstance(self.item, Item):
                            self.item.sprite.delete()
                            del self.item.sprite
                        del self.item
                self.should_be_deleted = True




























