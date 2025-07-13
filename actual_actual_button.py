import pyglet
from font import*
from image_handling import*

class Button:
    def __init__(self, x, y, width, height, text, batch, group):
        #self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=(50, 150, 255), batch=batch, group=group)
#def initialize_text_sprite(grid_to_use, width, height, width_per_char, height_per_char):
#         start_button = Button(150, 350, 200, 50, "Start Game", menu_batch, group_ui_menu)
# exit_button = Button(150, 250, 200, 60, "Exit", menu_batch, group_ui_menu)
        self.sprite = initialize_text_sprite(grid_font, width, height, 8, 8)
        change_text_sprite(grid_font, 30, 5, 8, 8, self.sprite, text, letter_order, "center")
        self.sprite.x = x  # Center horizontally
        self.sprite.y = y # Position near the top
        self.sprite.batch = batch
        self.sprite.group = group

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self):
        self.rect.draw()

    def hit_test(self, x, y):
        print(f"Hit test at ({x}, {y}) against {self.text} button at ({self.x}, {self.y}) with size ({self.width}, {self.height})")
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
