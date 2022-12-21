from Monster import Monster


class Monster_speed(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, 5, 2, 1, 5, ["key"], 10)
