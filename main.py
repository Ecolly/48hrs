import pyglet
import math
from image_handling import *
from button_class import *
from game_classes.player import *
from game_classes.face_direction import *
from game_classes.techniques import *
from game_classes.enemy import *
#from game_classes.item import *
from game_classes.map import *
from game_classes.item import Weapon, Consumable
from game_classes.item import Item

import turn_logic
import delete_object


pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

#made by zero and eco :)


#from button_object import *
#from shaders import *
has_won = 0
has_lost = 0
config = pyglet.gl.Config(double_buffer=True, sample_buffers=0, samples=0)
window = pyglet.window.Window(1152, 768, config=config)

#pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
#pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

gamestate = 1
partition_entity = -2
floor_level = 1
#current_entity_turn = -1


sprite_font = pyglet.image.load('font.png')
columns_font = sprite_font.width // 8
rows_font = sprite_font.height // 8
grid_font = pyglet.image.ImageGrid(sprite_font, rows_font, columns_font)

sprite_tinyfont = pyglet.image.load('tinyfont.png')
columns_tinyfont = sprite_tinyfont.width // 5
rows_tinyfont = sprite_tinyfont.height // 8
grid_tinyfont = pyglet.image.ImageGrid(sprite_tinyfont, rows_tinyfont, columns_tinyfont)

sprite_entities1 = pyglet.image.load('entities_level1.png')
columns_entities1 = sprite_entities1.width // 16
rows_entities1 = sprite_entities1.height // 16
grid_entities1 = pyglet.image.ImageGrid(sprite_entities1, rows_entities1, columns_entities1)

sprite_entities2 = pyglet.image.load('entities_level2.png')
columns_entities2 = sprite_entities2.width // 16
rows_entities2 = sprite_entities2.height // 16
grid_entities2 = pyglet.image.ImageGrid(sprite_entities2, rows_entities2, columns_entities2)

sprite_entities3 = pyglet.image.load('entities_level3.png')
columns_entities3 = sprite_entities3.width // 16
rows_entities3 = sprite_entities3.height // 16
grid_entities3 = pyglet.image.ImageGrid(sprite_entities3, rows_entities3, columns_entities3)

sprite_entities4 = pyglet.image.load('entities_level4.png')
columns_entities4 = sprite_entities4.width // 16
rows_entities4 = sprite_entities4.height // 16
grid_entities4 = pyglet.image.ImageGrid(sprite_entities4, rows_entities4, columns_entities4)

sprite_items = pyglet.image.load('items_and_fx.png')
columns_items = sprite_items.width // 16
rows_items = sprite_items.height // 16
grid_items = pyglet.image.ImageGrid(sprite_items, rows_items, columns_items)

sprite_bg = pyglet.image.load('bgtiles.png')
columns_bg = sprite_bg.width // 16
rows_bg = sprite_bg.height // 16
grid_bg = pyglet.image.ImageGrid(sprite_bg, rows_bg, columns_bg)

# def enemy_grid_to_use(level):
#     global grid_entities1 
#     global grid_entities2
#     global grid_entities3
#     global grid_entities4
#     if level < 2:
#         return grid_entities1
#     elif level == 2:
#         return grid_entities2
#     elif level == 3:
#         return grid_entities3
#     else:
#         return grid_entities4

from pyglet.graphics import Group
group_bg = Group(order=0)
group_items = Group(order=20)
group_enemies = Group(order=40)

group_effects = Group(order=42)

group_overlay = Group(order=45)

group_inv_bg = Group(order=50)
group_inv = Group(order=60)

group_inv_ext = Group(order=65)

group_ui_bg = Group(order=70)
group_ui = Group(order=80)

animation_presets = [
    [0],
    [0, 1, 2, 1, 0, 3, 4, 3],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4, 5, 6, 7]
]



letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬", "ä"];

all_buttons = []
all_anims = []

#floor_items = [item]
inventory_items = []

