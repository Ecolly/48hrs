
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
            if enemy.technique == Technique.MOVE and enemy.techniquefinished == 0 and enemy.techniquex == x and enemy.techniquey == y and enemy.should_be_deleted == False:#x == enemy.x and y == enemy.y:
                return False
            elif enemy.x == x and enemy.y == y and enemy.should_be_deleted == False:
                return False
        if player.x == x and player.y == y:
            return False
        return True



#for all entities, starting from player...
    #check AI (for player, this is already present)
    #do turn

def check_if_entity_is_on_screen(entity, player, result1, result2):
    if entity == None:
        return result1
    
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
        # print(f"Invalid tile cannot move{x, y}")
        return False
    else:
        for enemy in game_map.all_enemies:
            if enemy.x == x and enemy.y == y and enemy.should_be_deleted == False:
                return False
        if player.x == x and player.y == y:
            return False
        return True



def inflict_damage(attacker, target, player, chronology, list_of_animations, item, damage, damage_type, floor):
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
        elif isinstance(item, Miscellanious) == True and item.name == "Rock":
            damage += 10

        if target.equipment_shield != None:
            damage -= target.equipment_shield.defense
        damage -= target.defense
        if damage_type == "recoil":
            damage = math.floor(damage / 8)
        if damage < 1:
            damage = 1
    elif damage_type == "magic" or damage_type == "execution": #smoke
        if target.equipment_shield != None and target.equipment_shield.name == "Sun Shield":
            damage = math.ceil(damage/2)
        anim = animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(target, player, 1, 16), target.x, target.y, target.x, target.y, 0, None, None, None, None, None)
        list_of_animations.append(anim)
        pass
    
    target.health = target.health - damage
    #target.paralysis_turns = 0 #paralysis turns should be set to 0 if taking damage?

    if damage_type == "chemical":
        #damage number
        anim = animations.Animation(str(target.name) + " took " + str(damage) + " damage from " + str(attacker) + "." ,"-" + str(damage), 2, 0, (255, 0, 0, 0), chronology, check_if_entity_is_on_screen(target, player, 1, 50), target.x, target.y+0.5, target.x, target.y, 0, None, None, attacker, target, damage, defense_reduction=defense_reduction, strength_reduction=strength_reduction)
        list_of_animations.append(anim)
    else:
        #damage number
        anim = animations.Animation(str(target.name) + " took " + str(damage) + " damage from " + str(attacker.name) + "." ,"-" + str(damage), 2, 0, (255, 0, 0, 0), chronology, check_if_entity_is_on_screen(target, player, 1, 50), target.x, target.y+0.5, target.x, target.y, 0, None, None, attacker, target, damage, defense_reduction=defense_reduction, strength_reduction=strength_reduction)
        list_of_animations.append(anim)

    if target != player and not target.is_alive():
        if target.name == "CULTIST" and target.level > 2 and target.has_been_resurrected == 0 and random.uniform(0, 1) < 0.5:
            list_of_animations.append(animations.Animation(str(target.name) + " was resurrected by Tome of Resurrection!" ,23, 6, 1, (255, 0, 0, 0), chronology+2, check_if_entity_is_on_screen(target, player, 2, 50), target.x, target.y+0.5, target.x, target.y, 0, None, None, None, None, None))
            target.health = target.maxhealth 
            target.speed = 2 
            target.paralysis_turns = 0
            target.has_been_resurrected = 1
        else:
            target.should_be_deleted = True
            if player.extinction_state == 1 and (target.name in player.enemies_remaining): #if enemies previously went extinct, then the only remaining enemies should be enemies on this floor. if none remain, make them extinct again.
                allenemiesdeadflag = True 

                for enemy in floor.all_enemies:
                    if enemy.name == target.name and enemy.health > 0:
                        allenemiesdeadflag = False 

                if allenemiesdeadflag == True and target.name != "HAMSTER" and target.creaturetype != "Human": #if that was the last kind of this enemy on the floor, remove from the list
                    print(player.enemies_remaining)
                    print(target.name)
                    player.enemies_remaining.remove(target.name)
                    list_of_animations.append(animations.Animation(str(target.name) + " went extinct!" ,23, 6, 1, (255, 0, 0, 0), chronology+2, check_if_entity_is_on_screen(target, player, 2, 50), target.x, target.y+0.5, target.x, target.y, 0, None, None, None, None, None))

                if len(player.enemies_remaining) == 0:
                    list_of_animations.append(animations.Animation("All enemies cleared! Victory!", 0*29 + 24, 8, 4, (255, 255, 255, 0), chronology+3, 16, player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            
            if attacker == player:
                temp_level = attacker.level
                attacker.increase_experience(target.experience*exp_multiplier)
                if attacker.level != temp_level:
                    list_of_animations.append(animations.Animation(str(attacker.name) + " grew to level " + str(attacker.level) + "!", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(attacker, player, 1, 16), attacker.x, attacker.y, attacker.x, attacker.y, 0, None, None, None, None, None))
                elif isinstance(attacker, Enemy):
                    attacker.level_up()
                    list_of_animations.append(animations.Animation(str(attacker.name) + " leveled up!", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(attacker, player, 1, 16), attacker.x, attacker.y, attacker.x, attacker.y, 0, None, None, None, None, None))







def inflict_healing(amount, entity, player, list_of_animations, chronology):
    if (entity.health + amount > entity.maxhealth):
        amount = entity.maxhealth - entity.health
    amount = math.floor(amount)
    entity.health += amount
    if amount > 0:
        anim = animations.Animation(str(entity.name) + " recovered " + str(amount) + " HP.", "+" + str(amount), 2, 0, (0, 189, 66, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 50), entity.x, entity.y+0.5, entity.x, entity.y, 0, None, None, entity, entity, -amount)
        list_of_animations.append(anim)



def deduct_charges(entity, charges, floor):
    if entity.techniqueitem != None:
        entity.techniqueitem.charges -= charges
        entity.techniqueitem.price -= charges
        if entity.techniqueitem.charges < 1:
            if isinstance(entity.techniqueitem, Staff) and entity.name == "DAMIEN":
                blank_id = entity.inventory.index(entity.techniqueitem)
                objlist = entity.inventory
                objlist[blank_id].sprite.delete() 
                objlist[blank_id].hotbar_sprite.delete() 
                objlist[blank_id] = floor.create_item("Stick", objlist[blank_id].grid)
            else:
                entity.techniqueitem.should_be_deleted = True


def do_spell(floor, entity, enemy_hit, player, spellname, charges, chronology, list_of_animations):
    if "Flask" in spellname:
        #print(entity.techniquecharges)
        entity.techniqueitem.charges -= charges 
        entity.techniqueitem.price -= charges
        if entity.techniqueitem.charges < 1 and entity == player:
            blank_id = player.inventory.index(entity.techniqueitem)
            objlist = player.inventory
            objlist[blank_id].sprite.delete() 
            objlist[blank_id].hotbar_sprite.delete() 
            objlist[blank_id] = floor.create_item("Empty Flask", objlist[blank_id].grid)


        pass
    #alchemy, gardening do nothing in this section
    if spellname == "Staff of Cloning":
        if enemy_hit != None:
            spawn_enemies_within_turn_execution(1, enemy_hit.name, enemy_hit.level, enemy_hit, floor, player, chronology, list_of_animations)
            deduct_charges(entity, 1, floor)
    if spellname == "Staff of Metamorphosis":
        if enemy_hit != None:
            enemy_hit.should_be_deleted = True 
            name_to_spawn = random.choice(["LEAFALOTTA", "CHLOROSPORE", "GOOSE", "FOX", "S'MORE", "DRAGON", "CHROME DOME", "TETRAHEDRON", "SCORPION", "TURTLE", "CULTIST", "JUJUBE", "DEMON CORE", "VITRIOLIVE", "MONITAUR", "DODECAHEDRON"])
            level_to_spawn = random.randint(1, 4)
            spawn_enemies_within_turn_execution(1, name_to_spawn, level_to_spawn, enemy_hit, floor, player, chronology, list_of_animations)
            
            #spawn_enemies_within_turn_execution(1, enemy_hit.name, enemy_hit.level, enemy_hit, floor, player, chronology, list_of_animations)
            deduct_charges(entity, 1, floor)
    if spellname == "Greater Healing Staff":
        if enemy_hit != None:
            inflict_healing(enemy_hit.health/2, enemy_hit, player, list_of_animations, chronology)
            list_of_animations.append(animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges, floor)
    if spellname == "Lesser Healing Staff":
        if enemy_hit != None:
            inflict_healing(charges*2, enemy_hit, player, list_of_animations, chronology)
            list_of_animations.append(animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges, floor)
    if spellname == "Staff of Division":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, math.floor(enemy_hit.health/2), "magic", floor)
        deduct_charges(entity, charges, floor)
    if spellname == "Staff of Swapping":
        if enemy_hit != None:
            x, y = enemy_hit.x, enemy_hit.y
            enemy_hit.x, enemy_hit.y = entity.x, entity.y
            entity.x, entity.y = x, y
            list_of_animations.append(animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
            list_of_animations.append(animations.Animation(str(enemy_hit.name) + " swapped places with " + str(entity.name) + ".", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))

        deduct_charges(entity, charges, floor)
    if spellname == "Staff of Warping":
        if enemy_hit != None:
            i = 0
            while i < 100:
                y, x = random.choice(floor.valid_tiles)
                if enemy_hit.can_move_to(x, y, floor) == True:
                    enemy_hit.x, enemy_hit.y = x, y
                    list_of_animations.append(animations.Animation(str(enemy_hit.name) + " was teleported.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
                    break
                i = i + 1
        deduct_charges(entity, charges, floor)
    elif spellname == "Staff of Mana":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, charges*2, "magic", floor) #random.randint(charges, charges*3)
        deduct_charges(entity, charges, floor)
    elif spellname == "Staff of Primes":
        if enemy_hit != None:
            primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271]
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, primes[charges-1], "magic", floor) #random.randint(charges, charges*3)
        deduct_charges(entity, charges, floor)
    elif spellname == "Fibonnaci Staff":
        if enemy_hit != None:
            primes = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393, 196418, 317811, 514229, 832040, 1346269, 2178309, 3524578, 5702887, 9227465, 14930352, 24157817, 39088169, 63245986, 102334155]
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, primes[charges-1], "magic", floor) #random.randint(charges, charges*3)
        deduct_charges(entity, charges, floor)
    elif spellname == "Mirror Staff": #if mirror staff has nothing to copy, just copy player's strength
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, entity.strength, "magic", floor)
        deduct_charges(entity, charges, floor)
    elif spellname == "Staff of Ricochet" or spellname == "Piercing Staff" or spellname == "Staff of Alchemy" or spellname == "Gardening Staff":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 3, "magic", floor)
        deduct_charges(entity, charges, floor)
    elif spellname == "Execution Staff":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, charges, "execution", floor)
        deduct_charges(entity, charges, floor)
    elif spellname == "Staff of Lethargy":
        if enemy_hit != None:
            enemy_hit.speed = 1
            enemy_hit.speed_turns = charges
            list_of_animations.append(animations.Animation(str(enemy_hit.name) + " was slowed down.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges, floor)
    elif spellname == "Energizing Staff":
        if enemy_hit != None:
            enemy_hit.speed = 4
            enemy_hit.speed_turns = charges
            list_of_animations.append(animations.Animation(str(enemy_hit.name) + " was sped up.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges, floor)
    elif spellname == "Staff of Paralysis": #paralysis
        if enemy_hit != None:
            enemy_hit.paralysis_turns = charges
            list_of_animations.append(animations.Animation(str(enemy_hit.name) + " was paralyzed.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges, floor)
    elif spellname == "Staff of Violence": #rage
        if enemy_hit != None:
            enemy_hit.rage_ai_turns = charges
            list_of_animations.append(animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges, floor)
    elif spellname == "Phobia Staff": #fear
        if enemy_hit != None:
            enemy_hit.flee_ai_turns = charges
            list_of_animations.append(animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
        deduct_charges(entity, charges, floor)
    elif spellname == "Spores": #damage
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 1, "magic", floor)
            list_of_animations.append(animations.Animation("", 1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Spores 2": #decrease attack
        if enemy_hit != None:
            enemy_hit.strength = max(enemy_hit.strength-1, 1)
            enemy_hit.defense = max(enemy_hit.defense-1, 1)
            #anim goes here?
            list_of_animations.append(animations.Animation(str(enemy_hit.name) + "'s strength and defense dropped by 1!", 1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Spores 3": #slow
        if enemy_hit != None:
            enemy_hit.speed = 1
            enemy_hit.speed_turns = 6
            list_of_animations.append(animations.Animation(str(enemy_hit.name) + " was slowed down.", 1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Spores 4": #paralysis
        if enemy_hit != None:
            enemy_hit.paralysis_turns = 3
            list_of_animations.append(animations.Animation(str(enemy_hit.name) + " was paralyzed.", 1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy_hit, player, 1, 16), enemy_hit.x, enemy_hit.y, enemy_hit.x, enemy_hit.y, 0, None, None, None, None, None))
    elif spellname == "Dragon Fire":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 10, "magic", floor)
    elif spellname == "Dragon Fire 2":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 20, "magic", floor)
    elif spellname == "Dragon Fire 3":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 30, "magic", floor)
    elif spellname == "Dragon Fire 4":
        if enemy_hit != None:
            inflict_damage(entity, enemy_hit, player, chronology, list_of_animations, None, 40, "magic", floor)

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
    
    







def do_liquid_effect(entity, player, chronology, list_of_animations, floor):
    liq = floor.liquid_grid[floor.height-1-entity.y][entity.x]
    if liq == "#":
        return False
    elif liq == "W": #water
        spr = 2*29 + 16
        evap = 0.05
        
        if entity.creaturetype == "Plant":
            inflict_healing(random.randint(1, 3), entity, player, list_of_animations, chronology)
        
        if entity.strength != entity.maxstrength:
            entity.strength = entity.maxstrength
            list_of_animations.append(animations.Animation(str(entity.name) + "'s strength was restored!", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))  
        if entity.defense != entity.maxdefense:
            list_of_animations.append(animations.Animation(str(entity.name) + "'s defense was restored!", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))  
            entity.defense = entity.maxdefense

    elif liq == "D": #detergent
        spr = 2*29 + 12
        evap = 0.4
        if isinstance(entity.techniqueitem, Tome) == True:
            objlist = player.inventory
            i = 0
            for item in objlist:
                if item == entity.techniqueitem:
                    objlist[i].sprite.delete() 
                    objlist[i].hotbar_sprite.delete() 
                    objlist[i] = floor.create_item("Blank Tome", objlist[i].grid)
                i = i + 1
        if entity.creaturetype == "Abstract":
            inflict_damage("Detergent", entity, player, chronology, list_of_animations, None, random.randint(25, 45), "chemical", floor)
    elif liq == "A": #acid
        spr = 2*29 + 0
        evap = 0.33
        if entity.name != "VITRIOLIVE":
            inflict_damage("Acid", entity, player, chronology, list_of_animations, None, 1, "chemical", floor)
    elif liq == "M": #mercury (should slow creatures down)
        spr = 2*29 + 24
        evap = 0.05
        if entity.creaturetype == "Robotic":
            inflict_damage("Mercury", entity, player, chronology, list_of_animations, None, random.randint(25, 45), "chemical", floor)
    elif liq == "S": #syrup (should slow creatures down)
        spr = 2*29 + 4
        evap = 0.05
        if entity.creaturetype == "Food":
            inflict_healing(random.randint(1, 3), entity, player, list_of_animations, chronology)
        else:
            entity.speed = 1
            entity.speed_turns = 3
            list_of_animations.append(animations.Animation(str(entity.name) + " was slowed down.", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))  
    
    elif liq == "C": #cureall (paralyzes)
        spr = 2*29 + 8
        evap = 0.2
        inflict_healing(random.randint(2, 4), entity, player, list_of_animations, chronology)
        entity.paralysis_turns = 3
        list_of_animations.append(animations.Animation(str(entity.name) + " was paralyzed.", 1*29 + 8, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))
    elif liq == "P": #petroleum (should slow creatures down)
        spr = 2*29 + 20
        evap = 0.05
        if entity.creaturetype == "Robotic":
            inflict_healing(random.randint(1, 3), entity, player, list_of_animations, chronology)
        else:
            entity.speed = 1
            entity.speed_turns = 3
            list_of_animations.append(animations.Animation(str(entity.name) + " was slowed down.", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))  
    elif liq == "I": #ink
        spr = 2*29 + 20
        evap = 0.05

        if isinstance(entity, Enemy) == True:
            self.is_inked = True
            list_of_animations.append(animations.Animation(str(entity.name) + "stepped in Ink! Their tomes are now unreadable.", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))  

        if isinstance(entity.techniqueitem, Tome) == True:
            objlist = player.inventory
            i = 0
            for item in objlist:
                if item == entity.techniqueitem:
                    objlist[i].sprite.delete() 
                    objlist[i].hotbar_sprite.delete() 
                    objlist[i] = floor.create_item("Ruined Tome", objlist[i].grid)
                i = i + 1

        if entity.creaturetype == "Abstract":
            inflict_healing(random.randint(1, 3), entity, player, list_of_animations, chronology)
    else:
        return False
    
    if random.uniform(0, 1) < evap and entity.name != "VITRIOLIVE":
        x, y = entity.x, entity.y
        if ((x > player.x + 13 or x < player.x - 13) or (y > player.y + 9 or y < player.y - 9)):
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology, 1, x, y, x, y, "E", None, None, None, None, 0, None))
        else:
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology, 8, x, y, x, y, "E", None, None, None, None, 0, None))
        floor.liquid_grid[floor.height-1-y][x] = "#"
    return True



def pick_up_liquid(x, y, item, floor, chronology, list_of_animations, chron_i, player):
    liq = floor.liquid_grid[floor.height-1-y][x]
    if liq == "W":
        spr = 2*29 + 16
        liqname = "Water Flask"
    elif liq == "D":
        spr = 2*29 + 12
        liqname = "Detergent Flask"
    elif liq == "A":
        spr = 2*29 + 0
        liqname = "Acid Flask"
    elif liq == "M":
        spr = 2*29 + 24
        liqname = "Mercury Flask"
    elif liq == "S":
        spr = 2*29 + 4
        liqname = "Syrup Flask"
    elif liq == "C":
        spr = 2*29 + 8
        liqname = "Cureall Flask"
    elif liq == "P":
        spr = 2*29 + 20
        liqname = "Petroleum Flask"
    else:
        spr = 2*29 + 20
        liqname = "Ink Flask"

    if liq == item.name[0] and item.charges < item.maxcharges:
        item.charges += 1
        item.price += 1

        if ((x > player.x + 13 or x < player.x - 13) or (y > player.y + 9 or y < player.y - 9)):
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology+chron_i, 1, x, y, x, y, "E", None, None, None, None, 0, None))
        else:
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology+chron_i, 8, x, y, x, y, "E", None, None, None, None, 0, None))
        floor.liquid_grid[floor.height-1-y][x] = "#"
        return True 
    elif liq != "#" and item.name == "Empty Flask":

            
        blank_id = player.inventory.index(item)
        objlist = player.inventory
        objlist[blank_id].sprite.delete() 
        objlist[blank_id].hotbar_sprite.delete() 
        objlist[blank_id] = floor.create_item(liqname, objlist[blank_id].grid)
        objlist[blank_id].price = objlist[blank_id].price - objlist[blank_id].charges + 1
        objlist[blank_id].charges = 1
        if ((x > player.x + 13 or x < player.x - 13) or (y > player.y + 9 or y < player.y - 9)):
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology+chron_i, 1, x, y, x, y, "E", None, None, None, None, 0, None))
        else:
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology+chron_i, 8, x, y, x, y, "E", None, None, None, None, 0, None))
        floor.liquid_grid[floor.height-1-y][x] = "#"
        return True 
    
    return False



