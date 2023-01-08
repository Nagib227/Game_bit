class Player:
    def __init__(self, x, y, hp=10, max_hp=10):
        self.x = x
        self.y = y
        self.key = 0
        self.hp = hp
        self.max_hp = max_hp
        self.active_weapon = None
        self.hp_potion = []
        self.current_potion = None
        self.exp = 0

    def get_hp_potion(self):
        return self.hp_potion

    def set_coord(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return self.x, self.y

    def chang_weapon(self, weapon):
        old = self.active_weapon
        self.active_weapon = weapon
        return old

    def set_loot(self, loot):
        if not loot:
            return None
        for i in loot:
            if i == "key":
                self.add_key()
            if i.__class__.__name__ == "Healing_potion":
                self.hp_potion.append(i)

    def set_exp(self, exp):
        self.exp += exp

    def get_exp(self):
        return self.exp

    def get_weapon(self):
        return self.active_weapon

    def damage(self, damage):
        self.hp -= damage

    def get_max_heal(self):
        return self.max_hp

    def healing(self):
        if not self.hp_potion:
            return None
        i = self.hp_potion.pop(0)
        self.hp += i.get_heal()
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def add_key(self):
        self.key += 1

    def get_key(self):
        return self.key

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
