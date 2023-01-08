import pygame
from Load_image import load_image


class Bit(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image("bit.png"), (30, 50))

    def __init__(self, x, y, speed, f, *group):
        super().__init__(*group)
        self.image = Bit.image
        self.rect = self.image.get_rect()
        self.start = (x, y)
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.f = f

    def update(self):
        self.rect = self.rect.move(self.speed, 0)

    def set_start(self):
        self.rect.x = self.start[0]
        self.rect.y = self.start[1]
