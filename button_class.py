
import pyglet
import math
import image_handling

# sprite_font = pyglet.image.load('font.png')
# columns_font = sprite_font.width // 8
# rows_font = sprite_font.height // 8
# grid_font = pyglet.image.ImageGrid(sprite_font, rows_font, columns_font)



# letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬"];



class InteractiveObject:
    def __init__(self, x, y, width, height, sprites, colors, animtype, animmod, text, obj_type, extra_1, extra_2, rclick,
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
        self.rclick = rclick

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
    
    def draw(self, batch):
        base_x, base_y = self.get_screen_position()

        for i, sprite in enumerate(self.sprites):
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
            
            sprite.batch = batch
            if i == 0:
                sprite.z = 60
            else:
                sprite.z = 70


            #sprite.draw()



# def create_point_number(x, y, text, color, player):
#     global grid_font 
#     global letter_order
#     spr1 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles_wrapped(str("e35wWEF"), grid_font, letter_order, 10, "left"), 8, 8, 10))
#     spr1.z = 80
#     #spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_background(hp_string, grid_font, letter_order, 10, "left"), 8, 8, 10))
#     obj = InteractiveObject(
#         x=50,#1152/2 -24 - (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
#         y=50,#768/2-24 - (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
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
#         rclick = False,
#         extra_1 = 0,
#         extra_2 = 0
#     )








