SLOT_SIZE = 16
ROWS, COLS = 3, 5


import pyglet
batch = pyglet.graphics.Batch()

dragging_item = None
drag_offset = (0, 0)

class Slot:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.item = None  # can hold an Item object

    def draw(self):
        slot_box = pyglet.shapes.Rectangle(self.x, self.y, SLOT_SIZE, SLOT_SIZE, color=(50, 50, 50), batch=batch)
        if self.item:
            self.item.sprite.x = self.x
            self.item.sprite.y = self.y
            self.item.sprite.draw()

    def contains(self, x, y):
        return self.x <= x <= self.x + SLOT_SIZE and self.y <= y <= self.y + SLOT_SIZE