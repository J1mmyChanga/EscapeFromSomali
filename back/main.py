import sys
from settings import *
from level import Level
from all_levels import *

ITEMS = ['wood', 'oar', 'rope']
LEVELS = [level_1, level_2, level_3, level_4, level_5]
woods = 0
ropes = 0
oars = 0
coconuts = 0
cur_lev = 0


class Game:
    def __init__(self):
        self.current_health = 0
        self.coconuts = 0

    def create_level(self, data):
        self.level = Level(data, screen, self.change_health, cur_lev, self.move_to_next_level, woods, ropes, oars, coconuts)

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        global cur_lev, coconuts, woods, ropes, oars
        if self.current_health >= 6:
            self.current_health = 0
            coconuts = 0
            woods = 0
            ropes = 0
            oars = 0
            cur_lev = 0
            self.level = Level(level_1, screen, self.change_health, cur_lev, self.move_to_next_level, woods, ropes, oars, coconuts)

    def move_to_next_level(self, wood_lv, ropes_lv, oars_lv, cocs):
        global cur_lev, woods, ropes, oars, coconuts
        woods, ropes, oars, coconuts = wood_lv, ropes_lv, oars_lv, cocs
        if cur_lev < 4:
            cur_lev += 1
            self.level = Level(LEVELS[cur_lev], screen, self.change_health, cur_lev, self.move_to_next_level, woods, ropes, oars, coconuts)
        else:
            pass

    def run(self):
        self.level.run()
        self.check_game_over()


pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Escape from Somali')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
game = Game()
game.create_level(level_2)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.run()
    pygame.display.flip()
    clock.tick(60)