# string_to_draw = "The quick brown fox jumpeeeeeeeeeeeed over the lazy dog. This is the story of a man named Stanley. Stanley worked for a company at an office where he sat in room 427. etc etc buttons"
# tiles_to_draw = text_to_tiles_wrapped(string_to_draw, grid_font, letter_order, 20, "center")
# bg_to_draw = text_to_background(string_to_draw, grid_font, letter_order, 20, "center")

# combined_image = combine_tiles(tiles_to_draw, 8, 8, 20)
# combined_image_2 = combine_tiles(bg_to_draw, 8, 8, 20)

# mysprite = pyglet.sprite.Sprite(combined_image, x=0, y=0)
# mysprite2 = pyglet.sprite.Sprite(combined_image_2, x=0, y=0)

# my_object = InteractiveObject(
#     x=100,
#     y=200,
#     width=mysprite2.width,
#     height=mysprite2.height,
#     sprites=[mysprite2, mysprite],
#     colors=[[(168, 168, 168, 255), (98, 98, 98, 255), (54, 54, 54, 255)], [(98, 98, 98, 255), (54, 54, 54, 255), (33, 33, 33, 255)]],
#     animtype = [None, None],
#     animmod = [None, None],
#     text = [None, None],
#     alignment_x='center',
#     alignment_y='top',
#     depth=1,
#     obj_type="label",
#     draggable=True,
#     extra_1 = 0,
#     extra_2 = 0,
#     rclick = 0
# )
# all_buttons.append(my_object)





player = Player(
    name = "DAMIEN",
    health = 20,
    level = 1,
    experience = 0,
    x = 30,
    y = 30,
    sprite = create_sprite(grid_entities1, 20*8*8),
    spritegrid = grid_entities1,
    spriteindex = 20*8*8,
    color = (255, 255, 255, 255),
    animtype = 1,
    animmod = 1/8,
    animframe = 0,
)




batch = pyglet.graphics.Batch()



mouse_x = 0
mouse_y = 0

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)

mouse_state = pyglet.window.mouse.MouseStateHandler()
window.push_handlers(mouse_state)

@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

@window.event
def on_mouse_press(x, y, button, modifiers):
    global all_buttons
    global gamestate
    if button == pyglet.window.mouse.LEFT:

        if gamestate == 5:
            gamestate = 6 #6 means power bar mode
            create_power_bar(all_buttons, player.inventory[player.techniqueitem], mouse_x, mouse_y)
 
# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     pass
    # global dragging_item, drag_offset
    # for slot in inventory:
    #     if slot.item and slot.item.hit_test(x, y):
    #         dragging_item = slot.item
    #         drag_offset = (x - slot.x, y - slot.y)
    #         slot.item = None
    #         break

# @window.event
# def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#     pass
    # if dragging_item:
    #     dragging_item.sprite.x = x - drag_offset[0]
    #     dragging_item.sprite.y = y - drag_offset[1]


