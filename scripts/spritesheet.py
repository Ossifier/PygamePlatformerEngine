import pygame
import json


class SpriteSheet:
    def __init__(self, filename):
        # Sprite Sheet Data #
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert_alpha()
        self.meta_data = self.filename.replace('.png', '_config.json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

        # Sprite Animation Attributes #
        self.current_time = 0
        self.current_frame = 0
        self.current_state = 'idle'
        self.num_frames = 0
        self.animation_speed = 5

    def get_sprite(self, x, y, w, h):
        """NOTES: Retrieves an individual sprite from a sprite sheet image based on its position (x, y) and area
        (width, height) in the image file.

        This function can be used to build sprites or sprite sheets with static art."""
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))

        return sprite

    def build_animation_state_list(self):
        """NOTES: Builds a list of animation states from the corresponding sprite's JSON config file. It iterates
         through the animation states dictionary and returns the keys."""
        state_list = list(self.data['animationStates'].keys())
        return state_list

    def build_sprite_list(self, state):
        """NOTES: Builds a list of sprites from the sprite sheet. This function uses a JSON file loaded into the
        self.data attribute in order to coordinate how the function reads the image file and builds the frame list.
        The animation state must be supplied to properly retrieve configuration data.

        This function can be used to build sprite sheets that have simple, repeated, looping animations."""
        sheet = self.data['animationStates'][state]['frameList']
        frames = len(self.data['animationStates'][state]['frameList'])
        sprite_list = []

        for i in range(frames):
            x, y, w, h = sheet[i]['frame']['x'], sheet[i]['frame']['y'], sheet[i]['frame']['w'], sheet[i]['frame']['h']
            image = self.get_sprite(x, y, w, h)
            sprite_list.append(image)

        return sprite_list

    def build_sprite_dict(self, state_list):
        """NOTES: Builds a dictionary of lists from the sprite sheet. A list of animation states must be supplied, which
        are used as dictionary keys, to coordinate how the function reads the image file and builds the frame
        dictionary.

        This function can be used to build sprites that require complex, condition dependent animations, such as
        players, enemies, or entities that require more than frame lists."""
        sprite_dict = {}

        for i in range(len(state_list)):
            sprite_dict[state_list[i]] = self.build_sprite_list(state_list[i])

        return sprite_dict


if __name__ == '__main__':
    import pygame, sys, time

    screen = pygame.display.set_mode((1280, 960))
    display = pygame.Surface((1280, 960))
    clock = pygame.time.Clock()

    # test_sprite = SpriteSheet('../data/images/player/player_sheet.png')
    # print(test_sprite)
    # print(test_sprite.data)

    # Get sprites
    sprite_sheet = SpriteSheet('../data/images/player/player_sheet.png')

    # Get spritelists by state
    idle_sprites = sprite_sheet.build_sprite_list('idle')
    walk_sprites = sprite_sheet.build_sprite_list('walk')
    run_sprites = sprite_sheet.build_sprite_list('run')
    jump_sprites = sprite_sheet.build_sprite_list('jump')
    fall_sprites = sprite_sheet.build_sprite_list('fall')

    while True:
        display.fill((50, 50, 50))

        # display.blit(test_sprite.sprite_sheet, (0, 0))
        # display.blit(idle_sprites, (0, 0))

        for i in range(len(idle_sprites)):
            display.blit(idle_sprites[i], (i * 64, 0))
        for i in range(len(walk_sprites)):
            display.blit(walk_sprites[i], (i * 64, 100))
        for i in range(len(run_sprites)):
            display.blit(run_sprites[i], (i * 64, 200))
        for i in range(len(jump_sprites)):
            display.blit(jump_sprites[i], (i * 64, 300))
        for i in range(len(fall_sprites)):
            display.blit(fall_sprites[i], (i * 64, 400))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
        pygame.display.update()
        clock.tick(60)
