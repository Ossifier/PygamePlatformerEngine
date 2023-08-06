import pygame
from spritesheets import SpriteSheet
import animate


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Player Sprite #
        self.sprite_sheet = SpriteSheet('sprites/full_sheet.png')
        self.animation_states = self.sprite_sheet.build_animation_state_list()
        self.sprite_dict = self.sprite_sheet.build_sprite_dict(self.animation_states)
        # self.active_sprite_list = self.sprite_sheet.build_sprite_list('idle')

        # Player Animations
        # self.frame_index = 0
        self.image = self.sprite_dict['running'][self.sprite_sheet.current_frame]
        self.rect = self.image.get_rect(topleft=pos)

        # Player Animation Tests

        # Player Running Attributes #
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.max_running_speed = 4
        self.max_sprinting_speed = self.max_running_speed * 2
        self.speed_profile = self.speed
        self.gravity = 1
        self.max_falling_speed = 10
        self.momentum = 0.25

        # Player Jumping Attributes #
        self.max_jump_power = 16
        self.current_jump_power = self.max_jump_power
        self.jump_speed = -12
        self.jump_recharge_rate = 1

        # Player Stat Attributes #
        self.max_health = 1
        self.current_health = 1
        self.max_stamina = 200
        self.stamina = self.max_stamina
        self.stamina_recharge_rate = 2

        # Player States #
        self.player_state_x = 'idle'
        self.player_state_x_test = 'idle'             # This is for testing animations, to be deleted.
        self.player_state_y = 'on ground'
        self.player_facing_direction = 'right'
        self.jumping = False
        self.on_ground = False
        self.sprinting = False                        # Sprinting applies a multiplier to run speed, costing stamina.
        self.winded = False                           # 'Winded' simulates running out of breath while running/jumping.

        # Player Winded Stats:
        self.winded_reset_threshold = 0.5           # % of stam bar that needs to be filled to clear Winded status.
        self.winded_stamina_recharge_penalty = 0.125    # % reduction of stam bar recharge on being Winded.
        self.winded_stamina_jump_penalty = 0.5

    def get_player_inputs(self):
        """NOTES: This defines the general movement behavior for the player, including running, jumping
        momentum, falling, and the like. To be iterated upon later. This will likely get very complex.
        Additionally, the name may change later."""
        keys = pygame.key.get_pressed()

        # Running Right
        if keys[pygame.K_RIGHT]:
            if self.direction.x >= 0:
                if self.direction.x >= self.max_running_speed:
                    pass
                else:
                    self.direction.x += self.momentum
            elif self.direction.x <= 0:
                self.direction.x += self.momentum * 3

        # Running Left
        elif keys[pygame.K_LEFT]:
            if self.direction.x <= 0:
                if self.direction.x <= -self.max_running_speed:
                    pass
                else:
                    self.direction.x -= self.momentum
            elif self.direction.x >= 0:
                self.direction.x -= self.momentum * 3

        else:
            if self.direction.x > 0.2:
                self.direction.x -= self.momentum
            elif self.direction.x <= 0.2:
                self.direction.x += self.momentum

            if -0.5 < self.direction.x < 0.5:
                self.direction.x = 0

        # Jumping
        if keys[pygame.K_SPACE]:
            if self.on_ground is True and self.current_jump_power >= 6:
                self.jump()
                self.on_ground = False
            elif self.on_ground is False and self.jumping is True and self.player_state_y == 'ascending':
                if self.current_jump_power > 0:
                    self.jump()
                    self.current_jump_power -= 1
            else:
                self.jumping = False

        else:
            self.jumping = False

        # Sprinting
        if keys[pygame.K_d] and self.winded is False:
            self.sprinting = True
            if self.direction.x < self.max_sprinting_speed and keys[pygame.K_RIGHT] is True:
                self.direction.x += self.momentum
            if self.direction.x > -self.max_sprinting_speed and keys[pygame.K_LEFT] is True:
                self.direction.x -= self.momentum
        else:
            self.sprinting = False

        # Testing Return (Press Q to Print Movement Stats) #
        if keys[pygame.K_q]:
            print(f'Q: Player Dir_X: {self.direction.x}')
            print(f'Q: Player Dir_Y: {self.direction.y}')
            print(f'Q: Player Sp: {self.speed}')
            print(f'Q: Player Mtm: {self.momentum}')

    def get_player_states(self):
        """NOTES: This function retrieves the player states for both horizontal and vertical movement. This information
        is used to control player movement and behavior, and will also be used for specifying animations."""
        keys = pygame.key.get_pressed()

        # Horizontal Player States
        if self.direction.x == 0 and self.on_ground is True:
            self.player_state_x = 'idle'

        if self.direction.x > 0 and keys[pygame.K_RIGHT] is True:
            self.player_state_x = 'running right'
            self.player_facing_direction = 'right'
        elif self.direction.x > 0 and keys[pygame.K_LEFT] is True:
            self.player_state_x = 'running right turning left'

        if self.direction.x < 0 and keys[pygame.K_LEFT] is True:
            self.player_state_x = 'running left'
            self.player_facing_direction = 'left'
        elif self.direction.x < 0 and keys[pygame.K_RIGHT] is True:
            self.player_state_x = 'running left turning right'

        # Vertical Player States
        if self.direction.y > 1:
            self.player_state_y = 'descending'
            self.on_ground = False
        elif self.direction.y < 0:
            self.player_state_y = 'ascending'

        # Grounded Player States
        if self.direction.y == 0:
            if self.on_ground is False:
                pass
            else:
                self.player_state_y = 'on ground'

    def apply_gravity(self):
        """NOTES: This function applies gravity to the player. Rate of speed increase is controlled by self.gravity,
        while max falling speed is controlled by self.max_falling_speed. These are adjustable."""
        if self.direction.y >= self.max_falling_speed:
            self.direction.y = self.max_falling_speed
        else:
            self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        """NOTES: This function controls player jumping behavior. Unless this grows in complexity, it may be worth
        refactoring this in some way."""

        # Jump if Player is on Ground #
        if self.on_ground is True:
            self.jumping = True
            self.on_ground = False
            self.direction.y = self.jump_speed
        elif self.current_jump_power > 0 and self.winded is False:
            self.direction.y = self.jump_speed

    def stamina_handler(self):
        """NOTES: This function manages the player's stamina during actions like moving and jumping."""
        if (self.sprinting is True) or abs(self.direction.x) > self.max_running_speed:
            # Sprinting Stamina Draining Mechanics #
            if self.player_state_x != 'idle' and self.player_state_y != 'descending':
                if self.stamina > 0:
                    self.stamina -= 1
                else:
                    self.stamina = 0

        else:
            # Sprinting Stamina Recharge Mechanics #
            if self.player_state_y == 'on ground' and (self.sprinting is False or self.player_state_x == 'idle'):
                if self.stamina <= (self.max_stamina - self.stamina_recharge_rate) and self.winded is False:
                    self.stamina += self.stamina_recharge_rate
                elif self.stamina <= self.max_stamina - self.stamina_recharge_rate and self.winded is True:
                    self.stamina += (self.stamina_recharge_rate * self.winded_stamina_recharge_penalty)
                else:
                    self.stamina = self.max_stamina

        if self.jumping is True and self.on_ground is False and self.direction.y != 0:
            self.stamina -= 2

        if self.winded is True and self.stamina >= (self.max_stamina * self.winded_reset_threshold):
            self.winded = False

        if self.stamina <= 0:
            self.stamina = 0
            self.winded = True

    def sprinting_handler(self):
        """NOTES: This function handles the sprinting and running speed mechanics. Causes the player to slow as down
        to their max running speed as long as they aren't holding the sprint button."""

        # Slow Down Player if Sprint Button Isn't Held #
        if self.player_state_x == 'running left':
            if self.sprinting is False and self.direction.x < -self.max_running_speed:
                self.direction.x += self.momentum * 0.5
        elif self.player_state_x == 'running right':
            if self.sprinting is False and self.direction.x > self.max_running_speed:
                self.direction.x -= self.momentum * 0.5

    def jump_power_handler(self):
        """NOTES This function handles jump power recharging mechanics. Basically, whenever the player is on the ground,
        the maximum height the can jump recharges over time up to a limit. """
        if self.current_jump_power < self.max_jump_power and self.on_ground is True:
            self.current_jump_power += self.jump_recharge_rate

    def animate_player(self):
        ########################
        ### FOR TESTING ONLY ###
        ########################

        # Retrieve current sprite frame #
        self.sprite_sheet.current_frame = animate.animate_sprite_dict(
            self.sprite_sheet,
            self.player_state_x_test)

        # Gather user States (To Be Removed when all animation state sheets are complete and integrated) #
        # Consider moving this to the animate.py module. Only for testing now. #
        if self.direction.x != 0 or self.direction.y != 0:
            if self.player_state_x_test != 'running':
                self.sprite_sheet.current_frame = 0
            self.player_state_x_test = 'running'
        else:
            if self.player_state_x_test != 'idle':
                self.sprite_sheet.current_frame = 0
            self.player_state_x_test = 'idle'

        # Flip sprite according to direction player is facing. #
        # Consider moving this to the animate.py module. Only for testing now. #
        if self.player_facing_direction is 'right':
            self.image = self.sprite_dict[self.player_state_x_test][self.sprite_sheet.current_frame]
        elif self.player_facing_direction is 'left':
            img_flip = pygame.transform.flip(
                self.sprite_dict[self.player_state_x_test][self.sprite_sheet.current_frame],
                True, False)
            self.image = img_flip

        ########################
        ### FOR TESTING ONLY ###
        ########################

    def update(self):
        """NOTES: Updates the player's state attributes and inputs."""
        self.get_player_states()
        self.get_player_inputs()
        self.stamina_handler()
        self.sprinting_handler()
        self.jump_power_handler()
        self.animate_player()


