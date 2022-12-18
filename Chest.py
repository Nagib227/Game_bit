from Healing_potion import Healing_potion
from Speed_potion import Speed_potion
from Game_Board import board


class Chest:
    def __init__(self, coords):
        board.seed = board.randomize(board.seed)
        if board.seed[-1] % 2 == 0:
            self.item = Healing_potion(board.seed[0])
        else:
            self.item = Speed_potion(board.seed[0], 30)

    def get_item(self):
        return self.item
