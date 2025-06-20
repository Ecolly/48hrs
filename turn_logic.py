
import pyglet
from game_classes.techniques import *
from game_classes.enemy import *
from game_classes.player import *
import animations
from game_classes.projectiles import *









#for all entities, starting from player...
    #check AI (for player, this is already present)
    #do turn

def check_if_entity_is_on_screen(entity, player, result1, result2):
    if ((entity.x > player.x + 13 or entity.x < player.x - 13) or (entity.y > player.y + 9 or entity.y < player.y - 9)):
        return result1
    else:
        return result2

def adjust_rotation(entity, dx, dy):
    #adjust rotation state (gross)
    if dx == 1:
        if dy == 1:
            return FaceDirection.UP_RIGHT
        elif dy == -1:
            return FaceDirection.DOWN_RIGHT
        else:
            return FaceDirection.RIGHT
    elif dx == -1:
        if dy == 1:
            return FaceDirection.UP_LEFT
        elif dy == -1:
            return FaceDirection.DOWN_LEFT
        else:
            return FaceDirection.LEFT
    else:
        if dy == 1:
            return FaceDirection.UP
        elif dy == -1:
            return FaceDirection.DOWN
        else:
            return FaceDirection.DOWN



def can_move_to(x, y, game_map, player):
    #Detect walls
    if (y,x) not in game_map.valid_tiles:
        #print(f"Invalid tile cannot move{x, y}")
        return False
    else:
        for enemy in game_map.all_enemies:
            if enemy.x == x and enemy.y == y and enemy.should_be_deleted == False:
                return False
        if player.x == x and player.y == y:
            return False
        return True



def inflict_damage(attacker, target, player, chronology, list_of_animations, item, damage, damage_type):
    if target == None:
        return
    if damage_type == "physical":
        damage += attacker.strength
        if isinstance(item, Weapon) != False:
            if attacker.equipment_shield == None or attacker.equipment_shield.name != "Armor Plate":
                damage += attacker.equipment_weapon.damage
                if item.name == "Fury Cutter":
                    attacker.health = attacker.health - math.floor(damage/4)
        if target.equipment_shield != None:
            damage -= target.equipment_shield.defense
        damage -= target.defense
        if damage < 1:
            damage = 1

    target.health = target.health - damage

    if target != player and not target.is_alive():
        target.should_be_deleted = True
        #target.attacker = attacker

        #attacker.level_up()
        if attacker == player:
           attacker.increase_experience(target.experience)
        else:
           attacker.level_up()
    #print(damage_type, damage)

    anim = animations.Animation("-" + str(damage), 2, 0, (255, 0, 0, 0), chronology, check_if_entity_is_on_screen(target, player, 1, 50), target.x, target.y+0.5, target.x, target.y, 0, None, None, attacker, target, damage)
    #when this anim happens...

    list_of_animations.append(anim)







def do_spell(entity, enemy_hit, player, spellname, charges, chronology, list_of_animations):
    if spellname == "Red Staff":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, math.floor(enemy_hit.health/2), "magic")
        entity.inventory[entity.techniqueitem].charges -= charges
        if entity.inventory[entity.techniqueitem].charges < 1:
            entity.inventory[entity.techniqueitem].should_be_deleted = True
    if spellname == "Gold Staff":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, charges*2, "magic") #random.randint(charges, charges*3)
        entity.inventory[entity.techniqueitem].charges -= charges
        if entity.inventory[entity.techniqueitem].charges < 1:
            entity.inventory[entity.techniqueitem].should_be_deleted = True
    if spellname == "Green Staff":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 3, "magic") #random.randint(charges, charges*3)
        entity.inventory[entity.techniqueitem].charges -= charges
        if entity.inventory[entity.techniqueitem].charges < 1:
            entity.inventory[entity.techniqueitem].should_be_deleted = True
    elif spellname == "Spores":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 1, "magic")
    elif spellname == "Dragon Fire":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 10, "magic")


def find_reflection_angle(x, y, dx, dy, floor, targx, targy):
    #targx, targy are for when a projectile is reflecting off of an entity
    i = 0
    tilex = math.floor(x)
    tiley = math.floor(y)
    newx = x
    while (tiley,tilex) in floor.valid_tiles and (tilex != targx or tiley != targy) and i < 30:
        #print("A")
        newx = newx + dx
        tilex = math.floor(newx)
        i = i + 1
    tilex = math.floor(x)
    newy = y
    j = 0
    while (tiley,tilex) in floor.valid_tiles and (tilex != targx or tiley != targy) and j < 30:
        #print("b")
        newy = newy + dy
        tiley = math.floor(newy)
        j = j + 1
    if j > i:
        return "x"
    else:
        return "y"
    
    
