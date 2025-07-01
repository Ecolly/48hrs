#Main menu (displayed at the start of the game)
    #Load button, loads saved games
    
    #New button, starts a new game 

import pyglet
from enum import Enum

class MenuState(Enum):
    MAIN_MENU = 1
    LOAD_MENU = 2
    SAVE_MENU = 3
    WINLOSE_SCREEN = 4
    INGAME = 5


# def create_win_lose_screen(all_buttons, winlose):
#     global grid_font
#     global letter_order
#     color = (255, 255, 255)
#     color2 = (33, 33, 33, 90)
#     w = int((1152)/24)
#     h = int((768)/24)
#     txt = ""
#     txt = txt.zfill(w*h)

#     txt2 = ""
#     if winlose == "win":
#         txt2 = "You won!"
#     else:
#         txt2 = "You lost..."

#     txt2 = txt2 + "εPANDORIUMεMade by zeroBound & EconicεMusic: Cyber Dream Loopεby Eric Matyasεwww.soundimage.orgεPress TAB to quit.εä εä εä εä εä εä εä εä εä εä"
    
#     spr1 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_tiles_wrapped(txt2, grid_font, letter_order, w, "center"), 8, 8, w))
#     spr2 = pyglet.sprite.Sprite(image_handling.combine_tiles(image_handling.text_to_background(txt, grid_font, letter_order, w, "left"), 8, 8, w))
#     obj = InteractiveObject(
#         x=0, #- (player.prevx*16 + 8)*player.scale + (x*16 + 8)*3,
#         y=48*6 - 32, #- (player.prevy*16 + 8)*player.scale + (y*16 + 8)*3,
#         width=spr2.width,
#         height=spr2.height,
#         sprites=[spr2, spr1],
#         colors=[[color2, color2, color2], [color, color, color]],
#         animtype = [0, 0],
#         animmod = [None, None],
#         text = [None, None],
#         alignment_x='left',
#         alignment_y='top',
#         depth=1,
#         obj_type="menu stuff",
#         draggable=False,
#         supertype = "winlose",
#         extra_1 = 0,
#         extra_2 = 0
#     )
#     all_buttons.append(obj)


    
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