@window.event
def on_mouse_release(x, y, button, modifiers):
    global all_anims
    global all_enemies
    global all_buttons
    global gamestate
    global current_entity_turn
    global floor
    global has_won
    global sound_magic
    if gamestate == 1 or gamestate == 3 or gamestate == 4 or gamestate == 5 or gamestate == 6: #this stuff can only happen between turns or in inventory
        print("mouse release", button, x, y)
        if button == pyglet.window.mouse.LEFT:
            
            was_button_clicked = 0
            for button in all_buttons:
                button.clicked = False 
                if button.hovered == True:
                    if button.supertype != "overlay" and button.supertype != "power bar" and button.supertype != "power bar 2":
                        was_button_clicked = 1

                    if button.type == "CANCEL":
                        pass 
                    elif button.type == "MOVE HERE":
                        dirx = button.extra_1
                        diry = button.extra_2
                        player.move(dirx, diry, floor)
                        gamestate = 2
                        #partition_entity = construct_partitions()
                    elif button.type == "DROP":
                        player.drop_item(button.extra_1, floor.floor_items)
                        gamestate = 2

                        all_anims = turn_logic.do_turns(all_enemies, player, floor)
                        #partition_entity = construct_partitions()
                        delete_buttons_supertype(all_buttons, 'inventory')
                    elif button.type == "CONSUME":
                        player.technique = Technique.CONSUME 
                        player.techniqueitem = button.extra_1
                        gamestate = 2
                        all_anims = turn_logic.do_turns(all_enemies, player, floor)
                        #partition_entity = construct_partitions()
                        delete_buttons_supertype(all_buttons, 'inventory')
                    elif button.type == "EQUIP": #Equipping/unequipping doesnt take up a turn
                        if isinstance(player.inventory[button.extra_1], Weapon) == True:
                            player.equip_weapon(player.inventory[button.extra_1])
                        else:
                          player.equip_shield(player.inventory[button.extra_1])
                    elif button.type == "UNEQUIP":
                        if isinstance(player.inventory[button.extra_1], Weapon) == True:
                            player.unequip_weapon()
                        else:
                            player.unequip_shield()
                    elif button.type == "THROW": #if throwing, switch to a "choose target" GUI with a different gamestate.
                        gamestate = 4
                        player.techniqueitem = button.extra_1
                        delete_buttons_supertype(all_buttons, 'inventory')
                        pass
                    elif button.type == "CAST":
                        player.techniqueitem = button.extra_1
                        if player.inventory[button.extra_1].is_castable_projectile == True:
                            gamestate = 5
                        else:
                            gamestate = 2
                            player.cast_static()
                            #has_won = player.spellcasting(button.extra_1, all_enemies, all_buttons, has_won, floor, sound_magic, gamestate)
                            all_anims = turn_logic.do_turns(all_enemies, player, floor)

                            if has_won == 0:
                                #partition_entity = construct_partitions()
                                pass
                            else:
                                gamestate = 0
                                create_win_lose_screen(all_buttons, "win")

                
                            
                        delete_buttons_supertype(all_buttons, 'inventory')



                        #next_entity_turn = 0
                        #current_entity_turn, next_entity_turn = construct_partitions(current_entity_turn, next_entity_turn)
            delete_buttons_supertype(all_buttons, 'rclick')
            #print(gamestate, was_button_clicked)
            if gamestate == 1 and was_button_clicked == 0:
                mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                if (mouse_x_tilemap != player.prevx or mouse_y_tilemap != player.prevy) and player.prevx - 2 < mouse_x_tilemap < player.prevx + 2 and player.prevy - 2 < mouse_y_tilemap < player.prevy + 2:
                    player.hit(mouse_x_tilemap, mouse_y_tilemap)
                    gamestate = 2
                    all_anims = turn_logic.do_turns(all_enemies, player, floor)

            
            if gamestate == 4 and was_button_clicked == 0:
                mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                player.throw(mouse_x_tilemap, mouse_y_tilemap)
                gamestate = 2
                all_anims = turn_logic.do_turns(all_enemies, player, floor)
                


            if gamestate == 6 and was_button_clicked == 0: #button was released; check powerbar values

                for button2 in all_buttons:
                    if button2.type == "power bar":
                        speed = 2
                        func = ((button2.animframe - 0.0001)/speed % button2.extra_2) #self.extra_2*(math.asin(((self.animframe/(math.pi*3)) % 2) - 1) + math.pi/2)/math.pi
                        #t = func
                        if ((button2.animframe - 0.0001)/speed % (button2.extra_2*2)) > button2.extra_2 and func != button2.extra_2:
                            func = -func + button2.extra_2
                        button2.animframe = -24
                        #num of charges = func
                player.techniquecharges = max(round(func), 1)
                if func > player.inventory[button.extra_1].charges: #if num of charges exceeds amount remaining, just choose a random amount
                    func = random.randint(1, player.inventory[button.extra_1].charges)
                mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                player.cast(mouse_x_tilemap, mouse_y_tilemap)
                gamestate = 7 #gamestate 7 is when power bar flashes, showing you what result you made it to
                




        elif button == pyglet.window.mouse.RIGHT:
            delete_buttons_supertype(all_buttons, 'rclick')
            #get rclick options
            rclick_options = []
            rclick_extra_1 = []
            rclick_extra_2 = []
            #check what's here, such as...
            # 
            #   a button (e.g. in the case of a menu)
            #   a blank space near the player 
            #   an item
            #   an enemy
            #   an exit
            #   you
            # 
            #  
            # for item in floor_items:
            #     if item.is_mouse_over(mouse_x, mouse_y):
            #         rclick_options.append("EXAMINE")
            #         if item.inventory_slot != -1:
            #             rclick_options.append("USE")
            #             rclick_options.append("THROW")
            if gamestate == 1:
                mouse_x_tilemap = mouse_x/48 - (1152/2)/48 + (player.x + 0.5)
                mouse_y_tilemap = mouse_y/48 - (768/2)/48 + (player.y + 0.5)
                if player.prevx - 1 < mouse_x_tilemap < player.prevx + 2 and player.prevy - 1 < mouse_y_tilemap < player.prevy + 2:
                    rclick_options.append("MOVE HERE")
                    rclick_extra_1.append(math.floor(mouse_x_tilemap - player.x))
                    rclick_extra_2.append(math.floor(mouse_y_tilemap - player.y))
                    print(math.floor(mouse_x_tilemap - player.x))
                    print(math.floor(mouse_y_tilemap - player.y))
            elif gamestate == 3:
                inventory_x = math.floor((mouse_x - int((1152)/48)*12)/48) 
                inventory_y = math.floor((-mouse_y + int((768)/48)*32)/48) + 1
                inventory_slot = inventory_y*10 + inventory_x
                
                #print(inventory_slot, player.inventory)

                if inventory_slot > -1 and len(player.inventory) > inventory_slot:
                    item_to_eval = player.inventory[inventory_slot]

                    rclick_options.append("DROP")
                    rclick_extra_1.append(inventory_slot)
                    rclick_extra_2.append(0)

                    rclick_options.append("THROW")
                    rclick_extra_1.append(inventory_slot)
                    rclick_extra_2.append(0)

                    if item_to_eval.is_equipable == True:
                        if player.equipment_weapon == item_to_eval or player.equipment_shield == item_to_eval:
                            rclick_options.append("UNEQUIP")
                        else:
                            rclick_options.append("EQUIP")

                        rclick_extra_1.append(inventory_slot)
                        rclick_extra_2.append(0)

                    if item_to_eval.is_consumable == True:
                        rclick_options.append("CONSUME")
                        rclick_extra_1.append(inventory_slot)
                        rclick_extra_2.append(0)

                    if item_to_eval.is_castable == True:
                        rclick_options.append("CAST")
                        rclick_extra_1.append(inventory_slot)
                        rclick_extra_2.append(0)

                    if item_to_eval.is_usable == True:
                        rclick_options.append("USE")
                        rclick_extra_1.append(inventory_slot)
                        rclick_extra_2.append(0)

                    #rclick_extra_2.append(math.floor(mouse_y_tilemap - player.y))

                #print(inventory_x, inventory_y, inventory_slot)
                #pass

            print(rclick_options)
            rclick_extra_1.append(0)
            rclick_extra_2.append(0)

            print(rclick_options)

            i = 0
            for option in rclick_options:
                spr1 = pyglet.sprite.Sprite(combine_tiles(text_to_tiles_wrapped(option, grid_font, letter_order, 10, "left"), 8, 8, 10))
                spr2 = pyglet.sprite.Sprite(combine_tiles(text_to_background(option, grid_font, letter_order, 10, "left"), 8, 8, 10))
                option_obj = InteractiveObject(
                    x=mouse_x,
                    y=mouse_y - i*8*3-16,
                    width=spr2.width,
                    height=spr2.height,
                    sprites=[spr2, spr1],
                    colors=[[(168, 168, 168, 255), (98, 98, 98, 255), (54, 54, 54, 255)], [(98, 98, 98, 255), (54, 54, 54, 255), (33, 33, 33, 255)]],
                    animtype = [0, 0],
                    animmod = [None, None],
                    text = [None, None],
                    alignment_x='left',
                    alignment_y='top',
                    depth=1,
                    obj_type=option,
                    draggable=False,
                    supertype = 'rclick',
                    extra_1 = rclick_extra_1[i],
                    extra_2 = rclick_extra_2[i]
                )
                all_buttons.append(option_obj)
                i = i + 1


