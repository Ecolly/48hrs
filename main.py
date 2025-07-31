import pyglet
import math
from image_handling import *
from button_class import *
from game_classes.player import *
from game_classes.face_direction import *
from game_classes.techniques import *
from game_classes.enemy import *
#from game_classes.item import *
from game_classes.map import *
from game_classes.item import Weapon, Consumable
from game_classes.item import Item
from animations import *
from actual_actual_button import Button
from font import *
import cProfile
import tracemalloc
import gc
import sys 
import psutil
import os
import objgraph
from game_classes.hotbar import Hotbar
#from memory_profiler import profile
import turn_logic
import delete_object
import json
from menu_screens import *
from save_and_load import *
from font import *

#import xdot
import time
process = psutil.Process(os.getpid())
mem_info = process.memory_info()

from config import WINDOW_HEIGHT, WINDOW_WIDTH, INVENTORY_SLOT_SIZE, INVENTORY_SPACING

pyglet.image.Texture.default_min_filter = pyglet.gl.GL_NEAREST
pyglet.image.Texture.default_mag_filter = pyglet.gl.GL_NEAREST








def disable_errcheck():
    for name in dir(pyglet.gl.lib):
        func = getattr(pyglet.gl.lib, name)
        if callable(func) and hasattr(func, 'errcheck'):
            try:
                func.errcheck = lambda result, func, args: result
            except Exception:
                pass

disable_errcheck()




##########################################################################################






#from button_object import *
#from shaders import *
config = pyglet.gl.Config(double_buffer=True, sample_buffers=0, samples=0)


win_x = 384 #pixel-perfect size of window, without scaling
win_y = 256
scale = 3
win_true_x = win_x*scale
win_true_y = win_y*scale

window = pyglet.window.Window(win_true_x, win_true_y, config=config)

#pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
#pyglet.gl.glBlendFunc(pyglet.gl.GL_SRC_ALPHA, pyglet.gl.GL_ONE_MINUS_SRC_ALPHA)


#Game variables
gamestate = 1
has_won = 0
has_lost = 0
item_selected = None
#extinct_creatures = [] 
player, floor = None, None
all_enemies = None
floor_level = 0
all_buttons = []
all_anims = []
        

animation_presets = [
    [0],
    [0, 1, 2, 1, 0, 3, 4, 3],
    [0, 1, 2, 3, 4],
    [0, 1, 2, 3, 4, 5, 6, 7]
]

dragging_item = None
dragging_from_slot = None
drag_offset = (0, 0)
right_click_menu_enabled = False

