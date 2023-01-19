import pygame
from tiles import StaticTile
from settings import tile_size, screen_width, screen_height
from support import import_folder

class UI():
    def __init__(self):
        # hp
        self.hearts = pygame.sprite.Group()
        self.amount_of_hp = [0, 0, 0]
        self.last_dmg = 2
        self.images_of_hp = import_folder('../front/ui/hp')
        self.hp_group = pygame.sprite.Group()

        # ключевые вещи
        self.items = pygame.sprite.Group()
        def_val = tile_size // 1.5
        self.oar_image = import_folder('../front/consumables/items/oar')[0]
        self.rope_image = import_folder('../front/consumables/items/rope')[0]
        self.wood_image = import_folder('../front/consumables/items/wood')[0]
        for i in [self.wood_image, self.rope_image, self.oar_image]:
            sprite = StaticTile(screen_width - 2 * tile_size, def_val, tile_size, i)
            self.items.add(sprite)
            def_val += tile_size

    def take_damage(self):
        self.amount_of_hp[self.last_dmg] += 1
        if self.amount_of_hp[self.last_dmg] >= 2:
            self.last_dmg -= 1
        if sum(self.hp_group) >= 6:
            print('ure dead bruh...')

    def heal(self):
        self.amount_of_hp[self.last_dmg] -= 0.5

    def update_hp(self, surface):
        self.hp_group.empty()
        val = tile_size
        for i in self.amount_of_hp:
            sprite = StaticTile(val, tile_size // 1.5, tile_size, self.images_of_hp[i])
            val += tile_size
            self.hp_group.add(sprite)
        self.hp_group.draw(surface)

    def update_items(self, surface):
        self.items.draw(surface)