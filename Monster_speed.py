from Monster import Monster


class Monster_speed(Monster):
    def __init__(self, x, y):
        super().__init__(x, y, hp=4, speed=2, field_view=7, lyt=["key"], exp=10)

