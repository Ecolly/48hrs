
import pyglet
from game_classes.techniques import *
from game_classes.enemy import *
from game_classes.player import *
import animations
from game_classes.projectiles import *
from game_classes.id_shuffling import *




def can_move_to_but_not_a_cancerous_growth_on_society(x, y, game_map, player):
    #Detect walls
    if (y,x) not in game_map.valid_tiles:
        #print(f"Invalid tile cannot move{x, y}")
        return False
    else:
        for enemy in game_map.all_enemies:
            if enemy.technique == Technique.MOVE and enemy.techniquefinished == 0 and enemy.techniquex == x and enemy.techniquey == y:#x == enemy.x and y == enemy.y:
                return False
            elif enemy.x == x and enemy.y == y:
                return False
        if player.x == x and player.y == y:
            return False
        return True



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
    exp_multiplier = 1
    if damage_type == "execution":
        exp_multiplier = damage
        damage = 3


    strength_reduction = 0
    defense_reduction = 0
    if target == None or target.should_be_deleted == True:
        return
    if damage_type == "physical" or damage_type == "recoil":
        if attacker.name == "SCORPION":
            #strength_reduction = 1
            defense_reduction = 1
            if attacker.level == 2:
                pass
                #strength_reduction = 3
            elif attacker.level == 3:
                strength_reduction = 1
                defense_reduction = 1
            elif attacker.level == 4:
                strength_reduction = 3
                defense_reduction = 3

            target.strength = max(target.strength-strength_reduction, 1)
            target.defense = max(target.defense-defense_reduction, 1)

        damage += attacker.strength
        if isinstance(item, Weapon) != False:
            if attacker.equipment_shield == None or attacker.equipment_shield.name != "Armor Plate":
                damage += item.damage + item.bonus
                if item.name == "Fury Cutter":
                    attacker.health = attacker.health - math.floor(damage/4)
        if target.equipment_shield != None:
            damage -= target.equipment_shield.defense
        damage -= target.defense
        if damage_type == "recoil":
            damage = math.floor(damage / 8)
        if damage < 1:
            damage = 1
    else: #smoke
        anim = animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(target, player, 1, 16), target.x, target.y, target.x, target.y, 0, None, None, None, None, None)
        list_of_animations.append(anim)
        pass
    
    target.health = target.health - damage
    #target.paralysis_turns = 0 #paralysis turns should be set to 0 if taking damage?

    if target != player and not target.is_alive():
        target.should_be_deleted = True
        if attacker == player:
           attacker.increase_experience(target.experience*exp_multiplier)
        else:
           attacker.level_up()
           list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(attacker, player, 1, 16), attacker.x, attacker.y, attacker.x, attacker.y, 0, None, None, None, None, None))

    #damage number
    anim = animations.Animation("-" + str(damage), 2, 0, (255, 0, 0, 0), chronology, check_if_entity_is_on_screen(target, player, 1, 50), target.x, target.y+0.5, target.x, target.y, 0, None, None, attacker, target, damage, defense_reduction=defense_reduction, strength_reduction=strength_reduction)
    list_of_animations.append(anim)





def inflict_healing(amount, entity, player, list_of_animations, chronology):
    if (entity.health + amount > entity.maxhealth):
        amount = entity.maxhealth - entity.health
    amount = math.floor(amount)
    entity.health += amount
    anim = animations.Animation("+" + str(amount), 2, 0, (0, 189, 66, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 50), entity.x, entity.y+0.5, entity.x, entity.y, 0, None, None, entity, entity, -amount)
    list_of_animations.append(anim)



def deduct_charges(entity, charges):
    if entity.techniqueitem != None:
        entity.techniqueitem.charges -= charges
        if entity.techniqueitem.charges < 1:
            entity.techniqueitem.should_be_deleted = True


