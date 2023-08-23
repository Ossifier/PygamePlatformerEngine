import pygame
from tiles import Tile
from settings import tile_size, screen_width, screen_height
from player import Player
from camera import CameraGroup


class Level:
    def __init__(self, level_data, surface):
        # Level Setup
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.fps = 0

        # Camera Setup
        self.player_camera = CameraGroup()
        self.display_surface = surface
        self.setup_level(level_data)

        # Screen Scrolling Attributes
        self.level_camera_type = ''                # Camera selection for when multiple cameras are implemented.
        
    def setup_level(self, layout):
        """NOTES: This function loads the level layout and snaps the screen to the player's location. The layout
        argument can be specified in main.py by loading the appropriately named layout list from settings.py."""
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

        self.player_camera.snap_camera(self.player.sprite, self.tiles.sprites(), 0.25, 0.75)

    def level_camera(self):
        """NOTES: This function selects the level scrolling type from the CameraGroup class in the camera.py file. While only
        one camera function exists thus far, eventually more will be added for different types of levels like autoscrollers,
        static cameras, boss fights, ect."""
        player_sprite = self.player.sprite

        self.player_camera.scroll_x_follow(player_sprite)
        self.player_camera.scroll_y_follow(player_sprite)

    def draw_stat_bars(self):
        """Draws the Player's Stats as bars. For now, this includes the player's jump power and their stamina."""
        player = self.player.sprite
        pygame.draw.rect(self.display_surface, (255, 255, 0), (10, 10, player.stamina, 10))
        pygame.draw.rect(self.display_surface, (0, 255, 0), (10, 25, player.current_jump_power * 3, 10))

    def draw_debug_panel(self):
        player = self.player.sprite
        font = pygame.font.SysFont('courier', 15)

        WHITE = (255, 255, 255)
        DK_GREY = (35, 35, 35)

        fps = font.render(f'FPS: {round(self.fps, 3)}', True, WHITE)
        dir_x = font.render(f'Dir X: {round(player.direction.x, 3)}', True, WHITE)
        dir_y = font.render(f'Dir Y: {round(player.direction.y, 3)}', True, WHITE)
        w_shft_x = font.render(f'Wld_Shft X: {round(self.player_camera.world_shift_x, 3)}', True, WHITE)
        w_shft_y = font.render(f'Wld_Shft Y: {round(self.player_camera.world_shift_y, 3)}', True, WHITE)
        state_x = font.render(f'State X: {player.player_state_x}', True, WHITE)
        state_y = font.render(f'State Y: {player.player_state_y}', True, WHITE)
        on_grnd = font.render(f'On Grnd: {player.on_ground}', True, WHITE)
        jump = font.render(f'Jump: {player.jumping}', True, WHITE)
        jump_pwr = font.render(f'Jump Pwr: {player.current_jump_power}', True, WHITE)
        stam = font.render(f'Stamina: {player.stamina}', True, WHITE)

        

        pygame.draw.rect(self.display_surface, DK_GREY, (940, 10, 250, 175))
        self.display_surface.blit(fps, (950, 15))
        self.display_surface.blit(dir_x, (950, 30))
        self.display_surface.blit(dir_y, (950, 45))
        self.display_surface.blit(w_shft_x, (950, 60))
        self.display_surface.blit(w_shft_y, (950, 75))
        self.display_surface.blit(state_x, (950, 90))
        self.display_surface.blit(state_y, (950, 105))
        self.display_surface.blit(on_grnd, (950, 120))
        self.display_surface.blit(jump, (950, 135))
        self.display_surface.blit(jump_pwr, (950, 150))
        self.display_surface.blit(stam, (950, 165))

    def horizontal_movement_collision(self):
        """NOTES: This function controls horizontal collision with objects. If a collision is detected, the player
        rectangle is snapped to the proper side of the object.
        Directionality is determined by calculating the difference in absolute value between the different sides of the
        associated sprites. Specifically, the difference between player_right/sprite left and sprite_left/player
        right. The smaller of the two determines which side the collision occurred on, and snaps the player to that side
        of the sprite. Doing so this way eliminates a lot of troublesome bugs that arise when collisions are handled by
        checking player state and directionality, and greatly reduces function complexity."""
        player = self.player.sprite
        player.rect.x += player.direction.x * player.move_speed

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):

                sprite.image.fill('orange')     # For collision type testing purposes. Can be commented out.
                if abs(player.rect.left - sprite.rect.right) < abs(player.rect.right - sprite.rect.left):
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                    player.player_state_x = 'colliding left'
                else:
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0
                    player.player_state_x = 'colliding right'
                    
    def vertical_movement_collision(self):
        """NOTES: This function handles vertical collision events. Generally, this allows the player to remain on the
        ground without falling through. It also handles collisions with the ceiling."""
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                sprite.image.fill('purple')                     # For testing purposes. Can be commented out.
                if player.direction.y > 0:
                    # Floor Collision #
                    player.rect.bottom = sprite.rect.top
                    if self.player_camera.world_shift_y != 0:     # Corrects landing collision bugs at scroll borders
                        player.rect.centery -= player.direction.y
                    player.direction.y = 0
                    player.on_ground = True
                if player.direction.y < 0:
                    player.rect.top = sprite.rect.bottom
                    if self.player_camera.world_shift_y != 0:    # Corrects ceiling collision bugs at scroll borders.
                        self.player_camera.world_shift_y = 0
                    player.direction.y = 0
                    player.player_state_y = 'descending'
                    
    def run(self):
        """NOTES: This function runs the level and performs updates. Called in the main.py file. The order of functions
        is very important, and misordering especially collision functions has the potential to break the level and
        player behavior."""
        # Level Tiles
        self.tiles.update(self.player_camera.world_shift_x, self.player_camera.world_shift_y)
        self.tiles.draw(self.display_surface)
        self.level_camera()
        self.player.draw(self.display_surface)
        self.draw_stat_bars()
        self.draw_debug_panel()

        # Player
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
