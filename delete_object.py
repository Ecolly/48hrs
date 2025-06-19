




#this explicitly exists only to delete objects from lists
def delobj(objlist):
    i = 0
    while i < len(objlist):
        if objlist[i].should_be_deleted == True: #this attribute exists in all classes; set to True to delete an object.
            if hasattr(objlist[i], 'sprite') == True and objlist[i].sprite != None:
                objlist[i].sprite.delete()  
                del objlist[i].sprite       
            del objlist[i]  # removes the object from the list and deletes the reference
        else:
            i += 1

    return objlist