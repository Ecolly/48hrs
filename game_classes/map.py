import random
from game_classes.item import Item, Weapon, Consumable, Shield
from game_classes.enemy import*






def make_floor():
    number_of_rooms = random.randint(5, 9)  # Random number of rooms between 5 and 10
    test_map = Map(60, 60, number_of_rooms, default_tile='#')
    test_map.check_generate_room(test_map.rooms)
    test_map.connect_rooms()
    test_map.check_valid_tile()  # Populate valid tiles after room generation
    return test_map

class Map:
    def __init__(self, width, height, number_of_rooms, default_tile='#'):
        self.width = width
        self.height = height
        self.number_of_rooms = number_of_rooms
        self.rooms = []  # List to store the rooms
        self.map_grid = [['#' for _ in range(width)] for _ in range(height)]
        self.valid_tiles = set()
        self.list_of_all_item_names = ["Iron Sword", "Chicken", "Strawberry", "Shield_1"]
        self.floor_items = []  # List to hold items on the floor
        self.all_enemies = []
    
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
        self.all_enemies.append(generate_enemy("GOOSE", 1, 29, 29, grid_entities1))
        self.all_enemies.append(generate_enemy("GOOSE", 1, 30, 25, grid_entities1))
        self.all_enemies.append(generate_enemy("GOOSE", 1, 25, 30, grid_entities1))

        self.all_enemies.append(generate_enemy("FOX", 1, 25, 34, grid_entities1))
        self.all_enemies.append(generate_enemy("FOX", 1, 30, 32, grid_entities1))
        
    def check_valid_tile(self):
        self.valid_tiles = [
            (y, x)
            for y in range(self.height)
            for x in range(self.width)
            if self.map_grid[self.height-1-y][x] == '.'
        ]
        print("Valid tiles found:", self.valid_tiles)
        return self.valid_tiles
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
    
                


