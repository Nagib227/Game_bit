from Weapon import Weapon


class Bomb(Weapon):
    def __init__(self, damage, ammo, obl_atack, obl_damage):
        super().__init__(damage, ammo, obl_atack)
        self.obl_damage = obl_damage

    def get_obl_damage(self):
        return self.obl_damage
