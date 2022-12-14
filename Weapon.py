class Weapon:
    def __init__(self, damage, ammo, obl_atack):
        self.damage = damage
        self.ammo = ammo
        self.obl_atack = obl_atack

    def get_damage(self):
        return self.damage

    def set_ammo(self, ammo):
        self.ammo = ammo

    def get_ammo(self):
        return self.ammo

    def get_obl_atack(self):
        return self.obl_atack
