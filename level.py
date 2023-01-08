import pygame
from tiles import Tile
from settings import tile_size


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.setup_level(level_data)

    def setup_level(self, layout):
        self.tiles = pygame.sprite.Group()
        for row_index, row in layout:
            for col_index, col in row:
                if col == '#':
                    tile = Tile((col_index, row_index), tile_size, self.tiles)


    def run(self):
        self.tiles.draw(self.display_surface)