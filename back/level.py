import pygame
from tiles import Tile, StaticTile
from settings import tile_size, all_sprites, screen_width
from player import Player
from support import import_csv_layout, import_cut_tiles


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = -5

        ground_layout = import_csv_layout(level_data['ground'])
        self.ground_sprites = self.create_tile_group(ground_layout, 'ground')

    def create_tile_group(self, layout, type):
        tiles_sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                if id != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'ground':
                        ground_tile_list = import_cut_tiles('./front/ground/ground_tiles.png')
                        tile_surface = ground_tile_list[int(id)]
                        tile = StaticTile((x, y), tile_size, tile_surface)
                        tiles_sprite_group.add(tile)

        return tiles_sprite_group


    '''def camera_movement(self):                     #камера(двигается левел при достижении игроком краев экрана)
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        if player_x < screen_width // 3 and direction_x < 0:
            self.world_shift = 8
            player.speed = 0
        elif player_x > screen_width - screen_width // 3 and direction_x > 0:
            self.world_shift = -8
            player.speed = 0
        else:
            self.world_shift = 0
            player.speed = 8'''

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left  #запоминаем координату при столкновении
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right
        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        elif player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True
                elif player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
        if player.on_ground and player.direction.y < 0 or player.direction.y > player.gravity:   #переопределениее флага "на земле" если чел в воздухе
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0:
            player.on_ceiling = False

    def run(self):
        #self.camera_movement()                          #движение камеры(переопределение скорости движения игрока и уровня)
        #self.tiles.update(self.world_shift)            #смещение уровня по вышепереопределенным переменным
        self.ground_sprites.draw(self.display_surface)  #отрисовка
        self.ground_sprites.update(self.world_shift)                    #отрисовка

        #self.player.update()                           #метод игрока
        #self.horizontal_collision()                    #проверка на столкновения по вертикали и горизонтали и соответствующее изменение флагов
        #self.vertical_collision()
        #self.player.draw(self.display_surface)         #отрисовка