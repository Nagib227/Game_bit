from Healing_potion import Healing_potion
from Speed_potion import Speed_potion


class Chest:
    def __init__(self, coords):
        self.x = coords[0]
        self.y = coords[1]
        self.is_opened = False
        self.exp = 7
        self.item = Healing_potion(self.x + 1, self.y, 2)
        # if int(seed[-1]) % 2 == 0:
          #   self.item = Healing_potion(2, self.x + 1, self.y)
        # else:
          #   self.item = Speed_potion(2, 30, self.x + 1, self.y)

    def get_item(self):
        return self.item

    def get_coord(self):
        return self.x, self.y
