import pygame
from tiles import Tile
from player import Player
from camera import CameraGroup


class Level:
    def __init__(self, level_data, surface):
        # Level Setup
        self.tiles = pygame.sprite.Group()
        self.player = pygame.sprite.GroupSingle()
        self.fps = 0
        self.dt = 0

        # Camera Setup
        self.player_camera = CameraGroup()
        self.display_surface = surface
        self.setup_level(level_data)

        # Screen Scrolling Attributes
        self.level_camera_type = ''                 # Camera selection for when multiple cameras are implemented.

        # Debug Panel
        self.debug = True                          # For Toggling Debug Panel

        # Test DT Multiplier
        self.game_speed = 0

    def calc_test_mult(self):
        player = self.player.sprite
        player.game_speed = self.game_speed

    def setup_level(self, layout):
        """NOTES: This function loads the level layout and snaps the screen to the player's location. The layout
        argument can be specified in main.py by loading the appropriately named layout list from settings.py."""
        tile_size = 64

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
        """NOTES: This function selects the level scrolling type from the CameraGroup class in the camera.py file. While
        only one camera function exists thus far, eventually more will be added for different types of levels like
        autoscrollers, static cameras, boss fights, ect."""
        player_sprite = self.player.sprite
        horizontal_movement = (player_sprite.direction.x * player_sprite.move_speed)

        self.player_camera.scroll_x_follow(player_sprite, self.game_speed)
        self.player_camera.scroll_y_follow(player_sprite, self.game_speed)

    def draw_stat_bars(self):
        """NOTES: Draws the Player's Stats as bars. For now, this includes the player's jump power and their stamina."""
        player = self.player.sprite
        pygame.draw.rect(self.display_surface, (255, 255, 0), (10, 10, player.stamina, 10))
        pygame.draw.rect(self.display_surface, (0, 255, 0), (10, 25, player.current_jump_power * 3, 10))

    def draw_debug_panel(self):
        """NOTES: Builds and displays debug panels for player movement, animation."""
        player = self.player.sprite
        font = pygame.font.SysFont('courier', 15)

        # player.dt = self.dt

        WHITE = (255, 255, 255)
        DK_GREY = (35, 35, 35)

        if self.debug is True: 
            fps = font.render(f'FPS: {round(self.fps, 3)}', True, WHITE)
            dt = font.render(f'DT: {round(self.dt, 5)}', True, WHITE)
            fc_corr = font.render(f'Frame Mult: {round(self.game_speed, 5)}', True, WHITE)
            pos_x = font.render(f'Pos X: {round(player.rect.centerx, 3)}', True, WHITE)
            pos_y = font.render(f'Pos Y: {round(player.rect.centery, 3)}', True, WHITE)
            dir_x = font.render(f'Dir X: {round(player.direction.x, 3)}', True, WHITE)
            dir_y = font.render(f'Dir Y: {round(player.direction.y, 3)}', True, WHITE)
            w_shft_x = font.render(f'Wld_Shft X: {round(self.player_camera.world_shift_x, 3)}', True, WHITE)
            w_shft_y = font.render(f'Wld_Shft Y: {round(self.player_camera.world_shift_y, 3)}', True, WHITE)
            on_grnd = font.render(f'On Grnd: {player.on_ground}', True, WHITE)
            jump = font.render(f'Jump: {player.jumping}', True, WHITE)
            jump_pwr = font.render(f'Jump Pwr: {round(player.current_jump_power, 3)}', True, WHITE)
            stam = font.render(f'Stamina: {player.stamina}', True, WHITE)

            pygame.draw.rect(self.display_surface, DK_GREY, (940, 10, 250, 205))
            self.display_surface.blit(fps, (950, 15))
            self.display_surface.blit(dt, (950, 30))
            self.display_surface.blit(fc_corr, (950, 45))
            self.display_surface.blit(pos_x, (950, 60))
            self.display_surface.blit(pos_y, (950, 75))
            self.display_surface.blit(dir_x, (950, 90))
            self.display_surface.blit(dir_y, (950, 105))
            self.display_surface.blit(w_shft_x, (950, 120))
            self.display_surface.blit(w_shft_y, (950, 135))
            self.display_surface.blit(on_grnd, (950, 150))
            self.display_surface.blit(jump, (950, 165))
            self.display_surface.blit(jump_pwr, (950, 180))
            self.display_surface.blit(stam, (950, 195))

            state_x = font.render(f'Ani State: {player.player_state}', True, WHITE)
            p_dir = font.render(f'Face Dir: {player.player_facing_direction}', True, WHITE)
            col_st_x = font.render(f'Col State X : {player.collision_state_x}', True, WHITE)
            col_st_y = font.render(f'Col State Y: {player.collision_state_y}', True, WHITE)
            num_fr = font.render(f'Num Frms: {player.sprite_sheet.num_frames}', True, WHITE)
            curr_fr = font.render(f'Curr Frm: {player.sprite_sheet.current_frame + 1}', True, WHITE)
            curr_t = font.render(f'Curr Time: {player.sprite_sheet.current_time}', True, WHITE)
            anim_sp = font.render(f'Anim Spd: {player.sprite_sheet.animation_speed}', True, WHITE)


            pygame.draw.rect(self.display_surface, DK_GREY, (940, 225, 250, 130))
            self.display_surface.blit(state_x, (950, 230))
            self.display_surface.blit(p_dir, (950, 245))
            self.display_surface.blit(col_st_x, (950, 260))
            self.display_surface.blit(col_st_y, (950, 275))
            self.display_surface.blit(num_fr, (950, 290))
            self.display_surface.blit(curr_fr, (950, 305))
            self.display_surface.blit(curr_t, (950, 320))
            self.display_surface.blit(anim_sp, (950, 335))

            # pygame.draw.rect(self.display_surface, DK_GREY, (940, 350, 250, 115))         # For Addt'l Debug Vals

    def horizontal_movement_collision(self):
        """NOTES: This function controls horizontal collision with objects. If a collision is detected, the player
        rectangle is snapped to the proper side of the object.
        Directionality is determined by calculating the difference in absolute value between the different sides of the
        associated sprites. Specifically, the difference between player_right/sprite left and sprite_left/player
        right. The smaller of the two determines which side the collision occurred on, and snaps the player to that side
        of the sprite. Doing so this way eliminates a lot of troublesome bugs that arise when collisions are handled by
        checking player state and directionality, and greatly reduces function complexity."""
        player = self.player.sprite
        horizontal_movement = (player.direction.x * player.move_speed)

        player.rect.x += round(horizontal_movement * self.game_speed)

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):
                sprite.image.fill('orange')         # For collision type testing purposes. Can be removed.
                if abs(player.rect.left - sprite.rect.right) < abs(player.rect.right - sprite.rect.left):
                    player.rect.left = sprite.rect.right
                    player.direction.x = 0
                    player.collision_state_x = 'left'
                elif abs(player.rect.left - sprite.rect.right) > abs(player.rect.right - sprite.rect.left):
                    player.rect.right = sprite.rect.left
                    player.direction.x = 0
                    player.collision_state_x = 'right'
                    
    def vertical_movement_collision(self):
        """NOTES: This function handles vertical collision events. Generally, this allows the player to remain on the
        ground without falling through. It also handles collisions with the ceiling."""
        player = self.player.sprite
        player.apply_gravity()

        for sprite in self.tiles.sprites():
            if sprite.rect.colliderect(player.rect):

                sprite.image.fill('purple')                     # For testing purposes. Can be removed.
                if player.direction.y > 0:
                    # Floor Collision #
                    player.rect.bottom = sprite.rect.top
                    if self.player_camera.world_shift_y != 0:   # Corrects landing collision bugs at scroll borders
                        player.rect.centery -= player.direction.y * self.game_speed
                    player.direction.y = 0
                    player.on_ground = True
                if player.direction.y < 0:
                    # Ceiling Collision #
                    player.rect.top = sprite.rect.bottom
                    player.jumping = False
                    if self.player_camera.world_shift_y != 0:    # Corrects ceiling collision bugs at scroll borders.
                        self.player_camera.world_shift_y = 0     # !!! There is still a very rare collision bug that
                    player.direction.y = 0                       # occurs at scroll thresholds !!!
                    player.collision_state_y = 'ceiling'
                else:
                    player.collision_state_y = 'none'
                    
    def run(self):
        """NOTES: This function runs the level and performs updates. Called in the main.py file. The order of functions
        is very important, and misordering especially collision functions has the potential to break the level and
        player behavior."""
        # Calc DT
        self.calc_test_mult()

        # Level Setup
        self.tiles.update(self.player_camera.world_shift_x, self.player_camera.world_shift_y)
        self.tiles.draw(self.display_surface)
        self.level_camera()

        # Player Setup
        self.player.draw(self.display_surface)
        self.draw_stat_bars()
        self.draw_debug_panel()
        self.player.update()
        self.horizontal_movement_collision()
        self.vertical_movement_collision()
