import pygame
from settings import all_sprites

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, group):
        super().__init__(all_sprites, group)
        self.image = pygame.Surface((32, 64))
        self.image.fill(pygame.Color('yellow'))
        self.rect = self.image.get_rect(topleft = pos)

        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -12
        self.speed = 8

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        if keys[pygame.K_SPACE]:
            self.jump()

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.movement()
        self.rect.x += self.direction.x * self.speed
        self.apply_gravity()