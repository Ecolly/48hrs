from PIL import Image
import numpy as np
import math
import os
import random

# --- CONFIGURATION ---
input_path = "liqsall.png"  # Replace with your actual file path
tile_size = 16
tiled_size = 16
frames_per_texture = 16
textures_count = 16  # Expecting a strip of 16 tiles

output_image_path = "tile_liquid_animations.png"

# --- CHECK FILE ---
if not os.path.exists(input_path):
    raise FileNotFoundError(f"Input file '{input_path}' not found.")

# Load source image
source_image = Image.open(input_path).convert("RGBA")

# --- DISTORTION FUNCTION ---
def distort_image_angled(image, time, angle_deg=45, amplitude=0.5, frequency=2.0):
    arr = np.array(image)
    h, w = arr.shape[:2]
    distorted = np.zeros_like(arr)

    angle_rad = math.radians(angle_deg)
    dir_x = math.cos(angle_rad)
    dir_y = math.sin(angle_rad)

    perp_x = -dir_y
    perp_y = dir_x

    for y in range(h):
        for x in range(w):
            # Project onto wave axis
            wave_axis = (x * dir_x + y * dir_y)
            offset = amplitude * math.sin(wave_axis * frequency * 2 * math.pi / max(w, h) + time) * random.uniform(0.65, 1.35)

            # Apply perpendicular offset & modulo to valid range
            new_x = int(x + offset * perp_x) % w
            new_y = int(y + offset * perp_y) % h

            distorted[y, x] = arr[new_y, new_x]

    return Image.fromarray(distorted, mode="RGBA")







# --- CREATE FINAL COMPOSITE IMAGE ---
final_width = tiled_size * frames_per_texture
final_height = tiled_size * textures_count
final_image = Image.new("RGBA", (final_width, final_height))

for texture_index in range(textures_count):
    # Extract the 16x16 tile
    tile = source_image.crop((
        texture_index * tile_size, 0,
        (texture_index + 1) * tile_size, tile_size
    ))

    # Tile to fill 128x128
    base_tile = Image.new("RGBA", (tiled_size, tiled_size))
    for y in range(0, tiled_size, tile_size):
        for x in range(0, tiled_size, tile_size):
            base_tile.paste(tile, (x, y))

    # Generate all 32 frames
    for frame_index in range(frames_per_texture):
        time = (frame_index / frames_per_texture) * 2 * math.pi
        distorted = distort_image_angled(base_tile, time, angle_deg=120)
        final_image.paste(
            distorted,
            (frame_index * tiled_size, texture_index * tiled_size)
        )

# --- SAVE ---
final_image.save(output_image_path)
#print(f"Saved animation sheet to: {output_image_path}")