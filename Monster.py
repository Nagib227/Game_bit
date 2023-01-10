import pygame


pygame.init()
screen = pygame.display.set_mode((1, 1))


class Monster(pygame.sprite.Sprite):
    def __init__(self, x, y, group, hp=2, speed=1, damage=1, field_view=5, loot=None, exp=5, time_move=2):
        super().__init__(*group)
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.x = x
        self.y = y
        self.field_view = field_view
        self.loot = loot
        self.exp = exp
        self.time_move = time_move
        self.cur_move = 0  # [0] - частота хода, [1] - текущий ход

    def get_hp(self):
        return self.hp

    def update_img(self, move):
        pass

    def set_hp(self, damage):
        self.hp -= damage

    def get_field_view(self):
        return self.field_view

    def get_speed(self):
        return self.speed

    def get_coord(self):
        return self.x, self.y

    def set_move(self, move):
        if move == "up":
            self.x -= 1
        if move == "down":
            self.x += 1
        if move == "left":
            self.y -= 1
        if move == "right":
            self.y += 1
        self.update_img(move)

    def get_damage(self):
        return self.damage

    def get_loot(self):
        return self.loot

    def get_exp(self):
        return self.exp

    def found(self, pathArr, finPoint):
        weight = 1
        for i in range(len(pathArr) * len(pathArr[0])):
            weight += 1
            for y in range(len(pathArr)):
                for x in range(len(pathArr[y])):
                    if pathArr[y][x] == (weight - 1):
                        if y > 0 and pathArr[y - 1][x] == 0:
                            pathArr[y - 1][x] = weight
                        if y < (len(pathArr) - 1) and pathArr[y + 1][x] == 0:
                            pathArr[y + 1][x] = weight
                        if x > 0 and pathArr[y][x - 1] == 0:
                            pathArr[y][x - 1] = weight
                        if x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == 0:
                            pathArr[y][x + 1] = weight
                        if (abs(y - finPoint[0]) + abs(x - finPoint[1])) == 1:
                            pathArr[finPoint[0]][finPoint[1]] = weight
                            return True
        return False

    def printPath(self, pathArr, finPoint):
        y = finPoint[0]
        x = finPoint[1]
        weight = pathArr[y][x]
        result = list(range(weight))
        while (weight):
            weight -= 1
            if y > 0 and pathArr[y - 1][x] == weight:
                y -= 1
                result[weight] = 'down'
            elif y < (len(pathArr) - 1) and pathArr[y + 1][x] == weight:
                result[weight] = 'up'
                y += 1
            elif x > 0 and pathArr[y][x - 1] == weight:
                result[weight] = 'right'
                x -= 1
            elif x < (len(pathArr[y]) - 1) and pathArr[y][x + 1] == weight:
                result[weight] = 'left'
                x += 1
        return result[1:-1]

    def move(self, pozOut, field, monsters, items):
        pozIn = (self.x, self.y)
        labirint = field
        # path = [[x if x == 0 else -1 for x in y] for y in labirint]
        path = [[0 if x in [10, 12] else -1 for x in y] for y in labirint]
        for i in monsters:
            path[i.x][i.y] = -1
        for i in items:
            if i.__class__.__name__ == "Chest":
                path[i.x][i.y] = -1
        path[pozIn[0]][pozIn[1]] = 1
        if not self.found(path, pozOut):
            return None
        res = self.printPath(path, pozOut)
        return res

    def set_current_move(self):
        self.cur_move = (self.cur_move + 1) % self.time_move
        return not self.cur_move

    def can_move(self, coord_pl, field):
        d = {(self.x, self.y): 0}
        v = [(self.x, self.y)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= len(field[0]) or y + dy < 0 or y + dy >= len(field):
                        continue
                    if field[x + dx][y + dy] in [10, 12]:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
        dist = d.get(coord_pl[::1], -1)
        if -1 < dist <= self.field_view:
            if self.set_current_move():
                return True
