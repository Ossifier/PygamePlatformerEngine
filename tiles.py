import pygame


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill('grey')
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift, y_shift):
        """NOTES: This function updates the position of the level. This is used to control level scrolling behavior
        via the x_shift and y_shift arguments."""
        self.rect.x += x_shift
        self.rect.y += y_shift
