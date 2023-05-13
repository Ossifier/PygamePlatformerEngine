import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # Player Running Attributes
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.max_running_speed = 4
        self.max_sprinting_speed = self.max_running_speed * 2
        self.speed_profile = self.speed
        self.gravity = 1
        self.max_falling_speed = 10
        self.momentum = 0.25
        
        # Player Jumping Attributes
        self.max_jump_power = 16
        self.current_jump_power = self.max_jump_power
        self.jump_speed = -12
        self.jump_recharge_rate = 1
        
        # Player Stat Attributes
        self.max_stamina = 100
        self.stamina = self.max_stamina
        self.stamina_recharge_rate = 2
        
        # Player States
        self.player_state_x = 'idle'
        self.player_state_y = 'on ground'
        self.player_facing_direction = 'facing right'
        self.on_ground = False
        self.sprinting = False                          # Sprinting applies a multiplier to run speed, costing stamina.
        # self.winded = False                           # The 'winded' mechanic, may be added later, or removed.
        
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
            if self.on_ground is True:
                self.jump()
                if self.current_jump_power >= 1:
                    self.current_jump_power -= 1
                self.on_ground = False
            if self.on_ground is False and self.player_state_y != 'descending':
                if self.current_jump_power > 1:
                    self.jump()
                    self.current_jump_power -= 1
        # Sprinting
        if keys[pygame.K_d]:
            self.sprinting = True
            if self.player_state_x is 'running right' and self.direction.x < self.max_sprinting_speed:
                self.direction.x += self.momentum
            if self.player_state_x is 'running left' and self.direction.x > -self.max_sprinting_speed:
                self.direction.x -= self.momentum
        else:
            self.sprinting = False
            
        # Testing Statistics Return ::: Can Be Removed #
        if keys[pygame.K_q]:
            print(f'Q: Player Dir_X: {self.direction.x}')
            print(f'Q: Player Dir_Y: {self.direction.y}')
            print(f'Q: Player Sp: {self.speed}')
            print(f'Q: Player Mtm: {self.momentum}')
            
    def get_player_states(self):
        """NOTES: This function retrieves the player states for both horizontal and vertical movement. This information
        is used to control player movement and behavior, and will also be used for controlling animations."""
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
        self.direction.y = self.jump_speed
        if self.on_ground is True:
            self.stamina -= 20
            
    def stamina_handler(self):
        """NOTES: This function manages the player's stamina during actions like moving and jumping."""
        # If player stands still, and is not in the air, then their stamina recharges.
        if self.player_state_y == 'on ground' and (self.sprinting is False or self.player_state_x == 'idle'):
            if self.stamina <= self.max_stamina - self.stamina_recharge_rate:
                self.stamina += self.stamina_recharge_rate
            else:
                self.stamina = self.max_stamina
                
        # Drain stamina if the player is sprinting
        if self.sprinting is True and self.stamina >= 0:
            if self.player_state_y == 'on ground' and self.player_state_x != 'idle':
                self.stamina -= 1
        elif self.stamina < 0:
            self.stamina = 0
    
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
        
    def update(self):
        """NOTES: Updates the player's state attributes and inputs."""
        self.get_player_states()
        self.get_player_inputs()
        self.stamina_handler()
        self.sprinting_handler()
