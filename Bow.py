from Weapon import Weapon


class Bow(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y, 1, 3)
