def save_game(Player ):
    pass


def player_to_dict(player):
    return {
        'name': player.name,
        'health': player.health,
        'level': player.level,
        'experience': player.experience,

        'x': player.x,
        'y': player.y,
        'spriteindex': player.spriteindex, #needs to be implemented, get the index of the sprite
        'spritegrid': player.spritegrid, #needs to be implemented
        'itemgrid': player.itemgrid, #needs to be implemented
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
    }
        
        



    #These needs to be set after the items are created
        # self.equipment_weapon = None
        # self.equipment_shield = None

        #these are for displaying the stats during combat (THIS MAKES ME WANT TO CRY)
        # self.health_visual = health
        # self.maxhealth_visual = health
        # self.experience_visual = experience
        # self.level_visual = level
        #self.inventory = [None]*40
        

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

        # self.animtype = animtype #animation type. pulls from a set library of animation behaviors.
        # self.animframe = 0 #what frame of the animation it's on
        # self.animmod = 1/16 #a preset animation modifier (e.g. vibration amplitude)
        # self.scale = 3

        # self.default_speed = 2
        # self.speed = 2
        # self.turns_left_before_moving = 2
        # self.speed_turns = 0
        # self.speed_visual = 2
        
        # self.paralysis_turns = 0
        # self.paralysis_visual = 0

        # self.flee_ai_turns = 0
        # self.rage_ai_turns = 0

        # self.is_shopping = False


