import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((32, 64))
        self.image.fill('red')
        self.rect = self.image.get_rect(topleft=pos)

        # Player Movement
        self.direction = pygame.math.Vector2(0, 0)
        self.speed = 1
        self.max_running_speed = 8
        self.speed_profile = self.speed
        self.gravity = 1
        self.max_falling_speed = 10
        self.jump_speed = -12
        self.momentum = 0.2

        # Player States
        self.on_ground = False

    def get_input(self):
        """NOTES: This defines the general movement behavior for the player, including running, jumping
        momentum, falling, and the like. To be iterated upon later. This will likely get very complex.
        Additionally, the name may change later."""
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:

            if self.direction.x >= 0:
                if self.direction.x >= self.max_running_speed:
                    pass
                else:
                    self.direction.x += self.momentum
            elif self.direction.x <= 0:
                self.direction.x += self.momentum * 3

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

        if keys[pygame.K_SPACE]:
            self.jump()
            self.on_ground = False

        if keys[pygame.K_q]:
            print(f'Q: Player Dir_X: {self.direction.x}')
            print(f'Q: Player Dir_Y: {self.direction.y}')
            print(f'Q: Player Sp: {self.speed}')
            print(f'Q: Player Mtm: {self.momentum}')

            # print(self.rect.topleft)

            # Print(f'Direction.X: {self.direction.x}')
            # print(f'Self.Speed: {self.speed}')

    def get_player_states(self):

        if self.direction.y > 0:
            self.on_ground = False

        #if self.direction.y == 0:
        #    self.on_ground = True
        #else:
        #    self.on_ground = False
        pass

    def apply_gravity(self):
        if self.direction.y >= self.max_falling_speed:
            self.direction.y = self.max_falling_speed
            #print(self.direction.y)
        else:
            self.direction.y += self.gravity
        self.rect.y += self.direction.y

    def jump(self):
        ### Make this work in conjunction with scrolling mechanics.
        self.direction.y = self.jump_speed

    def update(self):
        self.get_player_states()
        self.get_input()