floor = make_floor()
floor.random_create_item(grid_items)
floor.generate_enemies(grid_entities1, floor_level)
all_enemies = floor.all_enemies
print(f"BEFORE{player.x, player.y}")
player.x, player.y = floor.spawnpoint
player.prevx, player.prevy = floor.spawnpoint
print(player.x, player.y)
print(floor.map_type)

fl_string = ""
if floor.map_type == "Simple":
    #Simple Map Initiation
    simple_color_sets = [(26,26), (29,29), (27,27)]
    wall_texture_value, floor_texture_base_value = random.choice(simple_color_sets)
    bg_order = ["#", ".", "*", "~", '%', '<', '>', "@"] #Filler, #Walls, #Space, @Stairs
    bg_tilekey = [wall_texture_value*16 + 8, wall_texture_value*16 + 6, floor_texture_base_value*16+9, floor_texture_base_value*16+7, floor_texture_base_value*16, floor_texture_base_value*16, floor_texture_base_value*16+1, floor_texture_base_value*16+13]
    for s in floor.map_grid:
        for s2 in s:
            fl_string += s2
else:
    #wall, floor, floorcodes,
    complex_wall_sets = [(12, 31, 4,4,4,4,4,4), (22,30,2,2,10,2,2,2), (21,31,1,9,10,11,0,3), (17, 24, 5,5+32,5+48,5+64,5+80,5+96)]
    #Map Initiation
    bg_order = [
        "#",   #filler
        '.',   #space
        '*',   #space texture
        '~',    #space texture
        '%',
        '<',
        '>',

    'a',   # 0: isolated
    'b',   # 1: up
    'c',   # 2: right
    'd',   # 3: up + right

    'e',   # 4: down
    'f',   # 5: up + down
    'g',  # 6: right + down
    'h',   # 7: up + right + down

    'i',   # 8: left
    'j',   # 9: up + left
    'k',   # 10: right + left
    'l',   # 11: up + right + left
    
    'm',  # 12: down + left
    'n',   # 13: up + down + left
    'o',   # 14: right + down + left
    'p',   # 15: all sides

        "@"    # stairs
    ]

    wall_texture_value, floor_texture_base_value, floor_texture_code_base, floor_texture_code1, floor_texture_code2, floor_texture_code3, floor_texture_code4, floor_texture_code5, = random.choice(complex_wall_sets)
    bg_tilekey = [26*16 + 8, floor_texture_base_value*16+floor_texture_code_base, floor_texture_base_value*16+floor_texture_code1,floor_texture_base_value*16+floor_texture_code2,floor_texture_base_value*16+floor_texture_code3, floor_texture_base_value*16+floor_texture_code4, floor_texture_base_value*16+floor_texture_code5,
                  
                wall_texture_value*16, wall_texture_value*16+15, wall_texture_value*16+13, wall_texture_value*16+9,
                wall_texture_value*16+12, wall_texture_value*16+8, wall_texture_value*16+6, wall_texture_value*16+2,
                wall_texture_value*16+14, wall_texture_value*16+11, wall_texture_value*16+10, wall_texture_value*16+5,
                wall_texture_value*16+7, wall_texture_value*16+4, wall_texture_value*16+1,wall_texture_value*16+3,
                floor_texture_base_value*16+13]
    
    for s in floor.textured_map:
        for s2 in s:
            fl_string += s2
