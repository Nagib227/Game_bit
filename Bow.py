from Weapon import Weapon
from Load_image import load_image
import pygame


class Bow(Weapon):
    image = load_image("bow.png")
    
    def __init__(self, x, y, *group, size=40):
        super().__init__(x, y, 1, 3, group)
        self.image = pygame.transform.scale(Bow.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = y * size
        self.rect.y = x * size
        self.size = size
    
    def get_img(self):
        return Bow.image

    def none_draw(self):
        self.rect.x = -self.size
        self.rect.y = -self.size

    def true_draw(self, x, y):
        self.rect.x = y * self.size
        self.rect.y = x * self.size
