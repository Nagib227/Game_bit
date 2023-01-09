import pygame
from Load_image import load_image


class Healing_potion(pygame.sprite.Sprite):    
    def __init__(self, x, y, group, heal=4, size=30):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("health_potion.png"), (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = y * size
        self.rect.y = x * size
        self.size = size
        self.x = x
        self.y = y
        self.heal = heal

    def get_heal(self):
        return self.heal

    def set_coord(self, x, y):
        if x is None:
            self.rect.x = -self.size
            self.rect.y = -self.size
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y
    
