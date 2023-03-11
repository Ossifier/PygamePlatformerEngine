import pygame
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player


class Level:
    def __init__(self, level_data, surface):
        # Level Setup
        self.display_surface = surface
        self.setup_level(level_data)
        self.center_camera_on_player()

        # Screen Scrolling Attributes
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.scroll_threshold_leftx = 0.25
        self.scroll_threshold_rightx = 0.5
        
    def setup_level(self, layout):
        """NOTES: This function loads the level layout. The layout argument can be specified by loading the
        appropriately named layout list from settings.py."""
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()

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

    def center_camera_on_player(self):
        """NOTES: This function centers the camera and the level on the player. Called when a level begins to place the
        player appropriately on the screen. This prevents the player from being placed off screen at the beginning
        of loading the level, forcing the screen to scroll to catch up with their position."""
        player = self.player.sprite

        player_x = player.rect.centerx
        player_y = player.rect.centery
        cam_adjust_x = screen_width * 0.25
        cam_adjust_y = screen_height * 0.75
        level_shift_x = player_x - cam_adjust_x
        level_shift_y = player_y - cam_adjust_y

        ### Center Player on Screen ###
        player.rect.centerx = cam_adjust_x
        player.rect.centery = cam_adjust_y

        ### Shift Level to Player's Location ###
        for sprite in self.tiles.sprites():
            sprite.rect.centerx -= level_shift_x
            sprite.rect.centery -= level_shift_y

    def scroll_x(self):
        """NOTES: This function scrolls the screen horizonally as the player approaches the edge of a specified
        threshold. These scrolling thresholds are controlled by the Level attributes self.scroll_threshold_leftx and
        self.scroll_threshold_rightx. They can be adjusted to meet the needs of a particular stage."""
        player = self.player.sprite
        player_x = player.rect.centerx
        direction_x = player.direction.x

        speed_profile = player.speed_profile

        if player_x < screen_width * self.scroll_threshold_leftx and direction_x < 0:
            self.world_shift_x = -round(direction_x) * speed_profile
            player.speed = 0
        elif player_x > screen_width * self.scroll_threshold_rightx and direction_x > 0:
            self.world_shift_x = -round(direction_x) * speed_profile
            player.speed = 0
        else:
            self.world_shift_x = 0
            player.speed = 1
            
    def scroll_y(self):
        """NOTES: This function scrolls the screen horizonally as the player approaches the edge of a specified
        threshold. This is a comparatively complex function to avoid troublesome collision bugs that can arise due to
        misalignments with the player/screen during scrolling."""
        player = self.player.sprite
        player_y = player.rect.top
        direction_y = player.direction.y

        player_speed = player.speed
        player_max_fall_speed = player.max_falling_speed
        speed_profile = player.speed_profile

        player_momentum = player.momentum

        ###>>> Bottom Screen Scrolling <<<###
        if player_y > screen_height * 0.75:
            # The player is on the ground, below the scroll threshold. #
            print('TEST1')
            if player.on_ground is True:
                if player_y > 0 and self.world_shift_y == 0:
                    player.rect.centery += player.direction.y
                if player_y > 0 and self.world_shift_y == -player_max_fall_speed:
                    player.rect.centery += self.world_shift_y
                    for sprite in self.tiles.sprites():
                        sprite.rect.centery += player.direction.y

                else:
                    self.world_shift_y = -player_max_fall_speed

            elif player.on_ground is False:
                # The player is in the air, below the scroll threshold.
                if self.world_shift_y <= 0:
                    self.world_shift_y = 0
                elif self.world_shift_y == 0:
                    player.rect.centery += player.direction.y
                    for sprite in self.tiles.sprites():
                        sprite.rect.centery += player.direction.y

                    self.world_shift_y = -player_max_fall_speed
                    player.rect.centery -= player.direction.y

        ###>>> Top Screen Scrolling <<<###
        elif player_y < screen_height * 0.50:
            # Player is in the air, and very high on the screen. #
            if player.on_ground is False and player_y < screen_height * 0.25:
                if player.direction.y < 0:
                    if self.world_shift_y == 0:
                        player.rect.centery += player.direction.y

                    self.world_shift_y = -player.direction.y
                    player.rect.centery -= player.direction.y

                else:
                    self.world_shift_y = 0
            # Player is in the air, and somewhat high on the screen. #
            elif player.on_ground is False and player_y > screen_height * 0.25:
                self.world_shift_y = 0
            # Player is on the ground, and high on the screen. #
            elif player.on_ground is True:
                if self.world_shift_y == 0:
                    player.rect.centery += player.direction.y
                if self.world_shift_y == player_max_fall_speed:
                    player.rect.centery += player_max_fall_speed
                    for sprite in self.tiles.sprites():
                        sprite.rect.centery += player.direction.y

                else:
                    self.world_shift_y = player_max_fall_speed

        ###>>> Player is Centered Within Scrolling Boundary <<<###
        else:
            if self.world_shift_y != 0:
                player.rect.centery += self.world_shift_y
            self.world_shift_y = 0
            
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
        self.scroll_x()
        self.scroll_y()
        self.player.draw(self.display_surface)

        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
        
