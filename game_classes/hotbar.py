import pyglet
from game_classes.item import Item  # Assuming Item class is defined in item.py

hotbar_image = pyglet.image.load("hotbar.png")
hotbar_selected_image = pyglet.image.load("hot_bar_selector.png")  


class Hotbar:
    def __init__(self, player_inventory, batch, group):
        self.slots = player_inventory[-10:]  # Each slot can hold an item or None
        self.selected = 0  # Index of currently selected slot

        #position of the hotbar on the screen
        self.x = 300
        self.y = 50
        self.scale = 3
        #draw the background of the hotbar
        self.hotbar_sprite = pyglet.sprite.Sprite(hotbar_image, x=self.x, y=self.y, batch=batch, group=group)
        self.hotbar_sprite.scale = self.scale
        self.selector_sprite = pyglet.sprite.Sprite(
            hotbar_selected_image,
            x=self.x + self.selected * 56,
            y=self.y,
            batch=batch,
            group=group
        )
        self.selector_sprite.scale = self.scale


    #change the selected slot based on mouse_direction
    def change_selection(self, direction):
        #print(f"change_selection called with direction={direction}, current selected={self.selected}")
        if direction>0 and self.selected>0:
            self.selected -= 1
            #print(f"Selected slot: {self.selected}")
        elif direction<0 and self.selected<len(self.slots)-1:
            self.selected += 1
            #print(f"Selected slot: {self.selected}")
    def update_hotbar(self, player_inventory):
        self.slots = player_inventory[-10:]
    #draw the selection highlight
    def draw_selected_slot(self):
        selected = self.selected
        self.selector_sprite.x = self.x+2 + selected * 57
        # selected_item = self.get_selected_item()
        # if selected_item is not None:
        #     selected_item.sprite.x = self.x + self.selected * 56

    def get_selected_item(self):
        return self.slots[self.selected]
    
    def draw_hotbar_items(self, batch, group):
        
        for i, item in enumerate(self.slots):
            x = self.x + i * 56 + 10  # 48px slot + 8px spacing
            y = self.y + 5
            print(f"Drawing item {i}: {item.name if item else 'None'} at position ({x}, {y})")
            #print(f"Drawing slot {i} at position ({x}, {y}) with item: {item}")
            # Draw slot background (rectangle or sprite)
            # Draw item sprite if item is not None
            # Highlight if i == hotbar.selected
            # Example (pseudo-code):
            # draw_rectangle(x, y, 48, 48, color=(200,200,200))
            if item is not None:
                item.hotbar_sprite.visible = True
                item.hotbar_sprite.x = x
                item.hotbar_sprite.y = y
                item.hotbar_sprite.batch = batch
                item.hotbar_sprite.group = group
                item.hotbar_sprite.scale = 3