class Player:
    def __init__(self, x, y, hp=9999999999999999999999999999999):
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

    def can_attack(self, coord_attack, field, items):
        coord_attack = coord_attack[::-1]
        print(self.get_coord(), "pl")
        print(coord_attack, "at")
        x_point = abs(self.y - coord_attack[1])
        y_point = abs(self.x - coord_attack[0])
        print(x_point, y_point)
        clos_coord = []
        for i in items:
            if i.__class__.__name__ == "Chest":
                clos_coord.append(i.get_coord())
        if x_point * y_point != 0:
            print("/")
            return False
        if max(x_point, y_point) > self.active_weapon.get_field_attack():
            return False
        for i in range(x_point + 1):
            if field[self.x][min(self.y, coord_attack[1]) + i] in [20] or\
               (self.x, min(self.y, coord_attack[1]) + i) in clos_coord:
                print("f")
                return False
        for i in range(y_point + 1):
            if field[min(self.x, coord_attack[0]) + i][self.y] in [20] or\
               (min(self.x, coord_attack[0]) + i, self.y) in clos_coord:
                print("f2")
                return False
        return True
