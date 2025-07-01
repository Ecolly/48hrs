import pyglet
from font import*

class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=(50, 150, 255))
        self.label = pyglet.text.Label(
            text,
            font_size=18,
            x=x + width // 2,
            y=y + height // 2,
            anchor_x='center',
            anchor_y='center',
            color=(255, 255, 255, 255)
        )
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def draw(self):
        self.rect.draw()
        self.label.draw()

    def hit_test(self, x, y):
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height