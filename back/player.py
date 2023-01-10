import pygame
from settings import all_sprites
from support import import_folder


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, surface, create_jump_particles):
        super().__init__()
        self.import_character_images()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.surface = surface
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)

        # частицы пыли
        self.import_dust_run_particles()
        self.dust_frame_index = 0
        self.dust_animation_speed = 0.15
        self.create_jump_particles = create_jump_particles

        self.direction = pygame.math.Vector2(0, 0)
        self.gravity = 0.8
        self.jump_speed = -16
        self.speed = 8
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False
        self.status = 'idle'
        self.facing_right = True

    def import_character_images(self):
        character_path = './front/character/'
        self.animations = {'idle':[], 'run':[], 'jump':[], 'fall':[]}
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)

    def import_dust_run_particles(self):
        self.run_particles = import_folder('./front/dust_particles/run')

    def run_dust_animation(self):
        if self.status == 'run' and self.on_ground:
            self.dust_frame_index = (self.dust_frame_index + self.dust_animation_speed) % len(
                self.run_particles)
            dust_particle = self.run_particles[int(self.dust_frame_index)]
            if self.facing_right:
                pos = self.rect.bottomleft - pygame.math.Vector2(6, 10)
                self.surface.blit(dust_particle, pos)
            else:
                pos = self.rect.bottomright - pygame.math.Vector2(6, 10)
                self.surface.blit(pygame.transform.flip(dust_particle, True, False), pos)

    def animate(self):
        animation = self.animations[self.status]
        self.frame_index = (self.frame_index + self.animation_speed) % len(animation)

        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            self.image = pygame.transform.flip(image, True, False)

        if self.on_ground and self.on_right:
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
        elif self.on_ceiling and self.on_right:
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

    def movement(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()
            self.create_jump_particles(self.rect.midbottom)

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > self.gravity:
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'

    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        self.direction.y = self.jump_speed

    def update(self):
        self.movement()     #проверка на нажатые клавиши
        self.get_status()   #получение состояния игрока
        self.animate()      #анимация игрока в соответствии со статусом
        self.run_dust_animation()  # запуск анимации частиц пылиa