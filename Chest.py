from Healing_potion import Healing_potion
from Speed_potion import Speed_potion


class Chest:
    def __init__(self, coords, seed):
        self.x = coords[0]
        self.y = coords[1]
        if int(seed[-1]) % 2 == 0:
            self.item = Healing_potion(2)
        else:
            self.item = Speed_potion(2, 30)

    def get_item(self):
        return self.item
