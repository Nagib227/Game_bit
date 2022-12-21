import math


class Weapon:
    def __init__(self, x, y, damage, field_atack):
        self.x = x
        self.y = y
        self.damage = damage
        self.field_atack = field_atack

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y

    def get_damage(self):
        return self.damage

    def get_field_atack(self):
        return self.field_atack

    def can_atack(self, coord_pl, coord_atack):
        x_point = coord_pl[0] - coord_atack[0]
        y_point = coord_pl[1] - coord_atack[1]
        return math.sqrt(x_point ** 2 + y_point ** 2) <= self.field_atack
