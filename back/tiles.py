from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, group):
        super().__init__(group)
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, dx):
        self.rect.x += dx


class StaticTile(Tile):
    def __init__(self, pos, size, surface):
        super().__init__(pos, size)
        self.image = surface