import pygame
from spritesheets import SpriteSheet


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Player Sprite #
        self.sprite_sheet = SpriteSheet('TestSprites/full_sheet.png')
        self.sprite_list_idle = self.sprite_sheet.build_sprite_list('running')   # Animation state can be changed.
        self.image = self.sprite_list_idle[0]                          # For testing currently, index # can be changed.
        self.rect = self.image.get_rect(topleft=pos)

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
        self.player_state_y = 'on ground'
        self.player_facing_direction = 'facing right'
        self.jumping = False
        self.on_ground = False
        self.sprinting = False                        # Sprinting applies a multiplier to run speed, costing stamina.
        self.winded = False                           # 'Winded' simulates running out of breath while running/jumping.

        # Player Winded Stats:
        self.winded_reset_threshold = 0.5           # % of stam bar needed to be filled to clear Winded status.
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
