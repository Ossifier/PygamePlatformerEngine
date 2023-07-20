import pygame
from spritesheets import SpriteSheet


def animate_sprite_dict(sprite_test, state, state_list, surface):
    sprite_dict = sprite_test.build_sprite_dict(state_list)
    sprite_test.num_frames = len(sprite_test.data['animation states'][state]['framelist'])

    if sprite_test.current_time != 0 and sprite_test.current_time % sprite_test.animation_speed == 0:
        if sprite_test.current_frame >= sprite_test.num_frames - 1:
            sprite_test.current_frame = -1
        sprite_test.current_frame += 1
        sprite_test.current_time = -1

    surface.blit(sprite_dict[state][sprite_test.current_frame], (0, 0))

    sprite_test.current_time += 1


if __name__ == "__main__":

    # BUILD SCREEN #
    pygame.init()
    DISPLAY_W, DISPLAY_H = 1000, 500
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    clock = pygame.time.Clock()
    FPS = 60

    test_sprite = SpriteSheet('Sprites/full_sheet.png')
    M_SPRITE = SpriteSheet('Sprites/full_sheet.png')

    st_list = ['idle', 'running']

    test_sprite_dict = M_SPRITE.build_sprite_dict(st_list)

    run = True
    while run:

        canvas.fill((50, 50, 50))

        animate_sprite_dict(M_SPRITE, M_SPRITE.current_state, ['idle', 'running'], canvas)

        ### TEST ANIMATIONS ###
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print('K_UP')
                    M_SPRITE.current_state = 'idle'
                    M_SPRITE.current_frame = 0
                    M_SPRITE.current_time = 0
                if event.key == pygame.K_DOWN:
                    print('K_DOWN')
                    M_SPRITE.current_state = 'running'
                    M_SPRITE.current_frame = 0
                    M_SPRITE.current_time = 0

            ### QUIT ###
            if event.type == pygame.QUIT:
                run = False

        window.blit(canvas, (0, 0))
        pygame.display.update()

        clock.tick(FPS)
