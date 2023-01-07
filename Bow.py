from Weapon import Weapon
from Load_image import load_image
import pygame


pygame.init()
screen = pygame.display.set_mode((0, 0))


class Bow(Weapon):
    image = load_image("bow.png")
    
    def __init__(self, x, y, *group):
        super().__init__(x, y, 1, 3, group)
        self.image = Bow.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
