def save_game(Player ):
    pass


def player_to_dict(player):
    return {
        'class': player.__class__.__name__,
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

        # self.scale = 3

def item_to_dict(item):
    return {
            "class": self.__class__.__name__,
            "name": self.name,
            "spriteindex": self.spriteindex,
            "x": self.x,
            "y": self.y,
            "quantity": self.quantity,
            "description": self.description,
            "price": getattr(self, "price", 0),
            # Add any other common attributes you want to save
        }
    