#bg = pyglet.sprite.Sprite(combine_tiles(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60))
bg = pyglet.sprite.Sprite(combine_tiles(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60))
bg.scale = 3
bg.z = 0

def go_to_next_level():
    global floor, all_enemies, player, bg, floor_level
    floor_level +=1
    print(floor_level)
    #Triggered after Detects stairs
    floor = make_floor()
    floor.random_create_item(grid_items)
    floor.generate_enemies(grid_entities1, floor_level)
    print(f"BEFORE{player.x, player.y}")
    player.x, player.y = floor.spawnpoint
    player.prevx, player.prevy = floor.spawnpoint
    all_enemies = floor.all_enemies
    #floor_level +=1
    print(floor.map_type)

    fl_string = ""
    if floor.map_type == "Simple":
        #Simple Map Initiation
        simple_color_sets = [(26,26), (29,29), (27,27)]
        wall_texture_value, floor_texture_base_value = random.choice(simple_color_sets)
        bg_order = ["#", ".", "*", "~", '%', '<', '>', "@"] #Filler, #Walls, #Space, @Stairs
        bg_tilekey = [wall_texture_value*16 + 8, wall_texture_value*16 + 6, floor_texture_base_value*16+9, floor_texture_base_value*16+7, floor_texture_base_value*16, floor_texture_base_value*16, floor_texture_base_value*16+1, floor_texture_base_value*16+13]
       
        for s in floor.map_grid:
            for s2 in s:
                fl_string += s2
    else:
        #wall, floor, floorcodes,
        complex_wall_sets = [(12, 31, 4,4,4,4,4,4), (22,30,2,2,10,2,2,2), (21,31,1,9,10,11,0,3), (17, 24, 5,5+32,5+48,5+64,5+80,5+96)]
        #Map Initiation
        bg_order = [
            "#",   #filler
            '.',   #space
            '*',   #space texture
            '~',    #space texture
            '%',
            '<',
            '>',

        'a',   # 0: isolated
        'b',   # 1: up
        'c',   # 2: right
        'd',   # 3: up + right

        'e',   # 4: down
        'f',   # 5: up + down
        'g',  # 6: right + down
        'h',   # 7: up + right + down

        'i',   # 8: left
        'j',   # 9: up + left
        'k',   # 10: right + left
        'l',   # 11: up + right + left
        
        'm',  # 12: down + left
        'n',   # 13: up + down + left
        'o',   # 14: right + down + left
        'p',   # 15: all sides

            "@"    # stairs
        ]

        wall_texture_value, floor_texture_base_value, floor_texture_code_base, floor_texture_code1, floor_texture_code2, floor_texture_code3, floor_texture_code4, floor_texture_code5, = random.choice(complex_wall_sets)
        bg_tilekey = [26*16 + 8, floor_texture_base_value*16+floor_texture_code_base, floor_texture_base_value*16+floor_texture_code1,floor_texture_base_value*16+floor_texture_code2,floor_texture_base_value*16+floor_texture_code3, floor_texture_base_value*16+floor_texture_code4, floor_texture_base_value*16+floor_texture_code5,
                    
                    wall_texture_value*16, wall_texture_value*16+15, wall_texture_value*16+13, wall_texture_value*16+9,
                    wall_texture_value*16+12, wall_texture_value*16+8, wall_texture_value*16+6, wall_texture_value*16+2,
                    wall_texture_value*16+14, wall_texture_value*16+11, wall_texture_value*16+10, wall_texture_value*16+5,
                    wall_texture_value*16+7, wall_texture_value*16+4, wall_texture_value*16+1,wall_texture_value*16+3,
                    floor_texture_base_value*16+13]
        
        for s in floor.textured_map:
            for s2 in s:
                fl_string += s2
    #bg = pyglet.sprite.Sprite(combine_tiles(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60))
    bg = pyglet.sprite.Sprite(combine_tiles(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60))
    bg.scale = 3
    bg.z = 0







