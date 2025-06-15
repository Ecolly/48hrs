




import pyglet
import math
from image_handling import *
from button_class import *
from game_classes.player import *
from game_classes.face_direction import *
from game_classes.enemy import *
#from game_classes.item import *
from game_classes.map import *
from game_classes.item import Weapon, Consumable
from game_classes.item import Item




#from button_object import *
#from shaders import *

window = pyglet.window.Window(1152, 768)

#pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
#pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

gamestate = 1
partition_entity = -2
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


animation_presets = [
    [0],
    [0, 1, 2, 1, 0, 3, 4, 3],
    [0, 1, 2, 3, 4]

]


letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬"];


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
#     custom_data={"label": "Click me!"}
# )






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

all_enemies = []

all_enemies.append(generate_enemy("GOOSE", 1, 29, 29, grid_entities1))
all_enemies.append(generate_enemy("GOOSE", 1, 30, 25, grid_entities1))
all_enemies.append(generate_enemy("GOOSE", 1, 25, 30, grid_entities1))

all_enemies.append(generate_enemy("FOX", 1, 25, 34, grid_entities1))
all_enemies.append(generate_enemy("FOX", 1, 30, 32, grid_entities1))



batch = pyglet.graphics.Batch()

all_buttons = []
#floor_items = [item]
inventory_items = []

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
    global all_buttons
    global gamestate
    global current_entity_turn
    if gamestate == 1: #this stuff can only happen between turns
        if button == pyglet.window.mouse.LEFT:
            for button in all_buttons:
                button.clicked = False 
                if button.hovered == True:
                    if button.type == "CANCEL":
                        pass 
                    elif button.type == "MOVE HERE":

                        
                        dirx = button.extra_1
                        diry = button.extra_2

                        player.move(dirx, diry)
                        gamestate = 2
                        current_entity_turn = -1
                        #next_entity_turn = 0
                        #current_entity_turn, next_entity_turn = construct_partitions(current_entity_turn, next_entity_turn)
            
            for button in all_buttons: #delete all buttons
                if button != -1 and button.rclick == True:
                    for sprite in button.sprites:
                        sprite.delete()
                        del sprite
                    id = all_buttons.index(button)
                    del button
                    all_buttons[id] = -1

        elif button == pyglet.window.mouse.RIGHT:
            for button in all_buttons: #delete all buttons (ew duplicate code, move to a function?)
                if button != -1 and button.rclick == True:
                    for sprite in button.sprites:
                        sprite.delete()
                        del sprite
                    id = all_buttons.index(button)
                    del button
                    all_buttons[id] = -1

                # button.clicked = False
                # if button.hovered == True:
                #     pass
                # else:
                #     pass


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

            mouse_x_tilemap = mouse_x/48 - (1152/2)/48 + (player.x + 0.5)
            mouse_y_tilemap = mouse_y/48 - (768/2)/48 + (player.y + 0.5)


            if player.prevx - 1 < mouse_x_tilemap < player.prevx + 2 and player.prevy - 1 < mouse_y_tilemap < player.prevy + 2:
                rclick_options.append("MOVE HERE")
                rclick_extra_1.append(math.floor(mouse_x_tilemap - player.x))
                rclick_extra_2.append(math.floor(mouse_y_tilemap - player.y))
                print(math.floor(mouse_x_tilemap - player.x))
                print(math.floor(mouse_y_tilemap - player.y))
                


            rclick_options.append("CANCEL")
            rclick_extra_1.append(0)
            rclick_extra_2.append(0)

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
                    rclick = True,
                    extra_1 = rclick_extra_1[i],
                    extra_2 = rclick_extra_2[i]
                )
                all_buttons.append(option_obj)
                i = i + 1






bg_order = ["#", "o", "."]
bg_tilekey = [26*16 + 8, 26*16 + 8, 26*16+6]
floor = make_floor()
fl_string = ""
for s in floor.map_grid:
    for s2 in s:
        fl_string += s2
bg = pyglet.sprite.Sprite(combine_tiles(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60))
bg.scale = 3
bg.z = 0




    # gui_hp.x = 0
    # gui_hp.y = 768 - 24
    # gui_hp.batch = batch

hp_string = str(player.health) + "/" + str(player.maxhealth) + " HP"

spr1 = pyglet.sprite.Sprite(combine_tiles(text_to_tiles_wrapped(hp_string, grid_font, letter_order, 10, "left"), 8, 8, 10))
spr2 = pyglet.sprite.Sprite(combine_tiles(text_to_background(hp_string, grid_font, letter_order, 10, "left"), 8, 8, 10))
option_obj = InteractiveObject(
    x=24,
    y=768-16,
    width=spr2.width,
    height=spr2.height,
    sprites=[spr2, spr1],
    colors=[[(0, 112, 234, 255), (0, 112, 234, 255), (0, 112, 234, 255)], [(33, 33, 33, 255), (33, 33, 33, 255), (33, 33, 33, 255)]],
    animtype = [0, 0],
    animmod = [None, None],
    text = [None, None],
    alignment_x='left',
    alignment_y='top',
    depth=1,
    obj_type="GUI_HP",
    draggable=False,
    rclick = False,
    extra_1 = player.health,
    extra_2 = player.maxhealth
)
all_buttons.append(option_obj)




