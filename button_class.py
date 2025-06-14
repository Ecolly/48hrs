
import pyglet
import math

class InteractiveObject:
    def __init__(self, x, y, width, height, sprites, colors, animtype, animmod, text, obj_type, 
                 alignment_x='left', alignment_y='bottom',
                 depth=0, draggable=False, rot=0, scale=3, **extras):
        
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

        # Extra user-defined properties
        self.extras = extras

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



