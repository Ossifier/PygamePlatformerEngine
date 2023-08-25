import pygame, sys
from settings import *
from level import Level

# Pygame Setup #
pygame.init()
screen = pygame.display.set_mode((screen_width, 900))
clock = pygame.time.Clock()
level = Level(level_test_3, screen)
FPS = 60

# Main Game Loop #
while True:

    level.fps = clock.get_fps()                                     # For Debug Panel

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:                            # Toggle Debug Panel w/ 0 Key
            if event.key == pygame.K_0 and level.debug is False:
                level.debug = True
            elif event.key == pygame.K_0 and level.debug is True:
                level.debug = False

    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(FPS)
