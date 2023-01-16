from support import load_image, import_folder
from settings import height_tile_number, tile_size, screen_width
from tiles import StaticTile, AnimatedTile
import pygame
from random import choice, randint


class Sky:
    def __init__(self, horizon):
        self.sky_top = load_image('../front/background/sky/sky_top.png')
        self.sky_middle = load_image('../front/background/sky/sky_middle.png')
        self.sky_bottom = load_image('../front/background/sky/sky_bottom.png')
        self.horizon = horizon

        self.sky_top = pygame.transform.scale(self.sky_top, (screen_width, tile_size))
        self.sky_middle = pygame.transform.scale(self.sky_middle, (screen_width, tile_size))
        self.sky_bottom = pygame.transform.scale(self.sky_bottom, (screen_width, tile_size))

    def draw(self, surface):
        for row in range(height_tile_number):
            y = row * tile_size
            if row < self.horizon:
                surface.blit(self.sky_top, (0, y))
            elif row == self.horizon:
                surface.blit(self.sky_middle, (0, y))
            else:
                surface.blit(self.sky_bottom, (0, y))


class Clouds:
    def __init__(self, level_width, horizon, number):
        clouds_list = import_folder('../front/background/clouds')
        min_x, max_x = -screen_width, level_width + screen_width
        min_y, max_y = 0, horizon
        self.cloud_sprite = pygame.sprite.Group()

        for cloud in range(number):
            cloud = choice(clouds_list)
            x = randint(min_x, max_x)
            y = randint(min_y, max_y)
            sprite = StaticTile(x, y, 0, cloud)
            self.cloud_sprite.add(sprite)

    def draw(self, surface, dx):
        self.cloud_sprite.update(dx)
        self.cloud_sprite.draw(surface)


class Water:
    def __init__(self, level_width, top):
        water_start_point = -screen_width
        water_tile_width = 192
        width_tile_number = (level_width + screen_width * 2) // water_tile_width
        self.water_sprite = pygame.sprite.Group()

        for tile in range(width_tile_number):
            x = tile * water_tile_width + water_start_point
            y = top
            sprite = AnimatedTile(x, y, water_tile_width, '../front/background/water')
            self.water_sprite.add(sprite)

    def draw(self, surface, dx):
        self.water_sprite.update(dx)
        self.water_sprite.draw(surface)