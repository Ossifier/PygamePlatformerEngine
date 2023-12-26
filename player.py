import pygame
from spritesheets import SpriteSheet
import animate


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Player Sprite #
        self.sprite_sheet = SpriteSheet('sprites/full_sheet(test).png')
        self.animation_states = self.sprite_sheet.build_animation_state_list()
        self.sprite_dict = self.sprite_sheet.build_sprite_dict(self.animation_states)

        # Player DT:
        self.frame_correct = 0
        self.dt = 0

        # Player Animations
        self.image = self.sprite_dict['idle'][self.sprite_sheet.current_frame]
        self.rect = self.image.get_rect(topleft=pos)

        # Player Running Attributes #
        self.direction = pygame.math.Vector2(0, 0)
        self.move_acceleration = 0.25
        self.move_speed = 0
        self.max_move_speed = 4
        self.max_move_speed_test = 40000
        self.max_running_speed = self.max_move_speed * 2
        # self.gravity = 0.098723234234                 ---> DEBUG/RETEST THIS, TO DO LATER
        self.gravity = 1
        self.max_falling_speed = 10

        # Player Jumping Attributes #
        self.max_jump_power = 20
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
        self.player_state = 'idle'
        self.collision_state_x = 'none'
        self.collision_state_y = 'none'
        self.player_facing_direction = 'right'
        self.jumping = False
        self.on_ground = True
        self.running = False                        # Running applies a multiplier to run speed, costing stamina.
        self.winded = False                           # 'Winded' simulates running out of breath while running/jumping.

        # Player Winded Stats:
        self.winded_reset_threshold = 0.25           # % of stam bar that needs to be filled to clear Winded status.
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
                if self.direction.x >= self.max_move_speed:
                    pass
                else:
                    self.direction.x += self.move_acceleration
            elif self.direction.x <= 0:
                self.direction.x += self.move_acceleration * 3

        # Running Left
        elif keys[pygame.K_LEFT]:
            if self.direction.x <= 0:
                if self.direction.x <= -self.max_move_speed:
                    pass
                else:
                    self.direction.x -= self.move_acceleration
            elif self.direction.x >= 0:
                self.direction.x -= self.move_acceleration * 3

        else:
            if self.direction.x > 0.2:
                self.direction.x -= self.move_acceleration
            elif self.direction.x <= 0.2:
                self.direction.x += self.move_acceleration

            if -0.5 < self.direction.x < 0.5:
                self.direction.x = 0

        # Jumping
        if keys[pygame.K_SPACE]:
            if self.on_ground is True and self.current_jump_power >= 6:
                self.jump()
            elif self.on_ground is False and self.jumping is True and self.current_jump_power > 0:
                self.jump()
                self.current_jump_power -= 1
            else:
                self.jumping = False

        else:
            self.jumping = False

        # Sprinting
        if keys[pygame.K_d] and self.winded is False:
            self.running = True
            if self.direction.x < self.max_running_speed and keys[pygame.K_RIGHT] is True:
                self.direction.x += self.move_acceleration
            if self.direction.x > -self.max_running_speed and keys[pygame.K_LEFT] is True:
                self.direction.x -= self.move_acceleration
        else:
            self.running = False

    def assign_player_states(self):
        """NOTES: This function assigns the player states for both horizontal and vertical movement. This information
        is used to control player movement and behavior, and is also be used for specifying animations."""
        keys = pygame.key.get_pressed()
        sprite = self.sprite_sheet
        current_state = self.player_state

        # Player Facing Direction
        if self.direction.x > 0:
            self.player_facing_direction = 'right'
        elif self.direction.x < 0:
            self.player_facing_direction = 'left'

        # FIX THIS!!!!!! Check Debug Panel #
        if self.collision_state_x == 'right' and self.direction.x < 0:
            self.collision_state_x = 'none'
        elif self.collision_state_x == 'left' and self.direction.x > 0:
            self.collision_state_x = 'none'

        # Horizontal Player States
        if self.on_ground is True:
            if abs(self.direction.x) > self.max_running_speed - 1 and keys[pygame.K_d]:
                self.player_state = animate.set_new_state(sprite, 'running', current_state, 0)
            elif self.direction.x > 0 or keys[pygame.K_RIGHT]:
                self.player_state = animate.set_new_state(sprite, 'walking', current_state, 0)
            elif self.direction.x < 0 or keys[pygame.K_LEFT]:
                self.player_state = animate.set_new_state(sprite, 'walking', current_state, 0)
            else:
                self.player_state = animate.set_new_state(sprite, 'idle', current_state, 0)

        # Falling State
        if self.direction.y > 1:
            self.player_state = animate.set_new_state(sprite, 'falling', current_state, 0)
            self.on_ground = False
            if self.on_ground is False and self.jumping is False:

                animate.animate_sprite_slice(sprite, 6, 9)

        # Jumping
        if self.on_ground is False and self.jumping is True or self.direction.y < 0:  # Jump or Dir for springs.
            if self.collision_state_y == 'ceiling':                                   # Fixes Bug/Ceiling Animation Bug.
                pass
            else: 
                self.player_state = animate.set_new_state(sprite, 'jumping', current_state, 0)

    def apply_gravity(self):
        """NOTES: This function applies gravity to the player. Rate of speed increase is controlled by self.gravity,
        while max falling speed is controlled by self.max_falling_speed. These are adjustable."""
        if self.direction.y >= self.max_falling_speed:
            self.direction.y = self.max_falling_speed
        else:
            self.direction.y += self.gravity
        self.rect.y += self.direction.y * self.frame_correct

        # print(f'PLAYER FALL SPEED - CORRECT: {self.direction.y * self.frame_correct}')
        # print(f'PLAYER FALL SPEED - DIR: {self.direction.y}')
        # print(f'PLAYER FALL SPEED - MULT: {self.frame_correct}\n')

    def jump(self):
        """NOTES: This function controls player jumping behavior. Unless this grows in complexity, it may be worth
        refactoring this in some way."""

        # Jump if Player is on Ground #
        if self.on_ground is True and self.stamina > 0 and self.current_jump_power > 0:
            self.jumping = True
            self.on_ground = False
            self.direction.y = self.jump_speed
        elif self.current_jump_power > 0 and self.winded is False:
            self.direction.y = self.jump_speed

        # Set Jumping to False if Jump Power Depleted.
        if self.current_jump_power <= 1:
            self.jumping = False

    def stamina_handler(self):
        """NOTES: This function manages the player's stamina during actions like moving and jumping."""
        if (self.running is True) or abs(self.direction.x) > self.max_move_speed:
            # Sprinting Stamina Draining Mechanics #
            if self.player_state != 'idle':
                if self.stamina > 0:
                    self.stamina -= 1
                else:
                    self.stamina = 0

        else:
            # Sprinting Stamina Recharge Mechanics #
            if self.on_ground is True and (self.running is False or self.player_state == 'idle'):
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
        if self.player_state == 'walking' and (self.running is False and self.direction.x < -self.max_move_speed):
            self.direction.x += self.move_acceleration * 0.5
        elif self.player_state == 'walking' and (self.running is False and self.direction.x > self.max_move_speed):
            self.direction.x -= self.move_acceleration * 0.5

    def jump_power_handler(self):
        """NOTES This function handles jump power recharging mechanics. Basically, whenever the player is on the ground,
        the maximum height the can jump recharges over time up to a limit. """
        if self.current_jump_power < self.max_jump_power and self.on_ground is True:
            self.current_jump_power += self.jump_recharge_rate

    def animate_player(self):
        """NOTES: Animates the player sprite using the sprite_sheet dictionary and the player state as dictionary
        keys."""
        player_sprite = self.sprite_dict[self.player_state][self.sprite_sheet.current_frame]

        # Retrieve Current Sprite Frame #
        self.sprite_sheet.current_frame = animate.animate_sprite_dict(
            self.sprite_sheet,
            self.player_state)

        # Flip image based on direction and animate. #
        self.image = animate.flip_img_xy(player_sprite, self.player_facing_direction)

    def update(self):
        """NOTES: Updates the player's state, attributes and inputs."""
        self.assign_player_states()
        self.get_player_inputs()
        # self.stamina_handler()                            # Commented Out for Testing/Convenience.
        self.sprinting_handler()
        self.jump_power_handler()
        self.animate_player()

        print(f'Player Jump State: {self.jumping}')
        
