
import json
import time

from game_classes import player as player_module
from game_classes.map import Map
from game_classes.item import Item, Weapon, Staff, Tome, Flask, Consumable, Shield, Miscellanious
from game_classes.enemy import Enemy
from font import*
from game_classes.face_direction import FaceDirection

def save_game_data(game_data):
    directory = "game_saves/"
    filename = time.strftime("save_%Y%m%d_%H%M%S.json")
    print(f"Saving game data to {directory + filename}")
    with open(directory + filename, 'w') as f:
        json.dump(game_data, f, indent=4)

def load_game(filename):
    directory = "game_saves"
    filename = f"{directory}/{filename}"
    print(f"Loading game data from {filename}")
    with open(filename, 'r') as f:
        game_data = json.load(f)
    print(game_data["player"])
    
    player_data = game_data["player"]
    if player_data:
        player = player_from_dict(player_data)
        map = map_from_dict(game_data["map"])
        floor_enemies = [enemy_from_dict(e) for e in game_data["floor_enemies"]]
    
    
    return player, map, floor_enemies

    

def player_to_dict(player):
    return {
        'class': player.__class__.__name__,
        'name': player.name,
        'health': player.health,
        'level': player.level,
        'experience': player.experience,
        "inventory": [item_to_dict(item) if item else None for item in player.inventory],

        'x': player.x,
        'y': player.y,
        'initx' : player.initx,
        'inity': player.inity,
        'prevx': player.prevx,
        'prevy': player.prevy,
        'spriteindex': player.spriteindex, #needs to be implemented, get the index of the sprite
        
        'animtype': player.animtype,

        'health_visual':player.health_visual,
        'health_visual': player.health_visual,
        'maxhealth_visual': player.maxhealth_visual,
        'experience_visual': player.experience_visual,
        'level_visual': player.level_visual,

        #separate attributes that needs to be added after the player is created
        "maxhealth": player.maxhealth,
        "strength": player.strength,
        "maxstrength": player.maxstrength,
        "strength_visual": player.strength_visual,
        "maxstrength_visual": player.maxstrength_visual,
        "defense": player.defense,
        "maxdefense": player.maxdefense,
        "defense_visual": player.defense_visual,
        "maxdefense_visual": player.maxdefense_visual,
        "gold": player.gold,
        "speed_turns": player.speed_turns,
        "speed_visual": player.speed_visual,
        "paralysis_turns": player.paralysis_turns,
        "paralysis_visual": player.paralysis_visual,
        "is_shopping": player.is_shopping,
        "current_holding": player.current_holding,

        "default_speed": player.default_speed,
        "speed": player.speed,
        "turns_left_before_moving": player.turns_left_before_moving,
        "speed_turns": player.speed_turns,
        "speed_visual": player.speed_visual,
        "paralysis_turns": player.paralysis_turns,
        "paralysis_visual": player.paralysis_visual,
        "flee_ai_turns": player.flee_ai_turns,
        "rage_ai_turns": player.rage_ai_turns,
        "is_shopping": player.is_shopping,
    }




        #self.active_spells = []
        # self.technique = Technique.NA
        # self.techniquex = 0
        # self.techniquey = 0
        # self.techniqueitem = None #used if technique uses an item and the object is needed (e.g. throwing)
        # self.techniqueframe = 0
        # self.techniquefinished = 0
        # self.techniquecharges = 0

        # self.sprite_weapon = image_handling.create_sprite(itemgrid, 0)
        # self.sprite_shield = image_handling.create_sprite(itemgrid, 0)
        # self.sprite_weapon.color = (0, 0, 0, 0)
        # self.sprite_shield.color = (0, 0, 0, 0)
        # self.itemgrid = itemgrid

        # self.sprite_weapon.batch = batch 
        # self.sprite_shield.batch = batch
        # self.sprite.batch = batch
        # self.sprite.group = group_enemies

        # self.scale = 3
