
import pyglet
import image_handling
import math
import random
from game_classes.face_direction import *
from game_classes.techniques import *
from enum import Enum, auto
from game_classes.item import *
from game_classes.enemy import *
from font import *
from game_classes.id_shuffling import *



def wipe_techniqueitem(entity):
    if isinstance(entity, Enemy) and entity.techniqueitem != None:
        entity.techniqueitem.sprite.delete() 
        entity.techniqueitem.hotbar_sprite.delete() 
        entity.techniqueitem = None

class Animation:
    def __init__(self, text, spriteindex, animtype, animspeed, color, start_time, duration, startx, starty, endx, endy, rot, associated_object, technique, attacker, target, damage, item=None, strength_reduction=0, defense_reduction=0, drop_item=False):
        global grid_items
        global grid_font
        global batch
        global group_effects
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
        self.text = text
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
        self.endx = endx 
        self.endy = endy
        self.associated_object = associated_object
        self.should_be_deleted = False
        self.technique = technique
        self.attacker = attacker 
        self.target = target
        self.damage = damage
        self.item = item
        self.proceed = False #if this is true for all animations, game will switch back to gamestate 1. useful for damage nums
        self.strength_reduction = strength_reduction
        self.defense_reduction = defense_reduction
        self.drop_item = drop_item

        self.spriteindex = spriteindex
        if self.spriteindex != None:
            if type(self.spriteindex) == str: #if it's a string, use the grid_font & generate the sprite using text handling
                self.sprite = image_handling.create_sprite_text_simple(grid_font, spriteindex)
                self.grid = grid_font
            else:
                self.sprite = image_handling.create_sprite(grid_items, spriteindex)
                self.grid = grid_items
            self.sprite.group = group_effects
            self.sprite.batch = batch

    def draw(self, player, group, floor, adventure_log, bg_liqs_foreground, rctrl):
        global grid_liqtile
        self.current_time += 1

        # if self.text != "":
        #     print(self.text, self.current_time, self.start_time)
        if (self.current_time == self.start_time or (self.current_time == 1 and self.start_time == 0)) and self.text != "":
            adventure_log.append(self.text)
            
        if self.current_time <= self.start_time:

            if hasattr(self, 'sprite') and isinstance(self.sprite, pyglet.sprite.Sprite):
                if self.sprite.opacity != 0:
                    self.sprite.opacity = 0

        else: #if the animation has started...
            frame = self.current_time - self.start_time
            if hasattr(self, 'sprite') and isinstance(self.sprite, pyglet.sprite.Sprite) and frame == 1:
                self.sprite.opacity = 1
                #print(self.text)

            if self.animtype == 0: #movement
                obj = self.associated_object
                
                # if obj.speed == 4:
                #     print("move", self.current_time, self.start_time, self.duration)
                obj.direction = self.rot
                
                obj.prevx = obj.prevx + round((abs(self.endx- obj.prevx)/(self.endx - obj.prevx+0.01)))/8
                obj.prevy = obj.prevy + round((abs(self.endy - obj.prevy)/(self.endy - obj.prevy+0.01)))/8
                if self.associated_object == player:
                    #print(obj.x, obj.y, self.startx, self.starty, self.endx, self.endy)
                    pass
                if frame > self.duration:
                    #print(self.endx, self.endy, obj.x, obj.y, obj.techniquex, obj.techniquey)

                    obj.prevx, obj.prevy, obj.offsetx, obj.offsety = self.endx, self.endy, 0, 0
                    self.should_be_deleted = True
                    if self.associated_object == player:
                        
                        if player.is_shopping == False:
                            if floor.map_grid[floor.height-1-player.y][player.x] == "S":
                                adventure_log.append("Welcome to the shop! Pick up or drop items to buy and sell.")
                                player.is_shopping = True
                        else:
                            if floor.map_grid[floor.height-1-player.y][player.x] != "S":
                                adventure_log.append(str(player.name) + " left the shop.")
                                player.is_shopping = False
                        if rctrl == False:
                            player.pick_up_item(floor.floor_items, adventure_log, floor)


                    wipe_techniqueitem(obj)

            elif self.animtype == 5: #spinning when casting a spell
                obj = self.associated_object
                obj.direction = FaceDirection((obj.direction.value + 1) % 8)
                #obj.current_holding = self.item[0]
                # if frame == 1:
                #     name_desc = get_display_name(self.item)
                #     adventure_log.append(str(obj.name) + " read a " + str(name_desc) + "!")
                #     if obj == player:
                #         discover_item(self.item, adventure_log)


                if frame > self.duration:
                    if self.item[1] == "Tome of Demotion":
                        player.level_visual -= 1
                        player.experience_visual = int(player.level_visual**3)
                        player.maxhealth_visual -= 4
                        player.health_visual -= 4 
                        player.strength_visual -= 1 
                        player.maxstrength_visual -= 1
                        for enemy in floor.all_enemies:
                            enemy.level_visual -= 1
                    elif self.item[1] == "Tome of Promotion": #level up everyone
                        player.level_visual += 1
                        player.experience_visual = int(player.level_visual**3)
                        player.maxhealth_visual += 4
                        player.health_visual += 4 
                        player.strength_visual += 1 
                        player.maxstrength_visual += 1
                        for enemy in floor.all_enemies:
                            enemy.level_visual += 1
                    elif self.item[1] == "Immunity Tome" or self.item[1] == "Paperskin Tome":
                        player.defense_visual = player.defense



                    obj.prevx, obj.prevy, obj.offsetx, obj.offsety = obj.x, obj.y, 0, 0
                    #obj.current_holding = False
                    self.should_be_deleted = True
                    wipe_techniqueitem(obj)





            elif self.animtype == 1: #hit anim
                obj = self.associated_object

                # if obj.speed == 4:
                #     print("hit", self.current_time, self.start_time, self.duration)
                obj.direction = self.rot
                quartic_eq = (-0.19*(0.25*frame)**4 + (0.25*frame)**3 - (0.25*frame)**2)/2.5
                if obj == player:
                    obj.offsetx = round((abs(self.endx - self.startx)/(self.endx - self.startx + 0.01)))*quartic_eq
                    obj.offsety = round((abs(self.endy - self.starty)/(self.endy - self.starty + 0.01)))*quartic_eq
                else:
                    obj.prevx = self.startx + round((abs(self.endx - self.startx)/(self.endx - self.startx + 0.01)))*quartic_eq
                    obj.prevy = self.starty + round((abs(self.endy - self.starty)/(self.endy - self.starty + 0.01)))*quartic_eq
                if frame > self.duration:
                    obj.prevx, obj.prevy, obj.offsetx, obj.offsety = self.startx, self.starty, 0, 0
                    self.should_be_deleted = True
                    wipe_techniqueitem(obj)



            elif self.animtype == 2: #point number
                self.color = (self.color[0], self.color[1], self.color[2], 255)
                base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y =  768/2-24-(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #+768/2-24?
                self.y += 1/32
                if frame == 6:
                    self.proceed = True
                    if self.attacker != None:
                        #check if a death was caused
                        is_dead = 0
                        if self.target.should_be_deleted == True:
                            self.target.invisible_frames = 9999999
                            if isinstance(self.target, Enemy) == True:
                                self.target.drop_item(self.target.current_holding, floor)
                            is_dead = 1
                        if self.attacker == player:
                            #if the player attacked something and it died, update the UI to reflect their new experience amounts
                            if is_dead == 1:
                                self.attacker.experience_visual += self.target.experience
                                new_level = int(self.attacker.experience_visual**(1/3))
                                while new_level>self.attacker.level_visual:
                                    self.attacker.level_visual+= 1
                                    self.attacker.maxhealth_visual += 4
                                    self.attacker.health_visual += 4
                                    self.attacker.strength_visual = 4 + math.floor((7*self.attacker.level)**(1/3))
                                    self.attacker.maxstrength_visual = 4 + math.floor((7*self.attacker.level)**(1/3))
                        elif isinstance(self.attacker, Enemy):
                            if is_dead == 1:
                                self.attacker.level_visual += 1
                                #pass
                                #update attacker sprite to reflect current level
                        self.target.health_visual = self.target.health_visual - self.damage
                        self.target.strength_visual = max(self.target.strength_visual - self.strength_reduction, 1)
                        self.target.defense_visual = max(self.target.defense_visual - self.defense_reduction, 1)
                elif frame > 20:
                    self.color = (self.color[0], self.color[1], self.color[2], random.choice([0, 255]))

                if frame > self.duration:
                    self.color = (0, 0, 0, 0)
                    self.should_be_deleted = True

                sprite = self.sprite
                sprite.color = self.color
                sprite.x = base_x
                sprite.y = base_y
                sprite.scale = self.scale
                
            elif self.animtype == 6: #nonmoving graphical effect (e.g. smoke)

                self.color = (self.color[0], self.color[1], self.color[2], 255)          
                base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y =  768/2-24-(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #+768/2-24?
                if frame > self.duration:
                    self.should_be_deleted = True

                #print(self.spriteindex)
                tile = self.grid[self.spriteindex+(math.floor(self.current_time/self.animspeed) % 4)]
                self.sprite.image.blit_into(tile, 0, 0, 0)

                sprite = self.sprite
                sprite.color = self.color
                sprite.x = base_x
                sprite.y = base_y
                sprite.scale = self.scale
            elif self.animtype == 8: #win condition
                if frame > self.duration:
                    self.should_be_deleted = True
                    player.haswon = True
            elif self.animtype == 7: #liquids

                self.color = (self.color[0], self.color[1], self.color[2], 255)          
                base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y =  768/2-24-(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #+768/2-24?

                if frame == 5 or (frame > self.duration and self.duration <= 5):
                    liquid_char_to_index = ["E", "q", "q", "q", "q", "q", "q", "q", "M", "C", "A", "D", "I", "S", "P", "W"]
                    i = 0
                    while i < 16:
                        bg_liqs_foreground[i].image.blit_into(grid_liqtile[i + liquid_char_to_index.index(self.rot)*16], self.x*16, self.y*16, 0)
                        i = i + 1



                if frame > self.duration:
                    self.should_be_deleted = True


                tile = self.grid[self.spriteindex+(math.floor(self.current_time/self.animspeed) % 2)]
                self.sprite.image.blit_into(tile, 0, 0, 0)

                sprite = self.sprite
                sprite.color = self.color
                sprite.x = base_x
                sprite.y = base_y
                sprite.scale = self.scale
            elif self.animtype == 3 or self.animtype == 4: #thrown item, casted projectile


                self.color = (self.color[0], self.color[1], self.color[2], 255)          
                base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
                base_y =  768/2-24-(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #+768/2-24?

                distance_x = self.endx - self.startx
                distance_y = self.endy - self.starty
                distance_total = max(math.sqrt(distance_x*distance_x + distance_y*distance_y), 0.001)

                distance_x_normalized = distance_x/(distance_total*5)
                distance_y_normalized = distance_y/(distance_total*5)
                
                self.x = self.x + distance_x_normalized
                self.y = self.y + distance_y_normalized
                if frame > self.duration:
                    #self.associated_object.current_holding = False
                    if self.target != None: #for spells
                        #note: the "item" here should be of class Projectile, meaning even if the staff gets deleted it can still access useful info such as the name
                        if self.item.name == "Staff of Lethargy" or self.item.name == "Spores 3" or self.item.name == "Energizing Staff":
                            self.target.speed_visual = self.target.speed
                        if self.item.name == "Staff of Paralysis" or self.item.name == "Spores 4":
                            self.target.paralysis_visual = self.target.paralysis_turns
                        if self.item.name == "Spores 2":
                            self.target.strength_visual = self.target.strength
                        if self.item.name == "Staff of Swapping" or self.item.name == "Staff of Warping":
                            self.target.prevx, self.target.prevy = self.target.x, self.target.y
                            self.target.initx, self.target.inity = self.target.x, self.target.y
                            self.attacker.prevx, self.attacker.prevy = self.attacker.x, self.attacker.y
                            self.attacker.initx, self.attacker.inity = self.attacker.x, self.attacker.y
                        

                if frame > self.duration:
                    self.color = (0, 0, 0, 0)
                    self.should_be_deleted = True
                    if self.item != None:
                        if self.drop_item == True and isinstance(self.item, Item):
                            self.item.x = math.floor(self.x)
                            self.item.y = math.floor(self.y)
                            coords_to_check = [[0, 0], [1, 1], [0, 1], [0, -1], [1, 0], [-1, 0], [1, -1], [0, -1], [-1, -1]]
                            for coords in coords_to_check:
                                x = self.item.x + coords[0]
                                y = self.item.y + coords[1]
                                itemchk = False
                                for i in floor.floor_items:
                                    if i.x == x and i.y == y:
                                        itemchk = True
                                if itemchk == False and (y,x) in floor.valid_tiles:
                                    floor.floor_items.append(self.item)

                                    if self.attacker == player:
                                        if floor.map_grid[floor.height-1-y][x] == "S":
                                            name_desc = get_display_name(self.item)
                                            self.attacker.gold += self.item.price
                                            adventure_log.append(str(self.attacker.name) + " sold " + name_desc + " for " + str(self.item.price) + " gold.")
                                            self.item.price = max(self.item.price+1, 1) #increase price by 1 after selling


                                    self.item.x = x
                                    self.item.y = y 
                                    self.item.color = None
                                    break








                        else:
                            if isinstance(self.item, Item):
                                self.item.sprite.delete()
                                del self.item.sprite
                            del self.item

                if self.animtype == 4:
                    tile = self.grid[self.spriteindex+(math.floor(self.current_time/self.animspeed) % 4)]
                    self.sprite.image.blit_into(tile, 0, 0, 0)
                    # if frame == 1:
                    #     if ("Staff" in item.name)  == True:
                    #         name_desc = get_display_name(self.item)
                    #         adventure_log.append(str(obj.name) + " swung the " + str(name_desc[0]) + "!")
                else:
                    pass
                    # if frame == 1:
                    #     name_desc = get_display_name_and_description(self.item)
                    #     adventure_log.append(str(self.attacker.name) + " threw the " + str(name_desc[0]) + "!")
                sprite = self.sprite
                sprite.color = self.color
                sprite.x = base_x
                sprite.y = base_y
                sprite.scale = self.scale


            # if frame > self.duration: #if the animation has ended...
            #     self.should_be_deleted = True










            # if self.associated_object != None and self.technique != Technique.THROW:
            #     obj = self.associated_object
            #     if self.animtype == 1: #hit anims
            #         if self.item != None:
            #             obj.current_holding = self.item
            #         obj.direction = self.rot
            #         quartic_eq = (-0.19*(0.25*frame)**4 + (0.25*frame)**3 - (0.25*frame)**2)/2.5
            #         if obj == player:
            #             obj.offsetx = round((abs(obj.techniquex - obj.x)/(obj.techniquex - obj.x + 0.01)))*quartic_eq
            #             obj.offsety = round((abs(obj.techniquey - obj.y)/(obj.techniquey - obj.y + 0.01)))*quartic_eq
            #         else:
            #             obj.prevx = obj.x + round((abs(obj.techniquex - obj.x)/(obj.techniquex - obj.x + 0.01)))*quartic_eq
            #             obj.prevy = obj.y + round((abs(obj.techniquey - obj.y)/(obj.techniquey - obj.y + 0.01)))*quartic_eq
            #         if frame > self.duration:
                        
            #             obj.current_holding = False
            #     else:
            #         if self.technique == Technique.CAST:
            #             obj.direction = FaceDirection((obj.direction.value + 1) % 8)
            #             obj.current_holding = self.item#obj.inventory[obj.techniqueitem]
            #         else:
            #             obj.direction = self.rot
            #             obj.prevx = obj.prevx + round((abs(obj.techniquex - obj.prevx)/(obj.techniquex - obj.prevx+0.01)))/8
            #             obj.prevy = obj.prevy + round((abs(obj.techniquey - obj.prevy)/(obj.techniquey - obj.prevy+0.01)))/8
            #         if frame > self.duration:
            #             obj.current_holding = False
            #             if self.associated_object == player:
            #                 player.pick_up_item(floor.floor_items)
            # else:
            #     self.color = (self.color[0], self.color[1], self.color[2], 255)




            #     base_x = 1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
            #     base_y =  768/2-24-(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #+768/2-24?

                
            #     if self.animtype == 1 or self.animtype == 4:


            #         tile = self.grid[self.spriteindex+(math.floor(self.current_time/self.animspeed) % 4)]
            #         self.sprite.image.blit_into(tile, 0, 0, 0)

            #         # # Get texture and set filtering
            #         # texture = tile.get_texture()
            #         # texture.min_filter = pyglet.gl.GL_NEAREST
            #         # texture.mag_filter = pyglet.gl.GL_NEAREST
            #         # # Assign directly — no blitting, no texture creation
            #         # self.sprite.image = texture


            #     elif self.animtype == 2: #point numbers
            #         #print("dwqdwdw")
            #         #base_y =  -(player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale #for some reason, base y alignment is different for letters
            #         self.y += 1/32
                    
            #         if frame == 6:
            #             self.proceed = True
            #             if self.attacker != None:
            #                 #check if a death was caused
            #                 is_dead = 0
            #                 if self.target.should_be_deleted == True:
            #                     self.target.color = (255, 255, 255, 0)
            #                     self.target.sprite.color = (255, 255, 255, 0)
            #                     is_dead = 1
            #                 if self.attacker == player:
            #                     #if the player attacked something and it died, update the UI to reflect their new experience amounts
            #                     if is_dead == 1:
            #                         self.attacker.experience_visual += self.target.experience
            #                         new_level = int(self.attacker.experience_visual**(1/3))
            #                         while new_level>self.attacker.level_visual:
            #                             self.attacker.level_visual+= 1
            #                             self.attacker.maxhealth_visual += 4
            #                             self.attacker.health_visual += 4
            #                             self.attacker.strength_visual += 1
            #                             self.attacker.maxstrength_visual += 1
            #                 else:
            #                     if is_dead == 1:
            #                         self.attacker.level_visual += 1
            #                         #pass
            #                         #update attacker sprite to reflect current level
            #                 self.target.health_visual = self.target.health_visual - self.damage
            #                 self.target.strength_visual = max(self.target.strength_visual - self.strength_reduction, 1)
            #                 self.target.defense_visual = max(self.target.defense_visual - self.defense_reduction, 1)

                            

            #         elif frame > 20:
            #             self.color = (self.color[0], self.color[1], self.color[2], random.choice([0, 255]))
                
                
            #     if self.animtype == 3 or self.animtype == 4: #thrown, casted projectiles
            #         #if self.animtype == 4 and isinstance(self.item, int) == True:
            #             #self.associated_object.current_holding = self.item#self.associated_object.inventory[self.associated_object.techniqueitem]
                    
            #         if frame > self.duration:
            #             #self.associated_object.current_holding = False
            #             if self.target != None: #for spells
            #                 if self.item.name == "Staff of Lethargy" or self.item.name == "Spores 3":
            #                     self.target.speed_visual = self.target.speed
            #                 if self.item.name == "Staff of Paralysis" or self.item.name == "Spores 4":
            #                     self.target.paralysis_visual = self.target.paralysis_turns
            #                 if self.item.name == "Spores 2":
            #                     self.target.strength_visual = self.target.strength
            #                 if self.item.name == "Staff of Swapping":
            #                     self.target.prevx, self.target.prevy = self.target.x, self.target.y
            #                     self.attacker.prevx, self.attacker.prevy = self.attacker.x, self.attacker.y


            #         self.color = (self.color[0], self.color[1], self.color[2], 255)           
            #         distance_x = self.endx - self.startx
            #         distance_y = self.endy - self.starty
            #         distance_total = max(math.sqrt(distance_x*distance_x + distance_y*distance_y), 0.001)

            #         distance_x_normalized = distance_x/(distance_total*5)
            #         distance_y_normalized = distance_y/(distance_total*5)
                    
            #         self.x = self.x + distance_x_normalized
            #         self.y = self.y + distance_y_normalized
                    
                    
                
                


            #     sprite = self.sprite
            #     sprite.color = self.color
            #     sprite.x = base_x
            #     sprite.y = base_y
            #     sprite.scale = self.scale
            #     sprite.group = group
            #     sprite.batch = batch
            # if frame > self.duration:
            #     #delete self
            #     if self.associated_object != None and self.technique != Technique.THROW:
                    
            #         obj.prevx = obj.x 
            #         obj.prevy = obj.y 
            #         obj.offsetx = 0 
            #         obj.offsety = 0
            #     else:
            #         self.color = (self.color[0], self.color[1], self.color[2], 0) #turn transparent
            #         sprite = self.sprite
            #         sprite.color = self.color
            #         sprite.group = group
            #         sprite.batch = batch
            #         if self.item != None:
            #             if self.drop_item == True and isinstance(self.item, Item):
            #                 self.item.x = math.floor(self.x)
            #                 self.item.y = math.floor(self.y)
            #                 coords_to_check = [[0, 0], [1, 1], [0, 1], [0, -1], [1, 0], [-1, 0], [1, -1], [0, -1], [-1, -1]]
            #                 for coords in coords_to_check:
            #                     x = self.item.x + coords[0]
            #                     y = self.item.y + coords[1]
            #                     itemchk = False
            #                     for i in floor.floor_items:
            #                         if i.x == x and i.y == y:
            #                             itemchk = True
            #                     if itemchk == False and (y,x) in floor.valid_tiles:
            #                         floor.floor_items.append(self.item)
            #                         self.item.x = x
            #                         self.item.y = y 
            #                         #self.item.sprite.color = (255, 255, 255, 255) 
            #                         self.item.color = None
            #                         break
            #             else:
            #                 if isinstance(self.item, Item):
            #                     self.item.sprite.delete()
            #                     del self.item.sprite
            #                 del self.item
            #     self.should_be_deleted = True




























