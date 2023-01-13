import pygame
from tiles import StaticTile, Crate
from settings import tile_size, screen_width
from player import Player
from particle import ParticleEffect
from support import import_csv_layout, import_cut_tiles


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0

        # частицы
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # игрок
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.spawn_player(player_layout)

        # земля
        ground_layout = import_csv_layout(level_data['ground'])
        self.ground_sprites = self.create_tile_group(ground_layout, 'ground')

        # трава
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # ящики
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')


    def create_tile_group(self, layout, type):
        tiles_sprite_group = pygame.sprite.Group()
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                if id != '-1':
                    x = col_index * tile_size
                    y = row_index * tile_size
                    if type == 'ground':
                        ground_tile_list = import_cut_tiles('../front/ground/ground_tiles.png')
                        tile_surface = ground_tile_list[int(id)]
                        tile = StaticTile((x, y), tile_size, tile_surface)
                    if type == 'grass':
                        grass_tile_list = import_cut_tiles('../front/background/grass/grass.png')
                        tile_surface = grass_tile_list[int(id)]
                        tile = StaticTile((x, y), tile_size, tile_surface)
                    if type == 'crates':
                        tile = Crate((x, y), tile_size)

                    tiles_sprite_group.add(tile)

        return tiles_sprite_group

    def spawn_player(self, layout):
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if id == '0':
                    sprite = Player((x, y), self.display_surface, self.create_jump_particles)
                    self.player.add(sprite)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(0, 12)
        else:
            pos += pygame.math.Vector2(0, -12)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

    def get_player_sprite_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(0, 20)
            else:
                offset = pygame.math.Vector2(0, 20)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom - offset, 'land')
            self.dust_sprite.add(fall_dust_particle)

    def camera_movement(self):                     #камера(двигается левел при достижении игроком краев экрана)
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
            player.speed = 8

    def horizontal_collision(self):
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed
        collidable_sprites = self.ground_sprites.sprites() + self.crates_sprites.sprites()

        for sprite in collidable_sprites:
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
        collidable_sprites = self.ground_sprites.sprites() + self.crates_sprites.sprites()

        for sprite in collidable_sprites:
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
        self.camera_movement()  # движение камеры(переопределение скорости движения игрока и уровня

        # земля
        self.ground_sprites.draw(self.display_surface)
        self.ground_sprites.update(self.world_shift)

        # ящики
        self.crates_sprites.draw(self.display_surface)
        self.crates_sprites.update(self.world_shift)

        # трава
        self.grass_sprites.draw(self.display_surface)
        self.grass_sprites.update(self.world_shift)

        self.player.update()
        self.player.draw(self.display_surface)

        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.horizontal_collision()
        self.get_player_sprite_on_ground()
        self.vertical_collision()  # проверка на столкновения по вертикали и горизонтали и соответствующее изменение флагов
        self.create_landing_dust()