import pyglet

sprite_font = pyglet.image.load('font.png')
columns_font = sprite_font.width // 8
rows_font = sprite_font.height // 8
grid_font = pyglet.image.ImageGrid(sprite_font, rows_font, columns_font)

sprite_tinyfont = pyglet.image.load('tinyfont.png')
columns_tinyfont = sprite_tinyfont.width // 5
rows_tinyfont = sprite_tinyfont.height // 8
grid_tinyfont = pyglet.image.ImageGrid(sprite_tinyfont, rows_tinyfont, columns_tinyfont)

letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬", "", "", "", "", "", "", "", "", "ä"]


def draw_tiny_texts(text, x, y, batch, group):
    """
    Draws text at the specified position using the provided font grid.
    """
    sprites = []
    for i, char in enumerate(text):
        if char in letter_order:
            index = letter_order.index(char)
            #print(f"Drawing character '{char}' at index {index}.")
            sprite = pyglet.sprite.Sprite(grid_tinyfont[index], x + i * 10, y, batch=batch, group=group)
            sprites.append(sprite)
            sprite.scale = 2
        else:
            print(f"Character '{char}' not found in letter order.")
    return sprites