def deposit_liquid(x, y, item, floor, chronology, list_of_animations, chron_i, player):

    if ((y, x) in floor.valid_tiles) and floor.check_liquid_at_tile(x, y) != item:
        floor.liquid_grid[floor.height-1-y][x] = item
        #if splashing a flask...
        if item == "W":
            spr = 2*29 + 16
        elif item == "D":
            spr = 2*29 + 12
        elif item == "A":
            #reduce shield and weapon str by 1
            spr = 2*29 
        elif item == "M":
            #destroy metal equipment?
            spr = 2*29 + 24
        elif item == "S":
            spr = 2*29 + 4
        elif item == "C":
            spr = 2*29 + 8
        elif item == "P":
            spr = 2*29 + 20
        elif item == "I":
            #ruin tomes
            spr = 2*29 + 20
        
        if ((x > player.x + 13 or x < player.x - 13) or (y > player.y + 9 or y < player.y - 9)):
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology+chron_i, 1, x, y, x, y, item, None, None, None, None, 0, None))
        else:
            list_of_animations.append(animations.Animation("", spr, 7, 5, (255, 255, 255, 0), chronology+chron_i, 8, x, y, x, y, item, None, None, None, None, 0, None))
        return True 
    
    return False



        # entity.techniqueitem.price -= charges
        # if entity.techniqueitem.charges < 1 and entity == player:
        #     blank_id = player.inventory.index(entity.techniqueitem)
        #     objlist = player.inventory
        #     objlist[blank_id].sprite.delete() 
        #     objlist[blank_id].hotbar_sprite.delete() 
        #     objlist[blank_id] = floor.create_item("Empty Flask", objlist[blank_id].grid)

