import pygame
from spritesheets import SpriteSheet


def animate_sprite_dict(sprite, state):
    """NOTES: Returns the next frame in the animation sequence for a sprite dictionary. Uses the sprite's loaded data,
    along with its current state to check against the current number of frames that have elapsed since the frame
    changed. If it is equal or larger, then it adds to the frame index, and resets the frame index back to zero if it is
    larger than the length of the state frame list."""
    sprite.num_frames = len(sprite.data['animationStates'][state]['frameList'])

    if sprite.current_time != 0 and sprite.current_time % sprite.animation_speed == 0:
        if sprite.current_frame >= sprite.num_frames - 1:
            sprite.current_frame = -1
        sprite.current_frame += 1
        sprite.current_time = -1

    sprite.current_time += 1

    return sprite.current_frame


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

    M_DICT = M_SPRITE.build_sprite_dict(st_list)

    run = True
    while run:

        canvas.fill((50, 50, 50))

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
