import pygame
import json


class SpriteSheet:
    def __init__(self, filename):
        # Sprite Sheet Data #
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

        # Sprite Animation Attributes #
        self.current_time = 0
        self.current_frame = 0
        self.current_state = ''
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

    def build_sprite_list(self, state):
        """NOTES: Builds a list of sprites from the sprite sheet. This function uses a JSON file loaded into the
        self.data attribute in order to coordinate how the function reads the image file and builds the frame list.
        The animation state must be supplied to properly retrieve configuration data.

        This function can be used to build sprite sheets that have simple, repeated, looping animations."""
        sheet = self.data['animation states'][state]['framelist']
        frames = len(self.data['animation states'][state]['framelist'])
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
