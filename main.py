import pygame, sys
from settings import *
from level import Level

# Pygame Setup #
pygame.init()
screen = pygame.display.set_mode((screen_width, 900))
clock = pygame.time.Clock()
level = Level(level_test_1, screen)

# Main Game Loop #
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill('black')
    level.run()

    pygame.display.update()
    clock.tick(60)
