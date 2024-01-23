import pygame
from scripts.entities import PhysicsEntity          # Import Hack :: imported from outside scripts directory in game.py


class Player(PhysicsEntity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.air_time = 0

        # Movement Attributes
        self.movement = pygame.math.Vector2(0, 0)

        # Jumping Attributes
        self.max_jump_count = 2
        self.jump_count = self.max_jump_count
        self.max_jump_power = 16
        self.current_jump_power = self.max_jump_power
        self.jump_speed = -12
        self.jump_recharge_rate = 1
        self.can_jump = True

        # Recovery Attributes
        self.jump_power_recharge = False
        self.jump_count_recharge = True
        self.stamina_recharge = False

        # Misc Attributes
        self.max_stamina = 200
        self.stamina = self.max_stamina

    def set_max_jumps(self):
        # Do I need to do anything with this?
        pass

    def run_and_jump(self):
        keys = pygame.key.get_pressed()

        # Running Left/Right
        if keys[pygame.K_LEFT]:
            self.movement[0] = 5
        else:
            self.movement[0] = 0
        if keys[pygame.K_RIGHT]:
            self.movement[1] = 5
        else:
            self.movement[1] = 0

        # Jumping
        if keys[pygame.K_SPACE] and self.current_jump_power > 0 and self.can_jump is True:     # Is this good?
            if self.jump_count_recharge is True and self.jump_count > 0:                       # Consider putting into
                self.jump_count -= 1                                                           # a separate function?
            elif self.jump_count <= 0:
                self.jump_count_recharge = False
            self.jump_count_recharge = False
            self.jump_power_recharge = False

            self.velocity[1] = -10
            self.current_jump_power -= 1
        else:
            self.jump_count_recharge = True
            self.can_jump = True

        if self.jump_power_recharge is True and self.current_jump_power < self.max_jump_power:
            self.current_jump_power += 1

        # Disable jumping after player runs out of jumps.
        if self.jump_count <= 0 and self.jump_count_recharge is True:
            self.can_jump = False
        else:
            self.can_jump = True

        self.set_max_jumps()

    def update(self, tile_map, movement=(0, 0)):
        super().update(tile_map, movement=movement)

        self.air_time += 1
        if self.collisions['down']:
            self.air_time = 0
            self.jump_count = self.max_jump_count
            self.jump_power_recharge = True
        if self.air_time > 4:
            self.set_action('jump')
        elif movement[0] != 0:
            self.set_action('walk')
        else:
            self.set_action('idle')
