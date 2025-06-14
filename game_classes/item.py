class Item:
    #very basics item class cause we dono what items there are
    def __init__(self, name, item_type, description="", stack_size=1):
        self.name = name
        self.item_type = item_type
        self.description = description
        self.stack_size = stack_size # How many of this item can be stacked together

    def use(self, target):
        pass