create_gui(all_buttons, player)
create_overlay(all_buttons)
create_mouse_overlay(all_buttons)


# player.inventory.append(floor.create_item("Blue Staff", grid_items))
# player.inventory.append(floor.create_item("Stick", grid_items))
# player.inventory.append(floor.create_item("Light Blue Staff", grid_items))
# player.inventory.append(floor.create_item("Armor Plate", grid_items))
player.inventory.append(floor.create_item("Red Staff", grid_items))
player.inventory.append(floor.create_item("Orange Staff", grid_items))
player.inventory.append(floor.create_item("Gold Staff", grid_items))
player.inventory.append(floor.create_item("Green Staff", grid_items))
player.inventory.append(floor.create_item("Rock", grid_items))
player.inventory.append(floor.create_item("Starfruit", grid_items))

# player.inventory.append(floor.create_item("Magenta Staff", grid_items))


# Load the music file (supports .mp3, .wav, .ogg, etc.)
music = pyglet.media.load('Cyber-Dream-Loop.mp3')  # Replace with your actual file path

# Create a player and queue the music
mplayer = pyglet.media.Player()
mplayer.queue(music)
mplayer.volume = 0#.25  

# Set to loop if desired
mplayer.loop = True

# Play the music
mplayer.play()

sound_hit = pyglet.media.load('hit.mp3', streaming=False)
sound_magic = pyglet.media.load('magic.mp3', streaming=False)

