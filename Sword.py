from Weapon import Weapon
from Load_image import load_image
import pygame


class Sword(Weapon):
    image = load_image("sword.png")
    
    def __init__(self, x, y, *group, size=40):
        super().__init__(x, y, 2, 1, group)
        self.image = pygame.transform.scale(Sword.image, (size, size))
        self.rect = self.image.get_rect()
        if x is not None:
            self.rect.x = y * size
            self.rect.y = x * size
        self.size = size

    def get_img(self):
        return Sword.image

    def none_draw(self):
        self.rect.x = -self.size
        self.rect.y = -self.size

    def true_draw(self, x, y):
        self.rect.x = y * self.size
        self.rect.y = x * self.size
