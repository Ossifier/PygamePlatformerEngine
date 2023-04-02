import pygame
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player
from camera import CameraGroup


class Level:
    def __init__(self, level_data, surface):
        # Level Setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.player_camera.center_camera_on_player(self)

        # Screen Scrolling Attributes
        self.level_type = ''
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.scroll_threshold_leftx = 0.25
        self.scroll_threshold_rightx = 0.5
        
    def setup_level(self, layout):
        """NOTES: This function loads the level layout and adds some additional Level class attributes.. The layout
        argument can be specified by loading the appropriately named layout list from settings.py."""
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.player_camera = CameraGroup

        for row_index, row in enumerate(layout):
            for col_index, cell in enumerate(row):
                x = col_index * tile_size
                y = row_index * tile_size
                if cell == 'X':
                    tile = Tile((x, y), tile_size)
                    self.tiles.add(tile)
                if cell == 'P':
                    player_sprite = Player((x, y))
                    self.player.add(player_sprite)

    def level_camera(self):
        """NOTES: This function selects the level scrolling type from the CameraGroup class in the camera.py file. While only
        one camera function exists thus far, eventually more will be added for different types of levels like autoscrollers,
        static cameras, boss fights, ect."""
        self.player_camera.scroll_x_follow(self)
        self.player_camera.scroll_y_follow(self)

    def horizontal_movement_collision(self):
        """NOTES: This function controls horizontal collision with objects. If a collision is detected, the player
        rectangle is snapped to the proper side of the object."""
        player = self.player.sprite
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):

                # sprite.image.fill('orange')                     # For testing purposes. Can be commented out.
                if player.direction.x < 0:
                    if player.direction.x < -12:
                        player.rect.left = sprite.rect.right
                        player.direction.x = 10
                        self.world_shift_x = 0
                    else:
                        self.world_shift_x = 0
                        player.direction.x = 0
                        player.rect.left = sprite.rect.right

                elif player.direction.x > 0:
                    if player.direction.x > 12:
                        player.rect.right = sprite.rect.left
                        player.direction.x = -10
                        self.world_shift_x = 0
                    else:
                        self.world_shift_x = 0
                        player.direction.x = 0
                        player.rect.right = sprite.rect.left

    def vertical_movement_collision(self):
        """NOTES: This function handles vertical collision events. Generally, this allows the player to remain on the
        ground without falling through."""
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):

                # sprite.image.fill('purple')                     # For testing purposes. Can be commented out.
                if player.direction.y > 0:
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    if player.current_jump_power < player.max_jump_power:
                        player.current_jump_power += player.jump_recharge_rate
                        
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    if self.world_shift_y > 0:
                        player.rect.centery += self.world_shift_y

    def run(self):
        """NOTES: This function runs the level and performs updates. Called in the main.py file. The order of functions
        is very important, and misordering especially collision functions has the potential to break the level and
        player behavior."""
        # Level Tiles
        self.tiles.update(self.world_shift_x, self.world_shift_y)
        self.tiles.draw(self.display_surface)
        self.level_camera()
        self.player.draw(self.display_surface)

        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