# gui_hp_2 = pyglet.sprite.Sprite(combine_tiles(text_to_background(option, grid_font, letter_order, 10, "left"), 8, 8, 10))
# gui_hp = pyglet.sprite.Sprite(combine_tiles(text_to_tiles(, grid_font, letter_order), 8, 8, 20))
# gui_hp.scale = 3
# gui_hp.z = 70
# gui_hp.color = (33, 33, 33, 255)







floor_items = []  # List to hold items on the floor

def create_item(name):
    # Example dummy factory
    if name == "Iron Sword":
        return Weapon(name, grid_items, sprite_locs = 0, damage=10, durability=100)
    elif name == "Health Potion":
        return Consumable(name, grid_items, sprite_locs = 2, nutrition_value=20)
    
list_of_all_item_names = ["Iron Sword", "Health Potion"]

#self, name, grid_items, x, y, quantity
for _ in range(3):  # Generate 3 items
    random_location = random.choice(floor.valid_tiles)
    x, y = random_location
    item_name = random.choice(list_of_all_item_names)
    item = create_item(item_name)
    item.x = x
    item.y = y
    floor_items.append(item)
    print(f"Created item: {item.name} at ({x}, {y})")




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
        if player.technique != "move":
            #do this technique
            partition_entity = -1
            
        else:
            #check if all enemies are also moving. if so, move everyone.
            for enemy in all_enemies:
                technique_to_do, techx, techy = enemy.do_AI(all_enemies, player)
                enemy.technique = technique_to_do
                enemy.techniquex = techx 
                enemy.techniquey = techy
                if technique_to_do != "move":
                    #not all enemies are moving. as a result, only do the player movement.
                    partition_entity = -1
                    break

    else:
        for enemy in all_enemies:
            if enemy.techniquefinished == 0:
                technique_to_do, techx, techy = enemy.do_AI(all_enemies, player)
                enemy.technique = technique_to_do
                enemy.techniquex = techx 
                enemy.techniquey = techy
                if technique_to_do != "move":
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
    
    window.clear()

    diry = 0
    dirx = 0

    if keys[pyglet.window.key.E] and keypress_chk == 0:
        #enter inventory
        if gamestate == 1:
            keypress_chk = 1

            #enter inventory
        elif gamestate == 3:
            keypress_chk = 1
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
    else:
        if gamestate == 2 or keys[pyglet.window.key.W] or keys[pyglet.window.key.S] or keys[pyglet.window.key.A] or keys[pyglet.window.key.D] or keys[pyglet.window.key.E] or keys[pyglet.window.key.ESCAPE]:
            pass
        else:
            keypress_chk = 0
    
    if diry != 0 or dirx != 0:
        #keypress_chk = 1
        player.move(dirx, diry)
        gamestate = 2
        partition_entity = construct_partitions()
        #current_entity_turn = -1

    if gamestate == 2:
        if partition_entity == -1:
            #if doing only the player's turn...

            player.process_turn()
            if partition_entity == -1 and player.techniquefinished == 1:
                partition_entity = construct_partitions()
        elif partition_entity == -2: #if doing all movement...

            is_allfinished_flag = 1

            if player.techniquefinished == 0:
                player.process_turn()
                if player.techniquefinished == 0:
                    is_allfinished_flag = 0

            for enemy in all_enemies:
                if enemy.techniquefinished == 0:
                    enemy.process_turn(all_enemies, player)
                    is_allfinished_flag = 0

            if is_allfinished_flag == 1:
                partition_entity = construct_partitions()
        else:

            enemy_to_evaluate = all_enemies[partition_entity]
            enemy_to_evaluate.process_turn(all_enemies, player)
            if enemy_to_evaluate.techniquefinished == 1:
                partition_entity = construct_partitions()


            # if player.technique == "n/a":
            #     gamestate = 1

    bg.x = 1152/2 - (player.prevx*16 + 8)*player.scale
    bg.y = 768/2 - (player.prevy*16 + 8)*player.scale

    bg.batch = batch


    #sprite.image = texture

    for button in all_buttons:
        if button == -1:
            all_buttons.remove(button)
        else:
            button.hovered = button.is_mouse_over(mouse_x, mouse_y)
            if button.type == "GUI_HP":
                hp_string = str(player.health) + "/" + str(player.maxhealth) + " HP"
                sprite = button.sprites[1]
                sprite.image = combine_tiles(text_to_tiles_wrapped(hp_string, grid_font, letter_order, 10, "left"), 8, 8, 10)
            button.draw(batch)

    player.draw(batch, animation_presets)
    for enemy in all_enemies:
        enemy.draw(batch, animation_presets, player)
    for item in floor_items:
        print(item.x, item.y)
        item.draw(batch, player)
    batch.draw()
    




pyglet.app.run()


