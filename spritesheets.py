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

    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite

    def build_sprite_list(self, state):
        sheet = self.data['animation states'][state]['framelist']
        sprite_list = []
        frames = self.data['animation states'][state]['data']['num of frames']

        for i in range(frames):
            x, y, w, h = sheet[i]['frame']['x'], sheet[i]['frame']['y'], sheet[i]['frame']['w'], sheet[i]['frame']['h']
            image = self.get_sprite(x, y, w, h)
            sprite_list.append(image)

        return sprite_list

    def build_sprite_dict(self, state_list):
        sprite_dict = {}

        for i in range(len(state_list)):
            sprite_dict[state_list[i]] = self.build_sprite_list(state_list[i])

        return sprite_dict
