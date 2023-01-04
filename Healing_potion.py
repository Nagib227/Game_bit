class Healing_potion:
    def __init__(self, heal, x=0, y=0):
        self.x = x
        self.y = y
        self.heal = heal

    def get_heal(self):
        return self.heal

    def set_coords(self, x, y):
        self.x = x
        self.y = y
