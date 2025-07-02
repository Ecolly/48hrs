
import json
import time

def save_game_data(game_data):
    directory = "game_saves/"
    filename = time.strftime("save_%Y%m%d_%H%M%S.json")
    print(f"Saving game data to {directory + filename}")
    with open(directory + filename, 'w') as f:
        json.dump(game_data, f, indent=4)
    
        


def player_to_dict(player):
    return {
        'class': player.__class__.__name__,
        'name': player.name,
        'health': player.health,
        'level': player.level,
        'experience': player.experience,
        #"inventory": [item_to_dict(item) if item else None for item in player.inventory],

        'x': player.x,
        'y': player.y,
        'spriteindex': player.spriteindex, #needs to be implemented, get the index of the sprite
        # 'spritegrid': player.spritegrid, #needs to be implemented
        # 'itemgrid': player.itemgrid, #needs to be implemented
        'animtype': player.animtype,


        #separate attributes that needs to be added after the player is created
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



        

    #These needs to be set after the items are created
        # self.equipment_weapon = None
        # self.equipment_shield = None

        #these are for displaying the stats during combat (THIS MAKES ME WANT TO CRY)
        # self.health_visual = health
        # self.maxhealth_visual = health
        # self.experience_visual = experience
        # self.level_visual = level
        

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

def item_to_dict(item):
    return {
            "class": item.__class__.__name__,
            "name": item.name,
            "spriteindex": item.spriteindex,
            "x": item.x,
            "y": item.y,
            "quantity": item.quantity,
            "description": item.description,
            "price": getattr(item, "price", 0),
            
            # Add any other common attributes you want to save
            
            # self.sprite = create_sprite_item(grid_items, 29*10+ sprite_locs)
            # self.hotbar_sprite = create_sprite_item(grid_items, 29*10+ sprite_locs)
            # self.grid = grid_items
            # self.spriteindex = 29*10+sprite_locs
            # self.color = (255, 255, 255, 255)
            # self.magic_color = sprite_locs

            #Projectiles
            # self.entity = None
            # self.chron_offset = 0
            
            "price": getattr(item, "price", 0),
            "friendly_fire": getattr(item, "friendly_fire", False),
            "scale": getattr(item, "scale", 3),
            "is_usable": getattr(item, "is_usable", False),
            "is_equipable": getattr(item, "is_equipable", False),
            "is_consumable": getattr(item, "is_consumable", False),
            "is_castable": getattr(item, "is_castable", False),
            "is_piercing": getattr(item, "is_piercing", False),
            "is_readable": getattr(item, "is_readable", False),
            "should_be_deleted": getattr(item, "should_be_deleted", False),
            "num_of_bounces": getattr(item, "num_of_bounces", 0),
            "num_of_pierces": getattr(item, "num_of_pierces", 0),
            "reverse": getattr(item, "reverse", ""),
        }


def enemy_to_dict(enemy):
    return{

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
        "direction": enemy.direction.name if hasattr(enemy.direction, "name") else enemy.direction,
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
    
def game_to_dict(game):
    pass
def map_to_dict(map_obj):
    return {
        "map_type": map_obj.map_type,
        "wall_type": map_obj.wall_type,
        "width": map_obj.width,
        "height": map_obj.height,
        "number_of_rooms": map_obj.number_of_rooms,
        "rooms": map_obj.rooms,  # Make sure each room is serializable!
        
        
        #sus ones that is not easily serializable
        "map_grid": map_obj.map_grid,
        "liquid_grid": map_obj.liquid_grid,
        "item_list": map_obj.item_list,      # If these are lists of strings/ints, it's fine
        "enemy_list": map_obj.enemy_list,

        "valid_tiles": map_obj.valid_tiles,
        "textured_map": map_obj.textured_map,
        "valid_entity_tiles": map_obj.valid_entity_tiles,
        "valid_tiles_noshop": map_obj.valid_tiles_noshop,
        "name": map_obj.name,
        
        "level_list": map_obj.level_list,
        # "floor_items": [item_to_dict(item) for item in map_obj.floor_items],  # Save items on the floor
        # "all_enemies": [enemy_to_dict(enemy) for enemy in map_obj.all_enemies],  # Save enemies
        "spawnpoint": list(map_obj.spawnpoint),  # Convert set to list for JSON
        "stairs": list(map_obj.stairs),    
    }