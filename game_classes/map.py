import random
from game_classes.item import Item, Weapon, Consumable, Shield, Staff, Miscellanious
from game_classes.enemy import*







def make_floor(type):
    number_of_rooms = random.randint(5, 9)  # Random number of rooms between 5 and 10
    test_map = Map(60, 60, number_of_rooms, default_tile='#')
    test_map.check_generate_room(test_map.rooms)
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
        self.map_grid = [['#' for _ in range(width)] for _ in range(height)]
        self.valid_tiles = []
        self.textured_map = [[]]
        self.valid_entity_tiles = []
        #self.list_of_all_enemy_names = ["LEAFALOTTA", "HAMSTER", "GOOSE", "CHLOROSPORE", "FOX", "S'MORE"]
        
        
        #self.list_of_all_enemies = [["LEAFALOTTA", "HAMSTER", "GOOSE"], ["LEAFALOTTA", "CHLOROSPORE", "FOX"], ["S'MORE", "CHLOROSPORE", "SCORPION"], ["SCORPION", "S'MORE", "CHROME DOME"], ["DRAGON", "S'MORE", "TETRAHEDRON"]]
        #self.list_of_all_levels = [[1, 1, 1], [1, 2, 2], [1, 2, 1], [2, 2, 2], [2, 3, 2]]
        #self.list_of_all_item_names = ["Knife", "Machete", "Scimitar", "Sickle", "Rapier", "Stick", "Fury Cutter", "Windsword", "Red Staff", "Orange Staff", "Gold Staff", "Green Staff", "Teal Staff", "Blue Staff", "Light Blue Staff", "Magenta Staff", "Black Staff", "Blue Shield", "Wood Shield", "Steel Shield", "Armor Plate", "Rock", "Note", "Poultry", "Mushrooms", "Leaves", "Apple", "Cherry", "Starfruit", "Durian", "Dragonfruit"]
        
        
        self.floor_items = []  # List to hold items on the floor
        self.all_enemies = []
        self.spawnpoint = set()
        self.stairs = set() #stairs location on the map
        
        
    
    #set the room tiles to be '.' (empty space)
    def assign_textures_to_all_floor_tiles(self):
        textures = ['.', '*', '~', '%', '<', '>']
        weights = [10, 1, 1, 1, 1, 1]
        for i in range(self.height):
            for j in range(self.width):
                if self.map_grid[i][j] == '.':
                    tile = random.choices(textures, weights=weights)[0]
                    self.map_grid[i][j] = tile

    # def assign_room_textures(self, x, y, room_width, room_height):
    #     textures = ['.', '*', '~', '%', '<', '>']
    #     weights = [10, 1, 1, 1, 1, 1]
    #     for i in range(y, y + room_height):
    #         for j in range(x, x + room_width):
    #             if 0 <= i < self.height and 0 <= j < self.width:
    #                 tile = random.choices(textures, weights=weights)[0]
    #                 self.map_grid[i][j] = tile

    #set the room borders to be 'o' (empty space)
    def generate_room(self, x, y, room_width, room_height):
        for i in range(y, y + room_height):
            for j in range(x, x + room_width):
                if 0 <= i < self.height and 0 <= j < self.width:
                    self.map_grid[i][j] = '.'  # Set the room area to empty space
    
    #check if a room can be generated at the given coordinates
    #checks it against existing rooms list
    def check_generate_room(self, rooms):
        max_possible_size = 12#18#min(self.width, self.height) // 2
        min_possible_size = 6#12

        max_size = max(min_possible_size, int(max_possible_size * (1 - (self.number_of_rooms / 20))))
        min_size = max(min_possible_size, int(max_size * 0.6))

        rooms_created = 0
        attempts = 0
        max_attempts = self.number_of_rooms * 10  # Limit attempts to avoid infinite loop


        while rooms_created < self.number_of_rooms and attempts < max_attempts:
            width = random.randint(min_size, max_size)
            height = random.randint(min_size, max_size)
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
                self.generate_room(x, y, width, height)
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
        random_location = random.choice(self.valid_entity_tiles)
        y, x = random_location
        self.valid_entity_tiles.remove(random_location)
        self.map_grid[self.height -1 -y][x] = '@'
        self.stairs = (x,y)

    def assign_spawnpoint(self):
        random_location = random.choice(self.valid_entity_tiles)
        y, x = random_location
        self.spawnpoint = (x,y)
        
    floor_items = []  # List to hold items on the floor

    def create_item(self, name, grid_items):
        # Example dummy factory

        if name == "Knife":
            return Weapon(name, grid_items, sprite_locs = 0, damage=4, durability=100, description="A common household chef's knife.")
        elif name == "Machete":
            return Weapon(name, grid_items, sprite_locs = 1, damage=5, durability=100, description="A long-bladed knife useful for cutting plants.")
        elif name == "Scimitar":
            return Weapon(name, grid_items, sprite_locs = 2, damage=7, durability=100, description="A sharp, curved blade.")
        elif name == "Sickle":
            return Weapon(name, grid_items, sprite_locs = 4, damage=3, durability=100, description="A crescent-shaped blade that can reach three enemies at once.")
        elif name == "Rapier":
            return Weapon(name, grid_items, sprite_locs = 5, damage=6, durability=100, description="A thin, slender weapon that can reach two tiles in front.")
        elif name == "Stick":
            return Weapon(name, grid_items, sprite_locs = 6, damage=2, durability=100, description="A thick tree branch that can be used as a crude weapon.")
        elif name == "Fury Cutter":
            return Weapon(name, grid_items, sprite_locs = 9, damage=20, durability=100, description="Ominous energy seeps off the cutting edge. The weapon returns 1/4 of damage dealt to the bearer.") #deducts 1/4 of attack damage from your hp
        elif name == "Windsword":
            return Weapon(name, grid_items, sprite_locs = 10, damage=9, durability=100, description="Imbued with magical runes, this longsword is more powerful than the average weapon.")
        elif name == "Red Staff":
            return Staff(name, grid_items, sprite_locs = 1, damage=10, projectile=True, description="Divides the target's HP by 2.") #divides enemy's hp by 2
        elif name == "Orange Staff":
            return Staff(name, grid_items, sprite_locs = 2, damage=10, projectile=False, description="Deducts 15 from HP of all enemies on the floor.") #deducts 15 from all enemy hp on floor
        elif name == "Gold Staff":
            return Staff(name, grid_items, sprite_locs = 7, damage=10, projectile=True, description="Damage depends on mana used.") #deals set damage according to # of charges used
        elif name == "Green Staff":
            return Staff(name, grid_items, sprite_locs = 10, damage=10, projectile=True, description="Projectile bounces off walls.") #bounces
        elif name == "Teal Staff":
            return Staff(name, grid_items, sprite_locs = 13, damage=10, projectile=True, description="Target's speed is reduced to 1/2. Duration depends on mana used.") #slows down enemy
        elif name == "Blue Staff":
            return Staff(name, grid_items, sprite_locs = 16, damage=10, projectile=True, description="Paralyzes target. Duration depends on mana used.") #paralyzes enemy
        elif name == "Light Blue Staff":
            return Staff(name, grid_items, sprite_locs = 17, damage=10, projectile=False, description="Levels up all creatures on the floor.") #levels up all enemies on a floor, including you
        elif name == "Magenta Staff":
            return Staff(name, grid_items, sprite_locs = 22, damage=10, projectile=True, description="Target pierces a number of enemies equal to mana used.") #pierces enemies
        elif name == "Black Staff":
            return Staff(name, grid_items, sprite_locs = 25, damage=10, projectile=False, description="That's strange. This one doesn't seem to do anything.") 
        elif name == "Blue Shield":
            return Shield(name, grid_items, sprite_locs=1, defense=4, description="A sturdy, shield painted with the emblem of a government.")
        elif name == "Mirror Shield":
            return Shield(name, grid_items, sprite_locs=2, defense=1, description="This shield is weak but will reflect projectiles.")
        elif name == "Wood Shield":
            return Shield(name, grid_items, sprite_locs=3, defense=2, description="A crude wooden shield usually used for training.")
        elif name == "Steel Shield":
            return Shield(name, grid_items, sprite_locs=4, defense=6, description="A thick, heavy shield made from a tough alloy.")
        elif name == "Armor Plate":
            return Shield(name, grid_items, sprite_locs=5, defense=18, description="Industrial plating once used to shield a tank from artillery fire. Holding it prevents weapons from being used.") #prevents weapons from adding to strength
        elif name == "Rock":
            return Miscellanious(name, grid_items, sprite_locs = 0, description = "A rock.")
        elif name == "Note":
            return Miscellanious(name, grid_items, sprite_locs = 1, description = "You already know what's on this.")
        elif name == "Poultry":
            return Consumable(name, grid_items, sprite_locs = 0, nutrition_value=100, description="Irregularly charred bird meat. Heals 100 HP.")
        elif name == "Mushrooms":
            return Consumable(name, grid_items, sprite_locs = 1, nutrition_value=5, description="Nutritious brown mushrooms. Heals 5 HP.") #increases maximum hp
        elif name == "Leaves":
            return Consumable(name, grid_items, sprite_locs = 3, nutrition_value=1, description="These probably won't do much if eaten.")
        elif name == "Apple":
            return Consumable(name, grid_items, sprite_locs = 4, nutrition_value=40, description="Crisp and crunchy. Heals 40 HP.")
        elif name == "Cherry":
            return Consumable(name, grid_items, sprite_locs = 5, nutrition_value=20, description="These would be more useful in a pie or pastry. Heals 20 HP.")
        elif name == "Starfruit":
            return Consumable(name, grid_items, sprite_locs = 6, nutrition_value=1000, description="Only grown under perfect conditions in a rare, faraway valley. Restores HP to full and increases speed to 2x.") #gain xp to get to next level
        elif name == "Durian":
            return Consumable(name, grid_items, sprite_locs = 7, nutrition_value=50, description="Mercurial, spiky, and divisive, this fruit can restore your HP above its normal amount.") #gives temporary hp beyond max
        elif name == "Dragonfruit":
            return Consumable(name, grid_items, sprite_locs = 8, nutrition_value=12, description="Messes with your stats.") #increase a random stat by 1

    #self, name, grid_items, x, y, quantity
    def random_create_item(self, grid_items, item_list):
        for _ in range(10):  # Generate 3 items
            random_location = random.choice(self.valid_tiles)
            y, x = random_location
            item_name = random.choice(item_list)
            print(item_name)
            item = self.create_item(item_name, grid_items)
            item.x = x
            item.y = y
            self.floor_items.append(item)
            print(f"Created item: {item.name} at ({x}, {y})")

    def generate_enemies(self, floor_level, enemy_list, level_list):
        enemy_Scale = min(floor_level // 3, len(enemy_list)-1)
        #enemies scale based on base stats
        # random_location = random.choice(self.valid_tiles)
        for _ in range(5):
            random_location = random.choice(self.valid_entity_tiles)
            y, x = random_location

            #choose a random enemy out of the enemy name & level options for this floor
            rng_enemy = random.randint(0, len(enemy_list)-1)
            enemy_name = enemy_list[rng_enemy]
            enemy_level = level_list[rng_enemy]

            self.valid_entity_tiles.remove(random_location)
            
            test_enemy = generate_enemy(enemy_name, enemy_level, x, y, enemy_grid_to_use(enemy_level))
            self.all_enemies.append(generate_enemy(enemy_name, enemy_level, x, y, enemy_grid_to_use(enemy_level)))
            print(f"the experience{test_enemy.experience}")


    def check_valid_tile(self):
        self.valid_tiles = [
            #stored in here is y, x
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            #actual map value (index based)
            if self.map_grid[self.height-1-y][x] in ['.', '*', '~', '%', '<', '>']
        ]
        self.valid_entity_tiles = self.valid_tiles.copy()
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
                self.map_grid[y1][x] = '.'
            # Vertical corridor
            for y in range(min(y1, y2), max(y1, y2) + 1):
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
    
                


