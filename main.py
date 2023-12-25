import pygame, sys, time
from settings import *
from level import Level

# Pygame Setup #
pygame.init()
screen = pygame.display.set_mode((screen_width, 900))
clock = pygame.time.Clock()
level = Level(level_test_3, screen)
FPS = 60

previous_time = time.time()                                         # For Calculating Frame Interp

# Main Game Loop #
while True:
    dt = time.time() - previous_time                                # For Calculating Frame Interp
    previous_time = time.time()                                     # For Calculating Frame Interp

    level.fps = clock.get_fps()                                     # For Debug Panel
    level.dt = dt                                                   # For Debug Panel / Distribute

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
