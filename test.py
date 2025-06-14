from game_classes import map
import random
from game_classes.item import Item
from game_classes.item import Weapon, Consumable

item_definitions = [
    # name, class, grid_items, x, y, quantity, sprite_index, [extra args...]
    ("Kitchen Knife", Weapon, 5, 5, 1, 0, 10, 100),  # sprite_index=0
    ("Health Potion", Consumable, 7, 7, 3, 5, 20),   # sprite_index=5
    ("Machete", Weapon, 10, 10, 1, 1, 15, 80),       # sprite_index=1
]

items = []
#self, name, grid_items, x, y, quantity
for _ in range(3):  # Generate 3 items
    definition = random.choice(item_definitions)
    name, cls, x, y, quantity, sprite_index, *extra = definition
    if cls is Weapon:
        item = cls(name, x, y, quantity)
    elif cls is Consumable:
        item = cls(name, x, y, quantity)
    else:
        item = cls(name, x, y, quantity,)
    items.append(item)

def make_floor():
    number_of_rooms = random.randint(5, 9)  # Random number of rooms between 5 and 10
    test_map = map.Map(60, 60, number_of_rooms, default_tile='.')
    test_map.check_generate_room(test_map.rooms)
    test_map.connect_rooms()
    return test_map


#print(test_map)