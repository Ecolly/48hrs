import random
from game_classes.item import Item, Weapon, Consumable, Shield, Staff, Miscellanious, Tome
from game_classes.enemy import*
from game_classes.id_shuffling import *
from font import *


#fakenames_staffs_names = ["Mahogany Staff", "Red Staff", "Orange Staff", ""]
def round_up_to_nearest_odd(n):
    # Round up to the nearest integer
    rounded = math.ceil(n)
    # If it's already odd, return it
    if rounded % 2 == 1:
        return rounded
    # If it's even, add 1 to make it odd
    return rounded + 1


def make_floor(type, item_list, enemy_list, level_list, shop_list, level):

    number_of_rooms = random.randint(5, 9)  # Random number of rooms between 5 and 10
    test_map = Map(60, 60, number_of_rooms, default_tile='#')

    test_map.enemy_list = enemy_list 
    test_map.level_list = level_list 
    test_map.item_list = item_list 

    test_map.level = level

    test_map.check_generate_room(test_map.rooms, shop_list)
    test_map.connect_rooms()
    test_map.check_valid_tile()
    test_map.create_stairs() # Populate valid tiles after room generation
    test_map.assign_spawnpoint()

    if type=="Complex":
        test_map.auto_tile_ascii()
        test_map.map_type = "Complex"
        test_map.map_grid = test_map.textured_map
    test_map.assign_textures_to_all_floor_tiles()
    print(test_map)
    return test_map

