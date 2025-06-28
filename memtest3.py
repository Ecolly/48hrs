import pygame
import gc 
import sys

TILE_SIZE = 16
def load_tiles(path, tile_width, tile_height, scale=3, tint_color=None):
    sheet = pygame.image.load(path).convert_alpha()
    tiles = []

    for y in range(sheet.get_height()-tile_height, -tile_height, -tile_height):
        for x in range(0, sheet.get_width(), tile_width):
            rect = pygame.Rect(x, y, tile_width, tile_height)
            tile = sheet.subsurface(rect)

            # Scale the tile
            scaled_tile = pygame.transform.scale(
                tile,
                (tile_width * scale, tile_height * scale)
            )

            tile_dict = {
                "original": scaled_tile
            }

            # Optional: precompute a tinted version
            if tint_color is not None:
                tinted = scaled_tile.copy()
                tinted.fill(tint_color, special_flags=pygame.BLEND_RGBA_MULT)
                tile_dict["tinted"] = tinted

            tiles.append(tile_dict)

    return tiles


class GameObject:
    def __init__(self, x, y, tile_dict):
        self.x = x
        self.y = y
        self.original_tile = tile_dict["original"]
        self.tinted_tile = tile_dict.get("tinted")
        self.use_tint = False  # Switch to tinted version when needed

    def draw(self, surface):
        tile = self.tinted_tile if self.use_tint and self.tinted_tile else self.original_tile
        surface.blit(tile, (self.x, self.y))

    def set_tile(self, tile_dict):
        self.original_tile = tile_dict["original"]
        self.tinted_tile = tile_dict.get("tinted")

    def enable_tint(self, enable=True):
        self.use_tint = enable



pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Load tiles with a red tint option
tiles = load_tiles("entities_level1.png", 16, 16, scale=3, tint_color=(255, 100, 100, 255))

player = GameObject(100, 100, tiles[0])
#player.enable_tint(True)

running = True
frame = 0
bg_animframe = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Change frame every few ticks
    if pygame.time.get_ticks() // 100 % len(tiles) != frame:
        frame = pygame.time.get_ticks() // 100 % len(tiles)
        player.set_tile(tiles[20*8*8 + frame])

    screen.fill((0, 0, 0))
    player.draw(screen)
    pygame.display.flip()
    clock.tick(60)
    bg_animframe += 1
    if bg_animframe%60 == 0:
        gc.collect(generation=2)
        sys._clear_internal_caches()
        print("allocated blocks: " + str(sys.getallocatedblocks()))

pygame.quit()