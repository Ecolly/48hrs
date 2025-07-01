import pyglet


letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬", "", "", "", "", "", "", "", "", "ä"]


pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST

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


sprite_liq = pyglet.image.load('all_liquid_animations.png')
columns_liq = sprite_liq.width // 128
rows_liq = sprite_liq.height // 128
grid_liq = pyglet.image.ImageGrid(sprite_liq, rows_liq, columns_liq)


sprite_liqtile = pyglet.image.load('tile_liquid_animations.png')
columns_liqtile = sprite_liqtile.width // 16
rows_liqtile = sprite_liqtile.height // 16
grid_liqtile = pyglet.image.ImageGrid(sprite_liqtile, rows_liqtile, columns_liqtile)

sprite_deeper = pyglet.image.load('deeper_bgs.png')
columns_deeper = sprite_deeper.width // 128
rows_deeper = sprite_deeper.height // 128
grid_deeper = pyglet.image.ImageGrid(sprite_deeper, rows_deeper, columns_deeper)


sprite_blank = pyglet.image.load('blank.png')
columns_blank = sprite_blank.width // (16*60)
rows_blank = sprite_blank.height // (16*60)
grid_blank = pyglet.image.ImageGrid(sprite_blank, rows_blank, columns_blank)

batch = pyglet.graphics.Batch()


from pyglet.graphics import Group

group_deeper = Group(order=4)
group_bg_pits = Group(order=5)
group_bg = Group(order=10)
group_bg_liqs = Group(order=15)
group_items = Group(order=20)
group_enemies_bg = Group(order=39)
group_enemies = Group(order=40)
group_enemies_fg = Group(order=41)
group_effects = Group(order=42)
group_hotbar = Group(order=43)
group_hotbar_selection = Group(order=44)
group_overlay = Group(order=45)
group_inv_bg = Group(order=50)
group_inv = Group(order=60)
group_inv_ext = Group(order=65)
group_inv_ext_2 = Group(order=67)
group_ui_bg = Group(order=70)
group_ui = Group(order=80)
group_ui_TEST = Group(order=100)
group_ui_menu = Group(order=110)



















def draw_tiny_texts(text, x, y, group):
    """
    Draws text at the specified position using the provided font grid.
    """
    global batch
    sprites = []
    for i, char in enumerate(text):
        if char in letter_order:
            index = letter_order.index(char)
            #print(f"Drawing character '{char}' at index {index}.")
            sprite = pyglet.sprite.Sprite(grid_tinyfont[index], x + i * 10, y, batch=batch, group=group)
            sprites.append(sprite)
            sprite.scale = 3
            sprite.color = (0, 0, 0, 255)
        else:
            print(f"Character '{char}' not found in letter order.")
    return sprites


def draw_texts(text, x, y, group):
    """
    Draws text at the specified position using the regular font grid.
    """
    global batch
    sprites = []
    for i, char in enumerate(text):
        if char in letter_order:
            index = letter_order.index(char)
            sprite = pyglet.sprite.Sprite(grid_font[index], x + i * 16, y, batch=batch, group=group)
            sprites.append(sprite)
            sprite.scale = 2
        else:
            print(f"Character '{char}' not found in letter order.")
    return sprites