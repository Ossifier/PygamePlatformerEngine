import sys

import pygame

from scripts.utils import load_image
from scripts.tilemap import Tilemap
from scripts.spritesheet import SpriteSheet

RENDER_SCALE = 0.5


class Editor:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('Editor')
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((2560, 1920))

        self.clock = pygame.time.Clock()

        self.ground_test = SpriteSheet('data/images/tile_sets/ground_test/ground_test.png')
        self.stone_test = SpriteSheet('data/images/tile_sets/stone_test/stone_test.png')
        self.ground_test_sprites = self.ground_test.build_sprite_list('static')
        self.stone_test_sprites = self.stone_test.build_sprite_list('static')

        self.assets = {
            'stone_1': [load_image('tile_sets/stone_1/stone_1.png')],
            'stone_2': [load_image('tile_sets/stone_2/stone_2.png')],
            'ground_test': self.ground_test_sprites,
            'stone_test': self.stone_test_sprites
        }
        
        self.movement = [False, False, False, False]
        
        self.tile_map = Tilemap(self, tile_size=16)
        
        try:
            self.tile_map.load('map.json')
        except FileNotFoundError:
            pass
        
        self.scroll = [0, 0]
        
        self.tile_list = list(self.assets)
        self.tile_group = 0
        self.tile_variant = 0
        
        self.clicking = False
        self.right_clicking = False
        self.shift = False
        self.on_grid = True
        
    def run(self):
        while True:
            self.display.fill((0, 0, 0))
            
            self.scroll[0] += (self.movement[1] - self.movement[0]) * 2
            self.scroll[1] += (self.movement[3] - self.movement[2]) * 2
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.tile_map.render(self.display, offset=render_scroll)
            
            current_tile_img = self.assets[self.tile_list[self.tile_group]][self.tile_variant].copy()
            current_tile_img.set_alpha(100)
            
            mpos = pygame.mouse.get_pos()
            mpos = (mpos[0] / RENDER_SCALE, mpos[1] / RENDER_SCALE)
            tile_pos = (int((mpos[0] + self.scroll[0]) // self.tile_map.tile_size), int((mpos[1] + self.scroll[1]) // self.tile_map.tile_size))
            
            if self.on_grid:
                self.display.blit(current_tile_img, (tile_pos[0] * self.tile_map.tile_size - self.scroll[0], tile_pos[1] * self.tile_map.tile_size - self.scroll[1]))
            else:
                self.display.blit(current_tile_img, mpos)
            
            if self.clicking and self.on_grid:
                self.tile_map.tilemap[str(tile_pos[0]) + ';' + str(tile_pos[1])] = {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant, 'pos': tile_pos}
            if self.right_clicking:
                tile_loc = str(tile_pos[0]) + ';' + str(tile_pos[1])
                if tile_loc in self.tile_map.tilemap:
                    del self.tile_map.tilemap[tile_loc]
                for tile in self.tile_map.offgrid_tiles.copy():
                    tile_img = self.assets[tile['type']][tile['variant']]
                    tile_r = pygame.Rect(tile['pos'][0] - self.scroll[0], tile['pos'][1] - self.scroll[1], tile_img.get_width(), tile_img.get_height())
                    if tile_r.collidepoint(mpos):
                        self.tile_map.offgrid_tiles.remove(tile)
            
            self.display.blit(current_tile_img, (5, 5))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.clicking = True
                        if not self.on_grid:
                            self.tile_map.offgrid_tiles.append(
                                {'type': self.tile_list[self.tile_group], 'variant': self.tile_variant,
                                 'pos': (mpos[0] + self.scroll[0], mpos[1] + self.scroll[1])})
                    if event.button == 3:
                        self.right_clicking = True

                if event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.clicking = False
                    if event.button == 3:
                        self.right_clicking = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_KP8:
                        self.tile_group = (self.tile_group - 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_KP2:
                        self.tile_group = (self.tile_group + 1) % len(self.tile_list)
                        self.tile_variant = 0
                    if event.key == pygame.K_KP4:
                        self.tile_variant = (self.tile_variant - 1) % len(self.assets[self.tile_list[self.tile_group]])
                    if event.key == pygame.K_KP6:
                        self.tile_variant = (self.tile_variant + 1) % len(self.assets[self.tile_list[self.tile_group]])

                    if event.key == pygame.K_a:
                        self.movement[0] = True + 4
                    if event.key == pygame.K_d:
                        self.movement[1] = True + 4
                    if event.key == pygame.K_w:
                        self.movement[2] = True + 4
                    if event.key == pygame.K_s:
                        self.movement[3] = True + 4
                    if event.key == pygame.K_g:
                        self.on_grid = not self.on_grid

                    if event.key == pygame.K_o:
                        self.tile_map.save('map.json')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.movement[0] = False
                    if event.key == pygame.K_d:
                        self.movement[1] = False
                    if event.key == pygame.K_w:
                        self.movement[2] = False
                    if event.key == pygame.K_s:
                        self.movement[3] = False

                    if event.key == pygame.K_LSHIFT:  # Change Sprite Variant
                        self.shift = False
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Editor().run()