def do_spell(floor, entity, enemy_hit, player, spellname, charges, chronology, list_of_animations):
    if spellname == "Greater Healing Staff":
        if enemy_hit != None:
            inflict_healing(enemy_hit.health/2, enemy_hit, player, list_of_animations, chronology)
            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges)
    if spellname == "Lesser Healing Staff":
        if enemy_hit != None:
            inflict_healing(charges*2, enemy_hit, player, list_of_animations, chronology)
            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges)
    if spellname == "Staff of Division":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, math.floor(enemy_hit.health/2), "magic")
        deduct_charges(entity, charges)
    if spellname == "Staff of Swapping":
        if enemy_hit != None:
            x, y = enemy_hit.x, enemy_hit.y
            enemy_hit.x, enemy_hit.y = entity.x, entity.y
            entity.x, entity.y = x, y
            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))

        deduct_charges(entity, charges)
    if spellname == "Staff of Warping":
        if enemy_hit != None:
            i = 0
            while i < 100:
                y, x = random.choice(floor.valid_tiles)
                if enemy_hit.can_move_to(x, y, floor) == True:
                    enemy_hit.x, enemy_hit.y = x, y
                    list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
                    break
                i = i + 1
        deduct_charges(entity, charges)
    elif spellname == "Staff of Mana":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, charges*2, "magic") #random.randint(charges, charges*3)
        deduct_charges(entity, charges)
    elif spellname == "Staff of Ricochet" or spellname == "Piercing Staff":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 3, "magic")
        deduct_charges(entity, charges)
    elif spellname == "Execution Staff":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, charges, "execution")
        deduct_charges(entity, charges)
    elif spellname == "Staff of Lethargy":
        enemy_hit.speed = 1
        enemy_hit.speed_turns = charges
        list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges)
    elif spellname == "Energizing Staff":
        enemy_hit.speed = 4
        enemy_hit.speed_turns = charges
        list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges)
    elif spellname == "Staff of Paralysis": #paralysis
        enemy_hit.paralysis_turns = charges
        list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges)
    elif spellname == "Staff of Violence": #rage
        enemy_hit.rage_ai_turns = charges
        list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges)
    elif spellname == "Phobia Staff": #fear
        enemy_hit.flee_ai_turns = charges
        list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges)
    elif spellname == "Spores": #damage
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 1, "magic")
        list_of_animations.append(animations.Animation(1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Spores 2": #decrease attack
        if enemy_hit != None:
            enemy_hit.strength = max(enemy_hit.strength-1, 1)
            enemy_hit.defense = max(enemy_hit.defense-1, 1)
            #anim goes here?
        list_of_animations.append(animations.Animation(1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Spores 3": #slow
        if enemy_hit != None:
            enemy_hit.speed = 1
            enemy_hit.speed_turns = 6
        list_of_animations.append(animations.Animation(1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Spores 4": #paralysis
        if enemy_hit != None:
            enemy_hit.paralysis_turns = 3
        list_of_animations.append(animations.Animation(1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Dragon Fire":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 10, "magic")
    elif spellname == "Dragon Fire 2":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 20, "magic")
    elif spellname == "Dragon Fire 3":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 30, "magic")
    elif spellname == "Dragon Fire 4":
        inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 40, "magic")

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
        item.xend = math.floor(tilex + (abs(tilex - item.xend) + 100*abs(distance_x_normalized))*math.copysign(1, item.xinit - item.xend))
        item.yend = math.floor(tiley + (abs(item.yend - tiley) + 100*abs(distance_y_normalized))*math.copysign(1, item.yend - item.yinit))
    elif reflection_result == "y":
        item.yend = math.floor(tiley + (abs(tiley - item.yend) + 100*abs(distance_y_normalized))*math.copysign(1, item.yinit - item.yend))
        item.xend = math.floor(tilex + (abs(item.xend - tilex) + 100*abs(distance_x_normalized))*math.copysign(1, item.xend - item.xinit))
    projectiles_remaining += 1

    if isinstance(item, Projectile) == True:
        entity.active_projectiles.append(Projectile(item.name, 0, tilex, tiley, item.xend, item.yend, entity, chron_i))
    else:
        entity.active_projectiles.append(item)
        item.x, item.y = tilex, tiley
        item.xend, item.yend = item.xend + 0.5, item.yend + 0.5
        item.xinit, item.yinit = tilex, tiley
        item.distance_to_travel = math.sqrt(abs(item.x - item.xend)**2 + abs(item.y - item.yend)**2)

    entity.active_projectiles[len(entity.active_projectiles)-1].num_of_bounces = item.num_of_bounces
    entity.active_projectiles[len(entity.active_projectiles)-1].friendly_fire = True

    return projectiles_remaining


def clamp(n, min, max): #why the fuck isnt this inbuilt
    if n < min:
        return min
    elif n > max:
        return max
    else:
        return n
    


def do_radioactivity(entity, player, chronology, list_of_animations, floor):
    if entity.name == "DEMON CORE":
        enemy = player
        dist = math.sqrt((enemy.x - entity.x)**2 + (enemy.y - entity.y)**2)
        damage = math.floor(((entity.level + 3)**2)/(dist*dist))
        if damage > 0:
            inflict_damage(entity, enemy, player, chronology, list_of_animations, None, damage, "magic")
        for enemy in floor.all_enemies:
            if enemy.name != "DEMON CORE":
                dist = math.sqrt((enemy.x - entity.x)**2 + (enemy.y - entity.y)**2)
                damage = math.floor(((entity.level + 3)**2)/(dist*dist))
                if damage > 0:
                    inflict_damage(entity, enemy, player, chronology, list_of_animations, None, damage, "magic")
    

def do_individual_turn(entity, floor, player, list_of_animations, chronology, prevtechnique):
    global fakenames_staffs_key, fakenames_tomes_key, fakenames_staffs_realnames, fakenames_tomes_realnames, grid_items
    do_radioactivity(entity, player, chronology, list_of_animations, floor)
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
            chronology += check_if_entity_is_on_screen(entity, player, 1, 8)

        entity.x = entity.techniquex
        entity.y = entity.techniquey
        return Technique.MOVE, chronology
    elif entity.technique == Technique.CONSUME:
        entity.consume_item(entity.techniqueitem, list_of_animations)
        return Technique.CONSUME, chronology+10
    elif entity.technique == Technique.HIT:
        rot = adjust_rotation(entity, clamp(entity.techniquex-entity.x, -1, 1), clamp(entity.techniquey-entity.y, -1, 1))
        target_list = [[entity.techniquex, entity.techniquey]]

        if entity.equipment_weapon != None:
            if entity.equipment_weapon.name == "Sickle":
                sickle_targ_list = [[entity.x+1, entity.y], [entity.x+1, entity.y+1], [entity.x, entity.y+1], [entity.x-1, entity.y+1], [entity.x-1, entity.y], [entity.x-1, entity.y-1], [entity.x, entity.y-1], [entity.x+1, entity.y-1]]
                if [entity.techniquex, entity.techniquey] in sickle_targ_list:
                    sickle_targ_index = sickle_targ_list.index([entity.techniquex, entity.techniquey])
                    target_list.append(sickle_targ_list[(sickle_targ_index + 1)%len(sickle_targ_list)])
                    target_list.append(sickle_targ_list[(sickle_targ_index - 1)%len(sickle_targ_list)])
            elif entity.equipment_weapon.name == "Rapier":
                #do piercing
                if abs(entity.techniquex - entity.x) < 2 and abs(entity.techniquey - entity.y) < 2: #if within normal 'strike' range
                    pass
                else: #else...
                    target_list.append([math.floor((entity.techniquex+entity.x)/2), math.floor((entity.techniquey+entity.y)/2)])
                pass

        for targ_tile in target_list:
            target = None
            if player.x == targ_tile[0] and player.y == targ_tile[1]:
                target = player
            else:
                for enemy in floor.all_enemies:
                    if enemy.x == targ_tile[0] and enemy.y == targ_tile[1] and entity.should_be_deleted == False:
                        target = enemy

            if target != None:
                inflict_damage(entity, target, player, chronology+check_if_entity_is_on_screen(entity, player, 1, 16), list_of_animations, entity.equipment_weapon, 0, "physical")
                if target.equipment_shield != None and target.equipment_shield.name == "Spiked Shield":
                    inflict_damage(entity, entity, player, chronology+check_if_entity_is_on_screen(entity, player, 1, 16), list_of_animations, entity.equipment_weapon, 0, "recoil")
                if target.name == "JUJUBE" and random.uniform(0, 1) < 0.3:
                    spawn_enemies_within_turn_execution(1, "JUJUBE", target.level, target, floor, player, chronology + check_if_entity_is_on_screen(entity, player, 1, 16), list_of_animations)





            


        anim2 = animations.Animation(None, 1, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.HIT, None, None, None)
        list_of_animations.append(anim2)
        chronology += check_if_entity_is_on_screen(entity, player, 1, 16)
        return Technique.HIT, chronology
    elif entity.technique == Technique.THROW: #works for throwing items, casting projectile spells, and other projectiles
        #print(entity.x, entity.y, entity.techniquex, entity.techniquey)

        rot = adjust_rotation(entity, clamp(-entity.x+entity.techniquex, -1, 1), clamp(-entity.y+entity.techniquey, -1, 1))

        if entity.techniqueitem != None and isinstance(entity.techniqueitem, Staff) == True:
            anim2 = animations.Animation(None, 1, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.HIT, None, None, None, item=entity.techniqueitem.spriteindex)
        else:
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
                    if (player != item.entity or item.friendly_fire == True) and tilex == player.x and tiley == player.y: #if hit the player and player isnt the source entity
                        enemy_hit = player
                    else:
                        for enemy in floor.all_enemies:
                            if (enemy != item.entity or item.friendly_fire == True) and enemy.x == math.floor(item.x) and enemy.y == math.floor(item.y) and entity.should_be_deleted == False: #if hit an enemy and enemy isnt the source entity
                                enemy_hit = enemy
                    
                    if enemy_hit == None: #if no creature was hit
                        
                        if floor.wall_type == "Solid" and ((tiley,tilex) not in floor.valid_tiles): #if a wall is hit...
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
                                    do_spell(floor, entity, None, player, item.name, entity.techniquecharges, chronology+chron_i, list_of_animations)

                            anim3 = animations.Animation(item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item, drop_item=True)
                            list_of_animations.append(anim3)
                            entity.active_projectiles[itemi] = -1
                            projectiles_remaining += -1
                        else:
                            #if nothing was hit
                            distance_travelled = math.sqrt(abs(tilex - entity.x)**2 + abs(tiley - entity.y)**2)
                            if distance_travelled > distance_total:
                                anim3 = animations.Animation(item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item, drop_item=True)
                                list_of_animations.append(anim3)
                                entity.active_projectiles[itemi] = -1
                                projectiles_remaining += -1 
                                if isinstance(item, Projectile) == True:
                                    do_spell(floor, entity, None, player, item.name, entity.techniquecharges, chronology+chron_i, list_of_animations)
                            
                    else: #if a creature was hit inflict damage on them
                        #if the enemy is reflective (i.e. chrome dome) then simply reflect the projectile
                        #items cannot bounce (if set to bounce, are bugged...)

                        enemy_shield = None if enemy_hit.equipment_shield == None else enemy_hit.equipment_shield.name
                        if (enemy_hit.name == "CHROME DOME" or enemy_shield == "Mirror Shield") and item.num_of_bounces > -3 and isinstance(item, Projectile):
                            projectiles_remaining = do_reflection(entity, item, enemy_hit, distance_x_normalized, distance_y_normalized, floor, chron_i, projectiles_remaining)
                        
                            anim3 = animations.Animation(item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, enemy_hit, 0, item)
                            list_of_animations.append(anim3)
                            entity.active_projectiles[itemi] = -1
                            projectiles_remaining += -1
                        else:
                            if isinstance(item, Projectile) == True:
                                do_spell(floor, entity, enemy_hit, player, item.name, entity.techniquecharges, chronology+chron_i, list_of_animations)
                            else:
                                inflict_damage(entity, enemy_hit, player, chronology+chron_i, list_of_animations, item, 0, "physical")
                            #if the projectile is piercing and didn't bounce, don't delete it and instead just set its entity of origin as the entity it just hit
                            #should this be changed to pierce enemies so long as the projectile killed the enemy it's trying to pierce?
                            if item.num_of_pierces > 0:
                                item.num_of_pierces += -1
                                if enemy_hit.should_be_deleted == False:
                                    item.entity = enemy_hit
                                    item.friendly_fire = False
                            else:
                                anim3 = animations.Animation(item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, enemy_hit, 0, item)
                                list_of_animations.append(anim3)
                                entity.active_projectiles[itemi] = -1
                                projectiles_remaining += -1

                
                

                itemi += 1
            chron_i += 1
        entity.active_projectiles = []

        chronology = chronology + max(chron_i, check_if_entity_is_on_screen(entity, player, 1, 16))
        return Technique.THROW, chronology
    elif entity.technique == Technique.CAST: #this is for static castings (not projectiles)


        item = entity.techniqueitem

        anim2 = animations.Animation(None, 5, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 24), entity.x, entity.y, entity.techniquex, entity.techniquey, entity.direction, entity, Technique.CAST, None, None, None, item=[item.spriteindex, item.name])
        list_of_animations.append(anim2)
        chronology += 24
    
        # if item.name == "Blank Tome":
        #     i = 39 
        #     while i > -1:
        #         if isinstance(player.inventory[i], Tome) == True:
        #             item.name = player.inventory[i].name
        #             break
        #         i = i - 1

        if item.name == "Tome of Recovery":
            inflict_healing(15, player, player, list_of_animations, chronology)
            for enemy in floor.all_enemies:
                inflict_healing(15, enemy, player, list_of_animations, chronology)
            deduct_charges(entity, 1)
        elif item.name == "Tome of Injury":
            inflict_damage(entity, player, player, chronology, list_of_animations, item, 15, "magic")
            for enemy in floor.all_enemies:
                inflict_damage(entity, enemy, player, chronology, list_of_animations, item, 15, "magic")
            deduct_charges(entity, 1)
        elif item.name == "Tome of Promotion":
            player.increase_experience(((player.level + 1)**3) - player.experience) 
            for enemy in floor.all_enemies:
                enemy.level_up()
                list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1)
        elif item.name == "Tome of Demotion":
            player.increase_experience(((player.level - 1)**3) - player.experience) 
            for enemy in floor.all_enemies:
                enemy.level_down()
                list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1)
        elif item.name == "Immunity Tome":
            player.defense = 100
            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(player, player, 1, 16), player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            for enemy in floor.all_enemies:
                enemy.defense = 100
                list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1)
        elif item.name == "Paperskin Tome":
            player.defense = -100
            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(player, player, 1, 16), player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            for enemy in floor.all_enemies:
                enemy.defense = -100
                list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1)
        elif item.name == "Banishing Tome":
            for enemy in floor.all_enemies:
                if abs(enemy.x - entity.x) < 2 and abs(enemy.y - entity.y) < 2 and enemy != entity:
                    i = 0
                    while i < 100:
                        y, x = random.choice(floor.valid_tiles)
                        if enemy.can_move_to(x, y, floor) == True:
                            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
                            enemy.x, enemy.y = x, y
                            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
                            break
                        i = i + 1
            deduct_charges(entity, 1)
        elif item.name == "Summoning Tome":
            enemies_to_summon = random.randint(3, 6)
            spawn_enemies_within_turn_execution(enemies_to_summon, None, None, entity, floor, player, chronology, list_of_animations)
            deduct_charges(entity, 1)
        elif item.name == "Sharpening Tome":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Weapon) == True:
                    player.inventory[i].bonus += 1
                    break
                i = i - 1
            deduct_charges(entity, 1)
        elif item.name == "Fortifying Tome":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Shield) == True:
                    player.inventory[i].bonus += 1
                    break
                i = i - 1
            deduct_charges(entity, 1)
        elif item.name == "Staffboost Tome":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True:
                    player.inventory[i].charges += 1
                    player.inventory[i].maxcharges += 1
                    break
                i = i - 1
            deduct_charges(entity, 1)
        elif item.name == "Tome of Reversal":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True or isinstance(player.inventory[i], Tome) == True:
                    objlist = player.inventory
                    charges, maxcharges = objlist[i].charges, objlist[i].maxcharges
                    objlist[i].sprite.delete() 
                    objlist[i].hotbar_sprite.delete() 
                    objlist[i] = floor.create_item(objlist[i].reverse, objlist[i].grid)
                    objlist[i].charges, objlist[i].maxcharges = charges, maxcharges
                    break
                i = i - 1
            deduct_charges(entity, 1)
        elif item.name == "Blank Tome":
            blank_id = player.inventory.index(item)

            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Tome) == True and player.inventory[i].name != "Blank Tome":
                    objlist = player.inventory
                    objlist[blank_id].sprite.delete() 
                    objlist[blank_id].hotbar_sprite.delete() 
                    objlist[blank_id] = floor.create_item(objlist[i].name, objlist[i].grid)
                    break
                i = i - 1
            #deduct_charges(entity, 1)
        elif item.name == "Tome of Consolidation":
            weapons_1_2 = []
            shields_1_2 = []
            staffs_1_2 = []
            i = 39
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True:
                    staffs_1_2.append(i)
                    if len(staffs_1_2) == 2:
                        player.inventory[staffs_1_2[0]].charges += 1
                        player.inventory[staffs_1_2[0]].maxcharges += 1
                        player.inventory[staffs_1_2[1]].should_be_deleted = True
                        break
                if isinstance(player.inventory[i], Shield) == True:
                    shields_1_2.append(i)
                    if len(shields_1_2) == 2:
                        player.inventory[shields_1_2[0]].bonus += player.inventory[shields_1_2[1]].bonus
                        player.inventory[shields_1_2[1]].should_be_deleted = True
                        break
                if isinstance(player.inventory[i], Weapon) == True:
                    weapons_1_2.append(i)
                    if len(weapons_1_2) == 2:
                        player.inventory[weapons_1_2[0]].bonus += player.inventory[weapons_1_2[1]].bonus
                        player.inventory[weapons_1_2[1]].should_be_deleted = True
                        break
                i = i - 1
            deduct_charges(entity, 1)
        elif item.name == "Coloring Tome":
            items_1_2 = []
            i = 39
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True or isinstance(player.inventory[i], Tome) == True:
                    items_1_2.append(i)
                    if len(items_1_2) == 2:
                        color = player.inventory[items_1_2[1]].magic_color
                        if isinstance(player.inventory[items_1_2[0]], Staff):
                            index = fakenames_staffs_key.index(color)
                            name = fakenames_staffs_realnames[index]
                        else:
                            index = fakenames_tomes_key.index(color)
                            name = fakenames_tomes_realnames[index]


                        objlist = player.inventory
                        charges, maxcharges = objlist[items_1_2[0]].charges, objlist[items_1_2[0]].maxcharges
                        objlist[items_1_2[0]].sprite.delete() 
                        objlist[items_1_2[0]].hotbar_sprite.delete() 
                        objlist[items_1_2[0]] = floor.create_item(name, objlist[items_1_2[0]].grid)
                        objlist[items_1_2[0]].charges, objlist[items_1_2[0]].maxcharges = charges, maxcharges

                        break
                i = i - 1
            deduct_charges(entity, 1)


        return Technique.CAST, chronology
    else:
        pass

    






