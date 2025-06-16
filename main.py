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
from game_classes.projectiles import *



#from button_object import *
#from shaders import *
has_won = 0
has_lost = 0
window = pyglet.window.Window(1152, 768)

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

from pyglet.graphics import Group
group_bg = Group(order=0)
group_items = Group(order=20)
group_enemies = Group(order=40)

group_overlay = Group(order=45)

group_inv_bg = Group(order=50)
group_inv = Group(order=60)

group_inv_ext = Group(order=65)

group_ui_bg = Group(order=70)
group_ui = Group(order=80)

animation_presets = [
    [0],
    [0, 1, 2, 1, 0, 3, 4, 3],
    [0, 1, 2, 3, 4]

]



letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬"];

all_buttons = []
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

# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     if button == pyglet.window.mouse.LEFT:
#         for button in all_buttons:
#             if button.hovered == True:
#                 button.clicked = True
#             else:
#                 #possibly delete the button
#                 pass
#     elif button == pyglet.window.mouse.RIGHT:
#         for button in all_buttons:
#             if button.hovered == True:
#                 button.clicked = True
#             else:
#                 pass

@window.event
def on_mouse_release(x, y, button, modifiers):
    global all_enemies
    global all_buttons
    global gamestate
    global current_entity_turn
    global floor
    global has_won
    if gamestate == 1 or gamestate == 3 or gamestate == 4 or gamestate == 5: #this stuff can only happen between turns or in inventory
        
        if button == pyglet.window.mouse.LEFT:
            was_button_clicked = 0
            for button in all_buttons:
                button.clicked = False 
                if button.hovered == True:
                    if button.supertype != "overlay":
                        was_button_clicked = 1

                    if button.type == "CANCEL":
                        pass 
                    elif button.type == "MOVE HERE":
                        dirx = button.extra_1
                        diry = button.extra_2
                        player.move(dirx, diry, floor)
                        gamestate = 2
                        partition_entity = construct_partitions()
                    elif button.type == "DROP":
                        player.drop_item(button.extra_1, floor.floor_items)
                        gamestate = 2
                        partition_entity = construct_partitions()
                        delete_buttons_supertype(all_buttons, 'inventory')
                    elif button.type == "CONSUME":
                        player.consume_item(button.extra_1, all_buttons)
                        gamestate = 2
                        partition_entity = construct_partitions()
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
                            has_won = player.spellcasting(button.extra_1, all_enemies, all_buttons, has_won, floor)
                            partition_entity = construct_partitions()
                            
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
                    partition_entity = construct_partitions()
            
            if gamestate == 4 and was_button_clicked == 0:
                mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                player.throw(mouse_x_tilemap, mouse_y_tilemap)
                gamestate = 2
                partition_entity = construct_partitions()

            if gamestate == 5 and was_button_clicked == 0:
                mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                player.cast_projectile(mouse_x_tilemap, mouse_y_tilemap)
                gamestate = 2
                partition_entity = construct_partitions()

            print(gamestate)

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

                if inventory_slot > 0 and len(player.inventory) > inventory_slot:
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

            rclick_options.append("CANCEL")
            rclick_extra_1.append(0)
            rclick_extra_2.append(0)

            print(rclick_options)

            i = 0
            for option in rclick_options:
                spr1 = pyglet.sprite.Sprite(combine_tiles(text_to_tiles_wrapped(option, grid_font, letter_order, 10, "left"), 8, 8, 10))
                spr2 = pyglet.sprite.Sprite(combine_tiles(text_to_background(option, grid_font, letter_order, 10, "left"), 8, 8, 10))
                option_obj = InteractiveObject(
                    x=mouse_x,
                    y=mouse_y - i*8*3,
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
    bg_order = ["#", ".", "*", "~", "@"] #Filler, #Walls, #Space, @Stairs
    bg_tilekey = [wall_texture_value*16 + 8, wall_texture_value*16 + 6, floor_texture_base_value*16+9,floor_texture_base_value*16+7, floor_texture_base_value*16+13]
    for s in floor.map_grid:
        for s2 in s:
            fl_string += s2
else:
    #wall, floor, floorcodes,
    complex_wall_sets = [(12, 31, 4,4,4), (11,28,4,4,4), (17, 25, 0,0,4)]
    #Map Initiation
    bg_order = [
        "#",   #filler
        '.',   #space
        '*',   #space texture
        '~',    #space texture

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

    wall_texture_value, floor_texture_base_value, floor_texture_code_base, floor_texture_code1, floor_texture_code2 = random.choice(complex_wall_sets)
    bg_tilekey = [26*16 + 8, floor_texture_base_value*16+floor_texture_code_base, floor_texture_base_value*16+floor_texture_code1,floor_texture_base_value*16+floor_texture_code2,
                  
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
        wall_texture_value, floor_texture_value = random.choice(simple_color_sets)
        bg_order = ["#", ".", "*", "~", "@"] #Filler, #Walls, #Space, @Stairs
        bg_tilekey = [wall_texture_value*16 + 8, wall_texture_value*16 + 6, floor_texture_value*16+9,floor_texture_value*16+7, floor_texture_value*16+13]
        for s in floor.map_grid:
            for s2 in s:
                fl_string += s2
    else:
        complex_wall_sets = [(12, 31, 4,4,4), (11,28,4,4,4), (17, 25, 0,0,9)]
        #Map Initiation
        bg_order = [
            "#",   #filler
            '.',   #space
            '*',   #space texture
            '~',    #space texture

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

        wall_texture_value, floor_texture_base_value, floor_texture_code_base, floor_texture_code1, floor_texture_code2 = random.choice(complex_wall_sets)

        bg_tilekey = [26*16 + 8, floor_texture_base_value*16+floor_texture_code_base, floor_texture_base_value*16+floor_texture_code1,floor_texture_base_value*16+floor_texture_code2,
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


player.inventory.append(floor.create_item("Blue Staff", grid_items))
player.inventory.append(floor.create_item("Stick", grid_items))
player.inventory.append(floor.create_item("Light Blue Staff", grid_items))
player.inventory.append(floor.create_item("Armor Plate", grid_items))
player.inventory.append(floor.create_item("Gold Staff", grid_items))
player.inventory.append(floor.create_item("Green Staff", grid_items))
player.inventory.append(floor.create_item("Magenta Staff", grid_items))


# Load the music file (supports .mp3, .wav, .ogg, etc.)
music = pyglet.media.load('Cyber-Dream-Loop.mp3')  # Replace with your actual file path

# Create a player and queue the music
mplayer = pyglet.media.Player()
mplayer.queue(music)
mplayer.volume = 0.25  

# Set to loop if desired
mplayer.loop = True

# Play the music
mplayer.play()

sound_hit = pyglet.media.load('hit.mp3', streaming=False)

global keypress_chk
keypress_chk = 0



def construct_partitions():
    global player
    global all_enemies 
    global partition_entity
    global gamestate

    partition_entity = -2 
    #if -2, move all entities that have technique_finished = 0.
    #if -1, do player's technique and only player's technique.
    #else, do technique of partition_entity id.


    if player.techniquefinished == 0: #this means its the very start of turn evaluation
        if player.technique != Technique.MOVE:
            #do this technique
            partition_entity = -1
            
        else:
            #check if all enemies are also moving. if so, move everyone.
            for enemy in all_enemies:
                technique_to_do, techx, techy = enemy.do_AI(all_enemies, player, floor, 0)
                
                enemy.technique = technique_to_do
                enemy.techniquex = techx 
                enemy.techniquey = techy
                if technique_to_do != Technique.MOVE and technique_to_do != Technique.STILL:
                    #not all enemies are moving. as a result, only do the player movement.
                    partition_entity = -1
                    break
                #Added an option for staying still because not everyone is a busy guy

    else: 
        for enemy in all_enemies:
            if enemy.techniquefinished == 0:
                technique_to_do, techx, techy = enemy.do_AI(all_enemies, player, floor, 1)
                enemy.technique = technique_to_do
                enemy.techniquex = techx 
                enemy.techniquey = techy
                if technique_to_do != Technique.MOVE and technique_to_do != Technique.STILL:
                    #do this technique
                    partition_entity = all_enemies.index(enemy)
                    break

        #this last loop will check if all enemies have had a turn. if so, break out of turn execution.
        alldone_flag = 1
        if partition_entity == -2:
            for enemy in all_enemies:
                if enemy.techniquefinished == 0:
                    alldone_flag = 0
                    break
        
            if alldone_flag == 1:
                player.techniquefinished = 0
                player.techniqueframe = 0
                player.offsetx = 0
                player.offsety = 0
                for enemy in all_enemies:
                    enemy.techniquefinished = 0
                    enemy.techniqueframe = 0
                gamestate = 1


    #print(partition_entity)
    return partition_entity

                
    

    
    
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

    window.clear()

    diry = 0
    dirx = 0

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

        if dirx == 0 and diry == 0 and keys[pyglet.window.key.E] == False:
            keypress_chk = 0
    else:
        if gamestate == 2 or keys[pyglet.window.key.W] or keys[pyglet.window.key.S] or keys[pyglet.window.key.A] or keys[pyglet.window.key.D] or keys[pyglet.window.key.E] or keys[pyglet.window.key.ESCAPE]:
            pass
        else:
            keypress_chk = 0
    
    if diry != 0 or dirx != 0:
        #keypress_chk = 1
        player.move(dirx, diry, floor)
        gamestate = 2
        partition_entity = construct_partitions()
        #current_entity_turn = -1

    if gamestate == 2:
        if partition_entity == -1:
            print(f"{floor.stairs} HERE IS FLOOR STAIRS")
            #if doing only the player's turn...
            tech = player.technique

            if keys[pyglet.window.key.Q]:
                while player.techniquefinished != 1:
                    player.process_turn(all_enemies, player, all_buttons, floor)
            else:
                player.process_turn(all_enemies, player, all_buttons, floor)
            
            if partition_entity == -1 and player.techniquefinished == 1:
                if tech == Technique.HIT:
                    sound_hit.play()
                print(f"{floor.stairs} HERE IS FLOOR STAIRS")
                print(player.x, player.y)
                if (player.x, player.y) == floor.stairs:
                    print("on stairs GOING TO NEXT LEVEL")
                    go_to_next_level()
                partition_entity = construct_partitions()
        elif partition_entity == -2: #if doing all movement...

            is_allfinished_flag = 1

            if player.techniquefinished == 0:

                if keys[pyglet.window.key.Q]:
                    while player.techniquefinished != 1:
                        player.process_turn(all_enemies, player, all_buttons, floor)
                else:
                    player.process_turn(all_enemies, player, all_buttons, floor)
                    
                if player.techniquefinished == 0:
                    is_allfinished_flag = 0

            for enemy in all_enemies:
                if enemy.techniquefinished == 0:
                    if keys[pyglet.window.key.Q] or ((enemy.techniquex > player.x + 10 or enemy.techniquex < player.x - 10) and (enemy.techniquey > player.y + 6 or enemy.techniquey < player.y + 6)):
                        while enemy.techniquefinished != 1:
                            enemy.process_turn(all_enemies, player, all_buttons, floor)
                    else:
                        enemy.process_turn(all_enemies, player, all_buttons, floor)
                    is_allfinished_flag = 0

            if is_allfinished_flag == 1:
                print(f"{floor.stairs} HERE IS FLOOR STAIRS")
                if(player.x, player.y) == floor.stairs:
                    print("on stairs GOING TO NEXT LEVEL")
                    go_to_next_level()
                partition_entity = construct_partitions()
        else:
            
            enemy_to_evaluate = all_enemies[partition_entity]
            if keys[pyglet.window.key.Q] or ((enemy_to_evaluate.techniquex > player.x + 10 or enemy_to_evaluate.techniquex < player.x - 10) and (enemy_to_evaluate.techniquey > player.y + 6 or enemy_to_evaluate.techniquey < player.y + 6)):
                
                while enemy_to_evaluate.techniquefinished != 1:
                    enemy_to_evaluate.process_turn(all_enemies, player, all_buttons, floor)
                partition_entity = construct_partitions()
            else:
                tech = enemy_to_evaluate.technique
                enemy_to_evaluate.process_turn(all_enemies, player, all_buttons, floor)
                if enemy_to_evaluate.techniquefinished == 1:
                    if tech == Technique.HIT:
                        sound_hit.play()
                    partition_entity = construct_partitions()


            # if player.technique == "n/a":
            #     gamestate = 1

    bg.x = 1152/2 - (player.prevx*16 + 8)*player.scale
    bg.y = 768/2 - (player.prevy*16 + 8)*player.scale

    bg.batch = batch

    #sprite.image = texture
    player.draw(batch, animation_presets, group_enemies)
    for enemy in all_enemies:
        enemy.draw(batch, animation_presets, player, group_enemies)

    for item in floor.floor_items:
        item.draw(batch, player, group_items)

    for item in player.active_projectiles:
        item.draw_projectiles(batch, player, group_items)

    for spell in player.active_spells:
        spell.draw(batch, player, group_items)

    i = 0 #theres probably a more pythonic way to do this, sowwy
    for item in player.inventory:
        item.draw_inventory(batch, player, group_inv, i, gamestate)
        i = i + 1



    for button in all_buttons:
        if button == -1:
            all_buttons.remove(button)
        else:
            button.hovered = button.is_mouse_over(mouse_x, mouse_y)

            button.draw(batch, group_ui_bg, group_ui, group_inv_bg, group_inv, group_overlay)

            if button.type == "GUI_HP":
                if has_won == 1:
                    player.health = 999
                    player.maxhealth = 999
                    gui_string = get_gui_string(player) + " " + str("WINNER!")
                else:
                    gui_string = get_gui_string(player)

                
                sprite = button.sprites[1]
                sprite.image = combine_tiles(text_to_tiles_wrapped(gui_string, grid_font, letter_order, len(gui_string)+1, "left"), 8, 8, len(gui_string)+1)
            elif button.type == "POINT_NUMBER":
                button.y += 1
                if button.animframe > 20:
                    if button.colors[0][0][3] == 255:
                        button.colors[0][0] = (button.colors[0][0][0], button.colors[0][0][1], button.colors[0][0][2], 0)
                    else:
                        button.colors[0][0] = (button.colors[0][0][0], button.colors[0][0][1], button.colors[0][0][2], 255)
                if button.animframe > 45:
                    delete_buttons_specific(all_buttons, button)
            elif button.type == "SMOKE CLOUD":
                if button.animframe > 20:
                    if button.colors[0][0][3] == 255:
                        button.colors[0][0] = (button.colors[0][0][0], button.colors[0][0][1], button.colors[0][0][2], 0)
                    else:
                        button.colors[0][0] = (button.colors[0][0][0], button.colors[0][0][1], button.colors[0][0][2], 255)
                if button.animframe > 45:
                    delete_buttons_specific(all_buttons, button)

            elif button.type == "overlay":
                if gamestate == 3:
                    button.colors = [[(33, 33, 33, 90), (33, 33, 33, 90), (33, 33, 33, 90)]]
                else:
                    button.colors = [[(33, 33, 33, 0), (33, 33, 33, 0), (33, 33, 33, 0)]]
            elif button.type == "mouse_overlay":
                if gamestate == 1 or gamestate == 2 or gamestate == 4 or gamestate == 5: 
                    button.colors = [[(33, 33, 33, 90), (33, 33, 33, 90), (33, 33, 33, 90)]]
                    # button.x = math.floor((mouse_x - 12)/48)*48 
                    # button.y = math.floor((mouse_y - 12)/48)*48

                    #print(math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5)), math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5)))

                    button.x = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))*16*3 + 1152/2 - (player.prevx*16 + 8)*player.scale
                    button.y = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))*16*3 + 768/2 - (player.prevy*16+8)*player.scale + 16
                else:
                    button.colors = [[(33, 33, 33, 0), (33, 33, 33, 0), (33, 33, 33, 0)]]
            
            
            


    batch.draw()
    




pyglet.app.run()


