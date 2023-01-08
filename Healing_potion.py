class Healing_potion:
    def __init__(self, x, y, heal=4):
        self.x = x
        self.y = y
        self.heal = heal

    def get_heal(self):
        return self.heal

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y
