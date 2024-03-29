import pygame
from Load_image import load_image


class Healing_potion(pygame.sprite.Sprite):    
    def __init__(self, x, y, *group, heal=4, size=40):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("health_potion.png"), (size, size))
        self.rect = self.image.get_rect()
        if y is None or x is None:
            self.rect.x = -size
            self.rect.y = -size
        if y is not None and x is not None:
            self.rect.x = y * size
            self.rect.y = x * size
        self.x = x
        self.y = y
        self.heal = heal
        self.size = size

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
    
