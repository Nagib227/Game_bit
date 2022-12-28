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
            
'''
        if not math.sqrt(x_point ** 2 + y_point ** 2) <= self.field_atack:
            return False
        
        x_m = round((x_point + 1) / (y_point + 1))
        x_last = x_point - x_m * y_point
        x = min(coord_pl[1], coord_atack[1])
        y = min(coord_pl[0], coord_atack[0])
        for i in range(min(coord_pl[0], coord_atack[0]),
                       max(coord_pl[0], coord_atack[0]) +
                       [1 if max(coord_pl[0], coord_atack[0]) - min(coord_pl[0], coord_atack[0]) <= 1 else 0][0]):
            y = i
            for j in range(x, x + x_m + [1 if x_m == 0 else 0][0]):
                x = j
                if i < 0 or i > len(field) or j < 0 or j > len(field[i]):
                    continue
                print(field[i][j], i, j)
                if field[i][j] in [20]:
                    return False
        for i in range(x, x + x_last):
            if field[y][i] in [20]:
                print(field[y + 1][i], y + 1, i)
                return False
        return True
'''
'''
    def can_atack(self, coord_pl, coord_atack, field, items):
        coord_pl = coord_pl[::-1]
        # print(coord_pl, coord_atack)
        y_point = abs(coord_pl[0] - coord_atack[0])
        x_point = abs(coord_pl[1] - coord_atack[1])
        # print(x_point, y_point, 222222)
        # print(not not math.sqrt(x_point ** 2 + y_point ** 2) <= self.field_atack)
        if not math.sqrt(x_point ** 2 + y_point ** 2) <= self.field_atack:
            # print(1)
            return False
        # print("###############################")
        x_p = max(x_point, y_point)
        y_point = min(x_point, y_point)
        x_point = x_p
        x_m = round((x_point + 1) / (y_point + 1))
        x_last = x_point - x_m * y_point
        x = min(coord_pl[1], coord_atack[1])
        y = min(coord_pl[0], coord_atack[0])
        coord_false = []
        for i in items:
            if i.__class__.__name__ == "Chest":
                coord_false.append((i.y, i.x))
        # print(x_m)
        for i in range(min(coord_pl[0], coord_atack[0]),
                       max(coord_pl[0], coord_atack[0]) + 1):
            y = i
            # print(i, "y")
            # print(x, x_m + 1)
            for j in range(x, x + x_m + 1):
                # print(x, "x")
                x = j
                # print(field[i][j], "f")
                if field[i][j] in [20] or (i, j)in coord_false:
                    return False
        for i in range(x, x_last):
            if field[y + 1][i] in [20] or (y + 1, i)in coord_false:
                    return False
        # print("###############################")
        # raise Exception('I know Python!')
        return True
'''
