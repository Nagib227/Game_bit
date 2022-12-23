class Monster:
    def __init__(self, x, y, hp=2, speed=1, damage=1, field_view=5, loot=None, exp=5, time_move=2):
        # чтобы не приходилось вводить всё каждый раз + если создавать особенного монстра, чтобы было понятно что где
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.x = x
        self.y = y
        self.field_view = field_view
        self.loot = loot
        self.exp = exp
        self.timing_move = (time_move, 0)  # [0] - частота хода, [1] - текущий ход

    def get_hp(self):
        return self.hp

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
            self.y -= 1
        if move == "down":
            self.y += 1
        if move == "left":
            self.x -= 1
        if move == "right":
            self.x += 1

    def get_damage(self):
        return self.damage

    def get_loot(self):
        return self.loot

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

    def move(self, pozOut, field):
        pozIn = (self.x, self.y)[::-1]
        pozOut = pozOut[::-1]
        labirint = []
        for i in field:
            labirint.append(i[:])
        # path = [[x if x == 0 else -1 for x in y] for y in labirint]
        path = [[0 if x == 10 else -1 for x in y] for y in labirint]
        path[pozIn[0]][pozIn[1]] = 1
        if not self.found(path, pozOut):
            return None
        res = self.printPath(path, pozOut)
        return res

    def can_move(self, coord_pl, field):
        d = {(self.x, self.y)[::-1]: 0}
        v = [(self.x, self.y)[::-1]]
        while len(v) > 0:
            x, y = v.pop(0)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= len(field[0]) or y + dy < 0 or y + dy >= len(field):
                        continue
                    if field[x + dx][y + dy] in [0]:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
        dist = d.get(coord_pl[::-1], -1)
        return -1 < dist <= self.field_view
