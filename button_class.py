
import pyglet
import math
import image_handling
import game_classes.map

sprite_font = pyglet.image.load('font.png')
columns_font = sprite_font.width // 8
rows_font = sprite_font.height // 8
grid_font = pyglet.image.ImageGrid(sprite_font, rows_font, columns_font)

sprite_tinyfont = pyglet.image.load('tinyfont.png')
columns_tinyfont = sprite_tinyfont.width // 5
rows_tinyfont = sprite_tinyfont.height // 8
grid_tinyfont = pyglet.image.ImageGrid(sprite_tinyfont, rows_tinyfont, columns_tinyfont)

sprite_bg = pyglet.image.load('bgtiles.png')
columns_bg = sprite_bg.width // 16
rows_bg = sprite_bg.height // 16
grid_bg = pyglet.image.ImageGrid(sprite_bg, rows_bg, columns_bg)

sprite_items = pyglet.image.load('items_and_fx.png')
columns_items = sprite_items.width // 16
rows_items = sprite_items.height // 16
grid_items = pyglet.image.ImageGrid(sprite_items, rows_items, columns_items)

letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬", "", "", "", "", "", "", "", "", "ä"];



class InteractiveObject:
    def __init__(self, x, y, width, height, sprites, colors, animtype, animmod, text, obj_type, extra_1, extra_2, supertype,
                 alignment_x='left', alignment_y='bottom',
                 depth=0, draggable=False, rot=0, scale=3):
        
        # Position and alignment
        self.x = x
        self.y = y
        self.alignment_x = alignment_x  # 'left', 'center', 'right'
        self.alignment_y = alignment_y  # 'bottom', 'center', 'top'

        # Sprite visuals
        self.sprites = sprites  # List of pyglet.sprite.Sprite
        self.colors = colors #list of colors for each sprite. 3 colors to use for static, hovered over, and clicked states. 
        self.animtype = animtype #list of animation 'types' for sprites. pulls from a set library of animation behaviors.
        self.animframe = 0 #what frame of the animation it's on
        self.animmod = animmod #a preset animation modifier (e.g. vibration amplitude)
        self.text = text

        self.rotation = rot
        self.scale = scale
            

        # Interaction and logic
        self.depth = depth
        self.type = obj_type
        self.width = width
        self.height = height
        self.draggable = draggable
        self.being_dragged = False
        self.hovered = False
        self.clicked = False
        self.supertype = supertype
        self.should_be_deleted = False

        self.extra_1 = extra_1
        self.extra_2 = extra_2



    def get_screen_position(self):
        """Compute the on-screen position based on alignment."""
        x = self.x
        y = self.y

        if self.alignment_x == 'center':
            x -= self.width // 2
        elif self.alignment_x == 'right':
            x -= self.width

        if self.alignment_y == 'center':
            y -= self.height // 2
        elif self.alignment_y == 'top':
            y -= self.height

        return x, y
    
    def is_mouse_over(self, mouse_x, mouse_y):
        """Check if a point is within this object's interactive bounds."""
        base_x, base_y = self.get_screen_position()
        #print(mouse_x, mouse_y, base_x, base_y)
        return (base_x <= mouse_x <= base_x + self.width*self.scale and
                base_y <= mouse_y <= base_y + self.height*self.scale)
    
    def draw(self, batch, group1, group2, group3, group4, group5, group6, player):
        global grid_items
        
        base_x, base_y = self.get_screen_position()

        for i, sprite in enumerate(self.sprites):
            #sprite.z = 100
            sprite.x = base_x
            sprite.y = base_y
            sprite.scale = self.scale

            self.animframe = self.animframe + 1

            if self.hovered == True:
                if self.clicked == True:
                    sprite.color = self.colors[i][2]
                else:
                    sprite.color = self.colors[i][1]
            else:
                sprite.color = self.colors[i][0]
            
            if self.type == "power bar":
                speed = 2
                func = ((self.animframe - 0.0001)/speed % self.extra_2) #self.extra_2*(math.asin(((self.animframe/(math.pi*3)) % 2) - 1) + math.pi/2)/math.pi
                #t = func
                if ((self.animframe - 0.0001)/speed % (self.extra_2*2)) > self.extra_2 and func != self.extra_2:
                    func = -func + self.extra_2

                
                if self.extra_1 > func:
                    sprite.color = (self.colors[i][0][0], self.colors[i][0][1], self.colors[i][0][2], 0)
                else:
                    sprite.color = (self.colors[i][0][0], self.colors[i][0][1], self.colors[i][0][2], 255)


            if self.supertype == 'rclick': #draw rclick buttons on top of other menus
                if i == 0:
                    sprite.group = group1
                else:
                    sprite.group = group2
            elif self.supertype == "overlay" or self.type == "power bar 2":
                sprite.group = group5
            else:
                if self.type == 'equip sword':
                    sprite.group = group6
                    if player.equipment_weapon == None:
                        sprite.color = (0, 189, 66, 0)
                    else:
                        sprite.color = (0, 189, 66, 255)
                        id = player.inventory.index(player.equipment_weapon)
                        inventory_x = id % 10
                        inventory_y = id // 10
                        self.x = inventory_x*48 + int(1152/48)*12
                        self.y = -inventory_y*48 + int(768/48)*32 - 1

                elif self.type == 'equip shield':
                    sprite.group = group6
                    if player.equipment_shield == None:
                        sprite.color = (0, 189, 66, 0)
                    else:
                        sprite.color = (0, 189, 66, 255)
                        id = player.inventory.index(player.equipment_shield)
                        inventory_x = id % 10
                        inventory_y = id // 10
                        self.x = inventory_x*48 + int(1152/48)*12
                        self.y = -inventory_y*48 + int(768/48)*32 - 1



                elif i == 0:
                    sprite.group = group3
                else:
                    sprite.group = group4
            sprite.batch = batch


            #sprite.draw()


