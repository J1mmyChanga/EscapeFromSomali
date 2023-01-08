import pygame, sys, os

def import_folder(path):
    surface_list = []
    for _, __, img_files in os.walk(path):
        for image in img_files:
            full_path = f'{path}/{image}'
            img_smurf = load_image(full_path)
            surface_list.append(img_smurf)
    return surface_list

def load_image(name, colorkey=None):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image