def do_reflection(entity, item, enemy_hit, distance_x_normalized, distance_y_normalized, floor, chron_i, projectiles_remaining):
    if enemy_hit != None:
        tilex = math.floor(item.x)
        tiley = math.floor(item.y)
        while (tilex == enemy_hit.x and tiley == enemy_hit.y): #go backwards until finding a free space
            item.x = item.x - distance_x_normalized 
            item.y = item.y - distance_y_normalized
            tilex = math.floor(item.x)
            tiley = math.floor(item.y)
        enem_x, enem_y = enemy_hit.x, enemy_hit.y
    else:
        tilex = math.floor(item.x)
        tiley = math.floor(item.y)
        enem_x, enem_y = -1, -1


    item.num_of_bounces += -1
    reflection_result = find_reflection_angle(item.x, item.y, distance_x_normalized, distance_y_normalized, floor, enem_x, enem_y)
    if reflection_result == "x": #if the tile hit was a vertical wall...
        entity.techniquex = tilex + tilex - entity.techniquex
    elif reflection_result == "y":
        entity.techniquey = tiley + tiley - entity.techniquey
    projectiles_remaining += 1

    if isinstance(item, Projectile) == True:
        entity.active_projectiles.append(Projectile(item.name, 0, tilex, tiley, entity.techniquex, entity.techniquey, chron_i))
    else:
        entity.active_projectiles.append(item)
        item.x, item.y = tilex, tiley
        item.xend, item.yend = entity.techniquex + 0.5, entity.techniquey + 0.5
        item.xinit, item.yinit = tilex, tiley
        item.distance_to_travel = math.sqrt(abs(item.x - item.xend)**2 + abs(item.y - item.yend)**2)

    entity.active_projectiles[len(entity.active_projectiles)-1].num_of_bounces = item.num_of_bounces
    entity.active_projectiles[len(entity.active_projectiles)-1].friendly_fire = True

    return projectiles_remaining



