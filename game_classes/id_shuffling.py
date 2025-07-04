
import random
from game_classes.item import *
#initialize fakename to realname list for staffs and tomes
#the 'key' number represents local sprite index (aka the color)
#any items wit a definite sprite & name are excluded (e.g. #28 (white) & #24 (black) for tomes)
fakenames_staffs_key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 26]
fakenames_tomes_key = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 23, 26]

fakenames_staffs_colornames = ["Mahogany Staff", "Red Staff", "Orange Staff", "Umber Staff", "Brown Staff", "Hazel Staff", "Dijon Staff", "Gold Staff", "Yellow Staff", "Broccoli Staff", "Green Staff", "Spring Staff", "Peacock Staff", "Cyan Staff", "Seafoam Staff", "Navy Staff", "Blue Staff", "Sky Blue Staff", "Blackberry Staff", "Violet Staff", "Lavender Staff", "Burgundy Staff", "Magenta Staff", "Pink Staff", "Black Staff", "Graphite Staff", "Grey Staff", "Ashen Staff", "White Staff"]
fakenames_tomes_colornames = ["Mahogany Tome", "Red Tome", "Orange Tome", "Umber Tome", "Brown Tome", "Hazel Tome", "Dijon Tome", "Gold Tome", "Yellow Tome", "Broccoli Tome", "Green Tome", "Spring Tome", "Peacock Tome", "Cyan Tome", "Seafoam Tome", "Navy Tome", "Blue Tome", "Sky Blue Tome", "Blackberry Tome", "Violet Tome", "Lavender Tome", "Burgundy Tome", "Magenta Tome", "Pink Tome", "Black Tome", "Graphite Tome", "Grey Tome", "Ashen Tome", "Blank Tome"]

fakenames_staffs_realnames = ("Greater Healing Staff", "Staff of Division", "Staff of Swapping", "Lesser Healing Staff", "Energizing Staff", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Phobia Staff", "Staff of Violence", "Staff of Cloning", "Staff of Metamorphosis", "Staff of Primes", "Fibonnaci Staff", "Staff of Alchemy", "Gardening Staff", "Mirror Staff", "Volatile Staff", "Staff of Osteoporosis", "Staff of Fatigue")
fakenames_tomes_realnames = ("Tome of Recovery", "Tome of Injury", "Tome of Promotion", "Tome of Demotion", "Immunity Tome", "Paperskin Tome", "Sharpening Tome", "Fortifying Tome", "Tome of Consolidation", "Tome of Reversal", "Coloring Tome", "Summoning Tome", "Banishing Tome", "Tome of Pizzazz", "Bankruptcy Tome", "Tome of Identification", "Tome of Ascendance", "Tome of Descendance", "Tome of Extinction", "Tome of Resurrection", "Duplication Tome", "Tome of Exchange", "Weaponsmithing Tome", "Shieldsmithing Tome")


random.shuffle(fakenames_staffs_key)
random.shuffle(fakenames_tomes_key)




discovered_staffs = []
discovered_tomes = [24, 28] #reveal Ruined, Blank, (and Reversal? , fakenames_tomes_key[9])

def get_display_name_and_description(item):
    global discovered_staffs 
    global discovered_tomes 
    global fakenames_staffs_colornames
    global fakenames_tomes_colornames
    if isinstance(item, Tome):
        if (item.magic_color in discovered_tomes) == True:
            return item.name, item.description
        else:
            return fakenames_tomes_colornames[item.magic_color], "This item hasn't been identified. (Type to give it a label)."
    elif isinstance(item, Staff):
        if (item.magic_color in discovered_staffs) == True:
            return item.name, item.description
        else:
            return fakenames_staffs_colornames[item.magic_color], "This item hasn't been identified. (Type to give it a label)."
    else:
        return item.name, item.description

def get_display_name(item):
    
    global discovered_staffs 
    global discovered_tomes 
    global fakenames_staffs_colornames
    global fakenames_tomes_colornames
    if (isinstance(item, Tome)) or (isinstance(item, list) and "Tome" in item[1]):
        if (item.magic_color in discovered_tomes) == True:
            return item.name
        else:
            return fakenames_tomes_colornames[item.magic_color]
    elif isinstance(item, Staff) or (isinstance(item, list) and "Staff" in item[1]):
        if (item.magic_color in discovered_staffs) == True:
            return item.name
        else:
            return fakenames_staffs_colornames[item.magic_color]
    else:
        return item.name
    
def discover_item(item):

    global discovered_staffs 
    global discovered_tomes 
    global fakenames_staffs_colornames
    global fakenames_tomes_colornames
    if isinstance(item, Tome):
        if (item.magic_color in discovered_tomes) == False:
            discovered_tomes.append(item.magic_color)
            return "The " + str(fakenames_tomes_colornames[item.magic_color]) + " was a " + str(item.name) + "!"
    elif isinstance(item, Staff):
        if (item.magic_color in discovered_staffs) == False:
            discovered_staffs.append(item.magic_color)
            return "The " + str(fakenames_staffs_colornames[item.magic_color]) + " was a " + str(item.name) + "!"
    return False









