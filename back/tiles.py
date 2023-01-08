from back.settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size, group):
        super().__init__(all_sprites, group)
        self.image = pygame.Surface((size, size))
        self.image.fill(pygame.Color('grey'))
        self.rect = self.image.get_rect(topleft = pos)

    def update(self, dx):
        self.rect.x += dx