def delete_buttons_supertype(all_buttons, supertype):
    #supertypes:
        #'rclick'
        #'inventory'
    for button in all_buttons: #delete all buttons
        if button.supertype == supertype:
            button.should_be_deleted = True

def delete_buttons_specific(all_buttons, button):
    button.should_be_deleted = True



def create_power_bar(all_buttons, item, x, y):
    global grid_font
    charges = item.charges
    maxcharges = item.maxcharges
    #power bar should be ~48 px wide. if a section is over 7 px width, set to 7 px width
    width_per_bar = min(4, math.ceil(48/maxcharges))


    tile = grid_font[112 + 8 - (width_per_bar-1)]
    spr = pyglet.sprite.Sprite(tile)

    tile2 = grid_font[112 + 8 - (width_per_bar)]
    spr2 = pyglet.sprite.Sprite(tile)
    #spr2.yscale = spr2.yscale*10/8

    i = 0
    while i < maxcharges:
        if i < charges:
            if i == 0:
                color = (36, 221, 185, 255) #lowest charge
            elif i == charges - 1:
                color = (255, 0, 0, 255) #highest charge
            elif i < charges/3:
                color = (97, 226, 142, 255)
            elif i < 2*charges/3:
                color = (223, 255, 0, 255)
            else:
                color = (255, 191, 0, 255)
        else:
            color = (98, 98, 98, 255)
        all_buttons.append(InteractiveObject(
            x=x+(i*width_per_bar)*3, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
            y=y, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
            width=int(spr.width),
            height=int(spr.height),
            sprites=[pyglet.sprite.Sprite(tile)],
            colors=[[color, color, color]],
            animtype = [0],
            animmod = [None],
            text = [None],
            alignment_x='left',
            alignment_y='top',
            depth=1,
            obj_type="power bar",
            draggable=False,
            supertype = "power bar",
            extra_1 = i,
            extra_2 = maxcharges
        ))

        color2 = (33, 33, 33, 255)
        all_buttons.append(InteractiveObject(
            x=x+(i*width_per_bar - 1)*3, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
            y=y-3, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
            width=int(spr2.width),
            height=int(spr2.height),
            sprites=[pyglet.sprite.Sprite(tile2)],
            colors=[[color2, color2, color2]],
            animtype = [0],
            animmod = [None],
            text = [None],
            alignment_x='left',
            alignment_y='top',
            depth=1,
            obj_type="power bar 2",
            draggable=False,
            supertype = "power bar",
            extra_1 = 0,
            extra_2 = 0
        ))

        all_buttons[len(all_buttons)-1].sprites[0].scale_y = all_buttons[len(all_buttons)-1].sprites[0].scale_y*(10/8)

        i = i + 1
    spr.delete()
    del spr
    spr2.delete()
    del spr2