def player_from_dict(data):

    player = player_module.Player(
    name=data['name'],
    health=data['health'],
    level=data['level'],
    experience=data['experience'],
    x=data['x'],
    y=data['y'],
    spriteindex=data['spriteindex'],
    animtype=data['animtype'],
        # Add any other required constructor args here
    )

    player.inventory = [item_from_dict(item_dict) if item_dict else None for item_dict in data["inventory"]]
    player.initx = data.get("initx", 0)
    player.inity = data.get("inity", 0)
    player.prevx = data.get("prevx", 0)
    player.prevy = data.get("prevy", 0)

    # Set additional attributes
    player.maxhealth = data.get("maxhealth", 20)  # Default to 20 if not provided
    player.health_visual = data.get("health_visual", 0)
    player.maxhealth_visual = data.get("maxhealth_visual", 0)
    player.experience_visual = data.get("experience_visual", 0)
    player.level_visual = data.get("level_visual", 0)

    player.strength = data.get("strength", 0)
    player.maxstrength = data.get("maxstrength", 0)
    player.strength_visual = data.get("strength_visual", 0)
    player.maxstrength_visual = data.get("maxstrength_visual", 0)
    player.defense = data.get("defense", 0)
    player.maxdefense = data.get("maxdefense", 0)
    player.defense_visual = data.get("defense_visual", 0)
    player.maxdefense_visual = data.get("maxdefense_visual", 0)
    player.gold = data.get("gold", 0)
    player.speed_turns = data.get("speed_turns", 0)
    player.speed_visual = data.get("speed_visual", 0)
    player.paralysis_turns = data.get("paralysis_turns", 0)
    player.paralysis_visual = data.get("paralysis_visual", 0)
    player.is_shopping = data.get("is_shopping", False)
    player.current_holding = data.get("current_holding", None)
    player.default_speed = data.get("default_speed", 0)
    player.speed = data.get("speed", 0)
    player.turns_left_before_moving = data.get("turns_left_before_moving", 0)
    player.flee_ai_turns = data.get("flee_ai_turns", 0)
    player.rage_ai_turns = data.get("rage_ai_turns", 0)
    # Add any other attributes as needed

    return player


def enemy_to_dict(enemy):
    return{
        "class": enemy.__class__.__name__,
        "name": enemy.name,
        "health": enemy.health,
        "maxhealth": enemy.maxhealth,
        "level": enemy.level,

        "strength": enemy.strength,
        "maxstrength": enemy.maxstrength,
        "strength_visual": enemy.strength_visual,
        "maxstrength_visual": enemy.maxstrength_visual,
        "defense": enemy.defense,
        "maxdefense": enemy.maxdefense,
        "defense_visual": enemy.defense_visual,
        "maxdefense_visual": enemy.maxdefense_visual,
        "basehealth": enemy.basehealth,
        "basestrength": enemy.basestrength,
        "basedefense": enemy.basedefense,
        "creaturetype": enemy.creaturetype,
        "x": enemy.x,
        "y": enemy.y,


    
        "inventory": [item_to_dict(item) for item in enemy.inventory],
        "active_projectiles": [],  # You can expand this if you want to save projectiles
        "technique": enemy.technique.name if hasattr(enemy.technique, "name") else enemy.technique,
        "techniquex": enemy.techniquex,
        "techniquey": enemy.techniquey,
        "techniqueframe": enemy.techniqueframe,
        "techniquefinished": enemy.techniquefinished,
        "techniquecharges": enemy.techniquecharges,
        "techniqueitem": item_to_dict(enemy.techniqueitem) if enemy.techniqueitem else None,
        "equipment_weapon": item_to_dict(enemy.equipment_weapon) if enemy.equipment_weapon else None,
        "equipment_shield": item_to_dict(enemy.equipment_shield) if enemy.equipment_shield else None,
        "should_be_deleted": enemy.should_be_deleted,
        "current_holding": item_to_dict(enemy.current_holding) if enemy.current_holding else None,
        
    
        "has_been_hit": enemy.has_been_hit,
        "spriteindex": enemy.spriteindex,
        "color": enemy.color,
        "animtype": enemy.animtype,
        "animframe": enemy.animframe,
        "animmod": enemy.animmod,
        "scale": enemy.scale,
        "loot": item_to_dict(enemy.loot) if enemy.loot else None,
        "experience": enemy.experience,
        "speed": enemy.speed,
        "default_speed": enemy.default_speed,
        "turns_left_before_moving": enemy.turns_left_before_moving,
        "speed_turns": enemy.speed_turns,
        "speed_visual": enemy.speed_visual,
        "paralysis_turns": enemy.paralysis_turns,
        "paralysis_visual": enemy.paralysis_visual,
        "flee_ai_turns": enemy.flee_ai_turns,
        "rage_ai_turns": enemy.rage_ai_turns,
        "invisible_frames": enemy.invisible_frames,
    }
