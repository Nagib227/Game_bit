import pygame
from Load_image import load_image


class Heart_bit(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("heart_bit.png"), (70, 80))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Heart_bit.image
        self.rect = self.image.get_rect()
        self.start = (x, y)
        self.rect.x = x
        self.rect.y = y

    def update(self, m):
        if m:
            self.image = pygame.transform.scale(load_image("heart_bit.png"), (150, 130))
            self.rect.x = self.start[0] - 25
            self.rect.y = self.start[1] - 25
        else:
            self.image = pygame.transform.scale(load_image("heart_bit.png"), (70, 80))
            self.rect.x = self.start[0]
            self.rect.y = self.start[1]