def refresh_entity_states(entity):
    entity.speed_turns += -1
    entity.paralysis_turns += -1
    entity.flee_ai_turns += -1
    entity.rage_ai_turns += -1
    if entity.speed_turns < 1:
        entity.speed = entity.default_speed
    




def do_turns(all_enemies, player, floor):
    list_of_animations = []
    chronology = 0
    prevtechnique = Technique.STILL

    if player.paralysis_turns > 0: #overwrite the player's technique if needed
        player.technique = Technique.STILL
    elif player.flee_ai_turns > 0: 
        player.technique = Technique.STILL
    elif player.rage_ai_turns > 0: 
        player.technique = Technique.STILL

    prevtechnique, chronology = do_individual_turn(player, floor, player, list_of_animations, chronology, prevtechnique)
    player.turns_left_before_moving += -1

    #for all enemies
        #if they have a higher speed than you, do 2 turns
        #if equal speed, do turn
        #if lower speed & 'turns left' 


    for enemy in all_enemies:
        if enemy.speed > player.speed: #double speed
            if enemy.should_be_deleted != True: #if enemy isnt already dead...
                enemy.technique, enemy.techniquex, enemy.techniquey = enemy.do_AI(all_enemies, player, floor)
                prevtechnique, chronology = do_individual_turn(enemy, floor, player, list_of_animations, chronology, prevtechnique)
            if enemy.should_be_deleted != True: #if enemy isnt already dead...
                enemy.technique, enemy.techniquex, enemy.techniquey = enemy.do_AI(all_enemies, player, floor)
                prevtechnique, chronology = do_individual_turn(enemy, floor, player, list_of_animations, chronology, prevtechnique)
                if player.turns_left_before_moving == 0:
                    refresh_entity_states(enemy)
        elif enemy.speed == player.speed: #normal speed
            if enemy.should_be_deleted != True: #if enemy isnt already dead...
                enemy.technique, enemy.techniquex, enemy.techniquey = enemy.do_AI(all_enemies, player, floor)
                prevtechnique, chronology = do_individual_turn(enemy, floor, player, list_of_animations, chronology, prevtechnique)
                if player.turns_left_before_moving == 0:
                    refresh_entity_states(enemy)
        else: #1/2 speed
            if player.turns_left_before_moving == 0:
                if enemy.should_be_deleted != True: #if enemy isnt already dead...
                    enemy.technique, enemy.techniquex, enemy.techniquey = enemy.do_AI(all_enemies, player, floor)
                    prevtechnique, chronology = do_individual_turn(enemy, floor, player, list_of_animations, chronology, prevtechnique)
                    refresh_entity_states(enemy)

    if player.turns_left_before_moving == 0:
        player.turns_left_before_moving = player.speed
        player.speed_turns += -(player.speed/2)
        player.paralysis_turns += -(player.speed/2)
        player.flee_ai_turns += -(player.speed/2)
        player.rage_ai_turns += -(player.speed/2)
        if player.speed_turns < 1:
            player.speed = player.default_speed
        player.speed_visual = player.speed
        player.paralysis_visual = player.paralysis_turns

        
    return list_of_animations


