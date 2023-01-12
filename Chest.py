from Healing_potion import Healing_potion
from Load_image import load_image
import pygame


class Chest(pygame.sprite.Sprite):
    def __init__(self, coords, *group, size=40, is_opened=False):
        super().__init__(*group)
        self.size = size
        self.is_opened = is_opened

        if self.is_opened:
            self.image = pygame.transform.scale(load_image("chest_open.png"), (self.size, self.size + 2))
        else:
            self.image = pygame.transform.scale(load_image("chest_close.png"), (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = coords[1] * size
        self.rect.y = coords[0] * size
        self.x = coords[0]
        self.y = coords[1]
        self.exp = 7
        self.size = size

    def get_item(self, *group):
        self.image = pygame.transform.scale(load_image("chest_open.png"), (self.size, self.size + 2))
        return Healing_potion(self.x + 1, self.y, group, heal=4, size=self.size)

    def get_coord(self):
        return self.x, self.y