def enemy_from_dict(data):

    # self, name, health, strength, defense, level, spriteindex, color, animtype, animframe, animmod, x, y, experience, speed, type
    enemy = Enemy(
        name=data["name"],
        health=data["health"],
        strength = data.get("strength", 0),
        defense = data.get("defense", 0),
        level=data.get("level", 1),
        
        spriteindex=data.get("spriteindex", 0),
        color = tuple(data.get("color", (255, 255, 255, 255))),
        animtype=data.get("animtype", 0),
        animframe= data.get("animframe", 0),
        animmod=data.get("animmod", 0),

        x=data.get("x", 0),
        y=data.get("y", 0),
        experience=data.get("experience", 0),
        speed=data.get("speed", 0),
        type = data.get("type", "default"),
        
    )



    # Inventory
    enemy.inventory = [
        item_from_dict(item_dict, grid_items) if item_dict else None
        for item_dict in data.get("inventory", [])
    ]

    # Equipment and items
    enemy.techniqueitem = item_from_dict(data["techniqueitem"]) if data.get("techniqueitem") else None
    enemy.equipment_weapon = item_from_dict(data["equipment_weapon"]) if data.get("equipment_weapon") else None
    enemy.equipment_shield = item_from_dict(data["equipment_shield"]) if data.get("equipment_shield") else None
    enemy.current_holding = item_from_dict(data["current_holding"]) if data.get("current_holding") else None
    enemy.loot = item_from_dict(data["loot"]) if data.get("loot") else None

    # Set other attributes
    enemy.maxhealth=data.get("maxhealth", data["health"]),
    enemy.maxhealth_visual = data.get("maxhealth_visual", 0)
    
    enemy.maxstrength = data.get("maxstrength", 0)
    enemy.strength_visual = data.get("strength_visual", 0)
    enemy.maxstrength_visual = data.get("maxstrength_visual", 0)
    enemy.maxdefense = data.get("maxdefense", 0)
    enemy.defense_visual = data.get("defense_visual", 0)
    enemy.maxdefense_visual = data.get("maxdefense_visual", 0)
    enemy.basehealth = data.get("basehealth", 0)
    enemy.basestrength = data.get("basestrength", 0)
    enemy.basedefense = data.get("basedefense", 0)
    enemy.creaturetype = data.get("creaturetype", "")
    enemy.technique = data.get("technique", 0)
    enemy.techniquex = data.get("techniquex", 0)
    enemy.techniquey = data.get("techniquey", 0)
    enemy.techniqueframe = data.get("techniqueframe", 0)
    enemy.techniquefinished = data.get("techniquefinished", 0)
    enemy.techniquecharges = data.get("techniquecharges", 0)
    enemy.should_be_deleted = data.get("should_be_deleted", False)
    enemy.has_been_hit = data.get("has_been_hit", False)
    enemy.spriteindex = data.get("spriteindex", 0)
   
    enemy.scale = data.get("scale", 1)
    enemy.default_speed = data.get("default_speed", 0)
    enemy.turns_left_before_moving = data.get("turns_left_before_moving", 0)
    enemy.speed_turns = data.get("speed_turns", 0)
    enemy.speed_visual = data.get("speed_visual", 0)
    enemy.paralysis_turns = data.get("paralysis_turns", 0)
    enemy.paralysis_visual = data.get("paralysis_visual", 0)
    enemy.flee_ai_turns = data.get("flee_ai_turns", 0)
    enemy.rage_ai_turns = data.get("rage_ai_turns", 0)
    enemy.invisible_frames = data.get("invisible_frames", 0)

    return enemy



def game_to_dict(game):
    pass
def map_to_dict(map_obj):
    return {
        "class": map_obj.__class__.__name__,
        "map_type": map_obj.map_type,
        "wall_type": map_obj.wall_type,
        "width": map_obj.width,
        "height": map_obj.height,
        "number_of_rooms": map_obj.number_of_rooms,
        "rooms": map_obj.rooms,  # Make sure each room is serializable!
        
        
        "map_grid": map_obj.map_grid,
        "liquid_grid": map_obj.liquid_grid,
        "tileset": list(map_obj.tileset),
        # "item_list": map_obj.item_list,      # If these are lists of strings/ints, it's fine
        # "enemy_list": map_obj.enemy_list,

        "valid_tiles": [list(t) for t in map_obj.valid_tiles],
        "textured_map": map_obj.textured_map,
        "valid_entity_tiles": [list(t) for t in map_obj.valid_entity_tiles],
        "valid_tiles_noshop": [list(t) for t in map_obj.valid_tiles_noshop],
        "name": map_obj.name,
        
        "level_list": map_obj.level_list,
        "floor_items": [item_to_dict(item) for item in map_obj.floor_items],  # Save items on the floor
        "all_enemies": [enemy_to_dict(enemy) for enemy in map_obj.all_enemies],  # Save enemies
        "spawnpoint": list(map_obj.spawnpoint),  # Convert set to list for JSON
        "stairs": list(map_obj.stairs),    
    }