def spawn_enemies_within_turn_execution(enemies_to_summon, enemy_name, enemy_level, entity, floor, player, chronology, list_of_animations):
    locs = [(1, 0), (1, 1), (0, 1), (1, -1), (-1, 1), (-1, -1), (-1, 0), (0, -1)]
    random.shuffle(locs)
    for loc in locs:
        if can_move_to_but_not_a_cancerous_growth_on_society(entity.x + loc[0], entity.y+loc[1], floor, player) == True and random.uniform(0, 1) < 0.75:
            x, y = loc[0] + entity.x, loc[1] + entity.y
            #choose a random enemy out of the enemy name & level options for this floor
            if enemy_name == None:
                rng_enemy = random.randint(0, len(floor.enemy_list)-1)
                enemy_name = floor.enemy_list[rng_enemy]
            
            if enemy_level == None:
                if isinstance(entity, Enemy) == False:
                    enemy_level = min(floor.level_list[rng_enemy] + round(random.uniform(0, 0.7)), 4)
                else:
                    enemy_level = min(entity.level + round(random.uniform(0, 0.7)), 4)
            #floor.valid_entity_tiles.remove((y, x)) this is suspect. maybe we shouldnt be using this at all
            
            test_enemy = generate_enemy(enemy_name, enemy_level, x, y, enemy_grid_to_use(enemy_level), floor)
            test_enemy.paralysis_turns = 1
            test_enemy.invisible_frames = chronology

            floor.all_enemies.append(test_enemy)

            list_of_animations.append(animations.Animation(1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(test_enemy, player, 1, 16), test_enemy.x, test_enemy.y, test_enemy.x, test_enemy.y, 0, None, None, None, None, None))

            enemies_to_summon += -1
            if enemies_to_summon == 0:
                break

            

















