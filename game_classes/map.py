class Map:
    def __init__(self, width, height, default_tile='#'):
        self.width = width
        self.height = height
        self.tiles = [
            [default_tile for _ in range(width)]
            for _ in range(height)
        ]