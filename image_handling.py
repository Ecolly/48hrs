





import pyglet
import math

def text_to_tiles(text, image_grid, letter_order):
    # Create a mapping from character to its index in the tile grid
    char_to_index = {char: i for i, char in enumerate(letter_order)}
    tile_list = []
    for char in text:
        index = char_to_index.get(char, char_to_index.get(" ", 0))  # fallback to space
        tile = image_grid[index]
        tile_list.append(tile)
    return tile_list

def text_to_tiles_setsize(text, image_grid, letter_order, setsize, height):
    # Create a mapping from character to its index in the tile grid
    char_to_index = {char: i for i, char in enumerate(letter_order)}
    tile_list = []
    for char in text:
        index = char_to_index.get(char, char_to_index.get(" ", 0))  # fallback to space
        tile = image_grid[index]
        tile_list.append(tile)

    while len(tile_list) < setsize - 1:
        tile_list.append(image_grid[char_to_index.get("╬", char_to_index.get(" ", 0))])
    
    i = 1
    while i < height:
        j = 0
        while j < setsize - 1:
            tile_list.append(image_grid[char_to_index.get("╬", char_to_index.get(" ", 0))])
            j = j + 1
        i = i + 1 

    return tile_list

def text_to_background(text, image_grid, letter_order, width, justify):
    output_txt = ""
    i = 0
    while i < width*math.floor(len(text)/width) + width:
        output_txt = output_txt + "╬"   
        i = i + 1
    return text_to_tiles_wrapped(output_txt, image_grid, letter_order, width, justify)





def tesselate(character, image_grid, width, height):
    # output_txt = ""
    # output_txt.zfill(width*height)
    # return text_to_floor(output_txt, image_grid, ["0"], [character], width)
    tile_list = []
    i = 0
    while i < width*height:
        tile_list.append(image_grid[character])
        i = i + 1
    return tile_list


def tesselate_inc(character, image_grid, width, height):
    # output_txt = ""
    # output_txt.zfill(width*height)
    # return text_to_floor(output_txt, image_grid, ["0"], [character], width)
    tile_list = []
    i = 0
    while i < width*height:
        tile_list.append(image_grid[character+i])
        i = i + 1
    return tile_list






def text_to_floor(text, image_grid, letter_order, letter_tile, width):
    tile_list = []
    for s in text:
        id = letter_order.index(s)
        tile_list.append(image_grid[letter_tile[id]])
    return tile_list









def text_to_tiles_wrapped(text, image_grid, letter_order, width, justify):
    # Create character-to-index mapping
    char_to_index = {char: i for i, char in enumerate(letter_order)}

    # Step 1: Handle manual line breaks (using ε)
    raw_lines = text.split("ε")
    wrapped_lines = []

    for raw_line in raw_lines:
        words = raw_line.split()
        current_line = ""

        for word in words:
            # Handle long word splitting *before* adding to current_line
            while len(word) > width:
                # Append current line before splitting the long word
                if current_line:
                    wrapped_lines.append(current_line)
                    current_line = ""

                # Append the chunk of the long word
                wrapped_lines.append(word[:width])
                word = word[width:]

            # Now try to add the remainder (or whole word) to current_line
            if len(current_line) + len(word) + (1 if current_line else 0) <= width:
                current_line += (" " if current_line else "") + word
            else:
                if current_line:
                    wrapped_lines.append(current_line)
                current_line = word

        # Append any leftover current_line
        if current_line:
            wrapped_lines.append(current_line)

    # Step 2: Justify and pad each line
    justified_lines = []
    for line in wrapped_lines:
        if justify == "left":
            padded = line.ljust(width)
        elif justify == "center":
            padded = line.center(width)
        elif justify == "right":
            padded = line.rjust(width)
        else:
            raise ValueError("justify must be 'left', 'center', or 'right'")
        justified_lines.append(padded)

    # Step 3: Convert characters to tiles
    tile_list = []
    for line in justified_lines:
        for char in line:
            index = char_to_index.get(char, char_to_index.get(" ", 0))
            tile_list.append(image_grid[index])

    # while len(tile_list) < width*len(justified_lines):
    #     tile_list.append(image_grid[char_to_index.get("╬", char_to_index.get(" ", 0))])

    return tile_list


def combine_tiles(tiles, tile_width, tile_height, total_width):
    if total_width < 1:
        raise ValueError("total_width must be at least 1")
    total_rows = (len(tiles) + total_width - 1) // total_width  # Ceiling division

    combined_width = total_width * tile_width
    combined_height = total_rows * tile_height

    combined = pyglet.image.Texture.create(combined_width, combined_height)


    combined.min_filter = pyglet.gl.GL_NEAREST
    combined.mag_filter = pyglet.gl.GL_NEAREST
    
    for i, tile in enumerate(tiles):
        col = i % total_width
        row = i // total_width
        x = col * tile_width
        y = (total_rows - 1 - row) * tile_height  # Pyglet's Y=0 is at bottom
        combined.blit_into(tile, x, y, 0)
    return combined


def combine_tiles_efficient(tiles, tile_width, tile_height, total_width, sprite):
    if total_width < 1:
        raise ValueError("total_width must be at least 1")
    total_rows = (len(tiles) + total_width - 1) // total_width  # Ceiling division
    
    for i, tile in enumerate(tiles):
        col = i % total_width
        row = i // total_width
        x = col * tile_width
        y = (total_rows - 1 - row) * tile_height  # Pyglet's Y=0 is at bottom
        if x < sprite.image.width and y < sprite.image.height:
            sprite.image.blit_into(tile, x, y, 0)
    return row





letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬", "ä"];



def initialize_text_sprite(grid_to_use, width, height, width_per_char, height_per_char):
    #returns a blank sprite at the specified width and height. width_per_char and height_per_char are 8, 8 for grid_font, 5, 8 for grid_tinyfont
    return pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_to_use, width, height), width_per_char, height_per_char, width))




def change_text_sprite(grid_to_use, width, height, width_per_char, height_per_char, sprite, text, letter_order, justification):
    #input a sprite made with initializE_text_sprite and this will change the text on it
    #justification can be either "left", "center", or "right"

    combine_tiles_efficient(tesselate(0, grid_to_use, width, height), width_per_char, height_per_char, width, sprite)

    combine_tiles_efficient(text_to_tiles_wrapped(text, grid_to_use, letter_order, width, justification), width_per_char, height_per_char, width, sprite)







    # return pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_to_use, width, height), width_per_char, height_per_char, width))












def create_sprite_text_simple(image_grid, txt):
    global letter_order
    tex = combine_tiles(text_to_tiles(txt, image_grid, letter_order), 8, 8, 200)
    return pyglet.sprite.Sprite(tex, x=0, y=0)

def create_sprite(image_grid, index):
    return pyglet.sprite.Sprite(image_grid[index], x=0, y=0)





