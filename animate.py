import pygame
from spritesheets import SpriteSheet


def flip_img_xy(sprite, direction):
    """NOTES: Flips the image based horizontally depending on which direction the entity is facing."""
    if direction == 'right':
        return sprite
    else:
        flipped_sprite = pygame.transform.flip(sprite, True, False)
        return flipped_sprite

    
def set_new_state(sprite, new_state, old_state, start_frame):
    """NOTES: Changes entity states. The first animation frame of the new state can be set with start_fr."""
    if new_state != old_state:
        sprite.current_frame = start_frame
    return new_state


def animate_sprite_slice(sprite, start_fr, end_fr):
    """NOTES: Animates a subsection of a sprite list."""
    if sprite.current_frame == end_fr and sprite.current_time == sprite.animation_speed:
        sprite.current_frame = start_fr
        sprite.current_time = 0


def animate_sprite_dict(sprite, state, game_speed):
    """NOTES: Returns the next frame in the animation sequence for a sprite dictionary. Uses the sprite's loaded data,
    along with its current state to check against the current number of frames that have elapsed since the frame
    changed. If it is equal or larger, then it adds to the frame index, and resets the frame index back to zero if it is
    larger than the length of the state frame list."""
    sprite.num_frames = len(sprite.data['animationStates'][state]['frameList'])

    print(f'Num Frames: {sprite.num_frames}')
    print(f'Frame Advance Speed: {game_speed}')

    if sprite.current_time != 0 and sprite.current_time % sprite.animation_speed == 0:
        if sprite.current_frame >= sprite.num_frames - 1:
            sprite.current_frame = -1
        sprite.current_frame += 1
        sprite.current_time = -1

    sprite.current_time += round(game_speed)                    # NEEDS BETTER ALGORITHM, but it sort of works for now.

    return sprite.current_frame