def do_individual_turn(entity, floor, player, list_of_animations, chronology, prevtechnique):
    if entity.technique == Technique.STILL:
        return Technique.STILL, chronology
    elif entity.technique == Technique.MOVE:
        if can_move_to(entity.techniquex, entity.techniquey, floor, player):
            pass
        elif can_move_to(entity.techniquex, entity.y, floor, player):
            entity.techniquey = entity.y 
        elif can_move_to(entity.x, entity.techniquey, floor, player):
            entity.techniquex = entity.x
        else:
            entity.techniquex = entity.x 
            entity.techniquey = entity.y
        rot = adjust_rotation(entity, entity.techniquex-entity.x, entity.techniquey-entity.y)
        anim = animations.Animation(None, 0, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 8), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.MOVE, None, None, None)
        list_of_animations.append(anim)
        #if previous technique was not 'move' or 'still', chronology must be incremented by 8
        if prevtechnique != Technique.MOVE and prevtechnique != Technique.STILL:
            chronology += 8

        entity.x = entity.techniquex
        entity.y = entity.techniquey
        return Technique.MOVE, chronology
    elif entity.technique == Technique.CONSUME:
        entity.consume_item(entity.techniqueitem, list_of_animations)
        return Technique.CONSUME, chronology+10
    elif entity.technique == Technique.HIT:
        rot = adjust_rotation(entity, entity.techniquex-entity.x, entity.techniquey-entity.y)
        target = None
        if player.x == entity.techniquex and player.y == entity.techniquey:
            target = player
        else:
            for enemy in floor.all_enemies:
                if enemy.x == entity.techniquex and enemy.y == entity.techniquey and entity.should_be_deleted == False:
                    target = enemy

        if target != None:
            inflict_damage(entity, target, player, chronology+16, list_of_animations, entity.equipment_weapon, 0, "physical")
        
        if ((entity.x > player.x + 13 or entity.x < player.x - 13) or (entity.y > player.y + 9 or entity.y < player.y + 9)):
            t = 1
        else:
            t = 16


        anim2 = animations.Animation(None, 1, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.HIT, None, None, None)
        list_of_animations.append(anim2)
        chronology += 16

        return Technique.HIT, chronology
    elif entity.technique == Technique.THROW: #works for throwing items, casting projectile spells, and other projectiles
        rot = adjust_rotation(entity, entity.techniquex-entity.x, entity.techniquey-entity.y)
        anim2 = animations.Animation(None, 1, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.HIT, None, None, None)
        list_of_animations.append(anim2)
        #chronology += 16

        chron_i = 1
        projectiles_remaining = len(entity.active_projectiles)
        while projectiles_remaining > 0: #while there are still projectiles to move...
            itemi = 0
            for item in entity.active_projectiles: #for each projectile, move 1 unit of distance further in trajectory
                if item != -1:
                    if isinstance(item, Projectile) == True:
                        animtype = 4
                    else:
                        animtype = 3

                    # print("fgfggfgfg")
                    # print(entity.x, entity.y, entity.techniquex, entity.techniquey)
                    # print(item.xinit, item.yinit, item.xend, item.yend)
                    distance_x = item.xend - item.xinit
                    distance_y = item.yend - item.yinit
                    distance_total = math.sqrt(distance_x*distance_x + distance_y*distance_y) + 0.5

                    distance_x_normalized = distance_x/(distance_total*5)
                    distance_y_normalized = distance_y/(distance_total*5)

                    item.x = item.x + distance_x_normalized
                    item.y = item.y + distance_y_normalized

                    tilex = math.floor(item.x)
                    tiley = math.floor(item.y)

                    if item.name == "Dragon Fire" and (tilex != math.floor(item.x - distance_x_normalized) or tiley != math.floor(item.y - distance_y_normalized)):
                        #if applicable, add a new animation at every single tile along the projectile's path
                        list_of_animations.append(animations.Animation(29*2, 1, 5, (255, 255, 255, 0), chronology+chron_i, 5, tilex, tiley, tilex, tiley, rot, None, None, None, None, 0, None))

                    enemy_hit = None
                    if (entity != player or item.friendly_fire == True) and tilex == player.x and tiley == player.y: #if hit the player and player isnt the source entity
                        enemy_hit = player
                    else:
                        for enemy in floor.all_enemies:
                            if (enemy != entity or item.friendly_fire == True) and enemy.x == math.floor(item.x) and enemy.y == math.floor(item.y) and entity.should_be_deleted == False: #if hit an enemy and enemy isnt the source entity
                                enemy_hit = enemy
                    
                    if enemy_hit == None: #if no creature was hit
                        
                        if (tiley,tilex) not in floor.valid_tiles: #if a wall is hit...
                            i = 0
                            while (tiley,tilex) not in floor.valid_tiles: #go backwards until finding a free space
                                item.x = item.x - distance_x_normalized 
                                item.y = item.y - distance_y_normalized
                                tilex = math.floor(item.x)
                                tiley = math.floor(item.y)
                            distance_travelled = math.sqrt(abs(tilex - entity.x)**2 + abs(tiley - entity.y)**2)
                            #add animation
                            #remove from projectiles remaining
                            

                            if item.num_of_bounces > 0:
                                projectiles_remaining = do_reflection(entity, item, None, distance_x_normalized, distance_y_normalized, floor, chron_i, projectiles_remaining)
                            else:
                                if isinstance(item, Projectile) == True:
                                    do_spell(entity, None, player, item.name, entity.techniquecharges, chronology+chron_i, list_of_animations)

                            anim3 = animations.Animation(item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item)
                            list_of_animations.append(anim3)
                            entity.active_projectiles[itemi] = -1
                            projectiles_remaining += -1





                        else:
                            #if nothing was hit
                            distance_travelled = math.sqrt(abs(tilex - entity.x)**2 + abs(tiley - entity.y)**2)
                            if distance_travelled > distance_total:
                                anim3 = animations.Animation(item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item)
                                list_of_animations.append(anim3)
                                entity.active_projectiles[itemi] = -1
                                projectiles_remaining += -1 
                                if isinstance(item, Projectile) == True:
                                    do_spell(entity, None, player, item.name, entity.techniquecharges, chronology+chron_i, list_of_animations)
                            
                    else: #if a creature was hit inflict damage on them
                        #if the enemy is reflective (i.e. chrome dome) then simply reflect the projectile
                        #items cannot bounce (they are bugged...)
                        if enemy_hit.name == "CHROME DOME" and item.num_of_bounces > -3 and isinstance(item, Projectile):
                            #print("testetetet")
                            projectiles_remaining = do_reflection(entity, item, enemy_hit, distance_x_normalized, distance_y_normalized, floor, chron_i, projectiles_remaining)
                        else:
                            if isinstance(item, Projectile) == True:
                                do_spell(entity, enemy_hit, player, item.name, entity.techniquecharges, chronology+chron_i, list_of_animations)
                            else:
                                inflict_damage(entity, enemy_hit, player, chronology+chron_i, list_of_animations, item, 0, "physical")
                        
                        
                        anim3 = animations.Animation(item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item)
                        list_of_animations.append(anim3)
                        entity.active_projectiles[itemi] = -1
                        projectiles_remaining += -1

                
                

                itemi += 1
            chron_i += 1
        entity.active_projectiles = []

        chronology = chronology + max(chron_i, 16)

        return Technique.THROW, chronology
    elif entity.technique == Technique.CAST: #this is for static castings (not projectiles)
        item = entity.inventory[entity.techniqueitem]
        if item.name == "Orange Staff":
            inflict_damage(entity, player, player, chronology, list_of_animations, item, 15, "magic")
            for enemy in floor.all_enemies:
                inflict_damage(entity, enemy, player, chronology, list_of_animations, item, 15, "magic")
        
        chronology += 10
        return Technique.CAST, chronology





                    # allowed_to_drop = 1
                    # for i in map.floor_items:
                    #     # Check if the item is at the player's current position
                    #     if i.x == entity.techniquex and i.y == entity.techniquey:
                    #         allowed_to_drop = 0

                    # if allowed_to_drop == 1: #if no enemy detected and no item is on this spot, simply drop the item on the floor at this tile
                    #     item.x = self.techniquex
                    #     item.y = self.techniquey
                    #     map.floor_items.append(item)
                    # else:
                    #     del item

                # if self.techniqueframe == 20:
                #     self.active_projectiles = []
                #     self.techniquex = self.x
                #     self.techniquey = self.y
                #     self.technique = Technique.MOVE
                #     self.techniquefinished = 1



        pass
    elif entity.technique == Technique.CAST:
        pass
    else:
        pass






