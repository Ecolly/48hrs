




import pyglet
import math
from image_handling import *
from button_class import *
#from button_object import *
#from shaders import *

window = pyglet.window.Window()

#pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
#pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)

sprite_sheet = pyglet.image.load('font.png')
columns = sprite_sheet.width // 8
rows = sprite_sheet.height // 8

image_grid = pyglet.image.ImageGrid(sprite_sheet, rows, columns)

letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬"];
# def pad_to_256(char_list):
#      return char_list + [" "] * (256 - len(char_list))
# letter_order = pad_to_256(letter_order)



string_to_draw = "The quick brown fox jumpeeeeeeeeeeeed over the lazy dog. This is the story of a man named Stanley. Stanley worked for a company at an office where he sat in room 427. etc etc buttons"
tiles_to_draw = text_to_tiles_wrapped(string_to_draw, image_grid, letter_order, 20, "center")
bg_to_draw = text_to_background(string_to_draw, image_grid, letter_order, 20, "center")

combined_image = combine_tiles(tiles_to_draw, 8, 8, 20)
combined_image_2 = combine_tiles(bg_to_draw, 8, 8, 20)

mysprite = pyglet.sprite.Sprite(combined_image, x=50, y=50)
mysprite2 = pyglet.sprite.Sprite(combined_image_2, x=50, y=50)

my_object = InteractiveObject(
    x=100,
    y=200,
    width=64,
    height=16,
    sprites=[mysprite2, mysprite],
    colors=[[(168, 168, 168, 255), (98, 98, 98, 255), (54, 54, 54, 255)], [(98, 98, 98, 255), (54, 54, 54, 255), (33, 33, 33, 255)]],
    animtype = [None, None],
    animmod = [None, None],
    text = [None, None],
    alignment_x='center',
    alignment_y='top',
    depth=1,
    obj_type="label",
    draggable=True,
    custom_data={"label": "Click me!"}
)

#mysprite.scale = 2
#mysprite.rotation = 45
#mysprite.color = (0, 255, 255, 255)

batch = pyglet.graphics.Batch()

# background_group = pyglet.graphics.OrderedGroup(0) #for tiles
# water_group = pyglet.graphics.OrderedGroup(10)
# items_group = pyglet.graphics.OrderedGroup(20)
# entities_group = pyglet.graphics.OrderedGroup(30)
# sfx_group = pyglet.graphics.OrderedGroup(40)
# textbg_group = pyglet.graphics.OrderedGroup(50)
# text_group = pyglet.graphics.OrderedGroup(60)

@window.event
def on_draw():
    window.clear()
    my_object.draw(batch)

    batch.draw()
    #




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


