class Weapon:
    def __init__(self, stun, ammo):
        self.stun = stun
        self.ammo = ammo

    def get_stun(self):
        return self.stun

    def set_ammo(self, ammo):
        self.ammo = ammo

    def get_ammo(self):
        return self.ammo
