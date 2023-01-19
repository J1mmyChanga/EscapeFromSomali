import pygame
from tiles import StaticTile
from settings import tile_size, screen_width, screen_height
from support import import_folder

class UI():
    def __init__(self):
        self.font = pygame.font.Font('../front/font/retro-land-mayhem.ttf', 48)

        # hp
        self.hearts = pygame.sprite.Group()
        self.amount_of_hp = [0, 0, 0]
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

        self.woods = 0
        self.ropes = 0
        self.oars = 0
        self.cocos = 0

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

        text_wood = self.font.render(f"{self.woods}/3", True, (255, 255, 255))
        x1, y1 = screen_width - 1.75 * tile_size - text_wood.get_rect().width, tile_size // 2 + 5

        text_rope = self.font.render(f"{self.ropes}/1", True, (255, 255, 255))
        x2, y2 = screen_width - 1.75 * tile_size - text_rope.get_rect().width, tile_size // 2 + 5 + self.def_size

        text_oar = self.font.render(f"{self.oars}/1", True, (255, 255, 255))
        x3, y3 = screen_width - 1.75 * tile_size - text_oar.get_rect().width, tile_size // 2 + 5 + self.def_size * 2

        text_cocos = self.font.render(f" {self.cocos}", True, (255, 255, 255))
        x4, y4 = 120, 116

        surface.blit(text_wood, (x1, y1))
        surface.blit(text_rope, (x2, y2))
        surface.blit(text_oar, (x3, y3))
        surface.blit(text_cocos, (x4, y4))