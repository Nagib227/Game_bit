import pygame

from Player import Player
from Monster import Monster


class Board:
    def __init__(self):
        self.width = 10
        self.height = 10
        self.board = [[1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                      [1, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 1, 0, 1, 0, 0],
                      [1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.key = 0
        self.monsters = [Monster(9, 9, 1, 1, 1, [1, 2], 10)]
        self.items = []
        self.player = Player(1, 1, 3)
        self.left = 10
        self.top = 10
        self.cell_size = 25

    def render(self, sc, color=(255, 255, 255)):
        for i in range(self.height):
            for j in range(self.width):
                x = self.cell_size * j + self.left
                y = self.cell_size * i + self.top
                if self.board[i][j] == 0:
                    pygame.draw.rect(sc, (0, 0, 0), ((x, y), (self.cell_size, self.cell_size)))
                elif self.board[i][j] == 1:
                    pygame.draw.rect(sc, (128, 128, 128), ((x, y), (self.cell_size, self.cell_size)))
                pygame.draw.rect(sc, color, (x, y, self.cell_size, self.cell_size), 1)
        x = self.cell_size * self.player.get_coord()[0] + self.left
        y = self.cell_size * self.player.get_coord()[1] + self.top
        pygame.draw.rect(sc, (0, 0, 255), ((x, y), (self.cell_size, self.cell_size)))
        for i in self.monsters:
            x = self.cell_size * i.get_coord()[0] + self.left
            y = self.cell_size * i.get_coord()[1] + self.top
            pygame.draw.rect(sc, (255, 0, 0), ((x, y), (self.cell_size, self.cell_size)))

    def move_player(self, x, y):
        x = self.player.get_coord()[0] + x
        y = self.player.get_coord()[1] + y
        if 0 <= x < self.width and 0 <= y < self.height and self.board[y][x] == 0:
            self.player.set_coord(x, y)

    def move_monsters(self):
        for i in self.monsters:
            move = i.move(self.player.get_coord(), self.board)
            print(move)
            if move:
                i.set_move(move[0])

    def move(self, obj, x, y):
        current_x, current_y = obj.get_coord()
        obj.set_coord(current_y + )
