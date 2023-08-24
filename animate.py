import pygame
from spritesheets import SpriteSheet


def flip_img_xy(direction, sprite):
    """NOTES: Flips the image based on which direction the entity is facing."""
    if direction is 'right':
        return sprite
    else:
        flipped_sprite = pygame.transform.flip(sprite, True, False)
        return flipped_sprite

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
