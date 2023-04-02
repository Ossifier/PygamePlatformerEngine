import pygame
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player


class CameraGroup:
    def __init__(self):
        super().__init__()
        self.tiles = pygame.sprite.Group()

        # Screen Scrolling Attributes
        self.world_shift_x = 0
        self.world_shift_y = 0
        self.scroll_threshold_leftx = 0.25
        self.scroll_threshold_rightx = 0.5

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

        print('Centered from CameraGroup')      # This is for testing purposes to ensure that importing works properly.

    def scroll_x_follow(self):
        """NOTES: This function scrolls the screen horizonally as the player approaches the edge of a specified
        threshold. These scrolling thresholds are controlled by the CameraGroup attributes self.scroll_threshold_leftx and
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

    def scroll_y_follow(self):
        """NOTES: This function scrolls the screen horizontally as the player approaches the edge of a specified
        threshold. This is a comparatively complex function to avoid troublesome collision bugs that can arise due to
        misalignments with the player/screen during scrolling."""

        player = self.player.sprite
        player_y = player.rect.top
        direction_y = player.direction.y

        player_speed = player.speed
        player_max_fall_speed = player.max_falling_speed
        speed_profile = player.speed_profile

        ###>>> Bottom Screen Scrolling <<<###

        if player_y > screen_height * 0.75:
            # The player is on the ground, below the scroll threshold. #
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
