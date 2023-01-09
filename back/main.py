import sys
from settings import *
from level import Level
from all_levels import level_1


def main():
    pygame.init()
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    level = Level(level_1, screen)
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


if __name__ == '__main__':
    main()