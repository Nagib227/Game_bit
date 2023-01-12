from Load_image import load_image
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, *group, hp=10, max_hp=10, keys=0, weapon=None, hp_potion=[], exp=0, size=30):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image("player_down.png"), (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = y * size
        self.rect.y = x * size
        self.size = size
        self.x = x
        self.y = y
        self.key = keys
        # self.key = 3
        self.hp = hp
        self.max_hp = max_hp
        self.active_weapon = weapon
        self.hp_potion = hp_potion
        self.exp = exp
        self.mask = pygame.mask.from_surface(self.image)

    def get_hp_potion(self):
        return self.hp_potion

    def set_coord(self, x, y):
        if y - self.y == 1:
            self.image = pygame.transform.scale(load_image("player_right.png"), (self.size, self.size))
        elif y - self.y == -1:
            self.image = pygame.transform.scale(load_image("player_left.png"), (self.size, self.size))
        elif x - self.x == 1:
            self.image = pygame.transform.scale(load_image("player_down.png"), (self.size, self.size))
        elif x - self.x == -1:
            self.image = pygame.transform.scale(load_image("player_up.png"), (self.size, self.size))
        self.rect.x = y * self.size
        self.rect.y = x * self.size
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y

    def chang_weapon(self, weapon):
        old = self.active_weapon
        self.active_weapon = weapon
        return old

    def set_loot(self, loot):
        if not loot:
            return None
        for i in loot:
            if i == "key":
                self.add_key()
            if i.__class__.__name__ == "Healing_potion":
                self.hp_potion.append(i)

    def set_exp(self, exp):
        self.exp += exp

    def get_exp(self):
        return self.exp

    def get_weapon(self):
        return self.active_weapon

    def damage(self, damage):
        self.hp -= damage

    def get_max_heal(self):
        return self.max_hp

    def healing(self):
        if not self.hp_potion:
            return None
        i = self.hp_potion.pop(0)
        self.hp += i.get_heal()
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_key(self):
        self.key += 1

    def get_key(self):
        return self.key

    def can_attack(self, coord_attack, field, items):
        coord_attack = coord_attack[::-1]
        x_p = self.y - coord_attack[1]
        y_p = self.x - coord_attack[0]
        x_point = abs(self.y - coord_attack[1])
        y_point = abs(self.x - coord_attack[0])
        clos_coord = []
        for i in items:
            if i.__class__.__name__ == "Chest":
                clos_coord.append(i.get_coord())
        if x_point * y_point != 0:
            print("/")
            return False
        if max(x_point, y_point) > self.active_weapon.get_field_attack():
            return False
        for i in range(x_point + 1):
            if field[self.x][min(self.y, coord_attack[1]) + i] in [20] or\
               (self.x, min(self.y, coord_attack[1]) + i) in clos_coord:
                print("f")
                return False
        for i in range(y_point + 1):
            if field[min(self.x, coord_attack[0]) + i][self.y] in [20] or\
               (min(self.x, coord_attack[0]) + i, self.y) in clos_coord:
                print("f2")
                return False
        if x_p > 0:
            self.image = pygame.transform.scale(load_image("player_left.png"), (self.size, self.size))
        elif x_p < 0:
            self.image = pygame.transform.scale(load_image("player_right.png"), (self.size, self.size))
        elif y_p > 0:
            self.image = pygame.transform.scale(load_image("player_up.png"), (self.size, self.size))
        elif y_p < 0:
            self.image = pygame.transform.scale(load_image("player_down.png"), (self.size, self.size))
        return True
