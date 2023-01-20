import pygame
from tiles import StaticTile
from settings import *
from support import import_folder


class UI():
    def __init__(self, cur_lev):
        self.font = pygame.font.Font('../front/font/retro-land-mayhem.ttf', 48)
        self.cur_lev = cur_lev

        # hp
        self.hearts = pygame.sprite.Group()
        self.last_dmg = 2
        self.images_of_hp = import_folder('../front/ui/hp')
        self.hp_group = pygame.sprite.Group()

        # ключевые вещи
        self.items = pygame.sprite.Group()
        def_val = tile_size // 2
        self.def_size = tile_size * 1.25

        self.oar_image = import_folder('../front/consumables/items/oar')[0]
        self.rope_image = import_folder('../front/consumables/items/rope')[0]
        self.wood_image = import_folder('../front/consumables/items/wood')[0]
        self.coco_image = import_folder('../front/consumables/coconuts')[0]

        for i in [self.wood_image, self.rope_image, self.oar_image]:
            i = pygame.transform.scale(i, (self.def_size, self.def_size))
            sprite = StaticTile(screen_width - 1.75 * tile_size, def_val, self.def_size, i)
            self.items.add(sprite)
            def_val += self.def_size

        i = pygame.transform.scale(self.coco_image, (self.def_size, self.def_size))
        sprite = StaticTile(tile_size - 10, tile_size * 1.75, self.def_size, i)
        self.items.add(sprite)

    def update_hp(self, surface, hp):
        self.hp_group.empty()
        val = tile_size
        for i in hp:
            sprite = StaticTile(val, tile_size // 1.5, tile_size, self.images_of_hp[i])
            val += tile_size
            self.hp_group.add(sprite)
        self.hp_group.draw(surface)

    def update_items(self, surface, woods, ropes, oars, coconuts):
        self.items.draw(surface)

        text_wood = self.font.render(f"{woods}/3", True, (51, 50, 61))
        x1, y1 = screen_width - 1.75 * tile_size - text_wood.get_rect().width, tile_size // 2 + 5

        text_rope = self.font.render(f"{ropes}/1", True, (51, 50, 61))
        x2, y2 = screen_width - 1.75 * tile_size - text_rope.get_rect().width, tile_size // 2 + 5 + self.def_size

        text_oar = self.font.render(f"{oars}/1", True, (51, 50, 61))
        x3, y3 = screen_width - 1.75 * tile_size - text_oar.get_rect().width, tile_size // 2 + 5 + self.def_size * 2

        text_cocos = self.font.render(f" {coconuts}", True, (51, 50, 61))
        x4, y4 = 120, 116

        text_level = self.font.render(f"Level {self.cur_lev + 1}", True, (255, 255, 255))
        x5, y5 = 32, 800

        surface.blit(text_wood, (x1, y1))
        surface.blit(text_rope, (x2, y2))
        surface.blit(text_oar, (x3, y3))
        surface.blit(text_cocos, (x4, y4))
        surface.blit(text_level, (x5, y5))