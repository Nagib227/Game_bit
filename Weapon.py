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

    def can_atack(self, coord_pl, coord_atack, field):
        y_point = abs(coord_pl[0] - coord_atack[0])
        x_point = abs(coord_pl[1] - coord_atack[1])
        print(x_point, y_point)
        if not math.sqrt(x_point ** 2 + y_point ** 2) <= self.field_atack:
            return False
        
        x_m = round((x_point + 1) / (y_point + 1))
        x_last = x_point - x_m * y_point
        x = min(coord_pl[1], coord_atack[1])
        y = min(coord_pl[0], coord_atack[0])
        a = 0
        for i in range(min(coord_pl[0], coord_atack[0]),
                       max(coord_pl[0], coord_atack[0])):
            y = i
            for j in range(x, x_m):
                x = j
                if field[i][j] == 1:
                    return False
        for i in range(x, x_last):
            if field[y + 1][i] == 1:
                    return False
        return True
