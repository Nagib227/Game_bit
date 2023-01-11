from Monster import Monster
from Load_image import load_image
import pygame


class Monster_speed(Monster):
    image = load_image("monster_speed_down.png")
    
    def __init__(self, x, y, *group, size=30):
        super().__init__(x, y, group, hp=5, speed=2, field_view=7, loot=["key"], exp=10)
        self.image = pygame.transform.scale(Monster_speed.image, (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = y * size
        self.rect.y = x * size
        self.size = size

    def update_img(self, move):
        self.image = pygame.transform.scale(load_image(f"monster_speed_{move}.png"), (self.size, self.size))
        self.rect.x = self.y * self.size
        self.rect.y = self.x * self.size
