import random
from game_classes.item import Item, Weapon, Consumable, Shield, Staff, Miscellanious
from game_classes.enemy import*



def make_floor():
    number_of_rooms = random.randint(5, 9)  # Random number of rooms between 5 and 10
    test_map = Map(60, 60, number_of_rooms, default_tile='#')
    test_map.check_generate_room(test_map.rooms)
    test_map.connect_rooms()
    test_map.check_valid_tile()
    test_map.create_stairs() # Populate valid tiles after room generation
    test_map.assign_spawnpoint()

    if random.randint(0,1)==0:
        test_map.auto_tile_ascii()
        test_map.map_type = "Complex"
        return test_map
    print(test_map)
    return test_map

class Map:
    def __init__(self, width, height, number_of_rooms, default_tile='#'):
        self.map_type = "Simple"
        self.width = width
        self.height = height
        self.number_of_rooms = number_of_rooms
        self.rooms = []  # List to store the rooms
        self.map_grid = [['#' for _ in range(width)] for _ in range(height)]
        self.valid_tiles = []
        self.textured_map = [[]]
        self.valid_entity_tiles = []
        self.list_of_all_item_names = ["Knife", "Machete", "Scimitar", "Sickle", "Rapier", "Stick", "Fury Cutter", "Windsword", "Red Staff", "Orange Staff", "Gold Staff", "Green Staff", "Teal Staff", "Blue Staff", "Light Blue Staff", "Magenta Staff", "Black Staff", "Blue Shield", "Wood Shield", "Steel Shield", "Armor Plate", "Rock", "Note", "Poultry", "Mushrooms", "Leaves", "Apple", "Cherry", "Starfruit", "Durian", "Dragonfruit"]
        self.floor_items = []  # List to hold items on the floor
        self.all_enemies = []
        self.spawnpoint = set()
        self.stairs = set() #stairs location on the map
        
    
    #set the room tiles to be '.' (empty space)
    def generate_room(self, x, y, room_width, room_height):
        textures = ['.', '*', '~']
        for i in range(y, y + room_height):
            for j in range(x, x + room_width):
                if 0 <= i < self.height and 0 <= j < self.width:
                    tile = random.choices(textures, weights=[10, 1, 1])[0]
                    self.map_grid[i][j] = tile
                    
    # #set the room borders to be 'o' (empty space)
    # def generate_room(self, x, y, room_width, room_height):
    #     for i in range(y-1, y + room_height+1):
    #         for j in range(x-1, x + room_width+1):
    #             if 0 <= i < self.height and 0 <= j < self.width:
    #                 self.map_grid[i][j] = 'o'
    
    #check if a room can be generated at the given coordinates
    #checks it against existing rooms list
    def check_generate_room(self, rooms):
        max_possible_size = min(self.width, self.height) // 2
        min_possible_size = 15

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
            return Weapon(name, grid_items, sprite_locs = 0, damage=5, durability=100)
        elif name == "Machete":
            return Weapon(name, grid_items, sprite_locs = 1, damage=6, durability=100)
        elif name == "Scimitar":
            return Weapon(name, grid_items, sprite_locs = 2, damage=7, durability=100)
        elif name == "Sickle":
            return Weapon(name, grid_items, sprite_locs = 4, damage=4, durability=100)
        elif name == "Rapier":
            return Weapon(name, grid_items, sprite_locs = 5, damage=9, durability=100)
        elif name == "Stick":
            return Weapon(name, grid_items, sprite_locs = 6, damage=1, durability=100)
        elif name == "Fury Cutter":
            return Weapon(name, grid_items, sprite_locs = 9, damage=30, durability=100) #deducts 1/4 of attack damage from your hp
        elif name == "Windsword":
            return Weapon(name, grid_items, sprite_locs = 10, damage=16, durability=100)
        elif name == "Red Staff":
            return Staff(name, grid_items, sprite_locs = 1, damage=10, projectile=True) #divides enemy's hp by 2
        elif name == "Orange Staff":
            return Staff(name, grid_items, sprite_locs = 2, damage=10, projectile=False) #deducts 15 from all enemy hp on floor
        elif name == "Gold Staff":
            return Staff(name, grid_items, sprite_locs = 7, damage=10, projectile=False)
        elif name == "Green Staff":
            return Staff(name, grid_items, sprite_locs = 10, damage=10, projectile=False)
        elif name == "Teal Staff":
            return Staff(name, grid_items, sprite_locs = 13, damage=10, projectile=False)
        elif name == "Blue Staff":
            return Staff(name, grid_items, sprite_locs = 16, damage=10, projectile=False)
        elif name == "Light Blue Staff":
            return Staff(name, grid_items, sprite_locs = 17, damage=10, projectile=False)
        elif name == "Magenta Staff":
            return Staff(name, grid_items, sprite_locs = 22, damage=10, projectile=False) #wins game
        elif name == "Black Staff":
            return Staff(name, grid_items, sprite_locs = 25, damage=10, projectile=False)
        elif name == "Blue Shield":
            return Shield(name, grid_items, sprite_locs=0, defense=8)
        elif name == "Wood Shield":
            return Shield(name, grid_items, sprite_locs=2, defense=5)
        elif name == "Steel Shield":
            return Shield(name, grid_items, sprite_locs=4, defense=12)
        elif name == "Armor Plate":
            return Shield(name, grid_items, sprite_locs=5, defense=24) #prevents weapons from adding to strength
        elif name == "Rock":
            return Miscellanious(name, grid_items, sprite_locs = 0, description = "")
        elif name == "Note":
            return Miscellanious(name, grid_items, sprite_locs = 1, description = "")
        elif name == "Poultry":
            return Consumable(name, grid_items, sprite_locs = 0, nutrition_value=100)
        elif name == "Mushrooms":
            return Consumable(name, grid_items, sprite_locs = 1, nutrition_value=5) #increases maximum hp
        elif name == "Leaves":
            return Consumable(name, grid_items, sprite_locs = 3, nutrition_value=1)
        elif name == "Apple":
            return Consumable(name, grid_items, sprite_locs = 4, nutrition_value=50)
        elif name == "Cherry":
            return Consumable(name, grid_items, sprite_locs = 5, nutrition_value=25)
        elif name == "Starfruit":
            return Consumable(name, grid_items, sprite_locs = 6, nutrition_value=1000) #gain xp to get to next level
        elif name == "Durian":
            return Consumable(name, grid_items, sprite_locs = 7, nutrition_value=50) #gives temporary hp beyond max
        elif name == "Dragonfruit":
            return Consumable(name, grid_items, sprite_locs = 8, nutrition_value=12) #increase a random stat by 1

    #self, name, grid_items, x, y, quantity
    def random_create_item(self, grid_items):
        for _ in range(10):  # Generate 3 items
            random_location = random.choice(self.valid_tiles)
            y, x = random_location
            item_name = random.choice(self.list_of_all_item_names)
            print(item_name)
            item = self.create_item(item_name, grid_items)
            item.x = x
            item.y = y
            self.floor_items.append(item)
            print(f"Created item: {item.name} at ({x}, {y})")

    def generate_enemies(self, grid_entities1):
        # random_location = random.choice(self.valid_tiles)
        # y, x = random_location
        #self.all_enemies.append(generate_enemy("GOOSE", 1, 26, 26, grid_entities1))

        #TODO Randomly generate enemies around the map temp
        for _ in range(5):
            random_location = random.choice(self.valid_entity_tiles)
            y, x = random_location
            self.valid_entity_tiles.remove(random_location)
            self.all_enemies.append(generate_enemy("GOOSE", 1, x, y, grid_entities1))
        for _ in range(10):
            random_location = random.choice(self.valid_entity_tiles)
            y, x = random_location
            self.valid_entity_tiles.remove(random_location)
            self.all_enemies.append(generate_enemy("FOX", 1, x, y, grid_entities1))
        for _ in range(10):
            random_location = random.choice(self.valid_entity_tiles)
            y, x = random_location
            self.valid_entity_tiles.remove(random_location)
            self.all_enemies.append(generate_enemy("S'MORE",1, x, y, grid_entities1))
        

    def check_valid_tile(self):
        self.valid_tiles = [
            #stored in here is y, x
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            #actual map value (index based)
            if self.map_grid[self.height-1-y][x] in ['.', '*', '~']
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
            if y > 0 and self.map_grid[y-1][x] == target_char:      # Up
                bitmask |= 1
            if x < self.width-1 and self.map_grid[y][x+1] == target_char: # Right
                bitmask |= 2
            if y < self.height-1 and self.map_grid[y+1][x] == target_char: # Down
                bitmask |= 4
            if x > 0 and self.map_grid[y][x-1] == target_char:      # Left
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
    
                