letter_order = [" ", "!", "\"", "#", "$", "%", "&", "\'", "(", ")", "*", "+", ",", "-", ".", "/", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?", "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_", "`", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "{", "|", "}", "~", "◯", "─", "│", "┌", "┐", "└", "┘", "α", "β", "╦", "╣", "╔", "╗", "╚", "╝", "╩", "╠", "╬", "ä"];



#floor_items = [item]
#inventory_items = []

color_templates = []
i = 0
while i < 256:
    color_templates.append((255, 255, 255, i))
    i = i + 1


color_templates.append((255, 0, 0, 255))
color_templates.append((189, 66, 0, 255))
color_templates.append((33, 33, 33, 90))




##################### MENU STUFF     ##########################


#menu stuff
menu_batch = pyglet.graphics.Batch()
side_bar_batch = pyglet.graphics.Batch()
load_menu_batch = pyglet.graphics.Batch()
save_menu_batch = pyglet.graphics.Batch()

current_menu = MenuState.MAIN_MENU
main_menu = create_main_menu_labels(batch=menu_batch, group=group_ui_menu)
start_button = Button((384*3)/2 - (10*8*3/2), 350, 10, 1, "Start Game", menu_batch, group_ui_menu)
exit_button = Button((384*3)/2 - (4*8*3/2), 250, 4, 1, "Exit", menu_batch, group_ui_menu)
load_button = Button((384*3)/2 - (9*8*3/2), 450, 9, 1, "Load Game", menu_batch, group_ui_menu)

game_side_menu = create_ingame_menu_labels(batch=side_bar_batch, group=group_ui_menu)
save_button = Button(300, 350, 9, 1, "Save Game", side_bar_batch, group_ui_menu)

#load_menu = create_load_menu(batch=load_menu_batch, group=group_ui_menu)
load_game_buttons = create_load_game_buttons(batch=load_menu_batch, group=group_ui_menu)



keys = pyglet.window.key.KeyStateHandler()
window.push_handlers(keys)
mouse_state = pyglet.window.mouse.MouseStateHandler()
window.push_handlers(mouse_state)
######################################### Game Initialization IF NEW GAME #################################


#FLOOR STUFF 

bg = pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_blank, 1, 1), 60*16, 60*16, 1))
bg.scale = 3
bg.group = group_bg
bg.batch = batch
# bg_pits = pyglet.sprite.Sprite(grid_bg[0])
# bg_pits.scale = 3

bg_liqs = []    
bg_liqs_foreground = []
typed_text = ""

i = 0
while i < 16:
    bg_liqs.append(pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_liq, 12, 12), 128, 128, 12)))
    bg_liqs[i].scale = 3
    bg_liqs[i].group = group_bg_pits
    bg_liqs[i].batch = menu_batch

    bg_liqs_foreground.append(pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_blank, 1, 1), 60*16, 60*16, 1)))
    bg_liqs_foreground[i].scale = 3
    bg_liqs_foreground[i].group = group_bg_liqs
    bg_liqs_foreground[i].batch = batch
    bg_liqs_foreground[i].color = color_templates[200]
    i = i + 1

bg_deeper = pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_liq, 12, 12), 128, 128, 12))
bg_deeper.scale = 3
bg_deeper.group = group_deeper
bg_deeper.batch = menu_batch






frameindexes = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]#[4, 5, 6, 6, 7, 7, 7, 6, 6, 5, 4, 3, 2, 1, 1, 0, 0, 0, 1, 1, 2, 3]

i = 0
while i < 16:
    combine_tiles_efficient(tesselate(frameindexes[i] + 16*9, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
    bg_liqs[i].scale = 3
    i = i + 1
combine_tiles_efficient(tesselate(1, grid_deeper, 12, 12), 128, 128, 12, bg_deeper)

def go_to_next_level(amount):
    global floor, all_enemies, player, bg, bg_liqs, bg_deeper, bg_liqs_foreground, floor_level, adventure_log, grid_blank

    itemlist_beginner = ["3 Gold", "3 Gold", "3 Gold","3 Gold","3 Gold","3 Gold","3 Gold","3 Gold","3 Gold","15 Gold","Knife", "Machete", "Sickle", "Stick", "Stick", "Stick", "Apple", "Apple", "Apple", "Mushrooms", "Mushrooms", "Leaves", "Leaves", "Lettuce", "Candy", "Rock", "Rock", "Rock", "Rock", "Staff of Mana", "Staff of Mana", "Staff of Mana", "Staff of Mana", "Staff of Mana", "Tome of Recovery", "Tome of Recovery", "Tome of Recovery", "Tome of Recovery", "Wood Shield", "Wood Shield", "Wood Shield", "Wood Shield", "Leaf Shield", "Leaf Shield", "Leaf Shield", "Leaf Shield", "Leaf Shield", "Blue Shield", "Blue Shield"]     
    #itemlist_beginner = ["Staff of Mana", "Staff of Mana", "Staff of Mana","Staff of Mana","Staff of Mana","Staff of Mana","Staff of Mana"]
    #"Shopping List 1", "Shopping List 2", "Shopping List 3", "Shopping List 4", "Predecessor's Scrawling", "Peer's Notes", "Coworker's Thoughts", "Coworker's Thoughts 2", "Coworker's Thoughts 3", "Compatriot's Ideas", "Scientist's Log 1", "Scientist's Log 2", "Scientist's Log 3", "Scientist's Log 4", "Scientist's Log 5", "Scientist's Log 6"

    #itemlist_outside = ["3 Gold", "Mushrooms", "Leaves", "Apple", "Mushrooms", "Leaves", "Apple", "Stick", "Rock", "Stick", "Rock", "Leaf Shield", "Shopping List 4"]
    itemlist_outside = ["Staff of Mana", "Staff of Mana", "Staff of Mana","Staff of Mana","Staff of Mana","Staff of Mana","Staff of Mana"]
    itemlist_sarcophagus = ["15 Gold", "60 Gold", "60 Gold", "60 Gold", "60 Gold", "Scientist's Log 1", "Scientist's Log 2", "Scientist's Log 3", "Scientist's Log 4", "Scientist's Log 5", "Scientist's Log 6"]

    itemlist_beginner2 = ["3 Gold", "3 Gold", "3 Gold","3 Gold","3 Gold","3 Gold","3 Gold","15 Gold","15 Gold","15 Gold","Knife", "Knife", "Knife", "Scimitar", "Rapier", "Obsidian Edge", "Windsword", "Machete", "Machete", "Sickle", "Stick", "Stick", "Water Flask", "Water Flask", "Petroleum Flask", "Empty Flask", "Empty Flask", "Empty Flask", "Cureall Flask", "Syrup Flask", "Mercury Flask", "Ink Flask", "Detergent Flask", "Acid Flask", "Rock", "Rock", "Wood Shield", "Wood Shield", "Leaf Shield", "Blue Shield", "Blue Shield", "Armor Plate", "Steel Shield", "Spiked Shield", "Mirror Shield", "Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Primes", "Fibonnaci Staff", "Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Blank Tome", "Ruined Tome", "Poultry", "Mushrooms", "Leaves", "Apple", "Apple", "Candy", "Starfruit", "Durian", "Dragonfruit", "Beet", "Lemon", "Lettuce", "Lettuce", "Kale", "Shopping List 1", "Shopping List 2", "Shopping List 3", "Shopping List 4", "Peer's Notes", "Predecessor's Scrawling", "Coworker's Thoughts"]

    itemlist_equal = ["3 Gold", "3 Gold", "3 Gold","3 Gold","3 Gold","3 Gold","15 Gold","15 Gold","15 Gold","15 Gold","Knife", "Scimitar", "Rapier", "Obsidian Edge", "Windsword", "Machete", "Sickle", "Stick", "Water Flask", "Petroleum Flask", "Empty Flask", "Cureall Flask", "Syrup Flask", "Mercury Flask", "Ink Flask", "Detergent Flask", "Acid Flask", "Rock", "Wood Shield", "Leaf Shield", "Blue Shield", "Armor Plate", "Steel Shield", "Spiked Shield", "Mirror Shield", "Sun Shield", "Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Cloning", "Staff of Metamorphosis", "Staff of Primes", "Fibonnaci Staff", "Staff of Alchemy", "Gardening Staff", "Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Tome of Descendance", "Tome of Resurrection", "Blank Tome", "Ruined Tome", "Poultry", "Mushrooms", "Leaves", "Apple", "Candy", "Starfruit", "Durian", "Dragonfruit", "Beet", "Lemon", "Lettuce", "Kale", "Shopping List 1", "Shopping List 2", "Shopping List 3", "Shopping List 4", "Coworker's Thoughts 2", "Peer's Notes", "Compatriot's Ideas", "Scientist's Log 1", "Scientist's Log 2", "Scientist's Log 3", "Duplication Tome", "Tome of Exchange", "Mirror Staff", "Volatile Staff", "Weaponsmithing Tome", "Shieldsmithing Tome", "Staff of Osteoporosis", "Staff of Fatigue"]

    itemlist_chasm = ["3 Gold", "3 Gold", "3 Gold","3 Gold","3 Gold","3 Gold","15 Gold","15 Gold","15 Gold","15 Gold", "Rock", "Rock", "Rock", "Rock", "Rock", "Rock", "Rock", "Rock","Rock", "Rock", "Rock", "Rock","Rock", "Rock", "Rock", "Rock","Knife", "Scimitar", "Rapier", "Obsidian Edge", "Windsword", "Machete", "Sickle", "Stick", "Water Flask", "Petroleum Flask", "Empty Flask", "Cureall Flask", "Syrup Flask", "Mercury Flask", "Ink Flask", "Detergent Flask", "Acid Flask", "Rock", "Wood Shield", "Leaf Shield", "Blue Shield", "Armor Plate", "Steel Shield", "Spiked Shield", "Mirror Shield", "Sun Shield", "Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Cloning", "Staff of Metamorphosis", "Staff of Primes", "Fibonnaci Staff", "Staff of Alchemy", "Gardening Staff", "Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Tome of Descendance", "Tome of Resurrection", "Blank Tome", "Ruined Tome", "Poultry", "Mushrooms", "Leaves", "Apple", "Candy", "Starfruit", "Durian", "Dragonfruit", "Beet", "Lemon", "Lettuce", "Kale", "Shopping List 1", "Shopping List 2", "Shopping List 3", "Shopping List 4", "Coworker's Thoughts 2", "Peer's Notes", "Compatriot's Ideas", "Scientist's Log 1", "Scientist's Log 2", "Scientist's Log 3", "Duplication Tome", "Tome of Exchange", "Mirror Staff", "Volatile Staff", "Weaponsmithing Tome", "Shieldsmithing Tome", "Staff of Osteoporosis", "Staff of Fatigue"]


    itemlist_end = ["Stick", "Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","Stick","3 Gold", "3 Gold", "3 Gold","3 Gold","3 Gold","3 Gold","15 Gold","15 Gold","15 Gold","15 Gold","Knife", "Scimitar", "Rapier", "Obsidian Edge", "Windsword", "Machete", "Sickle", "Stick", "Water Flask", "Petroleum Flask", "Empty Flask", "Cureall Flask", "Syrup Flask", "Mercury Flask", "Ink Flask", "Detergent Flask", "Acid Flask", "Rock", "Wood Shield", "Leaf Shield", "Blue Shield", "Armor Plate", "Steel Shield", "Spiked Shield", "Mirror Shield", "Sun Shield", "Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Cloning", "Staff of Metamorphosis", "Staff of Primes", "Fibonnaci Staff", "Staff of Alchemy", "Gardening Staff", "Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Tome of Descendance", "Tome of Resurrection", "Blank Tome", "Ruined Tome", "Poultry", "Mushrooms", "Leaves", "Apple", "Candy", "Starfruit", "Durian", "Dragonfruit", "Beet", "Lemon", "Lettuce", "Kale", "Shopping List 1", "Shopping List 2", "Shopping List 3", "Shopping List 4", "Coworker's Thoughts 3", "Compatriot's Ideas", "Scientist's Log 4", "Scientist's Log 5", "Scientist's Log 6", "Duplication Tome", "Tome of Exchange", "Mirror Staff", "Volatile Staff", "Weaponsmithing Tome", "Shieldsmithing Tome", "Staff of Osteoporosis", "Staff of Fatigue"]

    itemlist_boss = ["Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Cloning", "Staff of Metamorphosis", "Staff of Primes", "Fibonnaci Staff", "Staff of Alchemy", "Gardening Staff", "Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Tome of Ascendance", "Tome of Descendance", "Tome of Extinction", "Tome of Resurrection", "Blank Tome", "Ruined Tome", "Duplication Tome", "Tome of Exchange", "Mirror Staff", "Volatile Staff", "Weaponsmithing Tome", "Shieldsmithing Tome", "Staff of Osteoporosis", "Staff of Fatigue"]

 

    if random.uniform(0, 1) < 0.2:
        shop_equal = ["Poultry", "Mushrooms", "Leaves", "Apple", "Candy", "Starfruit", "Durian", "Dragonfruit", "Beet", "Lemon", "Lettuce", "Kale"]
    elif random.uniform(0, 1) < 0.15:
        shop_equal = ["Weaponsmithing Tome", "Shieldsmithing Tome", "Weaponsmithing Tome", "Shieldsmithing Tome", "Duplication Tome", "Tome of Exchange", "Tome of Consolidation", "Tome of Consolidation", "Tome of Consolidation", "Tome of Identification", "Sharpening Tome", "Fortifying Tome", "Sharpening Tome", "Fortifying Tome", "Sharpening Tome", "Fortifying Tome", "Coloring Tome"]
    elif random.uniform(0, 1) < 0.1:
        shop_equal = ["Staff of Osteoporosis", "Staff of Fatigue", "Mirror Staff", "Volatile Staff", "Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Cloning", "Staff of Metamorphosis", "Staff of Primes", "Fibonnaci Staff", "Staff of Alchemy", "Gardening Staff"]
    elif random.uniform(0, 1) < 0.02:
        shop_equal = ["Water Flask", "Empty Flask", "Detergent Flask", "Ink Flask", "Acid Flask", "Petroleum Flask", "Syrup Flask", "Mercury Flask", "Cureall Flask"]
    elif random.uniform(0,1) < 0.02:
        shop_equal = ["Weaponsmithing Tome", "Shieldsmithing Tome", "Duplication Tome", "Tome of Exchange", "Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Tome of Descendance", "Tome of Resurrection", "Blank Tome", "Ruined Tome"]
    else:
        shop_equal = ["Weaponsmithing Tome", "Shieldsmithing Tome", "Staff of Osteoporosis", "Staff of Fatigue", "Duplication Tome", "Tome of Exchange", "Mirror Staff", "Volatile Staff", "Knife", "Scimitar", "Rapier", "Obsidian Edge", "Windsword", "Machete", "Sickle", "Stick", "Sun Shield", "Water Flask", "Petroleum Flask", "Empty Flask", "Cureall Flask", "Syrup Flask", "Mercury Flask", "Ink Flask", "Detergent Flask", "Acid Flask", "Rock", "Wood Shield", "Leaf Shield", "Blue Shield", "Armor Plate", "Steel Shield", "Spiked Shield", "Mirror Shield", "Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Cloning", "Staff of Metamorphosis", "Staff of Primes", "Fibonnaci Staff", "Staff of Alchemy", "Gardening Staff", "Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Tome of Descendance", "Tome of Resurrection", "Blank Tome", "Ruined Tome", "Poultry", "Mushrooms", "Leaves", "Apple", "Candy", "Starfruit", "Durian", "Dragonfruit", "Beet", "Lemon", "Lettuce", "Kale"]



    floor_level +=amount

    if floor_level < -5:
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list= "Open Wilderness", "Simple", (26, 26), "Solid", ["HAMSTER", "HAMSTER", "HAMSTER"], [1, 2, 3, 4], itemlist_outside
    elif floor_level < -4:
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list= "Sarcophagus Exterior", "Simple 2", (26, 26), "Solid", ["DEBT COLLECTOR", "EXECUTIVE", "HAMSTER"], [4, 4, 4], itemlist_outside
    elif floor_level < -3:
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list= "Sarcophagus Lobby", "Complex", (10,31,4,4,4,4,4,4), "Solid", ["DEBT COLLECTOR", "EXECUTIVE", "EXECUTIVE"], [4, 4, 4], itemlist_sarcophagus
    elif floor_level < -1:
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list= "Sarcophagus Security Zone", "Complex", (9,23,4,4,4,4,4,4), "Solid", ["DEBT COLLECTOR", "DEBT COLLECTOR", "EXECUTIVE"], [4, 4, 4], itemlist_sarcophagus
    elif floor_level < 1:
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list= "Exclusion Zone Outskirts", "Complex", (7,26,0,6,6,6,6,1), "Pits", ["HAMSTER", "DEBT COLLECTOR", "DEBT COLLECTOR"], [1, 1, 1], itemlist_beginner
    elif floor_level < 3: #Abandoned Woods
        #floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Infested Workshop", "Complex", (15, 22, 5, 5+4*16,5+5*16,5+6*16,5+7*16,5+8*16), "Solid", ["SCORPION", "TETRAHEDRON", "DEMON CORE", "CHROME DOME", "DODECAHEDRON"], [4, 4, 4, 3, 2], itemlist_end         #multicolored porcelain
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list= "Abandoned Woods", "Simple", (26, 26), "Solid", ["LEAFALOTTA", "GOOSE", "HAMSTER"], [1, 1, 1], itemlist_beginner
    elif floor_level < 5: #Silent Tributary
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Silent Tributary", "Complex", (6,27,0,6,6,6,6,1), "Flowing Water", ["GOOSE", "CHLOROSPORE", "TURTLE"], [1, 2, 1], itemlist_beginner2                    #river zone
    elif floor_level < 7: #Dense Woods
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Dense Woods", "Simple", (27, 27), "Solid", ["LEAFALOTTA", "FOX", "TURTLE"], [2, 2, 1], itemlist_beginner2                      #river zone                                        #seafoam grass (replace? too much grass?)
    elif floor_level < 9: #Reservoir
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Reservoir", "Complex", (4,25,3,3,3,6,6,1), "Water", ["CHLOROSPORE", "GOOSE", "FOX"], [2, 2, 2], itemlist_beginner2                                #lake zone
    elif floor_level < 11: #Topsoil Cavern
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Topsoil Cavern", "Complex", (19,31,1,1,10,1,1,1), "Solid", ["S'MORE", "SCORPION", "VITRIOLIVE"], [2, 1, 1], itemlist_beginner2                           #brown basalt
    elif floor_level < 13: #Coal Vein
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Coal Vein", "Complex", (17,31,1,1,0,0,6,9), "Solid", ["SCORPION", "JUJUBE", "VITRIOLIVE"], [2, 1, 1], itemlist_beginner2                          #coal vein
    elif floor_level < 16: #Petroleum Deposit
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Petroleum Deposit", "Complex", (8,29,1,1,0,0,6,9), "Petroleum", ["DRAGON", "CHROME DOME", "MONITAUR"], [1, 1, 1], itemlist_equal                         #petroleum zone
    elif floor_level < 19: #Aquifer
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Aquifer", "Complex", (8,22,1,1,9,9,6,9), "Aquifer", ["CHLOROSPORE", "LEAFALOTTA", "JUJUBE", "CULTIST"], [3, 3, 2, 2], itemlist_equal                        #aquifer
    elif floor_level < 22: #Subterranean Mudflow
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Subterraean Mudflow", "Complex", (6,30,1,6,6,6,6,0), "Mud", ["CHLOROSPORE", "MONITAUR", "LEAFAOTTA", "CULTIST"], [3, 2, 3, 2], itemlist_equal                            #mud zone
    elif floor_level < 24: #Silt Stratum
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Silt Stratum", "Complex", (18,30,1,1,0,0,6,9), "Solid", ["DEMON CORE", "TETRAHEDRON", "S'MORE", "MONITAUR"], [1, 2, 3, 2], itemlist_equal                          #teal & gold
    elif floor_level < 26: #Silt Stratum
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Silt Stratum", "Complex", (20,30,2,9,10,11,0,3), "Solid", ["DEMON CORE", "VITRIOLIVE", "FOX", "S'MORE"], [1, 2, 3, 3], itemlist_equal                         #purple & gold
    elif floor_level < 28: #Ash Pits
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Chasm", "Complex", (7,23,1,6,6,6,6,0), "Pits", ["DRAGON", "DEMON CORE", "JUJUBE", "FOX"], [2, 2, 3, 3], itemlist_equal                             #grey pits
    elif floor_level < 30: #Ash Pits
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Chasm", "Complex", (7,23,1,6,6,6,6,0), "Glowing", ["DRAGON", "DODECAHEDRON", "CHLOROSPORE", "MONITAUR"], [2, 2, 4, 3], itemlist_equal                             #grey pits
    elif floor_level < 32: #Magma Chamber
        floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Chasm Bottom", "Complex", (8,23,2,2,2,2,2,2), "Lava", ["DRAGON", "DODECAHEDRON", "TETRAHEDRON", "CULTIST"], [3, 2, 3, 3], itemlist_end                             #wavy lava
    else: #Workshop Remnants
        if random.uniform(0, 1) < 0.5:
            floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Workshop Remnant", "Complex", (7, 22, 5,5+4*16,5+5*16,5+6*16,5+7*16,5+8*16), "Pit", ["SCORPION", "CHROME DOME", "DRAGON", "CULTIST", "DODECAHEDRON"], [4, 2, 3, 3, 2], itemlist_end             #multicolored porcelain pits
        else: #Infested Workshop 
            floor_name, sc, tileset, walltype, enemy_list, level_list, item_list = "Infested Workshop", "Complex", (15, 22, 5, 5+4*16,5+5*16,5+6*16,5+7*16,5+8*16), "Solid", ["SCORPION", "TETRAHEDRON", "DEMON CORE", "CHROME DOME", "DODECAHEDRON"], [4, 4, 4, 3, 2], itemlist_end         #multicolored porcelain
    
    adventure_log.append("Progressed to floor " + str(floor_level) + " (" + str(floor_name) + ").")

    player.strength = player.maxstrength
    player.strength_visual = player.strength

    player.defense = player.maxdefense 
    player.defense_visual = player.defense
    

    if player.gold < 0:
        adventure_log.append("Paid " + str(player.gold - round(player.gold*1.1)) + " in interest.")
        player.gold = round(player.gold*1.1) #interest payments
        enemy_list.append("DEBT COLLECTOR")
        level_list.append(1)

    for item in player.inventory: #recharge all staffs
        if isinstance(item, Staff):
            item.charges = min(math.floor(item.charges + item.maxcharges*random.uniform(0.21, 0.6)), item.maxcharges)


    #Triggered after Detects stairs
    floor = make_floor(sc, item_list, enemy_list, level_list, shop_equal, floor_level, floor_name)
    #print(floor.valid_tiles)

    enemy_amount = random.randint(5, 8)
    if player.extinction_state == 0.5:
        player.extinction_state = 1

    if player.extinction_state == 1:
        item_list = itemlist_boss
        enemy_list = player.enemies_remaining*3
        level_list = [3, 3, 4]*len(player.enemies_remaining)
        enemy_amount = 30
        
    floor.random_create_item(item_list)
    floor.generate_enemies(floor_level, enemy_list, level_list, enemy_amount, player)

    
    
    player.x, player.y = floor.spawnpoint
    player.prevx, player.prevy = floor.spawnpoint
    player.initx, player.inity = floor.spawnpoint
    all_enemies = floor.all_enemies
    #floor_level +=1
    floor.map_type = sc
    floor.wall_type = walltype
    floor.tileset = tileset

    draw_map()






def draw_map():
    global bg, bg_deeper, bg_liqs, bg_liqs_foreground, floor, grid_blank, grid_liqtile

    fl_string = ""
    if floor.map_type == "Simple" or floor.map_type == "Simple 2":
        #Simple Map Initiation
        #simple_color_sets = [(26,26), (29,29), (27,27)]
        wall_texture_value, floor_texture_base_value = floor.tileset#random.choice(simple_color_sets)
        bg_order = ["#", ".", "*", "~", '%', '<', '>', "@", "S", "U"] #Filler, #Walls, #Space, @Stairs
        if floor.map_type == "Simple 2":
            bg_tilekey = [wall_texture_value*16 + 8, wall_texture_value*16 + 5, floor_texture_base_value*16+5+32, floor_texture_base_value*16+5+16, floor_texture_base_value*16+5+48, floor_texture_base_value*16+5+64, floor_texture_base_value*16+5+80, floor_texture_base_value*16+13, floor_texture_base_value*16+5-16, floor_texture_base_value*16+12]
            floor.map_type == "Simple"
        else:
            bg_tilekey = [wall_texture_value*16 + 8, wall_texture_value*16 + 6, floor_texture_base_value*16+9, floor_texture_base_value*16+7, floor_texture_base_value*16, floor_texture_base_value*16, floor_texture_base_value*16+1, floor_texture_base_value*16+13, floor_texture_base_value*16+5, floor_texture_base_value*16+12]
       
        for s in floor.map_grid:
            for s2 in s:
                fl_string += s2
    else:
        #wall, floor, floorcodes,
        #complex_wall_sets = [(12, 31, 4,4,4,4,4,4), (22,30,2,2,10,2,2,2), (21,31,1,9,10,11,0,3), (17, 24, 5,5+32,5+48,5+64,5+80,5+96)]
        #Map Initiation
        bg_order = [
            "#",   #filler
            '.',   #space
            '*',   #space texture
            '~',    #space texture
            '%',
            '<',
            '>',
            'S',    #shop

        'a',   # 0: isolated
        'b',   # 1: up
        'c',   # 2: right
        'd',   # 3: up + right

        'e',   # 4: down
        'f',   # 5: up + down
        'g',  # 6: right + down
        'h',   # 7: up + right + down

        'i',   # 8: left
        'j',   # 9: up + left
        'k',   # 10: right + left
        'l',   # 11: up + right + left
        
        'm',  # 12: down + left
        'n',   # 13: up + down + left
        'o',   # 14: right + down + left
        'p',   # 15: all sides

            "@", 
            'U'    # stairs
        ]

        wall_texture_value, floor_texture_base_value, floor_texture_code_base, floor_texture_code1, floor_texture_code2, floor_texture_code3, floor_texture_code4, floor_texture_code5, = floor.tileset
        bg_tilekey = [26*16 + 8, floor_texture_base_value*16+floor_texture_code_base, floor_texture_base_value*16+floor_texture_code1,floor_texture_base_value*16+floor_texture_code2,floor_texture_base_value*16+floor_texture_code3, floor_texture_base_value*16+floor_texture_code4, floor_texture_base_value*16+floor_texture_code5, floor_texture_base_value*16+5,
                    
                    wall_texture_value*16, wall_texture_value*16+15, wall_texture_value*16+13, wall_texture_value*16+9,
                    wall_texture_value*16+12, wall_texture_value*16+8, wall_texture_value*16+6, wall_texture_value*16+2,
                    wall_texture_value*16+14, wall_texture_value*16+11, wall_texture_value*16+10, wall_texture_value*16+5,
                    wall_texture_value*16+7, wall_texture_value*16+4, wall_texture_value*16+1,wall_texture_value*16+3,
                    floor_texture_base_value*16+13, floor_texture_base_value*16+12]
        
        for s in floor.textured_map:
            for s2 in s:
                fl_string += s2

    #bg = pyglet.sprite.Sprite(combine_tiles(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60))
    
    i = 0
    while i < 16:
        combine_tiles_efficient(tesselate(0, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
        combine_tiles_efficient(tesselate(0, grid_blank, 1, 1), 60*16, 60*16, 1, bg_liqs_foreground[i]) #sprite_blank
        i = i + 1
        
    #print(fl_string)
    combine_tiles_efficient(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60, bg) #pyglet.sprite.Sprite(combine_tiles(text_to_floor(fl_string, grid_bg, bg_order, bg_tilekey, 60), 16, 16, 60))
    bg.scale = 3
    bg.color = (255, 255, 255, 255)
    #bg_pits.image = grid_bg[0]
    combine_tiles_efficient(tesselate(0, grid_liq, 12, 12), 128, 128, 12, bg_deeper)

    frameindexes = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]#[4, 5, 6, 6, 7, 7, 7, 6, 6, 5, 4, 3, 2, 1, 1, 0, 0, 0, 1, 1, 2, 3]

    #for tile liquids:

    liquid_char_to_index = ["E", "q", "q", "q", "q", "q", "q", "q", "M", "C", "A", "D", "I", "S", "P", "W"]
    
    x = 0
    while x < floor.width:
        y = 0
        while y < floor.height:
            

            item = floor.liquid_grid[floor.height-1-y][x]

            if item != "#":
                i = 0
                while i < 16:
                    

                    bg_liqs_foreground[i].image.blit_into(grid_liqtile[i + liquid_char_to_index.index(item)*16], x*16, y*16, 0)
                    i = i + 1
            y += 1
        x += 1
#self.height-1-y






    
    if floor.wall_type == "Solid":
        if floor.map_type == "Complex":
            combine_tiles_efficient(tesselate(wall_texture_value*16+3, grid_bg, 90, 90), 16, 16, 90, bg_deeper)
        else:
            combine_tiles_efficient(tesselate(wall_texture_value*16+8, grid_bg, 90, 90), 16, 16, 90, bg_deeper)
    elif floor.wall_type == "Glowing":
        combine_tiles_efficient(tesselate(2, grid_deeper, 12, 12), 128, 128, 12, bg_deeper)
    elif floor.wall_type == "Water":
        i = 0
        while i < 16:
            combine_tiles_efficient(tesselate(frameindexes[i] + 16*9, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
            bg_liqs[i].scale = 3
            i = i + 1
        combine_tiles_efficient(tesselate(1, grid_deeper, 12, 12), 128, 128, 12, bg_deeper)
    elif floor.wall_type == "Aquifer":
        i = 0
        while i < 16:
            combine_tiles_efficient(tesselate(frameindexes[i] + 16*10, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
            bg_liqs[i].scale = 3
            i = i + 1
        combine_tiles_efficient(tesselate(3, grid_deeper, 12, 12), 128, 128, 12, bg_deeper)
    elif floor.wall_type == "Lava":
        i = 0
        while i < 16:
            combine_tiles_efficient(tesselate(frameindexes[i] + 16*6, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
            bg_liqs[i].scale = 3
            i = i + 1
    elif floor.wall_type == "Flowing Water":
        i = 0
        while i < 16:
            combine_tiles_efficient(tesselate(frameindexes[i] + 16*7, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
            bg_liqs[i].scale = 3
            i = i + 1
        combine_tiles_efficient(tesselate(0, grid_deeper, 12, 12), 128, 128, 12, bg_deeper)
    elif floor.wall_type == "Mud":
        i = 0
        while i < 16:
            combine_tiles_efficient(tesselate(frameindexes[i] + 16*5, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
            bg_liqs[i].scale = 3
            i = i + 1
    elif floor.wall_type == "Petroleum":
        i = 0
        while i < 16:
            combine_tiles_efficient(tesselate(frameindexes[i] + 16*3, grid_liq, 12, 12), 128, 128, 12, bg_liqs[i])
            bg_liqs[i].scale = 3
            i = i + 1
    elif floor.wall_type == "Pits":
        combine_tiles_efficient(tesselate(3, grid_deeper, 12, 12), 128, 128, 12, bg_deeper)
        pass
    elif floor.wall_type == "Pits 2":
        combine_tiles_efficient(tesselate(0, grid_deeper, 12, 12), 128, 128, 12, bg_deeper)
        pass


@window.event
def on_mouse_motion(x, y, dx, dy):
    global mouse_x, mouse_y
    mouse_x, mouse_y = x, y

@window.event
def on_mouse_press(mouse_x, mouse_y, button, modifiers):
    global all_buttons
    global gamestate
    global dragging_item, drag_offset
    global right_click_menu_enabled
    global item_selected
    global discovered_staffs, discovered_tomes
    global current_menu
    global player, floor, all_enemies, hotbar, floor_level
    global bg_liqs, bg_deeper, batch, menu_batch, load_menu_batch 
    if button == pyglet.window.mouse.LEFT:
        #Main menu
        if current_menu == MenuState.MAIN_MENU:
            if start_button.hit_test(mouse_x, mouse_y):
                print("Start button clicked")
                player = Player(
                    name = "DAMIEN",
                    health = 20,
                    level = 1,
                    experience = 0,
                    x = 30,
                    y = 30,
                    spriteindex = 23*8*8,
                    animtype = 1,)
                
                hotbar = Hotbar(player.inventory, group_hotbar)

                go_to_next_level(1)
                create_gui(all_buttons, player, "Good luck!", floor_level)
                create_overlay(all_buttons)
                create_mouse_overlay(all_buttons)
                
                #player.health = 2000000

                # player.add_to_inventory(floor.create_item("Mirror Shield", grid_items))
                # player.add_to_inventory(floor.create_item("Obsidian Edge", grid_items))
                player.add_to_inventory(floor.create_item("Your Task", grid_items),0,0)
                for bg in bg_liqs:
                    bg.batch = batch
                bg_deeper.batch = batch

                current_menu = MenuState.INGAME
                return
            if load_button.hit_test(mouse_x, mouse_y):
                print("Load button clicked")
                for bg in bg_liqs:
                    bg.batch = load_menu_batch 
                bg_deeper.batch = load_menu_batch
                current_menu = MenuState.LOAD_MENU
                return
        #Side menu of the game
        elif current_menu == MenuState.SIDE_MENU:
            print(discovered_staffs)
            if save_button.hit_test(mouse_x, mouse_y):
                game_data = {
                    "player": player_to_dict(player),
                    "map": map_to_dict(floor),
                    "floor_enemies": [enemy_to_dict(enemy) for enemy in floor.all_enemies],
                    "floor_level": floor_level, 
                }
                save_game_data(game_data)
                
                print("Save button clicked")
                return
        elif current_menu == MenuState.LOAD_MENU:
            for btn in load_game_buttons:
                if btn.hit_test(mouse_x, mouse_y):
                    loaded_player, loaded_floor, loaded_all_enemies, loaded_floor_level, loaded_discovered_staffs, loaded_discovered_tomes, loaded_fakenames_staffs_colorname, loaded_fakenames_tomes_colorname, loaded_fakenames_staffs_key, loaded_fakenames_tomes_key = load_game(btn.text)
                    player = loaded_player
                    floor= loaded_floor
                    print("Valid tiles", floor.valid_tiles)
                    all_enemies = loaded_all_enemies
                    floor.all_enemies = all_enemies
                    floor_level = loaded_floor_level
                    hotbar = Hotbar(player.inventory, group_hotbar)
                    update_discovered_items(loaded_discovered_staffs, loaded_discovered_tomes, loaded_fakenames_staffs_colorname, loaded_fakenames_tomes_colorname, loaded_fakenames_staffs_key, loaded_fakenames_tomes_key)
                    
                    draw_map()
                    print("Class:", type(player).__name__)
                    for key, value in vars(player).items():
                        print(f"{key}: {value}")
                    create_gui(all_buttons, player, "Good luck!", floor_level)
                    create_overlay(all_buttons)
                    create_mouse_overlay(all_buttons)
                    gamestate = 1
                    current_menu = MenuState.INGAME
                    pass
        if current_menu == MenuState.INGAME:
            item_selected = hotbar.get_selected_item()
            if gamestate == 1 and isinstance(item_selected, Staff):
                gamestate = 6 #6 means power bar mode
                create_power_bar(all_buttons, item_selected, mouse_x, mouse_y)
            if gamestate == 3:  # Inventory state
            # Check if an item is clicked in the inventor

                inventory_x = math.floor((mouse_x - int((1152)/48)*12)/(48+9)) 
                inventory_y = math.floor((-mouse_y + int((768)/48)*32)/(48+9)) + 1

                # Calculate the inventory slot based on x and y coordinates
                inventory_slot = inventory_y*10 + inventory_x
                

                if 0 <= inventory_x < 10 and 0 <= inventory_y < 4:
                    if inventory_slot > -1 and len(player.inventory) > inventory_slot:
                        # Check if the clicked position corresponds to an inventory slot
                        if dragging_item is None:
                            item_to_eval = player.inventory[inventory_slot]

                            if item_to_eval:
                                dragging_item = item_to_eval
                                dragging_item.hotbar_sprite.visible = False
                                # Set the sprite position to the mouse position
                                drag_offset = (mouse_x - item_to_eval.sprite.x, mouse_y - item_to_eval.sprite.y)
                                #remove the item from the inventory slot
                                player.inventory[inventory_slot] = None
                                #print("Dragging item:", dragging_item.name)
                        else: 
                            #if there is an item being dragged
                            #place it in the moused over inventory slot if there are no items in that slot
                            if player.inventory[inventory_slot] is None:
                                player.inventory[inventory_slot] = dragging_item
                                dragging_item = None
                            else: #if there is an item in the slot, swap them
                                item_to_eval = player.inventory[inventory_slot]
                                player.inventory[inventory_slot] = dragging_item #swap items
                                dragging_item = item_to_eval #set dragging item to the one that was in the slot
                                dragging_item.hotbar_sprite.visible = False
                                drag_offset = (mouse_x - item_to_eval.sprite.x, mouse_y - item_to_eval.sprite.y)
                            
@window.event
def on_mouse_release(x, y, button, modifiers):
    global all_anims
    global all_enemies
    global all_buttons
    global player, hotbar, floor
    
    global gamestate
    global floor
    global has_won
    global sound_magic
    global right_click_menu_enabled
    global item_selected
    global adventure_log
    
    if current_menu == MenuState.INGAME and (gamestate == 1 or gamestate == 3 or gamestate == 4 or gamestate == 5 or gamestate == 6): #this stuff can only happen between turns or in inventory
        ###################### LEFT CLICK ##############################
        if button == pyglet.window.mouse.LEFT:
            # print("length of inventory")
            # print(len(player.inventory))
            item_selected = hotbar.get_selected_item()
            right_click_menu_enabled = False
            was_button_clicked = 0
            for i, enemy in enumerate(all_enemies):
                print(f"Enemy {i}: {enemy.name} at ({enemy.x}, {enemy.y}) - Health: {enemy.health}/{enemy.maxhealth}")
            if gamestate == 1: #if the button is hovered, and the gamestate is 1, then it was clicked
                if not isinstance(item_selected, Weapon):
                    player.unequip_weapon()
                if isinstance(item_selected, Consumable):
                    player.technique = Technique.CONSUME 
                    player.techniqueitem = item_selected                        
                    gamestate = 2
                    turn_logic.do_turns(all_enemies, player, floor, all_anims)
                elif isinstance(item_selected, Weapon):
                    player.equip_weapon(item_selected)
                    #attack with weapon
                    mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                    mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                    if (mouse_x_tilemap != player.prevx or mouse_y_tilemap != player.prevy) and ((abs(mouse_x_tilemap - player.prevx) < 2 and abs(mouse_y_tilemap - player.prevy) < 2) or (abs(mouse_x_tilemap - player.prevx) < 3 and abs(mouse_y_tilemap - player.prevy) < 3 and player.equipment_weapon.name == "Rapier")):
                        player.hit(mouse_x_tilemap, mouse_y_tilemap)
                        gamestate = 2
                        turn_logic.do_turns(all_enemies, player, floor, all_anims)
                elif isinstance(item_selected, Shield):
                    if player.equipment_shield is None:
                        player.equip_shield(item_selected)
                    else:
                        player.unequip_shield()
                elif isinstance(item_selected, Tome):
                    player.techniqueitem = item_selected 
                    gamestate = 2
                    player.cast_static()
                    turn_logic.do_turns(all_enemies, player, floor, all_anims)
                    if has_won == 0:
                        pass
                    else:
                        gamestate = 0
                        create_win_lose_screen(all_buttons, "win")
                elif isinstance(item_selected, Flask) and item_selected.name != "Empty Flask":
                    mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                    mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                    player.techniqueitem = item_selected
                    player.techniquecharges = 0
                    player.splash(mouse_x_tilemap, mouse_y_tilemap)
                    gamestate = 2
                    turn_logic.do_turns(all_enemies, player, floor, all_anims)
                # elif isinstance(item_selected, Staff): #this never happens because pressing lclick with staff brings gamestate to 6
                #     print("casting staff")
                #     player.techniqueitem = item_selected
                #     gamestate = 5
                else: #unarmed attack
                    mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                    mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                    if (mouse_x_tilemap != player.prevx or mouse_y_tilemap != player.prevy) and (abs(mouse_x_tilemap - player.prevx) < 2 and abs(mouse_y_tilemap - player.prevy) < 2):
                        player.hit(mouse_x_tilemap, mouse_y_tilemap)
                        gamestate = 2
                        turn_logic.do_turns(all_enemies, player, floor, all_anims)
                      
                delete_buttons_supertype(all_buttons, 'inventory')




            #if gamestate == 1 and was_button_clicked == 0:



            


            #print(gamestate, "fwefew")
            if gamestate == 6 and was_button_clicked == 0: #button was released; check powerbar values

                for button2 in all_buttons:
                    if button2.type == "power bar":
                        speed = 6
                        func = ((button2.animframe - 0.0001)/speed % button2.extra_2) #self.extra_2*(math.asin(((self.animframe/(math.pi*3)) % 2) - 1) + math.pi/2)/math.pi
                        #t = func
                        if ((button2.animframe - 0.0001)/speed % (button2.extra_2*2)) > button2.extra_2 and func != button2.extra_2:
                            func = -func + button2.extra_2
                        button2.animframe = -24

                        if button2.extra_1 > max(round(func), 1) - 1:
                            button2.colors = [[(button2.colors[0][0][0], button2.colors[0][0][1], button2.colors[0][0][2], 0)]]
                        else:
                            button2.colors = [[(button2.colors[0][0][0], button2.colors[0][0][1], button2.colors[0][0][2], 255)]]

                        #num of charges = func
                
                #print(func)





                #print(max(round(func), 1))

                player.techniqueitem = item_selected
                if player.techniqueitem.maxcharges > 48:
                    #maxcharges = 48

                    func = math.floor(func*(player.techniqueitem.maxcharges/48))
                    #charges = math.floor(48*(item.charges/item.maxcharges))
                if func > item_selected.charges: #if num of charges exceeds amount remaining, just choose a random amount
                    func = random.randint(1, item_selected.charges)
                player.techniquecharges = max(round(func), 1)
                # print(func)
                # print(max(round(func), 1))

                mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                player.cast(mouse_x_tilemap, mouse_y_tilemap)
                gamestate = 7 #gamestate 7 is when power bar flashes, showing you what result you made it to
                
        
                


        elif button == pyglet.window.mouse.RIGHT:
            right_click_menu_enabled = True
            delete_buttons_supertype(all_buttons, 'rclick')
            #get rclick options
            item_selected = hotbar.get_selected_item()
            if gamestate == 1:
                #THROWING VIA RIGHT CLICK
                if item_selected:

                    mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
                    mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
                    player.techniqueitem = item_selected
                    player.throw(mouse_x_tilemap, mouse_y_tilemap)
                    gamestate = 2
                    turn_logic.do_turns(all_enemies, player, floor, all_anims)
                    
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    global gamestate
    global item_selected
    global player, hotbar, all_buttons
    hotbar.change_selection(scroll_y)
    print("Mouse scrolled", hotbar.selected)
    hotbar.draw_selected_slot()
    item_selected = hotbar.get_selected_item()

    if item_selected is not None:
        inventory_slot = hotbar.translate_to_inventory()
        print(f"Inventory slot:", {inventory_slot})
        print(f"inventory_item", player.inventory[inventory_slot])
        if isinstance(item_selected, Weapon):
            player.equip_weapon(item_selected)
        elif isinstance(item_selected, Staff):
            pass #sustonium
            #print("casting staff")
            #player.techniqueitem = item_selected
            #gamestate = 5
        else:
            player.unequip_weapon()
    else:
        player.unequip_weapon()

@window.event
def on_text(text):
    global typed_text
    typed_text += text

@window.event
def on_key_press(symbol, modifiers):   
    global gamestate
    global all_anims
    global floor 
    global adventure_log
    global typed_text
    global invhover

    if symbol == pyglet.window.key.BACKSPACE:
        typed_text = typed_text[:-1]
    global current_menu

    if current_menu == MenuState.MAIN_MENU:
        return

    if symbol == pyglet.window.key.M and invhover == False:
        if current_menu == MenuState.INGAME:
            current_menu = MenuState.SIDE_MENU
            print("Opening in-game menu")
            return
        elif current_menu == MenuState.SIDE_MENU:
            current_menu = MenuState.INGAME
            print("Closing in-game menu")
            return
        
    item_selected = hotbar.get_selected_item() 
    if symbol == pyglet.window.key.Q:
        #Throw items
        if gamestate == 1:
            #throw the item in the hotbar
            if item_selected is not None:
                player.drop_item(item_selected, floor, adventure_log)
                gamestate = 2
                turn_logic.do_turns(all_enemies, player, floor, all_anims)
        
        elif gamestate == 3: #kind of works but not really becasue the enemies dont take a turn after
            slot = 0 #theres probably a more pythonic way to do this, sowwy
            for item in player.inventory:
                if item is not None:
                    # i is the slot at that position
                    #if mouse is hovering over that item, draw description
                    if item.test_hovering(mouse_x, mouse_y, slot, gamestate):
                        player.drop_item(item, floor, adventure_log)

                        gamestate = 2
                        turn_logic.do_turns(all_enemies, player, floor, all_anims)
                        delete_buttons_supertype(all_buttons, 'inventory')

                        #gamestate = 2
                        # all_anims = turn_logic.do_turns(all_enemies, player, floor)

                slot = slot + 1
    if pyglet.window.key._1 <= symbol <= pyglet.window.key._9:
        hotbar.selected = symbol - pyglet.window.key._1  # 0-8
        hotbar.draw_selected_slot()
        item_selected = hotbar.get_selected_item()
        if item_selected is not None:
            if isinstance(item_selected, Weapon):
                player.equip_weapon(item_selected)
            else:
                player.unequip_weapon()
        else:
            player.unequip_weapon()
    elif symbol == pyglet.window.key._0:
        hotbar.selected = 9  # Slot 9
        hotbar.draw_selected_slot()
        item_selected = hotbar.get_selected_item()



mouse_x = 0
mouse_y = 0


adventure_log = ["PANDORIUM - A game by zeroBound and Econic", "Good luck!"]

bg_desc = pyglet.sprite.Sprite(combine_tiles(tesselate(7*16, grid_tinyfont, 24, 12), 5, 8, 24))
bg_desc_text = pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_tinyfont, 24, 12), 5, 8, 24))

#DUMB DUMB DUMB DUMB DUMB DUMB DUMB DUIEWIFEWNOIGFEWNGOERINGIUREFOIW2Q398U4OIEWJKDS - THIS IS ACTUAL CANCER WHY IS IT IN MAIN yOU FUCK 
def draw_description_but_in_main_because_main_is_cool(item, invslot, gamestate):
    global batch
    global bg_desc, bg_desc_text
    spacing = 9
    if gamestate == 3: #if in the inventory menu
        #print(f"Drawing description: {self.description}")
        # Draw the description text at the specified position
        base_x = (invslot % 10)*(48+spacing) + int((1152)/48)*12 + 9 #1152/2 -24 - (player.prevx*16 + 8)*player.scale + (self.x*16 + 8)*self.scale
        base_y = -(invslot // 10)*(48+spacing)+ spacing + int((768)/48)*32 -10#768/2-24 - (player.prevy*16 + 8)*player.scale + (self.y*16 + 8)*self.scale
        
        description = get_display_name_and_description(item)
        #description = draw_tiny_texts(item.description, base_x, base_y, group)
        if isinstance(item, Weapon):
            additional_info = f"εDamage: {item.damage} Bonus: {item.bonus}"
        elif isinstance(item, Shield):
            additional_info = f"εDefense: {item.defense} Bonus: {item.bonus}"
        elif isinstance(item, Consumable):
            additional_info = f"εNutrition: {item.nutrition_value}"
        elif isinstance(item, Staff):
            additional_info = f"εMana: {item.charges}/{item.maxcharges}"
        elif isinstance(item, Flask) and item.name != "Empty Flask":
            additional_info = f"εContents: {item.charges}/{item.maxcharges}"
        else:
            additional_info = "" #for tomes or Miscellanious?

        
        combine_tiles_efficient(tesselate(0, grid_tinyfont, 24, 12), 5, 8, 24, bg_desc_text)
        row = combine_tiles_efficient(text_to_tiles_wrapped(description[0] + "ε" + description[1] + additional_info, grid_tinyfont, letter_order, 24, "left"), 5, 8, 24, bg_desc_text)
        
        combine_tiles_efficient(tesselate(0, grid_tinyfont, 24, 12), 5, 8, 24, bg_desc)
        combine_tiles_efficient(tesselate(7*16, grid_tinyfont, 24, row+1), 5, 8, 24, bg_desc)

        bg_desc.x = base_x + 16
        bg_desc.y = base_y
        bg_desc.batch = batch
        bg_desc.scale = 3

        bg_desc_text.x = base_x + 16
        bg_desc_text.y = base_y
        bg_desc_text.batch = batch 
        bg_desc_text.scale = 3
        
    return None



        #self.list_of_all_enemies = [["LEAFALOTTA", "HAMSTER", "GOOSE"], ["LEAFALOTTA", "CHLOROSPORE", "FOX"], ["S'MORE", "CHLOROSPORE", "SCORPION"], ["SCORPION", "S'MORE", "CHROME DOME"], ["DRAGON", "S'MORE", "TETRAHEDRON"]]
        #self.list_of_all_levels = [[1, 1, 1], [1, 2, 2], [1, 2, 1], [2, 2, 2], [2, 3, 2]]
        #self.list_of_all_item_names = ["Knife", "Machete", "Scimitar", "Sickle", "Rapier", "Stick", "Obsidian Edge", "Windsword", "Staff of Division", "Staff of Swapping", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Blue Shield", "Wood Shield", "Steel Shield", "Armor Plate", "Rock", "Note", "Poultry", "Mushrooms", "Leaves", "Apple", "Candy", "Starfruit", "Durian", "Dragonfruit"]
        

# bg_desc_text = pyglet.sprite.Sprite(combine_tiles(tesselate(0, grid_tinyfont, 24, 12), 5, 8, 24))

# combine_tiles_efficient(tesselate(0, grid_tinyfont, 24, 12), 5, 8, 24, bg_desc_text)


# combine_tiles_efficient(text_to_tiles_wrapped(text, grid_tinyfont, letter_order, width, "left"), 5, 8, width, bg_desc_text)
        


# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))
# player.add_to_inventory(floor.create_item("Rock", grid_items))

# player.add_to_inventory(floor.create_item("Tome of Extinction", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Extinction", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Extinction", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Extinction", grid_items))

# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Resurrection", grid_items))


# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))
# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))
# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))
# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))
# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))
# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))
# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))
# player.add_to_inventory(floor.create_item("Fibonnaci Staff", grid_items))

# player.add_to_inventory(floor.create_item("Tome of Ascendance", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Ascendance", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Descendance", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Descendance", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Descendance", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Descendance", grid_items))
# player.add_to_inventory(floor.create_item("Tome of Descendance", grid_items))



# player.health = 200000


# Load the music file (supports .mp3, .wav, .ogg, etc.)
music = pyglet.media.load(r'audio\Cyber-Dream-Loop.mp3')  # Replace with your actual file path
music2 = pyglet.media.load(r'audio\to-the-death-159171.mp3')   # Replace with your actual file path
music3 = pyglet.media.load(r'audio\birds-chirping-75156.mp3')   # Replace with your actual file path
music4 = pyglet.media.load(r'audio\solid-state-drive-161358.mp3')   # Replace with your actual file path






# Create a player and queue the music
mplayer = pyglet.media.Player()
mplayer.queue(music)
mplayer.volume = 0.30  
mplayer.loop = True


mstate = 1

# Play the music
mplayer.play()


#most sfx are loaded in animations.py

sound_stairs = pyglet.media.load(r'audio\69298__abel_k__stairs-reg-c-down-ak.mp3', streaming=False)









global keypress_chk
keypress_chk = 0

# def print_top_memory(dt):
#     snapshot = tracemalloc.take_snapshot()
#     top_stats = snapshot.statistics('lineno')
#     print("[Top 10 memory-consuming lines]")
#     for stat in top_stats[:10]:
#         print(stat)

#render_texture = pyglet.image.Texture.create(win_x, win_y)

bg_animframe = 0
fps_display = pyglet.window.FPSDisplay(window=window)
#profiler = cProfile.Profile()
fps_display.label.color = (0, 0, 0, 255)

invhover = False
fps = 60

def get_liq_sprite(item):
    if item == "W":
        spr = 2*29 + 16
    elif item == "D":
        spr = 2*29 + 12
    elif item == "A":
        spr = 2*29 
    elif item == "M":
        spr = 2*29 + 24
    elif item == "S":
        spr = 2*29 + 4
    elif item == "C":
        spr = 2*29 + 8
    elif item == "P":
        spr = 2*29 + 20
    elif item == "I":
        spr = 2*29 + 20
    else:
        return False 
    return spr

@window.event
def on_draw():
    global bg_animframe
    global fps
    global music, music2, music3, music4, mplayer, mstate, sound_stairs
    start = time.perf_counter()
    global fps_display
    global color_templates
    global keypress_chk
    global gamestate
    global all_buttons
    global has_won
    global all_anims
    global player
    global bg
    global bg_pits
    global bg_liqs
    global bg_deeper
    global bg_liqs_foreground
    global grid_liq
    global grid_deeper
    global grid_liqtile
    global typed_text
    global item_selected
    global win_true_x, win_true_y, win_x, win_y
    global adventure_log
    global floor_level
    global batch
    global bg_desc, bg_desc_text
    global invhover



    # framebuffer.get_texture().bind()
    # glViewport(0, 0, win_x, win_y)
    # glClearColor(0, 0, 0, 1)
    # glClear(GL_COLOR_BUFFER_BIT)
    # if random.uniform(0, 1) < 0.1:
    #     print(fps)

    

    # if random.uniform(0, 1) < 0.1:
    #     print(fps)
    if fps < 75: #for some reason the fps values are x2 what they should be
        lag_shortcut_target = 2
    else:
        lag_shortcut_target = 1

    lag_shortcut = 0
    while lag_shortcut < lag_shortcut_target:
        if lag_shortcut == lag_shortcut_target-1:
            window.clear()

        if current_menu != MenuState.INGAME:
            bg_animframe += 1

            bgdp_col = color_templates[200]
            liqcolor = 200
            bg_deeper.color = bgdp_col

            i = 0
            while i < 16:
                if bg_liqs[i].color != color_templates[liqcolor]:
                    bg_liqs[i].color = color_templates[liqcolor]
                bg_liqs[i].x = 50 + (int(bg_animframe/2) % 16 - i)*10000
                bg_liqs[i].y = 50
                i = i + 1

            bg_deeper.x = 50
            bg_deeper.y = 50
            



        if current_menu == MenuState.MAIN_MENU:
            
            menu_batch.draw()
            return 
        elif current_menu == MenuState.SAVE_MENU:
            save_menu_batch.draw()
            return
        elif current_menu == MenuState.LOAD_MENU:
            load_menu_batch.draw()
            return
        elif current_menu == MenuState.SIDE_MENU:
            side_bar_batch.draw()
            return
        elif current_menu == MenuState.INGAME:

            if floor.level < -5: #birds chirping
                if mstate != 3:
                    mplayer.pause()
                    mplayer.next_source()  # skip remaining if any
                    mplayer.queue(music3)
                    mplayer.play()
                    mstate = 3
            elif (player.extinction_state == 1 or floor.level < 1): #boss music
                if mstate != 2:
                    mplayer.pause()
                    mplayer.next_source()  # skip remaining if any
                    mplayer.queue(music2)
                    mplayer.volume = 0.30
                    mplayer.play()
                    mstate = 2
            elif floor.map_grid[floor.height-1-player.y][player.x] == "S":
                if mstate != 4: #shopping
                    mplayer.pause()
                    mplayer.next_source()  # skip remaining if any
                    mplayer.queue(music4)
                    mplayer.volume = 0.16
                    mplayer.play()
                    mstate = 4
            elif mstate != 1:
                mplayer.pause()
                mplayer.next_source()  # skip remaining if any
                mplayer.queue(music)
                mplayer.volume = 0.30
                mplayer.play()
                mstate = 1
                # Toggle track state
                #track_state['current'] = 2 if track_state['current'] == 1 else 1
            # print("player position", player.x, player.y)
            # print("player prev position", player.prevx, player.prevy)
            # print("map stairs", floor.stairs)
                
        # render_texture.bind()
        # pyglet.gl.glViewport(0, 0, win_x, win_y)
        # pyglet.gl.glClearColor(0, 0, 0, 1)
        # pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)
            # render_texture.bind()
            # pyglet.gl.glViewport(0, 0, win_x, win_y)
            # pyglet.gl.glClearColor(0, 0, 0, 1)
            # pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT)

            diry = 0
            dirx = 0
            bg_animframe += 1


            # mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
            # mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
            
            # print (mouse_x_tilemap, mouse_y_tilemap)
            # mouse_x_tilemap = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))
            # mouse_y_tilemap = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))
            
            # print (mouse_x_tilemap, mouse_y_tilemap)

            # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
            # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
            if keys[pyglet.window.key.TAB] and keypress_chk == 0:
                #enter main menu
                # if gamestate == 1:
                #     keypress_chk = 1
                #     create_main_menu(all_buttons)
                #     gamestate = 0
                if gamestate == 0:
                    exit()
                    keypress_chk = 1
                    gamestate = 1
                    delete_buttons_supertype(all_buttons, 'winlose')
            if keys[pyglet.window.key.E] and keypress_chk == 0 and invhover == False:
                #enter inventory
                if gamestate == 1:
                    keypress_chk = 1
                    print("Entering inventory")
                    create_inventory_menu(all_buttons)
                    gamestate = 3
            # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MIN_FILTER, pyglet.gl.GL_NEAREST)
            # pyglet.gl.glTexParameteri(pyglet.gl.GL_TEXTURE_2D, pyglet.gl.GL_TEXTURE_MAG_FILTER, pyglet.gl.GL_NEAREST)
            if keys[pyglet.window.key.TAB] and keypress_chk == 0:
                #enter main menu
                # if gamestate == 1:
                #     keypress_chk = 1
                #     create_main_menu(all_buttons)
                #     gamestate = 0
                if gamestate == 0:
                    exit()
                    keypress_chk = 1
                    gamestate = 1
                    delete_buttons_supertype(all_buttons, 'winlose')
            if keys[pyglet.window.key.E] and keypress_chk == 0 and invhover == False:
                #enter inventory
                if gamestate == 1:
                    keypress_chk = 1
                    print("Entering inventory")
                    
                    create_inventory_menu(all_buttons)
                    gamestate = 3
                    print("All enemies:")
                    

                    #enter inventory
                elif gamestate == 3:
                    keypress_chk = 1
                    gamestate = 1
                    delete_buttons_supertype(all_buttons, 'inventory')



            
            elif gamestate == 1:
            
            #elif gamestate == 1:

                if keys[pyglet.window.key.W]:
                    diry = 1
                elif keys[pyglet.window.key.S]:
                    diry = -1


                if keys[pyglet.window.key.D]:
                    dirx = 1
                elif keys[pyglet.window.key.A]:
                    dirx = -1

                

                if dirx == 0 and diry == 0 and keys[pyglet.window.key.E] == False and keys[pyglet.window.key.TAB] == False:
                    keypress_chk = 0

            
            if diry != 0 or dirx != 0:
                if keys[pyglet.window.key.F] and (diry == 0 or dirx == 0):
                    #if holding ctrl, pass if the direction isnt diagonal
                    pass
                else:
                    player.techniqueitem = hotbar.get_selected_item()
                    player.move(dirx, diry, floor)
                    gamestate = 2
                    print(gamestate, "gamestate")
                    turn_logic.do_turns(all_enemies, player, floor, all_anims)
            else:
                if gamestate == 2 or keys[pyglet.window.key.W] or keys[pyglet.window.key.S] or keys[pyglet.window.key.A] or keys[pyglet.window.key.D] or keys[pyglet.window.key.E] or keys[pyglet.window.key.TAB]:
                    pass
                else:
                    keypress_chk = 0
            
            # print (mouse_x_tilemap, mouse_y_tilemap)

            if gamestate == 2:
                if len(all_anims) == 0 or all(anim.proceed for anim in all_anims):
                    gamestate = 1
                    #print(adventure_log)
                    #we should refresh all visuals to match their actual counterparts here just for safety
                    refresh_all_visuals(player)
                    for enemy in all_enemies:
                        refresh_all_visuals(enemy)
                    if keys[pyglet.window.key.LCTRL] == False:
                        if(player.x, player.y) == floor.stairs:
                            sfxplayer = sound_stairs.play()
                            sfxplayer.volume = 0.3
                            go_to_next_level(1)
                        if(player.x, player.y) == floor.upstairs:
                            sfxplayer = sound_stairs.play()
                            sfxplayer.volume = 0.3
                            go_to_next_level(-1)
                        #print("test")

                    if player.is_alive() == False:
                        gamestate = 0
                        i = 0
                        while i < len(player.inventory):
                            item = player.inventory[i]
                            if item != None and item.name == "Tome of Resurrection":
                                item.should_be_deleted = True
                                player.health = player.maxhealth 
                                player.health_visual = player.health
                                player.speed = 2 
                                player.speed_visual = 2
                                player.paralysis_turns = 0
                                player.paralysis_visual = 0
                                all_anims.append(animations.Animation(str(player.name) + " was resurrected by " + str(item.name) + "!", 0*29 + 24, 6, 4, (255, 255, 255, 0), 0, 50, 0, 0, 0, 0, 0, None, None, None, None, None))
                                gamestate = 1
                                break
                            i = i + 1
                        if gamestate == 0:
                            create_win_lose_screen(all_buttons, "lose")
                    elif player.haswon == True:
                        gamestate = 0
                        create_win_lose_screen(all_buttons, "win")
                    elif player.paralysis_turns > 0 or player.flee_ai_turns > 0 or player.rage_ai_turns > 0: #if the player's AI is no longer controlled by player, just do another turn
                        gamestate = 2
                        turn_logic.do_turns(all_enemies, player, floor, all_anims)


            bg.x = 1152/2 - (player.prevx*16 + 8)*player.scale
            bg.y = 768/2 - (player.prevy*16 + 8)*player.scale
            


            bgdp_col = color_templates[255]
            

            
            liqcolor = 0
            if floor.wall_type == "Water" or floor.wall_type == "Flowing Water" or floor.wall_type == "Aquifer":
                bgdp_col = color_templates[200]
                liqcolor = 200
            elif floor.wall_type == "Mud" or floor.wall_type == "Petroleum":
                liqcolor = 255
            elif floor.wall_type == "Lava":
                liqcolor = 255 - int(30*(math.sin(bg_animframe/15)+1))#(255, 255, 255, 255 - int(30*(math.sin(bg_animframe/15)+1)))
            elif floor.wall_type == "Glowing":
                bgdp_col = color_templates[int(30*(math.sin(bg_animframe/15)+1))]#(255, 128, 0, 0 + int(30*(math.sin(bg_animframe/15)+1)))
            elif floor.wall_type == "Pits":
                bgdp_col = color_templates[0]

            if bg_deeper.color != bgdp_col:
                bg_deeper.color = bgdp_col

            i = 0
            while i < 16:
                if bg_liqs[i].color != color_templates[liqcolor]:
                    
                    bg_liqs[i].color = color_templates[liqcolor]

                bg_liqs_foreground[i].x = 1152/2 - (player.prevx*16 + 8)*player.scale + (int(bg_animframe/2) % 16 - i)*10000
                bg_liqs_foreground[i].y = 768/2 - (player.prevy*16 + 8)*player.scale

                bg_liqs[i].x = 1152/2 - (player.prevx*16 + 8)*player.scale - 16*15*player.scale + (int(bg_animframe/2) % 16 - i)*10000
                bg_liqs[i].y = 768/2 - (player.prevy*16 + 8)*player.scale - 16*15*player.scale

                i = i + 1

            bg_deeper.x = 1152/2 - (player.prevx*16 + 8)*player.scale - 16*15*player.scale
            bg_deeper.y = 768/2 - (player.prevy*16 + 8)*player.scale - 16*15*player.scale

            if bg_animframe % 12 == 0:
                item = get_liq_sprite(floor.liquid_grid[floor.height-1-player.y][player.x]) 
                if item != 0:

                    all_anims.append(animations.Animation("", item, 9, 5, (255, 255, 255, 0), 0, 12, player.x, player.y, player.x, player.y, floor.liquid_grid[floor.height-1-player.y][player.x], None, None, None, None, 0, None))

                for enemy in all_enemies:
                    item = get_liq_sprite(floor.liquid_grid[floor.height-1-enemy.y][enemy.x]) 
                    if ((enemy.x > player.x + 13 or enemy.x < player.x - 13) or (enemy.y > player.y + 9 or enemy.y < player.y - 9)) or item == 0:
                        pass
                    else:
                        all_anims.append(animations.Animation("", item, 9, 5, (255, 255, 255, 0), 0, check_if_entity_is_on_screen(enemy, player, 1, 12), enemy.x, enemy.y, enemy.x, enemy.y, floor.liquid_grid[floor.height-1-player.y][player.x], None, None, None, None, 0, None))


            player.draw(animation_presets, group_enemies, group_enemies_bg, group_enemies_fg, hotbar.get_selected_item(), all_anims, floor)

            for enemy in all_enemies:
                enemy.draw(animation_presets, player, group_enemies, group_enemies_bg, group_enemies_fg, all_anims, floor)

            for item in floor.floor_items:
                 item.draw(player, group_items)

            bg_desc.color = (128, 128, 128,0)

            bg_desc_text.color = (0, 0, 0, 0)

            flag = 0
            slot = 0 #theres probably a more pythonic way to do this, sowwy
            for item in player.inventory:
                if dragging_item:
                    dragging_item.sprite.x = mouse_x - drag_offset[0]
                    dragging_item.sprite.y = mouse_y - drag_offset[1]
                if item is not None:
                    # i is the slot at that position
                    item.draw_inventory(player, group_inv, slot, gamestate)
                    #if mouse is hovering over that item, draw description
                    if item.test_hovering(mouse_x, mouse_y, slot, gamestate):

                        flag2 = False
                        if invhover != item:
                            print("Fakenames_staffs_colormnames", fakenames_staffs_colornames)
                            typed_text = get_display_name(item)
                            #ttprev = typed_text
                            invhover = item
                            flag2 = True

                        #check keyboard 
                        if isinstance(item, Tome) or isinstance(item, Staff):

                            if isinstance(item, Staff):
                                if typed_text[:20] != fakenames_staffs_colornames[item.magic_color]:
                                    flag2 = True
                                fakenames_staffs_colornames[item.magic_color] = typed_text[:20]
                            else:
                                if typed_text[:20] != fakenames_tomes_colornames[item.magic_color]:
                                    flag2 = True
                                fakenames_tomes_colornames[item.magic_color] = typed_text[:20]
                                # fakenames_staffs_colornames = ["Mahogany Staff", "Red Staff", "Orange Staff", "Umber Staff", "Brown Staff", "Hazel Staff", "Dijon Staff", "Gold Staff", "Yellow Staff", "Broccoli Staff", "Green Staff", "Spring Staff", "Peacock Staff", "Cyan Staff", "Seafoam Staff", "Navy Staff", "Blue Staff", "Sky Blue Staff", "Blackberry Staff", "Violet Staff", "Lavender Staff", "Burgundy Staff", "Magenta Staff", "Pink Staff", "Black Staff", "Graphite Staff", "Grey Staff", "Ashen Staff", "White Staff"]
                                # fakenames_tomes_colornames = ["Mahogany Tome", "Red Tome", "Orange Tome", "Umber Tome", "Brown Tome", "Hazel Tome", "Dijon Tome", "Gold Tome", "Yellow Tome", "Broccoli Tome", "Green Tome", "Spring Tome", "Peacock Tome", "Cyan Tome", "Seafoam Tome", "Navy Tome", "Blue Tome", "Sky Blue Tome", "Blackberry Tome", "Violet Tome", "Lavender Tome", "Burgundy Tome", "Magenta Tome", "Pink Tome", "Black Tome", "Graphite Tome", "Grey Tome", "Ashen Tome", "Blank Tome"]

                        if flag2 == True:
                            draw_description_but_in_main_because_main_is_cool(item, slot, gamestate)
                        flag = 1


                        bg_desc.color = (33, 33, 33, 190)
                        bg_desc.group = group_inv_ext

                        bg_desc_text.color = (255, 255, 255, 255)
                        bg_desc_text.group = group_inv_ext_2
                slot = slot + 1

            if flag == 0:
                invhover = False
            
            hotbar.update_hotbar(player.inventory)
            hotbar.draw_hotbar_items(group_hotbar)

            
            if keys[pyglet.window.key.LSHIFT]:
                while len(all_anims) > 0:
                    for anim in all_anims:
                        anim.draw(player, group_effects, floor, adventure_log, bg_liqs_foreground, keys[pyglet.window.key.LCTRL])
                    delete_object.delobj(all_anims)
            else:
                for anim in all_anims:
                    anim.draw(player, group_effects, floor, adventure_log, bg_liqs_foreground, keys[pyglet.window.key.LCTRL])
                delete_object.delobj(all_anims)
            

            if gamestate != 2:
                delete_object.delobj(all_enemies)
            
            delete_object.delobj(floor.floor_items)
            # delete_object.delobj(player.active_projectiles) projectiles get deleted somehow even without this. so. whatev.
            delete_object.delobj(all_anims)
            #delete_object.delobj(player.inventory)
            delete_object.delobj(all_buttons)

            

            #unique inventory deletion script
            objlist = player.inventory
            i = 0
            while i < len(objlist):
                if objlist[i] is not None:
                    if objlist[i].should_be_deleted == True: #this attribute exists in all classes; set to True to delete an object.
                        if hasattr(objlist[i], 'sprite') == True and objlist[i].sprite != None:
                            objlist[i].sprite.delete()  
                            del objlist[i].sprite
                            del objlist[i].hotbar_sprite       
                        if hasattr(objlist[i], 'sprites') == True:
                            for sprite in objlist[i].sprites:
                                sprite.delete()  
                                del sprite       
                        objlist[i] = None
                    else:
                        i += 1
                else:
                        i += 1





            for button in all_buttons:
                button.hovered = button.is_mouse_over(mouse_x, mouse_y)

                button.draw(group_ui_bg, group_ui, group_inv_bg, group_inv, group_overlay, group_inv_ext, player, gamestate)

                if button.type == "GUI_HP":
                    button.sprites[1].y = button.sprites[0].y-48
                    button.sprites[3].y = button.sprites[3].y-24
                    button.sprites[4].y = button.sprites[4].y-48
                    pass
                    gui_string = get_gui_string(player, floor_level)
                    if gui_string != button.extra_1:
                        sprite = button.sprites[1] 
                        combine_tiles_efficient(text_to_tiles_wrapped(gui_string, grid_tinyfont, letter_order, len(gui_string)+1, "left"), 5, 8, len(gui_string)+1, sprite)
                        button.extra_1 = gui_string
                    if len(adventure_log)-1 != button.extra_2 // 8:
                        button.extra_2 += 1
                        
                        if button.extra_2 % 8 == 1:
                            button.extra_2 = int(button.extra_2)
                            advlog_string =  adventure_log[(button.extra_2 // 8)+1] +"ε"+ adventure_log[(button.extra_2 // 8)]+"ε"+adventure_log[(button.extra_2 // 8)-1]
                            sprite2 = button.sprites[2] 
                            combine_tiles_efficient(text_to_tiles_wrapped(advlog_string, grid_tinyfont, letter_order, len(advlog_string)+1, "left"), 5, 8, len(advlog_string)+1, sprite2)
                    button.sprites[2].y = button.sprites[2].y- 24-((button.extra_2 - 1) % 8 + 1)*3
                elif button.type == "overlay":
                    if gamestate == 3:
                        button.colors = [[(33, 33, 33, 90), (33, 33, 33, 90), (33, 33, 33, 90)]]
                    else:
                        button.colors = [[(33, 33, 33, 0), (33, 33, 33, 0), (33, 33, 33, 0)]]
                elif button.type == "mouse_overlay":
                    if gamestate == 1 or gamestate == 2 or gamestate == 4 or gamestate == 5: 
                        button.colors = [[(33, 33, 33, 90), (33, 33, 33, 90), (33, 33, 33, 90)]]
                        button.x = math.floor(mouse_x/48 - (1152/2)/48 + (player.x + 0.5))*16*3 + 1152/2 - (player.prevx*16 + 8)*player.scale
                        button.y = math.floor(mouse_y/48 - (768/2)/48 + (player.y + 0.5))*16*3 + 768/2 - (player.prevy*16+8)*player.scale + 16
                    else:
                        button.colors = [[(33, 33, 33, 0), (33, 33, 33, 0), (33, 33, 33, 0)]]
                elif button.supertype == "power bar":
                    
                    if gamestate != 6 and gamestate != 7:
                        button.should_be_deleted = True
                    if gamestate == 7 and button.animframe == 1:
                        
                        turn_logic.do_turns(all_enemies, player, floor, all_anims)
                        gamestate = 2
            lag_shortcut += 1


                    

            

    #s1 = time.perf_counter()

                    

            

    #s1 = time.perf_counter()


    # s2 = time.perf_counter()
    # s2 = time.perf_counter()

    batch.draw()

    # s2 = time.perf_counter()



    end = time.perf_counter()
    fps = 1/(end-start)
    #print(fps)
    # if bg_animframe%60 == 0:
    #     print(end-start, s2-s1)
    #     print(sum(1 for obj in gc.get_objects() if isinstance(obj, pyglet.image.Texture)))

    fps = 1/(end-start)
    #print(fps)
    # if bg_animframe%60 == 0:
  
    #fps_display.draw()
        # draw
    # profiler.disable()
    # profiler.dump_stats("on_draw.prof")

    # if bg_animframe%60 == 0:
    #     print(end-start, s2-s1)
    #     print(sum(1 for obj in gc.get_objects() if isinstance(obj, pyglet.image.Texture)))
        #gc.collect(generation=2)
        #sys._clear_internal_caches()
        #pass

        
        
        
        #print("allocated blocks: " + str(sys.getallocatedblocks()))
        #print(objgraph.count('Projectile'))
        #print(f"RSS (Resident Set Size): {mem_info.rss / (1024 * 1024):.2f} MB")
        #print(f"VMS (Virtual Memory Size): {mem_info.vms / (1024 * 1024):.2f} MB")
        #objgraph.show_growth()


pyglet.app.run()



