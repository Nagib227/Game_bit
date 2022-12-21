class Player:
    def __init__(self, x, y, hp):
        self.x = x
        self.y = y
        self.key = 0
        self.hp = hp
        self.active_weapon = None
        self.inventory = []

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y

    def chang_weapon(self, weapon):
        old = self.active_weapon
        self.active_weapon = weapon
        return old

    def get_weapon(self):
        return self.active_weapon

    def damage(self, damage):
        self.hp -= damage

    def heal(self):
        return self.hp

    def healing(self, hp):
        self.hp += hp

    def add_key(self):
        self.key += 1