def map_from_dict(data):
    #__init__(self, width, height, number_of_rooms, default_tile='#'):
    map_obj = Map(
        width=data['width'],
        height=data['height'],
        number_of_rooms=data['number_of_rooms'],
        
    )

    map_obj.map_type = data.get('map_type', 'default')
    map_obj.wall_type = data.get('wall_type', 'default')
    map_obj.name = data.get('name', 'Unnamed Map')
    map_obj.tileset = tuple(data.get("tileset", (26, 0, 0, 1, 2, 3, 4, 5)))
    # Set additional attributes that may not be in the constructor
    map_obj.rooms = data.get('rooms', [])
    map_obj.map_grid = data.get('map_grid', [])
    map_obj.liquid_grid = data.get('liquid_grid', [])
    
    # map_obj.valid_tiles = data.get('valid_tiles', [])
    map_obj.valid_tiles = set(tuple(pair) for pair in data.get('valid_tiles', []))
    map_obj.textured_map = data.get('textured_map', [])
    map_obj.valid_entity_tiles = set(tuple(pair) for pair in data.get('valid_entity_tiles', []))
    map_obj.valid_tiles_noshop = set(tuple(pair) for pair in data.get('valid_tiles_noshop', []))
    map_obj.level_list = data.get('level_list', [])
    map_obj.spawnpoint = tuple(data.get('spawnpoint', (0, 0)))
    map_obj.stairs = tuple(data.get('stairs', (0, 0)))
    # If you want to restore floor_items or all_enemies, do it here

    map_obj.floor_items = [item_from_dict(item_dict) if item_dict else None for item_dict in data["floor_items"]]
    map_obj.all_enemies = [enemy_from_dict(enemy_dict) for enemy_dict in data["all_enemies"]]

    return map_obj



def item_to_dict(item):
    return {
        "class": item.__class__.__name__,
        "name": item.name,
        "sprite_locs": item.sprite_locs,  # Assuming sprite_locs is an index or identifier
        "spriteindex": item.spriteindex,
        "magic_color": item.magic_color,
        "x": item.x,
        "y": item.y,
        "prevx": item.prevx,
        "prevy": item.prevy,
        "xinit": item.xinit,
        "yinit": item.yinit,
        "distance_to_travel": item.distance_to_travel,
        "xend": item.xend,
        "yend": item.yend,
        "entity": None,  # Not serializable, skip or handle specially if needed
        "chron_offset": item.chron_offset,
        "friendly_fire": item.friendly_fire,
        "quantity": item.quantity,
        "scale": item.scale,
        "is_usable": item.is_usable,
        "is_equipable": item.is_equipable,
        "is_consumable": item.is_consumable,
        "is_castable": item.is_castable,
        "is_piercing": item.is_piercing,
        "is_readable": item.is_readable,
        "should_be_deleted": item.should_be_deleted,
        "num_of_bounces": item.num_of_bounces,
        "num_of_pierces": item.num_of_pierces,
        "description": item.description,
        "is_hovered": item.is_hovered,
        "reverse": item.reverse,
        "price": item.price,
        "rarity": item.rarity,
        "color": list(item.color) if item.color else None,
        # "grid": ... # Only if you have a serializable version
    }