def do_turns(all_enemies, player, floor):
    list_of_animations = []
    chronology = 0
    prevtechnique = Technique.STILL
    prevtechnique, chronology = do_individual_turn(player, floor, player, list_of_animations, chronology, prevtechnique)
    player.turns_left_before_moving += -1

    for enemy in all_enemies:
        while enemy.turns_left_before_moving > player.turns_left_before_moving:
            if enemy.should_be_deleted != True: #if enemy isnt already dead...
                enemy.technique, enemy.techniquex, enemy.techniquey = enemy.do_AI(all_enemies, player, floor)
                prevtechnique, chronology = do_individual_turn(enemy, floor, player, list_of_animations, chronology, prevtechnique)
            enemy.turns_left_before_moving += -1
        if enemy.turns_left_before_moving == 0:
            enemy.turns_left_before_moving = enemy.speed
            enemy.speed_turns += -1
            if enemy.speed_turns < 1:
                enemy.speed = enemy.default_speed

    if player.turns_left_before_moving == 0:
        player.turns_left_before_moving = player.speed
        player.speed_turns += -1
        if player.speed_turns < 1:
            player.speed = player.default_speed
        
    return list_of_animations




    # if player.turns_left_before_moving == 0:
    #     for enemy in all_enemies:
    #         i = 0
    #         while i < enemy.speed:
    #             if enemy.should_be_deleted != True: #if enemy isnt already dead...
    #                 enemy.technique, enemy.techniquex, enemy.techniquey = enemy.do_AI(all_enemies, player, floor)
    #                 prevtechnique, chronology = do_individual_turn(enemy, floor, player, list_of_animations, chronology, prevtechnique)
    #             i = i + 1
    #         enemy.speed_turns += -1
    #         if enemy.speed_turns < 1:
    #             enemy.speed = enemy.default_speed
    #     player.turns_left_before_moving = player.speed
    #     player.speed_turns += -1
    #     if player.speed_turns < 1:
    #         player.speed = player.default_speed
    # return list_of_animations


