def create_inventory_menu(all_buttons):
    global grid_font
    global letter_order
    color = (255, 255, 255)
    w = int((1152)/48)
    h = int((768)/48)
    txt = ""
    txt = txt.zfill(w*h)
    sprite_inv = pyglet.image.load('inventory.png')
    # combined = pyglet.image.Texture.create(190, 76)

    # combined.blit_into(sprite_inv, 0, 0, 0)



    spr2 = pyglet.sprite.Sprite(sprite_inv)
    obj = InteractiveObject(
        x=0 + 24*(w/2), #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
        y=48*4.5+ 24*(h/2), #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
        width=spr2.width,
        height=spr2.height,
        sprites=[spr2],
        colors=[[color, color, color]],
        animtype = [0],
        animmod = [None],
        text = [None],
        alignment_x='left',
        alignment_y='top',
        depth=1,
        obj_type="MENU BG",
        draggable=False,
        supertype = "inventory",
        extra_1 = 0,
        extra_2 = 0
    )
    all_buttons.append(obj)

    spr3 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles("E", grid_font, letter_order), 8, 8, 2))
    color2 = (0, 0, 0, 0)
    obj = InteractiveObject(
        x=0, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
        y=0, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
        width=spr3.width,
        height=spr3.height,
        sprites=[spr3],
        colors=[[color2, color2, color2]],
        animtype = [0],
        animmod = [None],
        text = [None],
        alignment_x='left',
        alignment_y='top',
        depth=1,
        obj_type="equip sword",
        draggable=False,
        supertype = "inventory",
        extra_1 = 0,
        extra_2 = 0
    )
    all_buttons.append(obj)
    spr4 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles("E", grid_font, letter_order), 8, 8, 2))
    obj = InteractiveObject(
        x=0, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
        y=0, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
        width=spr4.width,
        height=spr4.height,
        sprites=[spr4],
        colors=[[color2, color2, color2]],
        animtype = [0],
        animmod = [None],
        text = [None],
        alignment_x='left',
        alignment_y='top',
        depth=1,
        obj_type="equip shield",
        draggable=False,
        supertype = "inventory",
        extra_1 = 0,
        extra_2 = 0
    )
    all_buttons.append(obj)



    
def create_win_lose_screen(all_buttons, winlose):
    global grid_font
    global letter_order
    color = (255, 255, 255)
    color2 = (33, 33, 33, 90)
    w = int((1152)/24)
    h = int((768)/24)
    txt = ""
    txt = txt.zfill(w*h)

    txt2 = ""
    if winlose == "win":
        txt2 = "You won!"
    else:
        txt2 = "You lost..."

    txt2 = txt2 + "εPANDORIUMεMade by zeroBound & EconicεMusic: Cyber Dream Loopεby Eric Matyasεwww.soundimage.orgεPress TAB to quit.εä εä εä εä εä εä εä εä εä εä"
    
    spr1 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles_wrapped(txt2, grid_font, letter_order, w, "center"), 8, 8, w))
    spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_background(txt, grid_font, letter_order, w, "left"), 8, 8, w))
    obj = InteractiveObject(
        x=0, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
        y=48*6 - 32, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
        width=spr2.width,
        height=spr2.height,
        sprites=[spr2, spr1],
        colors=[[color2, color2, color2], [color, color, color]],
        animtype = [0, 0],
        animmod = [None, None],
        text = [None, None],
        alignment_x='left',
        alignment_y='top',
        depth=1,
        obj_type="menu stuff",
        draggable=False,
        supertype = "winlose",
        extra_1 = 0,
        extra_2 = 0
    )
    all_buttons.append(obj)



def create_overlay(all_buttons):
    global grid_bg

    color = (33, 33, 33, 0)
    w = int((1152)/48)
    h = int((768)/48)
    txt = ""
    txt = txt.zfill(w*h)
    spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_floor(txt, grid_bg, ["0", "1"], [25*16, 0], w), 16, 16, w))
    obj = InteractiveObject(
        x=0, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
        y=48*6 - 32, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
        width=spr2.width,
        height=spr2.height,
        sprites=[spr2],
        colors=[[color, color, color]],
        animtype = [0],
        animmod = [None],
        text = [None],
        alignment_x='left',
        alignment_y='top',
        depth=1,
        obj_type="overlay",
        draggable=False,
        supertype = "overlay",
        extra_1 = 0,
        extra_2 = 0
    )
    all_buttons.append(obj)



