import pygame
from tiles import Tile
from settings import tile_size, all_sprites, screen_width
from player import Player
from particle import ParticleEffect


class Level:
    def __init__(self, level_data, surface):
        self.display_surface = surface
        self.world_shift = 0
        self.setup_level(level_data)

        #частицы
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

    def setup_level(self, layout):                  #создание тайлов и игрока(отрисовка в классах)
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.current_x = 0
        for row_index, row in enumerate(layout):
            for col_index, col in enumerate(row):
                x, y = col_index * tile_size, row_index * tile_size
                if col == '#':
                    tile = Tile((x, y), tile_size, self.tiles)
                elif col == 'P':
                    player = Player((x, y), self.player, self.display_surface, self.create_jump_particles)

    def create_jump_particles(self, pos):
        if self.player.sprite.facing_right:
            pos -= pygame.math.Vector2(10, -5)
        else:
            pos += pygame.math.Vector2(10, 5)
        jump_particle_effect = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_effect)

    def get_player_sprite_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_landing_dust(self):
        if not self.player_on_ground and self.player.sprite.on_ground and not self.dust_sprite.sprites():
            if self.player.sprite.facing_right:
                offset = pygame.math.Vector2(10, 15)
            else:
                offset = pygame.math.Vector2(-10, 15)
            fall_dust_particle = ParticleEffect(self.player.sprite.rect.midbottom, 'land')
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
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        self.camera_movement()                       #движение камеры(переопределение скорости движения игрока и уровня)
        self.tiles.update(self.world_shift)          #смещение уровня по вышепереопределенным переменным
        self.tiles.draw(self.display_surface)        #отрисовка

        self.player.update()                         #метод игрока
        self.horizontal_collision()
        self.get_player_sprite_on_ground()
        self.vertical_collision()                      #проверка на столкновения по вертикали и горизонтали и соответствующее изменение флагов
        self.create_landing_dust()
        self.player.draw(self.display_surface)       #отрисовка