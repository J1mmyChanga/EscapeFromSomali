import sys
from settings import *
from level import Level
from all_levels import *

ITEMS = ['wood', 'oar', 'rope']


class Game:
    def __init__(self):
        self.current_health = 0
        self.coconuts = 0

    def create_level(self, current_level):
        self.level = Level(current_level, screen, self.change_health)

    def change_health(self, amount):
        self.current_health += amount

    def check_game_over(self):
        if self.current_health >= 6:
            self.current_health = 0
            self.coconuts = 0
            self.level = Level(level_1, screen, self.change_health)

    def run(self):
        self.level.run()
        self.check_game_over()


pygame.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Escape from Somali')
pygame.mouse.set_visible(False)
clock = pygame.time.Clock()
game = Game()
game.create_level(level_5)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    game.run()
    pygame.display.flip()
    clock.tick(60)
