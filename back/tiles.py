from settings import *
from support import import_folder, load_image
from random import randint


class Tile(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.rect = self.image.get_rect(topleft = (x, y))

    def update(self, dx):
        self.rect.x += dx


class StaticTile(Tile):
    def __init__(self, x, y, size, surface):
        super().__init__(x, y, size)
        self.image = surface


class Crate(StaticTile):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, load_image('../front/ground/crate.png'))
        offset_y = y + size
        self.rect = self.image.get_rect(bottomleft=(x, offset_y))


class AnimatedTile(Tile):
    def __init__(self, x, y, size, path):
        super().__init__(x, y, size)
        self.frames = import_folder(path)
        self.frame_index = 0
        self.image = self.frames[self.frame_index]

    def animate(self):
        self.frame_index += 0.15
        self.image = self.frames[int(self.frame_index) % len(self.frames)]

    def update(self, dx):
        self.animate()
        self.rect.x += dx


class Palm(AnimatedTile):
    def __init__(self, x, y, size, path, offset):
        super().__init__(x, y, size, path)
        offset_y = y - offset
        self.rect.topleft = (x, offset_y)


class Consumables(AnimatedTile):
    def __init__(self, x, y, size, path):
        super().__init__(x, y, size, path)
        center_x, center_y = x + int(size / 2), y + int(size / 2)
        self.rect = self.image.get_rect(center=(center_x, center_y))


class Enemy(AnimatedTile):
    def __init__(self, x, y, size, path):
        super().__init__(x, y, size, path)
        self.rect.y += size - self.image.get_size()[1]
        self.speed = randint(2, 4)

    def move(self):
        self.rect.x += self.speed

    def reverse_image(self):
        if self.speed > 0:
            self.image = pygame.transform.flip(self.image, True, False)

    def reverse(self):
        self.speed *= -1

    def update(self, shift):
        self.rect.x += shift
        self.animate()
        self.move()
        self.reverse_image()