import random
from game_classes.item import Item, Weapon, Consumable, Shield
from game_classes.enemy import*






def make_floor():
    number_of_rooms = random.randint(5, 9)  # Random number of rooms between 5 and 10
    test_map = Map(60, 60, number_of_rooms, default_tile='#')
    test_map.check_generate_room(test_map.rooms)
    test_map.connect_rooms()
    test_map.check_valid_tile()  # Populate valid tiles after room generation
    test_map.create_stairs()
    print(f"stairs{test_map.stairs}")
    testmap2 = test_map.auto_tile_ascii()
    print(testmap2)
    return test_map

class Map:
    def __init__(self, width, height, number_of_rooms, default_tile='#'):
        self.width = width
        self.height = height
        self.number_of_rooms = number_of_rooms
        self.rooms = []  # List to store the rooms
        self.map_grid = [['#' for _ in range(width)] for _ in range(height)]
        self.valid_tiles = []
        self.textured_map = [[]]
        self.valid_entity_tiles = []
        self.list_of_all_item_names = ["Iron Sword", "Chicken", "Strawberry", "Shield_1"]
        self.floor_items = []  # List to hold items on the floor
        self.all_enemies = []
        self.stairs = set() #stairs location on the map
        
    
    #set the room tiles to be '.' (empty space)
    def generate_border(self, x, y, room_width, room_height):
        for i in range(y, y + room_height):
            for j in range(x, x + room_width):
                if 0 <= i < self.height and 0 <= j < self.width:
                    self.map_grid[i][j] = '.'
    #set the room borders to be 'o' (empty space)
    def generate_room(self, x, y, room_width, room_height):
        for i in range(y-1, y + room_height+1):
            for j in range(x-1, x + room_width+1):
                if 0 <= i < self.height and 0 <= j < self.width:
                    self.map_grid[i][j] = 'o'
    
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
                self.generate_border(x, y, width, height)
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

    # def pretti_fication(map_grid, x, y, target_char):
    #     height = len(map_grid)
    #     width = len(map_grid[0])
    #     bitmask = 0
    #     if y > 0 and map_grid[y-1][x] == target_char:      # Up
    #         bitmask |= 1
    #     if x < width-1 and map_grid[y][x+1] == target_char: # Right
    #         bitmask |= 2
    #     if y < height-1 and map_grid[y+1][x] == target_char: # Down
    #         bitmask |= 4
    #     if x > 0 and map_grid[y][x-1] == target_char:      # Left
    #         bitmask |= 8
    #     return bitmask

    
    floor_items = []  # List to hold items on the floor

    def create_item(self, name, grid_items):
        # Example dummy factory
        if name == "Iron Sword":
            return Weapon(name, grid_items, sprite_locs = 0, damage=10, durability=100)
        elif name == "Chicken":
            return Consumable(name, grid_items, sprite_locs = 0, nutrition_value=20)
        elif name == "Strawberry":
            return Consumable(name, grid_items, sprite_locs = 4, nutrition_value=10)
        elif name == "Shield_1":
            return Shield(name, grid_items, sprite_locs=0, defense=5)
        
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
        # for _ in range(5):
        #     random_location = random.choice(self.valid_entity_tiles)
        #     y, x = random_location
        #     self.valid_entity_tiles.remove(random_location)
        #     self.all_enemies.append(generate_enemy("GOOSE", 1, x, y, grid_entities1))
        for _ in range(5):
            random_location = random.choice(self.valid_tiles)
            y, x = random_location
            self.valid_entity_tiles.remove(random_location)
            self.all_enemies.append(generate_enemy("FOX", 1, x, y, grid_entities1))

    def check_valid_tile(self):
        self.valid_tiles = [
            #stored in here is y, x
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            #actual map value (index based)
            if self.map_grid[self.height-1-y][x] == '.'
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




    def auto_tile_ascii(self, target_char='o', bitmask_to_ascii=None):
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
    
                


