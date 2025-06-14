
import pyglet

def create_sprite_item(image_grid, index): #dumb. literally the same as the image handling function
    tex = pyglet.image.Texture.create(16, 16)
    tex.blit_into(image_grid[index], 0, 0, 0)
    return pyglet.sprite.Sprite(tex, x=0, y=0)

class Item:
    #very basics item class cause we dono what items there are
    def __init__(self, name, grid_items, x, y, quantity):

        item_names = ["Kitchen Knife", "Machete", "Scimitar", "Screwdriver", "Sickle"]
        item_fakenames = ["Kitchen Knife", "Machete", "Scimitar", "Screwdriver", "Sickle"]
        item_spritelocs = [29*10, 29*10+1, 29*10+2, 29*10+3, 29*10+4]
        item_is_usable = [1, 1, 1, 1, 1]

        self.name = name
        self.index = item_names.index(name)
        self.fakename = item_fakenames[self.index]
        self.sprite = create_sprite_item(grid_items, item_spritelocs[self.index])
        self.x = x
        self.y = y
        self.prevx = x
        self.prevy = y
        self.quantity = quantity
        self.scale = 3
        self.is_usable = item_is_usable[self.index]


    def use(self, target):
        pass


    def get_screen_position(self):
        if self.inventory_slot == -1:
            return self.scale*(self.prevx*16-8), self.scale*(self.prevy*16-8)
    
    def is_mouse_over(self, mouse_x, mouse_y):
        """Check if a point is within this object's interactive bounds."""
        base_x, base_y = self.get_screen_position()
        #print(mouse_x, mouse_y, base_x, base_y)
        return (base_x <= mouse_x <= base_x + self.width*self.scale and
                base_y <= mouse_y <= base_y + self.height*self.scale)
    
    def draw(self, batch):
        base_x, base_y = self.get_screen_position()
        sprite = self.sprite

        #tex = pyglet.image.Texture.create(16, 16)
        #print(self.animtype)
        #print(self.animframe)
        #tex.blit_into(grid_entities1[self.spriteindex + (self.direction.value)*8 + animation_presets[self.animtype][math.floor(self.animframe)]], 0, 0, 0)
        #sprite.image = tex

        #self.animframe = self.animframe + self.animmod
        #if self.animframe >= len(animation_presets[self.animtype]):
        #    self.animframe = 0

        sprite.x = base_x
        sprite.y = base_y
        sprite.scale = self.scale
        #sprite.color = self.color
        sprite.batch = batch
        sprite.z = 30














