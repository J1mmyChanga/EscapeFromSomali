from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, dx):
        self.rect.x += dx


class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, pos, size):
        super().__init__(pos, size, pygame.image.load('./front/ground/crate.png').convert_alpha())
        offset_y = pos[1] + size
        self.rect = self.image.get_rect(bottomleft=(pos[0], offset_y))