import pygame, sys, os
from csv import reader
from settings import tile_size


def import_folder(path):
    surface_list = []
    for _, __, img_files in os.walk(path):
        for image in img_files:
            full_path = f'{path}/{image}'
            img_smurf = load_image(full_path)
            surface_list.append(img_smurf)
    return surface_list


def load_image(name, colorkey=None):
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def import_csv_layout(path):
    layout_map = []
    with open(path) as lvl:
        level = reader(lvl, delimiter = ',')
        for row in level:
            layout_map.append(list(row))
        return layout_map


def import_cut_tiles(path):
    surface = load_image(path)
    tile_amount_x = surface.get_size()[0] // tile_size
    tile_amount_y = surface.get_size()[1] // tile_size

    cut_tiles = []
    for row in range(tile_amount_y):
        for col in range(tile_amount_x):
            x = col * tile_size
            y = row * tile_size
            new_surf = pygame.Surface((tile_size, tile_size), flags=pygame.SRCALPHA)
            new_surf.blit(surface, (0, 0), pygame.Rect(x, y, tile_size, tile_size))
            cut_tiles.append(new_surf)
    return cut_tiles


class Button:
    def __init__(self, x, y, path):
        self.image = load_image(path)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        action = False
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            action = True

        surface.blit(self.image, self.rect)

        return action
