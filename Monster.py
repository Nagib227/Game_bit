class Monster:
    def __init__(self, x, y, hp, speed, damage, lyt, exp):
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.x = x
        self.y = y
        self.lyt = lyt
        self.exp = exp

    def get_hp(self):
        return self.hp

    def set_hp(self, hp):
        self.hp = hp

    def get_speed(self):
        return self.speed

    def get_coord(self):
        return self.x, self.y

    def set_move(self, move):
        if move == "up":
            self.y -= self.speed
        if move == "down":
            self.y += self.speed
        if move == "left":
            self.x -= self.speed
        if move == "right":
            self.x += self.speed

    def get_damage(self):
        return self.damage

    def get_lyt(self):
        return self.lyt

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

        return result[1:]

    def move(self, pozOut, filed):
        pozIn = (self.x, self.y)[::-1]
        pozOut = pozOut[::-1]
        labirint = []
        for i in filed:
            labirint.append(i[:])
        path = [[x if x == 0 else -1 for x in y] for y in labirint]
        path[pozIn[0]][pozIn[1]] = 1
        if not self.found(path, pozOut):
            return None
        res = self.printPath(path, pozOut)
        return res
