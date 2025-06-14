




import pyglet
import math
from image_handling import *
from button_class import *
from game_classes.player import *
from game_classes.face_direction import *
#from game_classes.enemy import *
from game_classes.item import *
#from game_classes.map import *




#from button_object import *
#from shaders import *

window = pyglet.window.Window()

#pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
#pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

gamestate = 1
current_entity_turn = -1


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


]


letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬"];

string_to_draw = "The quick brown fox jumpeeeeeeeeeeeed over the lazy dog. This is the story of a man named Stanley. Stanley worked for a company at an office where he sat in room 427. etc etc buttons"
tiles_to_draw = text_to_tiles_wrapped(string_to_draw, grid_font, letter_order, 20, "center")
bg_to_draw = text_to_background(string_to_draw, grid_font, letter_order, 20, "center")

combined_image = combine_tiles(tiles_to_draw, 8, 8, 20)
combined_image_2 = combine_tiles(bg_to_draw, 8, 8, 20)

mysprite = pyglet.sprite.Sprite(combined_image, x=0, y=0)
mysprite2 = pyglet.sprite.Sprite(combined_image_2, x=0, y=0)



player = Player(
    name = "Damien",
    health = 20,
    level = 1,
    x = 2,
    y = 2,
    sprite = create_sprite(grid_entities1, 20*8*8),
    spriteindex = 20*8*8,
    color = (255, 255, 255, 255),
    animtype = 1,
    animmod = 1/8,
    animframe = 0,
)


item = Item(
    name = "Kitchen Knife",
    grid_items = grid_items,
    x = 8,
    y = 8,
    inventory_slot = -1,
    quantity = 1,
)








batch = pyglet.graphics.Batch()

all_buttons = []
all_items = [item]

mouse_x = 0
mouse_y = 0

keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)



@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

@window.event
def on_mouse_press(x, y, button, modifiers):
    if pyglet.window.mouse.LEFT:
        for button in all_buttons:
            if button.hovered == True:
                button.clicked = True
            else:
                #possibly delete the button
                pass
    elif pyglet.window.mouse.RIGHT:
        for button in all_buttons:
            if button.hovered == True:
                button.clicked = True
            else:
                pass

@window.event
def on_mouse_release(x, y, button, modifiers):
    if pyglet.window.mouse.LEFT:
        for button in all_buttons:
            button.clicked = False
            if button.hovered == True:
                pass
            else:
                pass
    elif pyglet.window.mouse.RIGHT:
        for button in all_buttons:
            button.clicked = False
            if button.hovered == True:

                rclick_options = []
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
                for item in all_items:
                    if item.is_mouse_over(mouse_x, mouse_y):
                        rclick_options.append("EXAMINE")
                        if item.inventory_slot != -1:
                            rclick_options.append("USE")
                            rclick_options.append("THROW")


                rclick_options.append("CANCEL")


                my_object = InteractiveObject(
    x=100,
    y=200,
    width=mysprite2.width,
    height=mysprite2.height,
    sprites=[mysprite2, mysprite],
    colors=[[(168, 168, 168, 255), (98, 98, 98, 255), (54, 54, 54, 255)], [(98, 98, 98, 255), (54, 54, 54, 255), (33, 33, 33, 255)]],
    animtype = [0, 0],
    animmod = [None, None],
    text = [None, None],
    alignment_x='center',
    alignment_y='top',
    depth=1,
    obj_type="label",
    draggable=True,
    custom_data={"label": "Click me!"}
)
                








                pass
            else:
                pass

# @window.event
# def on_key_press(symbol, modifiers):
#     diry = 0
#     dirx = 0

#     if symbol == pyglet.window.key.W:
#         diry = 1
#     elif symbol == pyglet.window.key.S:
#         diry = -1

#     if symbol == pyglet.window.key.D:
#         dirx = 1
#     elif symbol == pyglet.window.key.A:
#         dirx = -1
    
#     if diry != 0 or dirx != 0:
#         #initiate start of a turn.
#         player.move(dirx, diry)




#0 = main menu
#1 = your turn in the game world
#2 = turn is happening
#3 = inventory?
#4 = pause menu?

global keypress_chk
keypress_chk = 0

@window.event
def on_draw():
    global keypress_chk
    global gamestate
    global current_entity_turn
    window.clear()

    for button in all_buttons:
        button.hovered = button.is_mouse_over(mouse_x, mouse_y)
        button.draw(batch)

    for item in all_items:
        item.draw(batch)


    diry = 0
    dirx = 0

    #if keypress_chk == 0:

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
        current_entity_turn = -1


    if gamestate == 2:
        if current_entity_turn == -1:
            current_entity_turn = player.process_turn(current_entity_turn)
        else:
            gamestate = 1

    # print(gamestate)
    # print(current_entity_turn)
    # print(player.x)
    # print(player.y)
    # print(player.prevx)
    # print(player.prevy)
    # print(keypress_chk)



    player.draw(batch, grid_entities1, animation_presets)
    batch.draw()
    




    # texture = sprite_sheet.get_texture();
    # pyglet.glEnable(texture.GL_TEXTURE_2D)        # typically target is GL_TEXTURE_2D
    # pyglet.glBindTexture(texture.GL_TEXTURE_2D, texture.id)










# In your input events:
# @window.event
# def on_mouse_press(x, y, button, modifiers):
#     my_object.on_mouse_press(x, y, button, modifiers)

# @window.event
# def on_mouse_release(x, y, button, modifiers):
#     my_object.on_mouse_release(x, y, button, modifiers)

# @window.event
# def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
#     my_object.on_mouse_drag(x, y, dx, dy, buttons, modifiers)

pyglet.app.run()