class Map:
    def __init__(self, width, height, number_of_rooms, default_tile='#'):
        self.map_type = "Simple"
        self.wall_type = "Solid"
        self.width = width
        self.height = height
        self.number_of_rooms = number_of_rooms
        self.rooms = []  # List to store the rooms
        self.level = 1
        self.map_grid = [['#' for _ in range(width)] for _ in range(height)]
        self.liquid_grid = [['#' for _ in range(width)] for _ in range(height)]

        self.valid_tiles = []
        self.textured_map = [[]]
        self.valid_entity_tiles = []
        self.valid_tiles_noshop = []
        self.name = "Strange Floor"

        self.item_list = None #these are lists of what enemies/items can spawn in a level
        self.enemy_list = None 
        self.level_list = None
        #self.list_of_all_enemy_names = ["LEAFALOTTA", "HAMSTER", "GOOSE", "CHLOROSPORE", "FOX", "S'MORE"]
        
        
        #self.list_of_all_enemies = [["LEAFALOTTA", "HAMSTER", "GOOSE"], ["LEAFALOTTA", "CHLOROSPORE", "FOX"], ["S'MORE", "CHLOROSPORE", "SCORPION"], ["SCORPION", "S'MORE", "CHROME DOME"], ["DRAGON", "S'MORE", "TETRAHEDRON"]]
        #self.list_of_all_levels = [[1, 1, 1], [1, 2, 2], [1, 2, 1], [2, 2, 2], [2, 3, 2]]
        #self.list_of_all_item_names = ["Knife", "Machete", "Scimitar", "Sickle", "Rapier", "Stick", "Fury Cutter", "Windsword", "Staff of Division", "Staff of Swapping", "Staff of Mana", "Staff of Ricochet", "Staff of Lethargy", "Staff of Paralysis", "Staff of Warping", "Piercing Staff", "Execution Staff", "Blue Shield", "Wood Shield", "Steel Shield", "Armor Plate", "Rock", "Note", "Poultry", "Mushrooms", "Leaves", "Apple", "Cherry", "Starfruit", "Durian", "Dragonfruit"]
        
        
        self.floor_items = []  # List to hold items on the floor
        self.all_enemies = []
        self.spawnpoint = set()
        self.stairs = set() #stairs location on the map
        self.upstairs = set()
        
        
    
    #set the room tiles to be '.' (empty space)
    def assign_textures_to_all_floor_tiles(self):
        textures = ['.', '*', '~', '%', '<', '>']
        weights = [10, 1, 1, 1, 1, 1]
        for i in range(self.height):
            for j in range(self.width):
                if self.map_grid[i][j] == '.':
                    tile = random.choices(textures, weights=weights)[0]
                    self.map_grid[i][j] = tile

    def generate_room(self, x, y, room_width, room_height, shop, item_list):
        global grid_items
        for i in range(y, y + room_height):
            for j in range(x, x + room_width):
                if 0 <= i < self.height and 0 <= j < self.width:
                    if shop == True:
                        self.map_grid[i][j] = 'S'
                        #print(i, j, x, y, room_height, room_width)
                        lower_bound_y = math.floor((y+y+room_height)/2 - 1)
                        upper_bound_y = math.floor((y+y+room_height)/2 + 1)
                        lower_bound_x = math.floor((x+x+room_width)/2 - 1)
                        upper_bound_x = math.floor((x+x+room_width)/2 + 1)


                        if i <= upper_bound_y and i >= lower_bound_y and j <= upper_bound_x and j >= lower_bound_x: #((room_height > 6 or room_width > 6) and i > y + 1 and i < y+room_height-2 and j > x + 1 and j < x+room_width-2) or (i > y and i < y+room_height-1 and j > x and j < x+room_width-1):

                            item_name = random.choice(item_list)
                            item = self.create_item(item_name, grid_items)
                            print(item_name)
                            item.x = j
                            item.y = -i + self.height - 1
                            self.floor_items.append(item)



                    else:
                        self.map_grid[i][j] = '.'  # Set the room area to empty space








    
    #check if a room can be generated at the given coordinates
    #checks it against existing rooms list
    def check_generate_room(self, rooms, item_list):
        max_possible_size = 13#18#min(self.width, self.height) // 2
        min_possible_size = 5#12
        has_shop = False
        max_size = max(min_possible_size, int(max_possible_size * (1 - (self.number_of_rooms / 20))))
        min_size = max(min_possible_size, int(max_size * 0.6))
        #self.number_of_rooms = 2
        rooms_created = 0
        attempts = 0
        max_attempts = self.number_of_rooms * 10  # Limit attempts to avoid infinite loop


        while rooms_created < self.number_of_rooms and attempts < max_attempts:
            width = round_up_to_nearest_odd(random.randint(min_size, max_size))
            height = round_up_to_nearest_odd(random.randint(min_size, max_size))
            x = random.randint(0, self.width - width - 1)
            y = random.randint(0, self.height - height - 1)

            # Coordinates of the new room and how big it is
            new_room = (x, y, width, height)
            failed = False
            # Check if the new room overlaps with existing rooms
            for other_rooms in rooms:
                ox, oy, owidth, oheight = other_rooms
                if (x < ox + owidth and x + width > ox and
                    y < oy + oheight and y + height > oy):
                    failed = True
                    break
            if not failed:
                print(f"Room {rooms_created} generated at ({x}, {y}) with size ({width}, {height})")
                # If no overlap, generate the room
                if has_shop == False and random.uniform(0, 1) < 0.04:
                    self.generate_room(x, y, width, height, True, item_list)
                    has_shop = True

                else:
                    self.generate_room(x, y, width, height, False, item_list)
                #self.generate_border(x, y, width, height)
                rooms.append(new_room)
                rooms_created += 1
            attempts += 1


    def __str__(self):
        return '\n'.join(''.join(row) for row in self.map_grid)
    

    # def check_surrounding_tiles(self, x, y):
    #     """Check surrounding tiles for different texture"""
    #     for i in 

    def create_stairs(self):
        #initiated after the corridors are generated
        #need to find a better way to place it
        random_location = random.choice(self.valid_tiles_noshop)
        y, x = random_location
        self.valid_entity_tiles.remove(random_location)
        self.map_grid[self.height -1 -y][x] = '@'
        self.stairs = (x,y)

    def assign_spawnpoint(self):
        random_location = random.choice(self.valid_entity_tiles)
        y, x = random_location
        self.spawnpoint = (x,y)
        
    #floor_items = []  # List to hold items on the floor

    def create_item(self, name, grid_items):
        # Example dummy factory
        global fakenames_staffs_key
        global fakenames_tomes_key
        grid_items = grid_items


        if name == "Knife":
            return Weapon(name, sprite_locs = 0, damage=4, durability=100, description="A common household chef's knife.", price=10)
        elif name == "Machete":
            return Weapon(name, sprite_locs = 1, damage=5, durability=100, description="A long-bladed knife useful for cutting plants.", price=15)
        elif name == "Scimitar":
            return Weapon(name, sprite_locs = 2, damage=7, durability=100, description="A sharp, curved blade.", price=20)
        elif name == "Sickle":
            return Weapon(name, sprite_locs = 4, damage=3, durability=100, description="A crescent-shaped blade that can reach three enemies at once.", price=25)
        elif name == "Rapier":
            return Weapon(name, sprite_locs = 5, damage=6, durability=100, description="A thin, slender weapon that can reach two tiles in front.",price=30)
        elif name == "Stick":
            return Weapon(name, sprite_locs = 6, damage=2, durability=100, description="A thick tree branch that can be used as a crude weapon.",price=3)
        elif name == "Fury Cutter":
            return Weapon(name, sprite_locs = 9, damage=20, durability=100, description="Ominous energy seeps off the cutting edge. The weapon returns 1/4 of damage dealt to the bearer.",price=50) #deducts 1/4 of attack damage from your hp
        elif name == "Windsword":
            return Weapon(name, sprite_locs = 10, damage=9, durability=100, description="Imbued with magical runes, this longsword is more powerful than the average weapon.",price=80)
        
        
        
        
        
        
        
        elif name == "Greater Healing Staff":
            return Staff(name, reverse="Staff of Division",sprite_locs = fakenames_staffs_key[0], damage=10, projectile=True, description="Multiplies the target's HP by 2.", charges=5, rarity=2) #multiplies enemy's hp by 2
        elif name == "Staff of Division":
            return Staff(name, reverse="Greater Healing Staff",sprite_locs = fakenames_staffs_key[1], damage=10, projectile=True, description="Divides the target's HP by 2.", charges=5, rarity=2) #divides enemy's hp by 2
        elif name == "Staff of Swapping":
            return Staff(name, reverse="Staff of Warping", sprite_locs = fakenames_staffs_key[2], damage=10, projectile=True, description="Swap places with target.", charges=12, rarity=1) #swap places
        elif name == "Lesser Healing Staff":
            return Staff(name, reverse="Staff of Mana",sprite_locs = fakenames_staffs_key[3], damage=10, projectile=True, description="Healing depends on mana used.", charges=12, rarity=1) #deals set healing according to mana used
        elif name == "Energizing Staff":
            return Staff(name, reverse="Staff of Lethargy",sprite_locs = fakenames_staffs_key[4], damage=10, projectile=True, description="Target's speed is doubled. Duration depends on mana used.", charges=8, rarity=1) #deals set healing according to mana used
        elif name == "Staff of Mana":
            return Staff(name, reverse="Lesser Healing Staff", sprite_locs = fakenames_staffs_key[5], damage=10, projectile=True, description="Damage depends on mana used.", charges=12, rarity=1) #deals set damage according to # of charges used
        elif name == "Staff of Ricochet":
            return Staff(name, reverse="Piercing Staff", sprite_locs = fakenames_staffs_key[6], damage=10, projectile=True, description="Projectile bounces off walls.", charges=8, rarity=1) #bounces
        elif name == "Staff of Lethargy":
            return Staff(name,  reverse="Energizing Staff",sprite_locs = fakenames_staffs_key[7], damage=10, projectile=True, description="Target's speed is reduced to 1/2. Duration depends on mana used.", charges=8, rarity=2) #slows down enemy
        elif name == "Staff of Paralysis":
            return Staff(name,  reverse="Energizing Staff" ,sprite_locs = fakenames_staffs_key[8], damage=10, projectile=True, description="Paralyzes target. Duration depends on mana used.", charges=8, rarity=2) #paralyzes enemy
        elif name == "Staff of Warping":
            return Staff(name,  reverse="Staff of Swapping",sprite_locs = fakenames_staffs_key[9], damage=10, projectile=True, description="Warps target to a random location on the floor.", charges=5, rarity=2) #levels up all enemies on a floor, including you
        elif name == "Piercing Staff":
            return Staff(name,  reverse="Staff of Ricochet",sprite_locs = fakenames_staffs_key[10], damage=10, projectile=True, description="Target pierces a number of enemies equal to mana used.", charges=8, rarity=2) #pierces enemies
        elif name == "Execution Staff":
            return Staff(name,  reverse="Staff of Division", sprite_locs = fakenames_staffs_key[11], damage=10, projectile=True, description="Deals 3 damage. Enemies killed by the staff have experience yields multiplied by mana used.", charges=8, rarity=1) 
        elif name == "Phobia Staff":
            return Staff(name,  reverse="Staff of Violence",sprite_locs = fakenames_staffs_key[12], damage=10, projectile=True, description="Target flees from you. Duration depends on mana used.", charges=8, rarity=1) 
        elif name == "Staff of Violence":
            return Staff(name,  reverse="Phobia Staff", sprite_locs = fakenames_staffs_key[13], damage=10, projectile=True, description="Target attempts to fight you using physical attacks only. Duration depends on mana used.", charges=8, rarity=1) 
        elif name == "Staff of Cloning":
            return Staff(name,  reverse="Staff of Cloning",sprite_locs = fakenames_staffs_key[14], damage=10, projectile=True, description="A duplicate of the target is created.", charges=5, rarity=2)
        elif name == "Staff of Metamorphosis":
            return Staff(name,  reverse="Staff of Metamorphosis", sprite_locs = fakenames_staffs_key[15], damage=10, projectile=True, description="Target is transformed into a random enemy at a random level.", charges=5, rarity=2) 
        elif name == "Staff of Primes":
            return Staff(name,  reverse="Staff of Primes",sprite_locs = fakenames_staffs_key[16], damage=10, projectile=True, description="Damage depends on mana used. Will be a prime number.", charges=12, rarity=1)
        elif name == "Fibonnaci Staff":
            return Staff(name,  reverse="Fibonnaci Staff", sprite_locs = fakenames_staffs_key[17], damage=10, projectile=True, description="Damage depends on mana used; follows the fibonnaci sequence.", charges=8, rarity=2) 
        elif name == "Staff of Alchemy":
            return Staff(name,  reverse="Gardening Staff",sprite_locs = fakenames_staffs_key[18], damage=10, projectile=True, description="The projectile transmutes liquids it travels over randomly.", charges=5, rarity=3)
        elif name == "Gardening Staff":
            return Staff(name,  reverse="Staff of Alchemy", sprite_locs = fakenames_staffs_key[19], damage=10, projectile=True, description="The projectile materializes water over tiles it travels over.", charges=5, rarity=2) 
        # elif name == "Blasting Staff":
        #     return Staff(name,  reverse="Staff of Suffocation",sprite_locs = fakenames_staffs_key[20], damage=10, projectile=True, description="The projectile can be used to make tunnels.", charges=5, rarity=3)
        # elif name == "Staff of Suffocation":
        #     return Staff(name,  reverse="Blasting Staff", sprite_locs = fakenames_staffs_key[21], damage=10, projectile=True, description="The projectile materializes a 3x3 square of walls wherever it hits.", charges=5, rarity=2) 
        
        
        
        
        
        elif name == "Tome of Recovery":
            return Tome(name,  reverse="Tome of Injury", sprite_locs = fakenames_tomes_key[0], damage=10, projectile=False, description="Heal 15 HP from all creatures on the floor.", price=20)
        elif name == "Tome of Injury":
            return Tome(name,  reverse="Tome of Recovery", sprite_locs = fakenames_tomes_key[1], damage=10, projectile=False, description="Deduct 15 HP from all creatures on the floor.", price=20)
        elif name == "Tome of Promotion":
            return Tome(name,  reverse="Tome of Demotion", sprite_locs = fakenames_tomes_key[2], damage=10, projectile=False, description="Level up all creatures on the floor.", price=30)
        elif name == "Tome of Demotion":
            return Tome(name,  reverse="Tome of Promotion", sprite_locs = fakenames_tomes_key[3], damage=10, projectile=False, description="Level down all creatures on the floor.", price=30)
        elif name == "Immunity Tome":
            return Tome(name,  reverse="Paperskin Tome", sprite_locs = fakenames_tomes_key[4], damage=10, projectile=False, description="Temporarily boost defense of all creatures on the floor to 100.", price=40)
        elif name == "Paperskin Tome":
            return Tome(name,  reverse="Immunity Tome", sprite_locs = fakenames_tomes_key[5], damage=10, projectile=False, description="Makes all creatures on the floor die to a single physical attack.", price=40)
        elif name == "Sharpening Tome":
            return Tome(name,  reverse="Fortifying Tome", sprite_locs = fakenames_tomes_key[6], damage=10, projectile=False, description="Finds the last weapon in your inventory and boosts attack by 1.", price=20)
        elif name == "Fortifying Tome":
            return Tome(name,  reverse="Sharpening Tome", sprite_locs = fakenames_tomes_key[7], damage=10, projectile=False, description="Finds the last shield in your inventory and boosts defense by 1.", price=20)
        #elif name == "Staffboost Tome":
        #    return Tome(name,  reverse="Sharpening Tome", sprite_locs = fakenames_tomes_key[8], damage=10, projectile=False, description="Finds the last staff in your inventory and boosts max mana by 1.", price=30)
        elif name == "Tome of Consolidation":
            return Tome(name,  reverse="Coloring Tome", sprite_locs = fakenames_tomes_key[8], damage=10, projectile=False, description="Finds the last two staffs, shields, or weapons in your inventory. For shields and weapons, last item gains the bonus of the first item. For staffs, combine mana if staffs are the same kind. First item is destroyed.", price=40)
            return Tome(name,  reverse="Coloring Tome", sprite_locs = fakenames_tomes_key[8], damage=10, projectile=False, description="Finds the last two staffs, shields, or weapons in your inventory. For shields and weapons, last item gains the bonus of the first item. For staffs, combine mana if staffs are the same kind. First item is destroyed.", price=40)
        elif name == "Tome of Reversal":
            return Tome(name,  reverse="Blank Tome", sprite_locs = fakenames_tomes_key[9], damage=10, projectile=False, description="Finds the last staff or tome in your inventory. Item effect is reversed or altered.", price=40)
            return Tome(name,  reverse="Blank Tome", sprite_locs = fakenames_tomes_key[9], damage=10, projectile=False, description="Finds the last staff or tome in your inventory. Item effect is reversed or altered.", price=40)
        elif name == "Coloring Tome":
            return Tome(name,  reverse="Tome of Consolidation",sprite_locs = fakenames_tomes_key[10], damage=10, projectile=False, description="Finds the last two staffs or tomes in your inventory. Last item gains the color of the first item.", price=30)
            return Tome(name,  reverse="Tome of Consolidation",sprite_locs = fakenames_tomes_key[10], damage=10, projectile=False, description="Finds the last two staffs or tomes in your inventory. Last item gains the color of the first item.", price=30)
        elif name == "Summoning Tome":
            return Tome(name,  reverse="Banishing Tome", sprite_locs = fakenames_tomes_key[11], damage=10, projectile=False, description="Summons enemies around your position.",price=20)
            return Tome(name,  reverse="Banishing Tome", sprite_locs = fakenames_tomes_key[11], damage=10, projectile=False, description="Summons enemies around your position.",price=20)
        elif name == "Banishing Tome":
            return Tome(name,  reverse="Summoning Tome",sprite_locs = fakenames_tomes_key[12], damage=10, projectile=False, description="All enemies directly adjacent to you are teleported to a random location on the floor.",price=30)
            return Tome(name,  reverse="Summoning Tome",sprite_locs = fakenames_tomes_key[12], damage=10, projectile=False, description="All enemies directly adjacent to you are teleported to a random location on the floor.",price=30)
        elif name == "Tome of Pizzazz":
            return Tome(name,  reverse="Bankruptcy Tome", sprite_locs = fakenames_tomes_key[13], damage=10, projectile=False, description="Find the last item in your inventory. Sell price is boosted by 50%.",price=40)
            return Tome(name,  reverse="Bankruptcy Tome", sprite_locs = fakenames_tomes_key[13], damage=10, projectile=False, description="Find the last item in your inventory. Sell price is boosted by 50%.",price=40)
        elif name == "Bankruptcy Tome":
            return Tome(name,  reverse="Tome of Pizzazz",sprite_locs = fakenames_tomes_key[14], damage=10, projectile=False, description="Gold is set to 0.",price=20)
            return Tome(name,  reverse="Tome of Pizzazz",sprite_locs = fakenames_tomes_key[14], damage=10, projectile=False, description="Gold is set to 0.",price=20)
        elif name == "Tome of Identification":
            return Tome(name,  reverse="Ruined Tome", sprite_locs = fakenames_tomes_key[15], damage=10, projectile=False, description="Find the last item in your inventory. Identify the item if not already identified.",price=30)
            return Tome(name,  reverse="Ruined Tome", sprite_locs = fakenames_tomes_key[15], damage=10, projectile=False, description="Find the last item in your inventory. Identify the item if not already identified.",price=30)
        #elif name == "Tome of Obscuration":
        #    return Tome(name,  reverse="Tome of Identification",sprite_locs = fakenames_tomes_key[17], damage=10, projectile=False, description="Removes all identifications.",price=30)
        elif name == "Tome of Ascendance":
            return Tome(name,  reverse="Tome of Descendance", sprite_locs = fakenames_tomes_key[16], damage=10, projectile=False, description="Instantly go up one floor.",price=30)
            return Tome(name,  reverse="Tome of Descendance", sprite_locs = fakenames_tomes_key[16], damage=10, projectile=False, description="Instantly go up one floor.",price=30)
        elif name == "Tome of Descendance":
            return Tome(name,  reverse="Tome of Ascendance",sprite_locs = fakenames_tomes_key[17], damage=10, projectile=False, description="Instantly go down one floor.",price=30)
            return Tome(name,  reverse="Tome of Ascendance",sprite_locs = fakenames_tomes_key[17], damage=10, projectile=False, description="Instantly go down one floor.",price=30)
        elif name == "Tome of Extinction":
            return Tome(name,  reverse="Tome of Resurrection", sprite_locs = fakenames_tomes_key[18], damage=10, projectile=False, description="Causes all monsters to go extinct.",price=50)
            return Tome(name,  reverse="Tome of Resurrection", sprite_locs = fakenames_tomes_key[18], damage=10, projectile=False, description="Causes all monsters to go extinct.",price=50)
        elif name == "Tome of Resurrection":
            return Tome(name,  reverse="Tome of Extinction",sprite_locs = fakenames_tomes_key[19], damage=10, projectile=False, description= "Brings a species back from the dead.",price=50)
        
        
        
        
        

        
        elif name == "Blank Tome":
            return Tome(name,  reverse="Tome of Reversal", sprite_locs = 28, damage=10, projectile=False, description="Finds the last tome in your inventory and turns into a copy.",price=30)
        
        
        elif name == "Ruined Tome":
            return Tome(name,  reverse="Blank Tome", sprite_locs = 24, damage=10, projectile=False, description="This tome is drenched in ink. It's completely unreadable.",price=10)
        
        
        elif name == "Water Flask":
            return Flask(name,  reverse="Petroleum", evaporation_rate=0.05, product="Air", liquid="Water", sprite_locs = 17, description="A flask of water. Heals plant-type creatues.", price=10)
        elif name == "Petroleum Flask":
            return Flask(name,  reverse="Water", evaporation_rate=0.05, product="Air", liquid="Petroleum", sprite_locs = 25, description="A flask of thick petroleum that slows down anything inside. Heals robot-type creatures.", price=10)
        elif name == "Syrup Flask":
            return Flask(name,  reverse="Water", evaporation_rate=0.05, product="Air", liquid="Syrup", sprite_locs = 6, description="Sickeningly sweet syrup that slows creatures in it. Heals food-type creatures and boosts the healing effects of food eaten.", price=10)
        elif name == "Ink Flask":
            return Flask(name,  reverse="Detergent", evaporation_rate=0.5, product="Air", liquid="Ink", sprite_locs = 24, description="This dark black liquid renders tomes unusable. Heals abstract-type creatures.", price=10)
        elif name == "Detergent Flask":
            return Flask(name,  reverse="Ink", evaporation_rate=0.4, product="Water", liquid="Detergent", sprite_locs = 13, description="Floral-scented and foamy, this liquid can be used to cleanse tomes. Lethal to abstract-type creatures.", price=30)
        elif name == "Acid Flask":
            return Flask(name,  reverse="Cureall Flask", evaporation_rate=0.4, product="Water", liquid="Acid", sprite_locs = 1, description="Bubbling acid, this liquid deals damage to any who step in it.", price=15)
        elif name == "Cureall Flask":
            return Flask(name,  reverse="Acid", evaporation_rate=0.4, product="Water", liquid="Cureall", sprite_locs = 10, description="This liquid heals creatures, but has paralyzing side effect.", price=50)
        elif name == "Mercury Flask":
            return Flask(name,  reverse="Petroleum", evaporation_rate=0.05, product="Air", liquid="Mercury", sprite_locs = 27, description="Destroys all metal equipment. Lethal to robot-type creatures.", price=30)
        elif name == "Empty Flask":
            return Flask(name,  reverse="None", evaporation_rate=0.05, product="Air", liquid="Air", sprite_locs = 28, description="An empty flask. Walk over liquids while holding it to pick them up.",price=5)







        elif name == "Blue Shield":
            return Shield(name,  sprite_locs=1, defense=5, description="A sturdy shield painted with the emblem of a government.", price=12)
        elif name == "Mirror Shield":
            return Shield(name,  sprite_locs=2, defense=1, description="This shield is weak but will reflect projectiles.", price=25)
        elif name == "Wood Shield":
            return Shield(name,  sprite_locs=3, defense=3, description="A crude wooden shield usually used for training.", price=8)
        elif name == "Steel Shield":
            return Shield(name,  sprite_locs=4, defense=7, description="A thick, heavy shield made from a tough alloy.", price=25)
        elif name == "Armor Plate":
            return Shield(name,  sprite_locs=5, defense=18, description="Industrial plating once used to shield a tank from artillery fire. Holding it prevents weapons from being used.", price=50) #prevents weapons from adding to strength
        elif name == "Leaf Shield":
            return Shield(name,  sprite_locs=6, defense=1, description="A large, rubbery leaf.", price=2)
        elif name == "Spiked Shield":
            return Shield(name,  sprite_locs=0, defense=3, description="Studded with thorns, this shield will return damage back to any attackers.", price=30)
        elif name == "Sun Shield":
            return Shield(name,  sprite_locs=8, defense=4, description="Fractal networks of microcrystalline fiber adsorbs the effects of magical damage.", price=100)
        elif name == "Balance Shield":
            return Shield(name,  sprite_locs=7, defense=4, description="Shares damage between you and your attacker.", price=100)

        elif name == "Rock":
            return Miscellanious(name,  sprite_locs = 0, description = "A rock.", price=2)
        elif name == "Note":
            return Miscellanious(name,  sprite_locs = 1, description = "[REDACTED].", price=80)
        
        elif name == "3 Gold":
            return Miscellanious(name,  sprite_locs = 4, description = "A few coins.", price=3)
        elif name == "15 Gold":
            return Miscellanious(name,  sprite_locs = 5, description = "A pile of coins.", price=15)
        elif name == "60 Large Gold":
            return Miscellanious(name,  sprite_locs = 6, description = "A dragon's hoard of coins.", price=60)
        
        elif name == "Poultry":
            return Consumable(name,  sprite_locs = 0, nutrition_value=50, description="Irregularly charred bird meat. Heals 50 HP.", price=20)
        elif name == "Mushrooms":
            return Consumable(name,  sprite_locs = 1, nutrition_value=1, description="Nutritious brown mushrooms. Heals 1 HP and increases maximum HP.", price=8) #increases maximum hp
        elif name == "Leaves":
            return Consumable(name,  sprite_locs = 3, nutrition_value=0, description="Heals 5% of your maximum HP.", price=2)
        elif name == "Lettuce":
            return Consumable(name,  sprite_locs = 2, nutrition_value=0, description="Heals 15% of your maximum HP.", price=5)
        elif name == "Kale":
            return Consumable(name,  sprite_locs = 9, nutrition_value=0, description="Heals 30% of your maximum HP.", price=13)
        elif name == "Apple":
            return Consumable(name,  sprite_locs = 4, nutrition_value=15, description="Crisp and crunchy. Heals 15 HP.", price=5)
        elif name == "Cherry":
            return Consumable(name,  sprite_locs = 5, nutrition_value=10, description="These would be more useful in a pie or pastry. Heals 10 HP.", price=4)
        elif name == "Starfruit":
            return Consumable(name,  sprite_locs = 6, nutrition_value=1000, description="Only grown under perfect conditions in a rare, faraway valley. Restores HP to full and increases speed to 2x.", price=40) #gain xp to get to next level
        elif name == "Durian":
            return Consumable(name,  sprite_locs = 7, nutrition_value=50, description="Mercurial, spiky, and divisive, this fruit can restore your HP above its normal amount.", price=40) #gives temporary hp beyond max
        elif name == "Dragonfruit":
            return Consumable(name,  sprite_locs = 8, nutrition_value=12, description="Immediately increases your level by 1.", price=30) #increase a random stat by 1
        elif name == "Beet":
            return Consumable(name,  sprite_locs = 10, nutrition_value=5, description="Unappetizing but nutritious. Heals 5 HP and increases maximum HP.", price=30) #increase a random stat by 1
        elif name == "Lemon":
            return Consumable(name,  sprite_locs = 11, nutrition_value=1, description="...You want me to eat this raw...?", price=2) #increase a random stat by 1

    #self, name,  x, y, quantity
    def random_create_item(self,  item_list):
        for _ in range(random.randint(4, 9)):  # Generate 4-9 items
            random_location = random.choice(self.valid_tiles)
            y, x = random_location
            is_item_here_flag = False
            for itemchk in self.floor_items:
                if itemchk.x == x and itemchk.y == y:
                    is_item_here_flag = True 
                    break 
            if is_item_here_flag == False:
                item_name = random.choice(item_list)
                print(item_name)
                item = self.create_item(item_name, grid_items)
                item.x = x
                item.y = y
                self.floor_items.append(item)


    def generate_enemies(self, floor_level, enemy_list, level_list):
        enemy_Scale = min(floor_level // 3, len(enemy_list)-1)
        #enemies scale based on base stats
        # random_location = random.choice(self.valid_tiles)
        for _ in range(5):
            random_location = random.choice(self.valid_entity_tiles)
            if (random_location in self.valid_tiles_noshop) == True:
                y, x = random_location

                #choose a random enemy out of the enemy name & level options for this floor
                rng_enemy = random.randint(0, len(enemy_list)-1)
                enemy_name = enemy_list[rng_enemy]
                enemy_level = level_list[rng_enemy]

                self.valid_entity_tiles.remove(random_location)
                
                self.all_enemies.append(generate_enemy(enemy_name, enemy_level, x, y, enemy_grid_to_use(enemy_level), self))



    def check_valid_tile(self):
        self.valid_tiles = [
            #stored in here is y, x
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            #actual map value (index based)
            if self.map_grid[self.height-1-y][x] in ['.', '*', '~', '%', '<', '>', 'S']
        ]
        self.valid_entity_tiles = self.valid_tiles.copy()
        self.valid_tiles_noshop = [
            #stored in here is y, x
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            #actual map value (index based)
            if self.map_grid[self.height-1-y][x] in ['.', '*', '~', '%', '<', '>']
        ]
    
    def check_liquid_at_tile(self, x, y):
        return self.liquid_grid[self.height-1-y][x]





    # Connect rooms with corridors
    def center_of_room(self, room):
        x, y, width, height = room
        center_x = x + width // 2
        center_y = y + height // 2
        return center_x, center_y
    
    def connect_rooms(self):
        for i in range(1, len(self.rooms)):
            x1, y1 = self.center_of_room(self.rooms[i-1])
            x2, y2 = self.center_of_room(self.rooms[i])
            # Horizontal corridor
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if self.map_grid[y1][x] != "S":
                    self.map_grid[y1][x] = '.'
            # Vertical corridor
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if self.map_grid[y][x2] != "S":
                    self.map_grid[y][x2] = '.'


    def auto_tile_ascii(self, target_char='#', bitmask_to_ascii=None):
        if bitmask_to_ascii is None:
            bitmask_to_ascii = {
                0: 'a',    # isolated
                1: 'b',    # up
                2: 'c',    # right
                3: 'd',    # up+right
                4: 'e',    # down
                5: 'f',    # up+down
                6: 'g',   # right+down
                7: 'h',    # up+right+down
                8: 'i',    # left
                9: 'j',    # up+left
                10: 'k',   # right+left
                11: 'l',   # up+right+left
                12: 'm',  # down+left
                13: 'n',   # up+down+left
                14: 'o',   # right+down+left
                15: 'p',   # all sides
            }

        def get_bitmask(x, y):
            bitmask = 0
            if y == 0 or (self.map_grid[y-1][x] == target_char):      # Up
                bitmask |= 1
            if x == self.width-1 or (self.map_grid[y][x+1] == target_char): # Right
                bitmask |= 2
            if y == self.height-1 or (self.map_grid[y+1][x] == target_char): # Down
                bitmask |= 4
            if x == 0 or (self.map_grid[y][x-1] == target_char):      # Left
                bitmask |= 8
            return bitmask

    # Create a copy so we don't overwrite neighbor info during processing
        new_grid = [row[:] for row in self.map_grid]

        for y in range(self.height):
            for x in range(self.width):
                if self.map_grid[y][x] == target_char:
                    bitmask = get_bitmask(x, y)
                    new_grid[y][x] = bitmask_to_ascii.get(bitmask, target_char)

        self.textured_map = new_grid