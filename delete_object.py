#this explicitly exists only to delete objects from lists
from game_classes.item import Weapon, Consumable
from game_classes.item import Item

def delobj(objlist):
    i = 0
    while i < len(objlist):
        if objlist[i] is not None:
            if objlist[i].should_be_deleted == True: #this attribute exists in all classes; set to True to delete an object.
                if hasattr(objlist[i], 'sprite') == True and objlist[i].sprite != None:
                    objlist[i].sprite.delete()  
                    del objlist[i].sprite       
                if hasattr(objlist[i], 'sprites') == True:
                    for sprite in objlist[i].sprites:
                        sprite.delete()  
                        del sprite       
                del objlist[i]  # removes the object from the list and deletes the reference
            else:
                i += 1
        else:
                i += 1

    return objlist