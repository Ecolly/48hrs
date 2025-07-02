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
    SIDE_MENU = 6


def create_main_menu_labels(batch, group):
    background = pyglet.shapes.Rectangle(
        0, 0, WINDOW_WIDTH, WINDOW_HEIGHT,
        color=(100, 100, 200),
        batch=batch,
        group=group
    )

    menu_label = pyglet.text.Label(
        "PANDORIUM",
        font_name="Arial",
        font_size=48,
        x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT - 100,
        anchor_x="center", anchor_y="center",
        color=(255, 255, 255, 255),
        batch=batch,
        group=group
    )
    menu_stats = pyglet.text.Label(
        "Press ENTER to Start\nPress L to Load",
        font_name="Arial",
        font_size=18,
        x=WINDOW_WIDTH // 2, y=WINDOW_HEIGHT // 2,
        anchor_x="center", anchor_y="center",
        color=(200, 200, 200, 255),
        batch=batch,
        group=group
    )
    return background, menu_label, menu_stats



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

    

def create_ingame_menu_labels(batch, group):
    background = pyglet.shapes.Rectangle(
        0, 0, WINDOW_WIDTH/2, WINDOW_HEIGHT,
        color=(100, 100, 200),
        batch=batch,
        group=group
    )
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