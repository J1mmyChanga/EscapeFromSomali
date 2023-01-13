import pygame
from support import import_folder
from settings import all_sprites


class ParticleEffect(pygame.sprite.Sprite):
    def __init__(self, pos, type):
        super().__init__(all_sprites)
        self.frame_index = 0
        self.animation_speed = 0.5
        if type == 'jump':
            self.frames = import_folder('../front/dust_particles/jump')
        elif type == 'land':
            self.frames = import_folder('../front/dust_particles/land')
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self, dx):
        self.animate()
        self.rect.x += dx