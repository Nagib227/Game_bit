class Player:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.key = 0
        self.hp = hp
        self.active = None
        self.inventory = []

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y

    def add_weapon(self, weapon):
        if weapon in self.inventory:
            return None
        self.active = weapon
        self.inventory.append(weapon)

    def chang_weapon(self, index):
        self.active = self.inventory[index]

    def find_weapon(self, weapon):
        if weapon in self.inventory:
            return self.inventory.index(weapon)

    def heal(self):
        return self.hp

    def healing(self, hp):
        self.hp += hp

    def add_key(self):
        self.key += 1
