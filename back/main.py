import sys
from settings import *
from back.level import Level


pygame.init()
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
level = Level(level_map, screen)
running = True


def terminate():
    pygame.quit()
    sys.exit()

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    level.run()
    pygame.display.flip()
    clock.tick(60)
terminate()