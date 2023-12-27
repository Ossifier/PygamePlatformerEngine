import pygame, sys, time
from maps import *
from level import Level
from settings import screen_width, screen_height, target_fps, game_speed

# Pygame Setup #
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
level = Level(level_test_3, screen)

previous_time = time.time()                                         # For Calculating Frame Interp

# Main Gameloop #
while True:
    dt = time.time() - previous_time                                # For Calculating Frame Interp
    previous_time = time.time()                                     # For Calculating Frame Interp
    level.fps = clock.get_fps()                                     # For Debug Panel
    level.dt = dt                                                   # For Debug Panel / Distribute

    level.game_speed = dt * game_speed

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:                            # Toggle Debug Panel w/ 0 Key
            if event.key == pygame.K_0 and level.debug is False:
                level.debug = True
            elif event.key == pygame.K_0 and level.debug is True:
                level.debug = False
            elif event.key == pygame.K_1:                           # Toggle FPS = 30 w/ 1 Key
                target_fps = 30
            elif event.key == pygame.K_2:                           # Toggle FPS = 60 w/ 2 Key
                target_fps = 60
            elif event.key == pygame.K_3:                           # Toggle FPS = 120 w/ 3 Key
                target_fps = 120

    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(target_fps)
