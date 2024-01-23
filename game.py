import sys

import pygame

from scripts.utils import load_image, load_images, Animation
# from scripts.entities import PhysicsEntity, Player
from scripts.player import Player
from scripts.tilemap import Tilemap
from scripts.clouds import Clouds

from scripts.spritesheet import SpriteSheet


class Game:
    def __init__(self):
        pygame.init()

        pygame.display.set_caption('ninja game')
        self.screen = pygame.display.set_mode((1280, 960))
        self.display = pygame.Surface((1280, 960))

        self.clock = pygame.time.Clock()
        
        # self.movement = [False, False]
        # self.movement = pygame.math.Vector2(0, 0)

        self.player_sprite_sheet = SpriteSheet('data/images/player/player_sheet.png')
        self.idle_sprites = self.player_sprite_sheet.build_sprite_list('idle')
        self.walk_sprites = self.player_sprite_sheet.build_sprite_list('walk')
        self.run_sprites = self.player_sprite_sheet.build_sprite_list('run')
        self.jump_sprites = self.player_sprite_sheet.build_sprite_list('jump')
        self.fall_sprites = self.player_sprite_sheet.build_sprite_list('fall')

        self.ground_test = SpriteSheet('data/images/tile_sets/ground_test/ground_test.png')
        self.stone_test = SpriteSheet('data/images/tile_sets/stone_test/stone_test.png')
        self.ground_test_sprites = self.ground_test.build_sprite_list('static')
        self.stone_test_sprites = self.stone_test.build_sprite_list('static')

        self.assets = {
            'player': load_image('player/player.png'),
            'player_idle': self.idle_sprites[0],
            'player_fall': self.fall_sprites[3],
            'stone_1': [load_image('tile_sets/stone_1/stone_1.png')],
            'stone_2': [load_image('tile_sets/stone_2/stone_2.png')],
            # 'background': load_image('background.png'),
            'clouds': load_image('tile_sets/clouds/test_cloud.png'),
            'ground_test': self.ground_test_sprites,
            'stone_test': self.stone_test_sprites,

            'player/idle': Animation(self.idle_sprites, img_dur=6),
            'player/walk': Animation(self.walk_sprites, img_dur=4),
            'player/run': Animation(self.run_sprites, img_dur=4),
            'player/jump': Animation(self.jump_sprites, img_dur=4),
            'player/fall': Animation(self.fall_sprites, img_dur=4)
        }
        
        self.clouds = Clouds(self.assets['clouds'], count=16)
        
        self.player = Player(self, (50, 50), (64, 64))
        self.movement = self.player.movement
        
        self.tilemap = Tilemap(self, tile_size=64)
        self.tilemap.load('map.json')
        
        self.scroll = [0, 0]
        
    def run(self):
        while True:
            # self.display.blit(self.assets['background'], (0, 0))
            self.display.fill((50, 50, 50))
            
            self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30
            self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30
            render_scroll = (int(self.scroll[0]), int(self.scroll[1]))
            
            self.clouds.update()
            self.clouds.render(self.display, offset=render_scroll)
            
            self.tilemap.render(self.display, offset=render_scroll)
            
            self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))
            self.player.render(self.display, offset=render_scroll)

            self.player.run_and_jump()

            pygame.draw.rect(self.display, (255, 255, 0), (10, 10, self.player.stamina, 10))
            pygame.draw.rect(self.display, (0, 255, 0), (10, 25, self.player.current_jump_power * 3, 10))

            events = pygame.event.get()

            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.player.run_and_jump()

            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)


Game().run()