if __name__ == '__main__':
    pygame.init()
    DISPLAY_W, DISPLAY_H = 1000, 500
    canvas = pygame.Surface((DISPLAY_W, DISPLAY_H))
    window = pygame.display.set_mode((DISPLAY_W, DISPLAY_H))
    pygame.display.set_caption('[player.py]')
    clock = pygame.time.Clock()
    FPS = 60

    PLAYER = Player((0, 0))

    run = True
    while run:

        canvas.fill((50, 50, 50))

        ### TO FIX LATER ###
        index_test = animate.animate_sprite_dict(
            PLAYER.sprite_sheet,
            PLAYER.sprite_sheet.current_state)

        # print(f'PLAYER SPRITE SHEET: {PLAYER.sprite_sheet}\n'
        #       f'PLAYER SPRITE DICT: {PLAYER.sprite_dict}\n'
        #       f'PLAYER SPRITE SHEET - Current State: {PLAYER.sprite_sheet.current_state}\n'
        #       f'PLAYER SPRITE SHEET - Current Frame: {PLAYER.sprite_sheet.current_frame}\n'
        #       f'PLAYER SPRITE SHEET - Current Time: {PLAYER.sprite_sheet.current_time}')
        ### TO FIX LATER ###

        canvas.blit(PLAYER.sprite_dict[PLAYER.player_state_x][index_test], (0, 0))
        canvas.blit(PLAYER.image, (0, 64))
        window.blit(canvas, (0, 0))
        pygame.display.update()

        ### TEST ANIMATIONS ###
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    # print('K_UP')
                    PLAYER.player_state_x = 'idle'
                    PLAYER.sprite_sheet.current_frame = 0
                    PLAYER.sprite_sheet.current_time = 0
                if event.key == pygame.K_DOWN:
                    # print('K_DOWN')
                    PLAYER.player_state_x = 'running'
                    PLAYER.sprite_sheet.current_frame = 0
                    PLAYER.sprite_sheet.current_time = 0

            ### QUIT ###
            if event.type == pygame.QUIT:
                run = False

        clock.tick(FPS)