def shatter_flask(x, y, item, floor, chronology, list_of_animations, chron_i, player):



    coordanites_0 = [(0, 0)]
    coordanites_1 = [(0, 1), (1, 0), (0, -1), (-1, 0), (-1, -1), (1, 1), (-1, 1), (1, -1)]
    coordanites_2 = [(2, 0), (0, 2), (-2, 0), (0, -2), (2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (-1, 2), (1, -2), (-1, -2), (2, 2), (2, -2), (-2, 2), (-2, -2)]

    random.shuffle(coordanites_1) 
    random.shuffle(coordanites_2)
    coordanites = [coordanites_0, coordanites_1, coordanites_2]

    num_of_liq_to_deposit = item.charges
    coordlist = 0
    coordentry = 0
    while num_of_liq_to_deposit > 0 and coordlist < 3:
        xtochk = x + coordanites[coordlist][coordentry][0]
        ytochk = y + coordanites[coordlist][coordentry][1]
        coordentry += 1
        if coordentry >= len(coordanites[coordlist]):
            coordlist += 1

        if deposit_liquid(xtochk, ytochk, item.liquid[0], floor, chronology, list_of_animations, chron_i, player) == True:
            num_of_liq_to_deposit += -1



    #1. find tiles around the target to deposit liquid
    #2. deposit liquid
    pass










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
        item.xend = math.floor(tilex + (abs(tilex - item.xend) + 30*abs(distance_x_normalized))*math.copysign(1, item.xinit - item.xend))
        item.yend = math.floor(tiley + (abs(item.yend - tiley) + 30*abs(distance_y_normalized))*math.copysign(1, item.yend - item.yinit))
    elif reflection_result == "y":
        item.yend = math.floor(tiley + (abs(tiley - item.yend) + 30*abs(distance_y_normalized))*math.copysign(1, item.yinit - item.yend))
        item.xend = math.floor(tilex + (abs(item.xend - tilex) + 30*abs(distance_x_normalized))*math.copysign(1, item.xend - item.xinit))
    projectiles_remaining += 1

    if isinstance(item, Projectile) == True:
        entity.active_projectiles.append(Projectile(item.name, 0, tilex, tiley, item.xend, item.yend, entity, "", chron_i))
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
        if dist != 0:
            damage = math.floor(((entity.level + 3)**2)/(dist*dist))
            if damage > 0:
                inflict_damage(entity, enemy, player, chronology, list_of_animations, None, damage, "magic", floor)
            for enemy in floor.all_enemies:
                if enemy.name != "DEMON CORE":
                    dist = math.sqrt((enemy.x - entity.x)**2 + (enemy.y - entity.y)**2)
                    damage = math.floor(((entity.level + 3)**2)/(dist*dist))
                    if damage > 0:
                        inflict_damage(entity, enemy, player, chronology, list_of_animations, None, damage, "magic", floor)
    




def do_individual_turn(entity, floor, player, list_of_animations, chronology, prevtechnique):
    global fakenames_staffs_key, fakenames_tomes_key, fakenames_staffs_realnames, fakenames_tomes_realnames, grid_items
    do_radioactivity(entity, player, chronology, list_of_animations, floor)
    if entity.technique == Technique.STILL:
        do_liquid_effect(entity, player, chronology, list_of_animations, floor)
        return Technique.STILL, chronology
    elif entity.technique == Technique.MOVE:
        print("Moving to AFTER MOVE", entity.techniquex, entity.techniquey, "from", entity.x, entity.y)
        if can_move_to(entity.techniquex, entity.techniquey, floor, player):
            print("Moving to", entity.techniquex, entity.techniquey, "from", entity.x, entity.y)
            pass

        elif can_move_to(entity.techniquex, entity.y, floor, player):
            entity.techniquey = entity.y 
        elif can_move_to(entity.x, entity.techniquey, floor, player):
            entity.techniquex = entity.x
        else:
            # if isinstance(entity, Enemy):
            #     # dist = math.sqrt((entity.x-player.x)**2 + (entity.y-player.y)**2)
            #     # dist2 = math.sqrt((entity.x-player.x)**2 + ((entity.y + entity.y-entity.techniquey))-player.y)**2)
            #     # dist3 = math.sqrt(((entity.x + entity.x - entity.techniquex))-player.x)**2 + (entity.y-player.y)**2)
            #     if can_move_to(entity.x, entity.y + entity.y-entity.techniquey, floor, player):
            #         entity.techniquey = entity.y + entity.y-entity.techniquey
            #     elif can_move_to(entity.x + entity.x - entity.techniquex, entity.y, floor, player):
            #         entity.techniquex = entity.x + entity.x - entity.techniquex
            #     else:
            #         entity.techniquex = entity.x 
            #         entity.techniquey = entity.y 
            # else:
                entity.techniquex = entity.x 
                entity.techniquey = entity.y

        rot = adjust_rotation(entity, entity.techniquex-entity.x, entity.techniquey-entity.y)
        list_of_animations.append(animations.Animation("", None, 0, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 8), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.MOVE, None, None, None))
        print("Moving to but in individual turn just kill me already", entity.techniquex, entity.techniquey, "from", entity.prevx, entity.prevy)

        if isinstance(entity.techniqueitem, Flask):
            pick_up_liquid(entity.techniquex, entity.techniquey, entity.techniqueitem, floor, chronology, list_of_animations, 0, player)
        elif entity.name == "VITRIOLIVE":
            deposit_liquid(entity.techniquex, entity.techniquey, "A", floor, chronology, list_of_animations, 0, player)

        #if previous technique was not 'move' or 'still', chronology must be incremented by 8
        if prevtechnique != Technique.MOVE and prevtechnique != Technique.STILL:
            chronology += check_if_entity_is_on_screen(entity, player, 1, 8)

        entity.x = entity.techniquex
        entity.y = entity.techniquey
        do_liquid_effect(entity, player, chronology, list_of_animations, floor)
        return Technique.MOVE, chronology
    elif entity.technique == Technique.CONSUME:
        if prevtechnique == Technique.MOVE or prevtechnique == Technique.STILL:
            chronology += check_if_entity_is_on_screen(entity, player, 1, 8)
        entity.consume_item(entity.techniqueitem, list_of_animations)
        chronology += 10
        do_liquid_effect(entity, player, chronology, list_of_animations, floor)
        return Technique.CONSUME, chronology
    elif entity.technique == Technique.HIT:
        if prevtechnique == Technique.MOVE or prevtechnique == Technique.STILL:
            chronology += check_if_entity_is_on_screen(entity, player, 1, 8)
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
                inflict_damage(entity, target, player, chronology+check_if_entity_is_on_screen(entity, player, 1, 16), list_of_animations, entity.equipment_weapon, 0, "physical", floor)
                if target.equipment_shield != None and target.equipment_shield.name == "Spiked Shield":
                    inflict_damage(entity, entity, player, chronology+check_if_entity_is_on_screen(entity, player, 1, 16), list_of_animations, entity.equipment_weapon, 0, "recoil", floor)
                if target.name == "JUJUBE" and random.uniform(0, 1) < 0.3:
                    spawn_enemies_within_turn_execution(1, "JUJUBE", target.level, target, floor, player, chronology + check_if_entity_is_on_screen(entity, player, 1, 16), list_of_animations)





            



        list_of_animations.append(animations.Animation("", None, 1, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.HIT, None, None, None))
        chronology += check_if_entity_is_on_screen(entity, player, 1, 16)
        do_liquid_effect(entity, player, chronology, list_of_animations, floor)
        return Technique.HIT, chronology
    elif entity.technique == Technique.THROW: #works for throwing items, casting projectile spells, and other projectiles
        #print(entity.x, entity.y, entity.techniquex, entity.techniquey)
        if prevtechnique == Technique.MOVE or prevtechnique == Technique.STILL:
            chronology += check_if_entity_is_on_screen(entity, player, 1, 8)
        rot = adjust_rotation(entity, clamp(-entity.x+entity.techniquex, -1, 1), clamp(-entity.y+entity.techniquey, -1, 1))

        if entity.techniqueitem != None and isinstance(entity.techniqueitem, Staff) == True:
            anim2 = animations.Animation("", None, 1, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.HIT, None, None, None, item=entity.techniqueitem.spriteindex)
        else:
            anim2 = animations.Animation("", None, 1, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.techniquex, entity.techniquey, rot, entity, Technique.HIT, None, None, None)
        
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
                        if chron_i == 1:
                            list_of_animations.append(animations.Animation(item.text, 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))
                    else:
                        animtype = 3
                        if chron_i == 1:
                            name_desc = get_display_name(item)
                            list_of_animations.append(animations.Animation(str(entity.name) + " threw the " + name_desc + "!", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))

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
                        list_of_animations.append(animations.Animation("", 29*2, 6, 5, (255, 255, 255, 0), chronology+chron_i, 5, tilex, tiley, tilex, tiley, rot, None, None, None, None, 0, None))




                    used_up_flag = False

                    if ("Flask" in item.name or item.name == "Gardening Staff" or item.name == "Staff of Alchemy") and isinstance(item, Projectile) and (tilex != math.floor(item.x - distance_x_normalized) or tiley != math.floor(item.y - distance_y_normalized)):
                        if item.name == "Staff of Alchemy":
                            liq = floor.liquid_grid[floor.height-1-tiley][tilex]
                            if liq != "#":
                                liq = random.choice(["W", "D", "P", "M", "A", "I", "S", "C"])
                        elif item.name == "Gardening Staff":
                            liq = "W"
                        else:
                            liq = item.name[0]

                        if liq != "E" and deposit_liquid(tilex, tiley, liq, floor, chronology, list_of_animations, chron_i, player) == True and "Flask" in item.name:
                            #print("frfr", entity.techniquecharges)
                            item.damage += -1
                            entity.techniquecharges += 1
                        if item.damage == 0:
                            used_up_flag = True

                    # if item.name == "Staff of Alchemy" and isinstance(item, Projectile) and (tilex != math.floor(item.x - distance_x_normalized) or tiley != math.floor(item.y - distance_y_normalized)):
                    #     if deposit_liquid(tilex, tiley, item.name[0], floor, chronology, list_of_animations, chron_i, player) == True:
                    #         item.damage += -1
                    #         entity.techniquecharges += 1
                    #     if item.damage == 0:
                    #         used_up_flag = True


                        #list_of_animations.append(animations.Animation("", spr, 6, 5, (255, 255, 255, 0), chronology+chron_i, 5, tilex, tiley, tilex, tiley, rot, None, None, None, None, 0, None))
                        
                        #place a liquid tile here
                        #subtract 1 from remaining charges
                        #if 0, terminate projectile






                    enemy_hit = None
                    if (player != item.entity or item.friendly_fire == True) and tilex == player.x and tiley == player.y: #if hit the player and player isnt the source entity
                        enemy_hit = player
                    else:
                        for enemy in floor.all_enemies:
                            if (enemy != item.entity or item.friendly_fire == True) and enemy.x == math.floor(item.x) and enemy.y == math.floor(item.y) and entity.should_be_deleted == False: #if hit an enemy and enemy isnt the source entity
                                enemy_hit = enemy
                    
                    if enemy_hit == None or used_up_flag == True: #if no creature was hit
                        
                        if used_up_flag == False and (floor.wall_type == "Solid" and ((tiley,tilex) not in floor.valid_tiles)): #if a wall is hit...
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

                            anim3 = animations.Animation("", item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item, drop_item=True)
                            list_of_animations.append(anim3)
                            entity.active_projectiles[itemi] = -1
                            projectiles_remaining += -1
                        else:
                            #if nothing was hit OR used_up_flag == true
                            distance_travelled = math.sqrt(abs(tilex - entity.x)**2 + abs(tiley - entity.y)**2)
                            if distance_travelled > distance_total or used_up_flag == True:
                                if isinstance(item, Flask) == True:
                                    shatter_flask(tilex, tiley, item, floor, chronology, list_of_animations, chron_i, player)
                                    list_of_animations.append(animations.Animation("", item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item, drop_item=False))
                                else:
                                    list_of_animations.append(animations.Animation("", item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, None, 0, item, drop_item=True))

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
                        
                            anim3 = animations.Animation("", item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, enemy_hit, 0, item)
                            list_of_animations.append(anim3)
                            entity.active_projectiles[itemi] = -1
                            projectiles_remaining += -1
                        else:
                            if isinstance(item, Projectile) == True:
                                do_spell(floor, entity, enemy_hit, player, item.name, entity.techniquecharges, chronology+chron_i, list_of_animations)
                            else:
                                inflict_damage(entity, enemy_hit, player, chronology+chron_i, list_of_animations, item, 0, "physical", floor)
                            #if the projectile is piercing and didn't bounce, don't delete it and instead just set its entity of origin as the entity it just hit
                            #should this be changed to pierce enemies so long as the projectile killed the enemy it's trying to pierce?
                            if item.num_of_pierces > 0:
                                item.num_of_pierces += -1
                                if enemy_hit.should_be_deleted == False:
                                    item.entity = enemy_hit
                                    item.friendly_fire = False
                            else:
                                anim3 = animations.Animation("", item.spriteindex, animtype, 5, (255, 255, 255, 0), chronology+item.chron_offset, chron_i-item.chron_offset, item.xinit, item.yinit, tilex, tiley, rot, entity, Technique.THROW, entity, enemy_hit, 0, item)
                                list_of_animations.append(anim3)
                                entity.active_projectiles[itemi] = -1
                                projectiles_remaining += -1

                
                

                itemi += 1
            chron_i += 1
        entity.active_projectiles = []

        chronology = chronology + max(chron_i, check_if_entity_is_on_screen(entity, player, 1, 16))
        do_liquid_effect(entity, player, chronology, list_of_animations, floor)
        return Technique.THROW, chronology
    elif entity.technique == Technique.CAST: #this is for static castings (not projectiles)
        if prevtechnique == Technique.MOVE or prevtechnique == Technique.STILL:
            chronology += check_if_entity_is_on_screen(entity, player, 1, 8)

        item = entity.techniqueitem

        name_desc = get_display_name(item)


        list_of_animations.append(animations.Animation(str(entity.name) + " read the " + str(name_desc) + "!", None, 5, 0, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 24), entity.x, entity.y, entity.techniquex, entity.techniquey, entity.direction, entity, Technique.CAST, None, None, None, item=[item.spriteindex, item.name]))
        chronology += 24
        #print(str(entity.name) + " read a " + str(name_desc) + "!")

        if entity == player:
            discoverstring = discover_item(item)
            if discoverstring != False:
                list_of_animations.append(animations.Animation(discoverstring, 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))

        
        # if item.name == "Blank Tome":
        #     i = 39 
        #     while i > -1:
        #         if isinstance(player.inventory[i], Tome) == True:
        #             item.name = player.inventory[i].name
        #             break
        #         i = i - 1
        if item.name == "Bankruptcy Tome":
            if player.gold < 0:
                player.credit_score = 0
            player.gold = 0 
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Pizzazz":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Item) == True:
                    player.inventory[i].price = math.ceil(player.inventory[i].price*1.5)
                    break
                i = i - 1
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Recovery":
            inflict_healing(15, player, player, list_of_animations, chronology)
            for enemy in floor.all_enemies:
                inflict_healing(15, enemy, player, list_of_animations, chronology)
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Injury":
            inflict_damage(entity, player, player, chronology, list_of_animations, item, 15, "magic", floor)
            for enemy in floor.all_enemies:
                inflict_damage(entity, enemy, player, chronology, list_of_animations, item, 15, "magic", floor)
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Extinction":

            #kill all nonhamsters
            for enemy in floor.all_enemies:
                if enemy.name != "HAMSTER" and enemy.creaturetype != "Human":
                    inflict_damage(entity, enemy, player, chronology, list_of_animations, item, 999999, "magic", floor)
                    list_of_animations.append(animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            
            #get 'remaining list' which starts with list of all non-hamster creatures 
            list_of_enemies = player.enemies_remaining

            #extinct them all
            for enemy in list_of_enemies:
                if enemy != "CULTIST" or player.extinction_state == 1:
                    list_of_animations.append(animations.Animation(enemy + " went extinct!", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, 16, player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            
            
            if player.extinction_state != 1:
                list_of_animations.append(animations.Animation("The Tome of Extinction was unable to eradicate all CULTISTs...?", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, 16, player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            
                player.extinction_state = 0.5
                player.enemies_remaining = ["CULTIST"]
            #else:
                # player.enemies_remaining = [] (this is handled by inflict_damage now)
                # #check if all enemies are dead; if they are, win
                # allenemiesdeadflag = True 
                # for enemy in floor.all_enemies:
                #     if enemy.name != "HAMSTER" and enemy.creaturetype != "Human" and enemy.health > 0:
                #         allenemiesdeadflag = False 
                #         if (enemy.name in player.enemies_remaining) == False:
                #             player.enemies_remaining.append(enemy.name)

                
                # if allenemiesdeadflag == True:
                #     list_of_animations.append(animations.Animation("All enemies cleared! Victory!", 0*29 + 24, 8, 4, (255, 255, 255, 0), chronology+3, 16, player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Resurrection":
            
            entity.has_been_resurrected = 1

            chklist = ["LEAFALOTTA", "CHLOROSPORE", "GOOSE", "FOX", "S'MORE", "DRAGON", "CHROME DOME", "TETRAHEDRON", "SCORPION", "TURTLE", "CULTIST", "JUJUBE", "DEMON CORE", "VITRIOLIVE", "DODECAHEDRON", "MONITAUR"]
            random.shuffle(chklist)
            did_resurrection = 0
            for enemy in chklist:
                if (enemy in player.enemies_remaining) == False:
                    player.enemies_remaining.append(enemy)
                    did_resurrection = 1
                    list_of_animations.append(animations.Animation(str(enemy) + "'s species was resurrected!", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, 16, player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
                    break

            if did_resurrection == 0:
                list_of_animations.append(animations.Animation("No effect- no species are currently extinct.", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, 16, player.x, player.y, player.x, player.y, 0, None, None, None, None, None))


            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Promotion":
            player.increase_experience(((player.level + 1)**3) - player.experience) 
            list_of_animations.append(animations.Animation(str(player.name) + " grew to level " + str(player.level) + "!", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(player, player, 1, 16), player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            for enemy in floor.all_enemies:
                enemy.level_up()
                list_of_animations.append(animations.Animation(str(enemy.name) + " leveled up!", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Demotion":
            player.increase_experience(((player.level - 1)**3) - player.experience) 
            list_of_animations.append(animations.Animation(str(player.name) + "'s level was reduced to " + str(player.level) + "...", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(player, player, 1, 16), player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            for enemy in floor.all_enemies:
                enemy.level_down()
                list_of_animations.append(animations.Animation(str(enemy.name) + " lost a level!", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1, floor)
        elif item.name == "Immunity Tome":
            player.defense = 100
            list_of_animations.append(animations.Animation(str(player.name) + "'s defenses skyrocketed!", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(player, player, 1, 16), player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            for enemy in floor.all_enemies:
                enemy.defense = 100
                list_of_animations.append(animations.Animation(str(enemy.name) + "'s defenses skyrocketed!", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1, floor)
        elif item.name == "Paperskin Tome":
            player.defense = -100
            list_of_animations.append(animations.Animation(str(player.name) + "'s defenses plummeted!", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(player, player, 1, 16), player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            for enemy in floor.all_enemies:
                enemy.defense = -100
                list_of_animations.append(animations.Animation(str(enemy.name) + "'s defenses plummeted!", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
            deduct_charges(entity, 1, floor)
        elif item.name == "Banishing Tome":
            for enemy in floor.all_enemies:
                if abs(enemy.x - entity.x) < 2 and abs(enemy.y - entity.y) < 2 and enemy != entity:
                    i = 0
                    while i < 100:
                        y, x = random.choice(floor.valid_tiles)
                        if enemy.can_move_to(x, y, floor) == True:
                            list_of_animations.append(animations.Animation("", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
                            enemy.x, enemy.y = x, y
                            list_of_animations.append(animations.Animation(str(enemy.name) + " was teleported.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(enemy, player, 1, 16), enemy.x, enemy.y, enemy.x, enemy.y, 0, None, None, None, None, None))
                            break
                        i = i + 1
            deduct_charges(entity, 1, floor)
        elif item.name == "Summoning Tome":
            enemies_to_summon = random.randint(3, 6)
            spawn_enemies_within_turn_execution(enemies_to_summon, None, None, entity, floor, player, chronology, list_of_animations)
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Ascendance":
            
            floor.upstairs = (player.x,player.y)

            if floor.level == -6:
                list_of_animations.append(animations.Animation("Escaped Pandorium! Victory!", 0*29 + 24, 8, 4, (255, 255, 255, 0), chronology+3, 16, player.x, player.y, player.x, player.y, 0, None, None, None, None, None))
            
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Descendance":
            floor.stairs = (player.x,player.y)
            deduct_charges(entity, 1, floor)
            
        
        elif item.name == "Tome of Obscuration":
            while len(discovered_staffs) > 0:
                discovered_staffs.pop(0)
            while len(discovered_tomes) > 0:
                discovered_tomes.pop(0)
            list_of_animations.append(animations.Animation("All Staff and Tome names were cleared.", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))
        
        elif item.name == "Tome of Identification":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Item) == True:
                    discoverstring = discover_item(player.inventory[i])
                    if discoverstring != False:
                        list_of_animations.append(animations.Animation(discoverstring, 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))
                    else:
                        list_of_animations.append(animations.Animation("The " + str(player.inventory[i].name) + " was already identified...", 0*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(entity, player, 1, 16), entity.x, entity.y, entity.x, entity.y, 0, None, None, None, None, None))
                    break
                i = i - 1
            deduct_charges(entity, 1, floor)
        elif item.name == "Sharpening Tome":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Weapon) == True:
                    player.inventory[i].bonus += 1
                    break
                i = i - 1
            deduct_charges(entity, 1, floor)
        elif item.name == "Fortifying Tome":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Shield) == True:
                    player.inventory[i].bonus += 1
                    break
                i = i - 1
            deduct_charges(entity, 1, floor)
        elif item.name == "Staffboost Tome":
            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True:
                    player.inventory[i].charges += 1
                    player.inventory[i].maxcharges += 1
                    break
                i = i - 1
            deduct_charges(entity, 1, floor)
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
            deduct_charges(entity, 1, floor)
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
        elif item.name == "Duplication Tome":
            blank_id = player.inventory.index(item)

            i = 39 
            while i > -1:
                if isinstance(player.inventory[i], Item) == True: #and player.inventory[i].name != "Blank Tome":
                    objlist = player.inventory
                    objlist[blank_id].sprite.delete() 
                    objlist[blank_id].hotbar_sprite.delete() 
                    objlist[blank_id] = floor.create_item(objlist[i].name, objlist[i].grid)
                    if isinstance(objlist[blank_id], Flask) or isinstance(objlist[blank_id], Staff):
                        objlist[blank_id].charges = objlist[i].charges 
                        objlist[blank_id].maxcharges = objlist[i].maxcharges 
                    elif isinstance(objlist[blank_id], Weapon) or isinstance(objlist[blank_id], Shield):
                        objlist[blank_id].bonus = objlist[i].bonus
                    objlist[blank_id].price = objlist[i].price

                    break
                i = i - 1
        elif item.name == "Tome of Exchange":
            equip_1_2 = []
            staffs_1_2 = []
            i = 39
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True:
                    staffs_1_2.append(i)
                    if len(staffs_1_2) == 2:
                        tempcharges = player.inventory[staffs_1_2[0]].charges
                        tempmax = player.inventory[staffs_1_2[0]].maxcharges

                        player.inventory[staffs_1_2[0]].charges = player.inventory[staffs_1_2[1]].charges
                        player.inventory[staffs_1_2[0]].maxcharges = player.inventory[staffs_1_2[1]].maxcharges

                        player.inventory[staffs_1_2[1]].charges = tempcharges
                        player.inventory[staffs_1_2[1]].maxcharges = tempmax
                        break
                if isinstance(player.inventory[i], Shield) == True or isinstance(player.inventory[i], Weapon) == True:
                    equip_1_2.append(i)
                    if len(equip_1_2) == 2:
                        tempbonus = player.inventory[equip_1_2[0]].bonus
                        player.inventory[equip_1_2[0]].bonus = player.inventory[equip_1_2[1]].bonus
                        player.inventory[equip_1_2[1]].bonus = tempbonus
                        break
                i = i - 1
            deduct_charges(entity, 1, floor)
        elif item.name == "Tome of Consolidation":
            weapons_1_2 = []
            shields_1_2 = []
            staffs_1_2 = []
            i = 39
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True:
                    staffs_1_2.append(i)
                    if len(staffs_1_2) == 2 and player.inventory[staffs_1_2[0]].name == player.inventory[staffs_1_2[1]].name:
                        player.inventory[staffs_1_2[0]].charges += player.inventory[staffs_1_2[1]].charges
                        player.inventory[staffs_1_2[0]].maxcharges += player.inventory[staffs_1_2[1]].charges
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
            deduct_charges(entity, 1, floor)
        elif item.name == "Coloring Tome":
            items_1_2 = []
            i = 39
            while i > -1:
                if isinstance(player.inventory[i], Staff) == True or (isinstance(player.inventory[i], Tome) == True and (len(items_1_2) != 1 or (player.inventory[i].name != "Blank Tome" and player.inventory[i].name != "Ruined Tome"))):
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
            deduct_charges(entity, 1, floor)

        do_liquid_effect(entity, player, chronology, list_of_animations, floor)
        return Technique.CAST, chronology
    else:
        do_liquid_effect(entity, player, chronology, list_of_animations, floor)
        return Technique.STILL, chronology

    






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
    
    print("do turn", player.techniquex, player.techniquey, player.technique)
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
                #print(chronology)
            if enemy.should_be_deleted != True: #if enemy isnt already dead...
                enemy.technique, enemy.techniquex, enemy.techniquey = enemy.do_AI(all_enemies, player, floor)
                prevtechnique, chronology = do_individual_turn(enemy, floor, player, list_of_animations, chronology, prevtechnique)
                #print(chronology)
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
    if enemy_name == "DAMIEN" or enemy_name == "DEBT COLLECTOR" or enemy_name == "EXECUTIVE":
        list_of_animations.append(animations.Animation(enemy_name + " is immune to cloning.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, 1, 0, 0, 0, 0, 0, None, None, None, None, None))
        return

    if len(player.enemies_remaining) == 0:
        return
    
    locs = [(1, 0), (1, 1), (0, 1), (1, -1), (-1, 1), (-1, -1), (-1, 0), (0, -1)]
    random.shuffle(locs)
    locs.insert(0, (0, 0))
    for loc in locs:
        if can_move_to_but_not_a_cancerous_growth_on_society(entity.x + loc[0], entity.y+loc[1], floor, player) == True and random.uniform(0, 1) < 0.75:
            x, y = loc[0] + entity.x, loc[1] + entity.y
            #choose a random enemy out of the enemy name & level options for this floor
            if enemy_name == None:
                rng_enemy = random.randint(0, len(player.enemies_remaining)-1)
                enemy_name = player.enemies_remaining[rng_enemy]
            
            if enemy_level == None:
                if isinstance(entity, Enemy) == False:
                    enemy_level = random.choice(floor.level_list)#min(floor.level_list[rng_enemy] + round(random.uniform(0, 0.7)), 4)
                else:
                    enemy_level = min(entity.level + round(random.randint(0, 1)), 4)
            #floor.valid_entity_tiles.remove((y, x)) this is suspect. maybe we shouldnt be using this at all
            
            test_enemy = generate_enemy(enemy_name, enemy_level, x, y, enemy_grid_to_use(enemy_level), floor, player)
            test_enemy.paralysis_turns = 1
            test_enemy.invisible_frames = chronology

            floor.all_enemies.append(test_enemy)

            list_of_animations.append(animations.Animation("A " + str(test_enemy.name) + " was summoned.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, check_if_entity_is_on_screen(test_enemy, player, 1, 16), test_enemy.x, test_enemy.y, test_enemy.x, test_enemy.y, 0, None, None, None, None, None))

            enemies_to_summon += -1
            if enemies_to_summon == 0:
                return 
    
    list_of_animations.append(animations.Animation("No enemies could be summoned.", 1*29 + 24, 6, 4, (255, 255, 255, 0), chronology, 1, 0, 0, 0, 0, 0, None, None, None, None, None))


            

