global keypress_chk
keypress_chk = 0

    

    
    
    # while next_entity_turn < len(all_enemies):
    #     if all_enemies[next_entity_turn].name == "GOOSE":
            

    #     elif all_enemies[next_entity_turn].name == "FOX":

        

    #     next_entity_turn += 1
















#0 = main menu
#1 = your turn in the game world
#2 = turn is happening
#3 = inventory?
#4 = pause menu?

@window.event
def on_draw():
    global keypress_chk
    global gamestate
    global partition_entity
    global all_buttons
    global has_won
    global all_anims

    window.clear()

    diry = 0
    dirx = 0


    # mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
    # mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
    
    # print (mouse_x_tilemap, mouse_y_tilemap)

    # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
    # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
    if keys[pyglet.window.key.TAB] and keypress_chk == 0:
        #enter main menu
        # if gamestate == 1:
        #     keypress_chk = 1
        #     create_main_menu(all_buttons)
        #     gamestate = 0
        if gamestate == 0:
            exit()
            keypress_chk = 1
            gamestate = 1
            delete_buttons_supertype(all_buttons, 'winlose')
    if keys[pyglet.window.key.E] and keypress_chk == 0:
        #enter inventory
        if gamestate == 1:
            keypress_chk = 1
            create_inventory_menu(all_buttons)
            gamestate = 3

            #enter inventory
        elif gamestate == 3:
            keypress_chk = 1
            gamestate = 1
            delete_buttons_supertype(all_buttons, 'inventory')

            #exit inventory
    elif gamestate == 1:

        if keys[pyglet.window.key.W]:
            diry = 1
        elif keys[pyglet.window.key.S]:
            diry = -1

        if keys[pyglet.window.key.D]:
            dirx = 1
        elif keys[pyglet.window.key.A]:
            dirx = -1

        if dirx == 0 and diry == 0 and keys[pyglet.window.key.E] == False and keys[pyglet.window.key.TAB] == False:
            keypress_chk = 0

        if player.is_alive() == False:
            gamestate = 0
            create_win_lose_screen(all_buttons, "lose")
    else:
        if gamestate == 2 or keys[pyglet.window.key.W] or keys[pyglet.window.key.S] or keys[pyglet.window.key.A] or keys[pyglet.window.key.D] or keys[pyglet.window.key.E] or keys[pyglet.window.key.TAB]:
            pass
        else:
            keypress_chk = 0
    
    if diry != 0 or dirx != 0:
        #keypress_chk = 1
        player.move(dirx, diry, floor)
        gamestate = 2
        all_anims = turn_logic.do_turns(all_enemies, player, floor)

        #partition_entity = construct_partitions()
        #current_entity_turn = -1

    if gamestate == 2:
        if len(all_anims) == 0 or all(anim.proceed for anim in all_anims):
            gamestate = 1
            if(player.x, player.y) == floor.stairs:
                print("on stairs GOING TO NEXT LEVEL")
                go_to_next_level()

    bg.x = 1152/2 - (player.prevx*16 + 8)*player.scale
    bg.y = 768/2 - (player.prevy*16 + 8)*player.scale

    bg.batch = batch

    #sprite.image = texture
    player.draw(batch, animation_presets, group_enemies)
    for enemy in all_enemies:
        enemy.draw(batch, animation_presets, player, group_enemies)

    for item in floor.floor_items:
        item.draw(batch, player, group_items)

    # for item in player.active_projectiles:
    #     item.draw_projectiles(batch, player, group_items)

    # for spell in player.active_spells:
    #     spell.draw(batch, player, group_items)

    i = 0 #theres probably a more pythonic way to do this, sowwy
    for item in player.inventory:
        item.draw_inventory(batch, player, group_inv, i, gamestate)
        i = i + 1

    if keys[pyglet.window.key.Q]:
        while len(all_anims) > 0:
            for anim in all_anims:
                anim.draw(batch, player, group_effects, floor)
            delete_object.delobj(all_anims)
    else:
        for anim in all_anims:
            anim.draw(batch, player, group_effects, floor)
        delete_object.delobj(all_anims)


    if gamestate != 2:
        delete_object.delobj(all_enemies)
    
    delete_object.delobj(floor.floor_items)
    # delete_object.delobj(player.active_projectiles)
    delete_object.delobj(all_anims)
    delete_object.delobj(player.inventory)
    delete_object.delobj(all_buttons)

    for button in all_buttons:
        button.hovered = button.is_mouse_over(mouse_x, mouse_y)

        button.draw(batch, group_ui_bg, group_ui, group_inv_bg, group_inv, group_overlay, group_inv_ext, player, gamestate)

        if button.type == "GUI_HP":
            if has_won == 1:
                player.health = 999
                player.maxhealth = 999

            gui_string = get_gui_string(player)
            sprite = button.sprites[1]
            sprite.image = combine_tiles(text_to_tiles_wrapped(gui_string, grid_font, letter_order, len(gui_string)+1, "left"), 8, 8, len(gui_string)+1)
        elif button.type == "overlay":
            if gamestate == 3:
                button.colors = [[(33, 33, 33, 90), (33, 33, 33, 90), (33, 33, 33, 90)]]
            else:
                button.colors = [[(33, 33, 33, 0), (33, 33, 33, 0), (33, 33, 33, 0)]]
        elif button.type == "mouse_overlay":
            if gamestate == 1 or gamestate == 2 or gamestate == 4 or gamestate == 5: 
                button.colors = [[(33, 33, 33, 90), (33, 33, 33, 90), (33, 33, 33, 90)]]
                button.x = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))*16*3 + 1152/2 - (player.prevx*16 + 8)*player.scale
                button.y = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))*16*3 + 768/2 - (player.prevy*16+8)*player.scale + 16
            else:
                button.colors = [[(33, 33, 33, 0), (33, 33, 33, 0), (33, 33, 33, 0)]]
        elif button.supertype == "power bar":
            
            if gamestate != 6 and gamestate != 7:
                button.should_be_deleted = True
            if gamestate == 7 and button.animframe == 1:
                
                all_anims = turn_logic.do_turns(all_enemies, player, floor)
                gamestate = 2


                
            


    batch.draw()
    




pyglet.app.run()


