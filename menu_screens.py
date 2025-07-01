#Main menu (displayed at the start of the game)
    #Load button, loads saved games
    
    #New button, starts a new game 

import pyglet
from enum import Enum
from config import*

menu_batch = pyglet.graphics.Batch()

class MenuState(Enum):
    MAIN_MENU = 1
    LOAD_MENU = 2
    SAVE_MENU = 3
    WINLOSE_SCREEN = 4
    INGAME = 5


class MenuButton:
    def __init__(self, x, y, width, height, text, batch, group, on_click):
        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=(60, 60, 120), batch=batch, group=group)
        self.label = pyglet.text.Label(
            text,
            font_name="Arial",
            font_size=18,
            x=x + width // 2,
            y=y + height // 2,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255),
            batch=batch,
            group=group
        )
        self.x, self.y, self.width, self.height = x, y, width, height
        self.on_click = on_click

    def hit_test(self, mx, my):
        return self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height

# Example usage in your menu creation function:
def create_main_menu_labels(batch, group, window_width, window_height, on_start, on_load):
    background = pyglet.shapes.Rectangle(
        0, 0, window_width, window_height,
        color=(100, 100, 200),
        batch=batch,
        group=group
    )
    menu_label = pyglet.text.Label(
        "PANDORIUM",
        font_name="Arial",
        font_size=48,
        x=window_width // 2, y=window_height - 100,
        anchor_x="center", anchor_y="center",
        color=(255, 255, 255, 255),
        batch=batch,
        group=group
    )
    start_button = MenuButton(
        x=window_width // 2 - 100, y=window_height // 2 + 20,
        width=200, height=50,
        text="Start Game",
        batch=batch, group=group,
        on_click=on_start
    )
    load_button = MenuButton(
        x=window_width // 2 - 100, y=window_height // 2 - 50,
        width=200, height=50,
        text="Load Game",
        batch=batch, group=group,
        on_click=on_load
    )
    return [background, menu_label, start_button, load_button]




def create_save_menu_labels(batch, group):
    labels = []
    # Title
    title_label = pyglet.text.Label(
        "SAVE GAME",
        font_name="Arial",
        font_size=36,
        x=384 // 2, y=256 - 60,
        anchor_x="center", anchor_y="center",
        color=(255, 255, 255, 255),
        batch=batch,
        group=group
    )
    labels.append(title_label)
    # Save slots
    # Back button
    back_label = pyglet.text.Label(
        "Press ESC to go back",
        font_name="Arial",
        font_size=16,
        x=384 // 2, y=40,
        anchor_x="center", anchor_y="center",
        color=(180, 180, 180, 255),
        batch=batch,
        group=group
    )
    labels.append(back_label)
    return labels

    
#Load menu (displayed when the load button is clicked)
    #List of saved games, each with a load button
    #Back button, returns to main menu

#Side menu opens, when player press exit button in game
    #Save button, goes to save meu
    #exit button, exit to main menu (no saving)

#Save menu (displayed when the save button is clicked)
    #List of saved games/slots, player can either overwrite or create a new save
    #Back button, returns to game




#winlose screen (displayed when player wins or loses)
    #Displays a message, and a button to return to main menu