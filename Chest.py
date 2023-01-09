from Healing_potion import Healing_potion
from Load_image import load_image
import pygame


class Chest(pygame.sprite.Sprite):
    def __init__(self, coords, *group, size=30):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("chest_close.png"), (size, size))
        self.rect = self.image.get_rect()
        self.is_opened = False
        self.rect.x = coords[1] * size
        self.rect.y = coords[0] * size
        self.x = coords[0]
        self.y = coords[1]
        self.exp = 7
        self.size = size
        # if int(seed[-1]) % 2 == 0:
          #   self.item = Healing_potion(2, self.x + 1, self.y)
        # else:
          #   self.item = Speed_potion(2, 30, self.x + 1, self.y)

    def get_item(self, *group):
        self.image = pygame.transform.scale(load_image("chest_open.png"), (self.size, self.size + 2))
        return Healing_potion(self.x + 1, self.y, group, heal=2, size=self.size)

    def get_coord(self):
        return self.x, self.y
