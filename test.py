from game_classes import map
import random

def make_floor():
    number_of_rooms = random.randint(5, 9)  # Random number of rooms between 5 and 10
    test_map = map.Map(60, 60, number_of_rooms, default_tile='.')
    test_map.check_generate_room(test_map.rooms)
    test_map.connect_rooms()
    return test_map


#print(test_map)