def item_from_dict(data):
    cls = data.get("class", "Item")
    # Default arguments for all items
    name = data["name"]
    sprite_locs = data.get("sprite_locs", 0)
    x = data.get("x", 0)
    y = data.get("y", 0)
    quantity = data.get("quantity", 1)
    description = data.get("description", "")

    if cls == "Weapon":
        item = Weapon(
            name=name,
            sprite_locs=sprite_locs,
            x=x,
            y=y,
            quantity=quantity,
            damage=data.get("damage", 0),
            durability=data.get("durability", 0),
            is_equipable=data.get("is_equipable", True),
            description=description,
            price=data.get("price", 0)
        )
        item.damage_type = data.get("damage_type", "slashing")
        item.bonus = data.get("bonus", 0)
    elif cls == "Staff":
        item = Staff(
            name=name,
            reverse=data.get("reverse", ""),
            sprite_locs=sprite_locs,
            projectile=data.get("is_castable_projectile", False),
            x=x,
            y=y,
            quantity=quantity,
            damage=data.get("damage", 0),
            charges=data.get("charges", 7),
            description=description,
            rarity=data.get("rarity", 0)
        )
        item.maxcharges = data.get("maxcharges", item.charges)
        item.damage_type = data.get("damage_type", "slashing")
    elif cls == "Tome":
        item = Tome(
            name=name,
            reverse=data.get("reverse", ""),
            sprite_locs=sprite_locs,
            projectile=data.get("is_castable_projectile", False),
            x=x,
            y=y,
            quantity=quantity,
            damage=data.get("damage", 0),
            charges=data.get("charges", 1),
            description=description,
            price=data.get("price", 0)
        )
        item.maxcharges = data.get("maxcharges", item.charges)
        item.damage_type = data.get("damage_type", "slashing")
        item.to_be_converted = data.get("to_be_converted", None)
    elif cls == "Flask":
        item = Flask(
            name=name,
            reverse=data.get("reverse", ""),
            evaporation_rate=data.get("evaporation_rate", 0),
            liquid=data.get("liquid", ""),
            product=data.get("product", ""),
            sprite_locs=sprite_locs,
            x=x,
            y=y,
            quantity=quantity,
            damage=data.get("damage", 0),
            description=description,
            price=data.get("price", 0)
        )
        item.charges = data.get("charges", 15)
        item.maxcharges = data.get("maxcharges", 15)
    elif cls == "Consumable":
        item = Consumable(
            name=name,
            sprite_locs=sprite_locs,
            nutrition_value=data.get("nutrition_value", 0),
            x=x,
            y=y,
            quantity=quantity,
            description=description,
            price=data.get("price", 0)
        )
    elif cls == "Shield":
        item = Shield(
            name=name,
            sprite_locs=sprite_locs,
            x=x,
            y=y,
            quantity=quantity,
            defense=data.get("defense", 0),
            is_equipable=data.get("is_equipable", True),
            description=description,
            price=data.get("price", 0)
        )
        item.bonus = data.get("bonus", 0)
    elif cls == "Miscellanious":
        item = Miscellanious(
            name=name,
            sprite_locs=sprite_locs,
            x=x,
            y=y,
            quantity=quantity,
            description=description,
            price=data.get("price", 0)
        )
    else:
        item = Item(
            name=name,
            sprite_locs=sprite_locs,
            x=x,
            y=y,
            quantity=quantity,
            description=description
        )

    # Set common fields
    item.spriteindex = data.get("spriteindex", item.spriteindex)
    item.magic_color = data.get("magic_color", item.magic_color)
    item.prevx = data.get("prevx", item.x)
    item.prevy = data.get("prevy", item.y)
    item.xinit = data.get("xinit", item.x)
    item.yinit = data.get("yinit", item.y)
    item.distance_to_travel = data.get("distance_to_travel", 0)
    item.xend = data.get("xend", item.x)
    item.yend = data.get("yend", item.y)
    item.chron_offset = data.get("chron_offset", 0)
    item.friendly_fire = data.get("friendly_fire", False)
    item.scale = data.get("scale", 3)
    item.is_usable = data.get("is_usable", False)
    item.is_equipable = data.get("is_equipable", False)
    item.is_consumable = data.get("is_consumable", False)
    item.is_castable = data.get("is_castable", False)
    item.is_piercing = data.get("is_piercing", False)
    item.is_readable = data.get("is_readable", False)
    item.should_be_deleted = data.get("should_be_deleted", False)
    item.num_of_bounces = data.get("num_of_bounces", 0)
    item.num_of_pierces = data.get("num_of_pierces", 0)
    item.is_hovered = data.get("is_hovered", False)
    item.rarity = data.get("rarity", 0)
    if "color" in data and data["color"] is not None:
        item.color = tuple(data["color"])
    # entity and grid are not restored here (not serializable)
    return item