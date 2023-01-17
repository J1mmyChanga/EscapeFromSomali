import pygame

height_tile_number = 14
width_tile_number = 22
tile_size = 64

screen_height = height_tile_number * tile_size
screen_width = width_tile_number * tile_size
size = (screen_width, screen_height)
all_sprites = pygame.sprite.Group()