from Weapon import Weapon


class Sword(Weapon):
    def __init__(self, x, y):
        super().__init__(x, y, 2, 1)
