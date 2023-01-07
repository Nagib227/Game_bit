from Weapon import Weapon
from Load_image import load_image
import pygame


pygame.init()
screen = pygame.display.set_mode((0, 0))


class Sword(Weapon):
    image = load_image("sword.png", -1)
    
    def __init__(self, x, y, *group):
        super().__init__(x, y, 2, 1, group)
        self.image = Sword.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