def create_mouse_overlay(all_buttons):
    global grid_bg

    color = (33, 33, 33, 0)
    w = int((1152)/48)
    h = int((768)/48)
    txt = "0"
    spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_floor(txt, grid_bg, ["0", "1"], [25*16, 0], w), 16, 16, w))
    obj = InteractiveObject(
        x=0, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
        y=48*6 - 32, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
        width=spr2.width,
        height=spr2.height,
        sprites=[spr2],
        colors=[[color, color, color]],
        animtype = [0],
        animmod = [None],
        text = [None],
        alignment_x='left',
        alignment_y='top',
        depth=1,
        obj_type="mouse_overlay",
        draggable=False,
        supertype = "overlay",
        extra_1 = 0,
        extra_2 = 0
    )
    all_buttons.append(obj)





# def create_point_number(x, y, text, color, player, all_buttons):
#     global grid_font 
#     global letter_order
#     spr1 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles_wrapped(str(text), grid_font, letter_order, 10, "left"), 8, 8, 10))
#     #spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_background(hp_string, grid_font, letter_order, 10, "left"), 8, 8, 10))
#     obj = InteractiveObject(
#         x=1152/2 -24 - (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
#         y=768/2 - (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
#         width=spr1.width,
#         height=spr1.height,
#         sprites=[spr1],
#         colors=[[color, color, color]],
#         animtype = [0],
#         animmod = [None],
#         text = [None],
#         alignment_x='left',
#         alignment_y='top',
#         depth=1,
#         obj_type="POINT_NUMBER",
#         draggable=False,
#         supertype = "graphics",
#         extra_1 = 0,
#         extra_2 = 0
#     )
#     all_buttons.append(obj)

# def create_graphical_effect(x, y, color, player, all_buttons):
#     global grid_items 
#     global letter_order
#     spr1 = image_handling.create_sprite(grid_items, 29 + 4*color)
#     #spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_background(hp_string, grid_font, letter_order, 10, "left"), 8, 8, 10))
#     obj = InteractiveObject(
#         x=1152/2 -24 - (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
#         y=768/2 - (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
#         width=spr1.width,
#         height=spr1.height,
#         sprites=[spr1],
#         colors=[[(255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255)]],
#         animtype = [0],
#         animmod = [None],
#         text = [None],
#         alignment_x='left',
#         alignment_y='top',
#         depth=1,
#         obj_type="SMOKE CLOUD",
#         draggable=False,
#         supertype = "graphics",
#         extra_1 = 0,
#         extra_2 = 0
#     )
#     all_buttons.append(obj)

def get_gui_string(player):
    strength = str(player.strength)
    defense = str(player.defense)

    if player.equipment_shield != None:
        defense = defense + "+" + str(player.equipment_shield.defense)
    if player.equipment_weapon != None:
        if player.equipment_shield != None:
            if player.equipment_shield.name != "Armor Plate":
                strength = strength + "+" + str(player.equipment_weapon.damage)
        else:
            strength = strength + "+" + str(player.equipment_weapon.damage)

    #stats gui
    gui_string = str(player.health_visual) + "/" + str(player.maxhealth_visual) + " HP, " + str(strength) + "/" + str(player.maxstrength) + " STR, " + str(defense) + "/" + str(player.maxdefense) + " DEF, LV " + str(player.level_visual) + ", " + str(player.experience_visual) + " EXP"
    return gui_string


def create_gui(all_buttons, player):
    global grid_font 
    global letter_order
    gui_string = get_gui_string(player)
    spr1 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles_wrapped(gui_string, grid_font, letter_order, len(gui_string), "left"), 8, 8, len(gui_string)+1))
    spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_background((gui_string+"______"), grid_font, letter_order, len(gui_string)+7, "left"), 8, 8, len(gui_string)+7))
    option_obj = InteractiveObject(
        x=24,
        y=768-16,
        width=spr2.width,
        height=spr2.height,
        sprites=[spr2, spr1],
        colors=[[(33, 33, 33, 90), (33, 33, 33, 90), (33, 33, 33, 90)], [(255, 255, 255, 255), (255, 255, 255, 255), (255, 255, 255, 255)]],
        animtype = [0, 0],
        animmod = [None, None],
        text = [None, None],
        alignment_x='left',
        alignment_y='top',
        depth=1,
        obj_type="GUI_HP",
        draggable=False,
        supertype = "none",
        extra_1 = player.health,
        extra_2 = player.maxhealth
    )
    all_buttons.append(option_obj)

