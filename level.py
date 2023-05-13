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
        """NOTES: This function loads the level layout and adds some additional Level class attributes. The layout
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

    def draw_stat_bars(self):
        """Draws the Player's Stats as bars. For now, this includes the player's jump power (green) and their stamina (yellow).
        None of these stats function as of yet, so this is only for testing purposes for now."""
        player = self.player.sprite
        pygame.draw.rect(self.display_surface, (0, 255, 0), (10, 10, player.current_jump_power * 3, 10))
        pygame.draw.rect(self.display_surface, (255, 255, 0), (10, 25, player.stamina, 10))

    def horizontal_movement_collision(self):
        """NOTES: This function controls horizontal collision with objects. If a collision is detected, the player
        rectangle is snapped to the proper side of the object.
        
        Directionality is determined by calculating the differnece in absolute value between the different sides of the
        associated sprites. Specifically, the difference between player_right/sprite left and sprite_left/player
        right. The smaller of the two determines which side the collision occured on, and snaps the player to that side
        of the sprite. Doing so this way elimiates a lot of troublesome bugs that arise when collisions are handled by
        checking player state and directionality, and greatly reduces function complexity."""
        player = self.player.sprite
        player_state_x = player.player_state_x
        player.rect.x += player.direction.x * player.speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                sprite.image.fill('orange')     # For collision type testing purposes. Can be commented out.
                
                if abs(player.rect.left - sprite.rect.right) < abs(player.rect.right - sprite.rect.left):
                    # Left Collision #
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                    self.world_shift_x = 0
                    player.player_state_x = 'colliding left'
                else:
                    # Right Collision #
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0
                    self.world_shift_x = 0
                    player.player_state_x = 'colliding right'
                print(f'Player State X: {player.player_state_x}')  # This is for testing purposes, can be commented out.
                
    def vertical_movement_collision(self):
        """NOTES: This function handles vertical collision events. Generally, this allows the player to remain on the
        ground without falling through. It also handles collisions with the ceilings."""
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):

                sprite.image.fill('purple')                     # For testing purposes. Can be commented out.
                if player.direction.y > 0:
                    # Floor Collision #
                    player.rect.bottom = sprite.rect.top
                    player.direction.y = 0
                    player.on_ground = True
                    if player.current_jump_power < player.max_jump_power:
                        player.current_jump_power += player.jump_recharge_rate
                if player.direction.y < 0:
                    # Ceiling Collision #
                    player.rect.top = sprite.rect.bottom
                    player.direction.y = 0
                    if self.world_shift_y != 0:
                        self.world_shift_y = 0
                    if self.world_shift_y < 0:
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
        self.draw_stat_bars()

        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
