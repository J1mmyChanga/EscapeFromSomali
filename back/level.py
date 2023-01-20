import pygame
from tiles import *
from settings import screen_height, screen_width
from player import Player
from particle import ParticleEffect
from support import import_csv_layout, import_cut_tiles, Button
from background import Sky, Clouds, Water
from ui import *


class Level:
    def __init__(self, level_data, surface, change_health, cur_lev, move_to_next_level, woods, ropes, oars, coconuts):
        self.change_health = change_health
        self.level_data = level_data
        self.cur_lev = cur_lev
        self.move_to_next_level = move_to_next_level
        self.woods, self.ropes, self.oars, self.coconuts = woods, ropes, oars, coconuts
        self.check_if_coc = 0
        self.reset(level_data, surface, cur_lev)


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
                        tile = StaticTile(x, y, tile_size, tile_surface)
                        self.coord_tuples.append((col_index, row_index))
                    if type == 'grass':
                        grass_tile_list = import_cut_tiles('../front/background/grass/grass.png')
                        tile_surface = grass_tile_list[int(id)]
                        tile = StaticTile(x, y, tile_size, tile_surface)
                    if type == 'crates':
                        tile = Crate(x, y, tile_size)
                    if type == 'foreground palms':
                        if id == '0':
                            tile = Palm(x, y, tile_size, '../front/ground/palm_large', 72)
                        if id == '1':
                            tile = Palm(x, y, tile_size, '../front/ground/palm_small', 38)
                    if type == 'background palms':
                        tile = Palm(x, y, tile_size, '../front/ground/bg_palm', 64)
                    if type == 'consumables':
                        if id == '0':
                            tile = Consumables(x, y, tile_size, '../front/consumables/bananas')
                        if id == '2':
                            tile = Consumables(x, y, tile_size, '../front/consumables/coconuts')
                    if type == 'player':
                        if id == '1':
                            tile = Consumables(x, y, tile_size, '../front/consumables/items/wood')
                        elif id == '2':
                            tile = Consumables(x, y, tile_size, '../front/consumables/items/rope')
                        elif id == '3':
                            tile = Consumables(x, y, tile_size, '../front/consumables/items/oar')
                        else:
                            continue
                    if type == 'enemies':
                        tile = Enemy(x, y, tile_size, '../front/enemies/run')
                    if type == 'obstacles':
                        tile = Tile(x, y, tile_size)

                    tiles_sprite_group.add(tile)

        return tiles_sprite_group

    def spawn_player(self, layout, change_health):
        for row_index, row in enumerate(layout):
            for col_index, id in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if id == '0':
                    tile = Player(x, y, self.display_surface, self.create_jump_particles, change_health)
                    self.player.add(tile)

    def get_player_sprite_on_ground(self):
        if self.player.sprite.on_ground:
            self.player_on_ground = True
        else:
            self.player_on_ground = False

    def create_jump_particles(self, pos):
        pos -= pygame.math.Vector2(0, 15)
        jump_particle_sprite = ParticleEffect(pos, 'jump')
        self.dust_sprite.add(jump_particle_sprite)

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
        if not self.dead:
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
        collidable_sprites = self.ground_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palm_sprites.sprites()
        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.x < 0:
                    player.rect.left = sprite.rect.right
                    player.on_left = True
                    self.current_x = player.rect.left
                elif player.direction.x > 0:
                    player.rect.right = sprite.rect.left
                    player.on_right = True
                    self.current_x = player.rect.right

        if player.on_left and (player.rect.left < self.current_x or player.direction.x >= 0):
            player.on_left = False
        if player.on_right and (player.rect.right > self.current_x or player.direction.x <= 0):
            player.on_right = False

    def vertical_collision(self):
        player = self.player.sprite
        player.apply_gravity()
        collidable_sprites = self.ground_sprites.sprites() + self.crates_sprites.sprites() + self.fg_palm_sprites.sprites()

        for sprite in collidable_sprites:
            if sprite.rect.colliderect(player.rect):
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                elif player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    player.on_ceiling = True

        if player.on_ground and player.direction.y < 0 or player.direction.y > 1:
            player.on_ground = False
        if player.on_ceiling and player.direction.y > 0.1:
            player.on_ceiling = False

    def check_death(self):
        if self.player.sprite.rect.top > screen_height:
            self.dead = True
            self.world_shift = 0
            self.check_if_coc = 1
            if self.restart_button.draw(self.display_surface):
                self.reset(self.level_data, self.display_surface, self.cur_lev)
                self.coconuts = 0

    def reset(self, level_data, surface, cur_lev):
        self.display_surface = surface
        self.coord_tuples = []
        self.world_shift = 0
        self.dead = False
        self.ui = UI(cur_lev)
        self.restart_button = Button((screen_width - 120) // 2, screen_height // 2, '../front/ui/buttons/restart_btn.png')

        # частицы
        self.dust_sprite = pygame.sprite.GroupSingle()
        self.player_on_ground = False

        # игрок
        player_layout = import_csv_layout(level_data['player'])
        self.player = pygame.sprite.GroupSingle()
        self.spawn_player(player_layout, self.change_health)

        # земля
        ground_layout = import_csv_layout(level_data['ground'])
        self.ground_sprites = self.create_tile_group(ground_layout, 'ground')

        # враги
        self.explosion_sprites = pygame.sprite.Group()

        enemies_layout = import_csv_layout(level_data['enemies'])
        self.enemies_sprites = self.create_tile_group(enemies_layout, 'enemies')

        # трава
        grass_layout = import_csv_layout(level_data['grass'])
        self.grass_sprites = self.create_tile_group(grass_layout, 'grass')

        # ящики
        crates_layout = import_csv_layout(level_data['crates'])
        self.crates_sprites = self.create_tile_group(crates_layout, 'crates')

        # фрукты
        consumables_layout = import_csv_layout(level_data['consumables'])
        self.consumables_sprites = self.create_tile_group(consumables_layout, 'consumables')

        # ключевой предмет для перехода на новый уровень
        key_item_layout = import_csv_layout(level_data['player'])
        self.key_item_sprite = self.create_tile_group(key_item_layout, 'player')

        # пальмы переднего фона
        fg_palm_layout = import_csv_layout(level_data['foreground palms'])
        self.fg_palm_sprites = self.create_tile_group(fg_palm_layout, 'foreground palms')

        # пальмы заднего фона
        bg_palm_layout = import_csv_layout(level_data['background palms'])
        self.bg_palm_sprites = self.create_tile_group(bg_palm_layout, 'background palms')

        # препятствия для врагов
        obstacles_layout = import_csv_layout(level_data['obstacles'])
        self.obstacles_sprites = self.create_tile_group(obstacles_layout, 'obstacles')

        # задний фон
        level_width = len(ground_layout[0]) * tile_size
        self.sky = Sky(8)
        self.clouds = Clouds(level_width, 300, 25)
        self.water = Water(level_width, screen_height - 40)

        self.left_edge, self.right_edge = sorted(self.coord_tuples)[0], sorted(self.coord_tuples)[-1]
        for sprite in self.ground_sprites:
            if (sprite.rect.x // tile_size, sprite.rect.y // tile_size) == self.left_edge:
                self.left_edge_tile = sprite
            elif (sprite.rect.x // tile_size, sprite.rect.y // tile_size) == self.right_edge:
                self.right_edge_tile = sprite

    def enemy_collision(self):
        for enemy in self.enemies_sprites.sprites():
            if pygame.sprite.spritecollide(enemy, self.obstacles_sprites, False):
                enemy.reverse()

    def check_fruit_collision(self):
        for sprite in self.consumables_sprites:
            if pygame.sprite.collide_mask(sprite, self.player.sprite):
                sprite.kill()
                if sprite.type == 'coconuts':
                    self.coconuts += 1
                elif sprite.type == 'bananas':
                    #self.player.sprite.heal()
                    pass

    def check_key_items_collision(self):
        global woods, ropes, oars
        for sprite in self.key_item_sprite:
            if pygame.sprite.collide_mask(sprite, self.player.sprite):
                sprite.kill()
                if sprite.type == 'wood':
                    self.woods += 1
                    self.move_to_next_level(self.woods, self.ropes, self.oars, self.coconuts)
                elif sprite.type == 'rope':
                    self.ropes += 1
                    self.move_to_next_level(self.woods, self.ropes, self.oars, self.coconuts)
                elif sprite.type == 'oar':
                    self.oars += 1
                    self.move_to_next_level(self.woods, self.ropes, self.oars, self.coconuts)

    def check_enemy_collisions(self):
        enemy_collisions = pygame.sprite.spritecollide(self.player.sprite, self.enemies_sprites, False)

        if enemy_collisions:
            for enemy in enemy_collisions:
                enemy_center = enemy.rect.centery
                enemy_top = enemy.rect.top
                player_bottom = self.player.sprite.rect.bottom
                if enemy_top < player_bottom < enemy_center and self.player.sprite.direction.y >= 0:
                    self.player.sprite.direction.y = -15
                    explosion_sprite = ParticleEffect(enemy.rect.center, 'explosion')
                    self.explosion_sprites.add(explosion_sprite)
                    enemy.kill()
                else:
                    self.player.sprite.get_damage()

    def check_level_ending(self):
        player = self.player.sprite
        if (self.left_edge_tile.rect.x == tile_size and player.direction.x < 0) or \
        (self.right_edge_tile.rect.x == screen_width - 2 * tile_size and player.direction.x > 0):
            self.world_shift = 0
            player.speed = 8

    def run(self):
        self.camera_movement()  # движение камеры(переопределение скорости движения игрока и уровня
        self.check_level_ending() # проверка на конец лвла

        # задний фон
        self.sky.draw(self.display_surface)
        self.clouds.draw(self.display_surface, self.world_shift)

        # пальмы заднего фона
        self.bg_palm_sprites.update(self.world_shift)
        self.bg_palm_sprites.draw(self.display_surface)

        # земля
        self.ground_sprites.update(self.world_shift)
        self.ground_sprites.draw(self.display_surface)

        # враги и невидимые препятствия
        self.enemies_sprites.update(self.world_shift)
        self.obstacles_sprites.update(self.world_shift)
        self.enemy_collision()
        self.enemies_sprites.draw(self.display_surface)
        self.explosion_sprites.update(self.world_shift)
        self.explosion_sprites.draw(self.display_surface)

        # ящики
        self.crates_sprites.update(self.world_shift)
        self.crates_sprites.draw(self.display_surface)

        # фрукты
        self.consumables_sprites.update(self.world_shift)
        self.consumables_sprites.draw(self.display_surface)

        # ключевой предмет для перехода на новый уровень
        self.key_item_sprite.update(self.world_shift)
        self.key_item_sprite.draw(self.display_surface)

        # трава
        self.grass_sprites.update(self.world_shift)
        self.grass_sprites.draw(self.display_surface)

        # пальмы переднего фона
        self.fg_palm_sprites.update(self.world_shift)
        self.fg_palm_sprites.draw(self.display_surface)

        # игрок

        self.player.update(self.dead)
        self.horizontal_collision()

        self.get_player_sprite_on_ground()
        self.vertical_collision()
        self.create_landing_dust()

        self.player.draw(self.display_surface)
        self.check_death()

        # проверка на столкновение с фруктами и врагами
        self.check_fruit_collision()
        self.check_key_items_collision()
        self.check_enemy_collisions()

        # вода
        self.water.draw(self.display_surface, self.world_shift)

        # частицы
        self.dust_sprite.update(self.world_shift)
        self.dust_sprite.draw(self.display_surface)

        # ui
        self.ui.update_hp(self.display_surface, self.player.sprite.amount_of_hp)
        self.ui.update_items(self.display_surface, self.woods, self.ropes, self.oars, self.coconuts)