import pygame

from END import END

from Sword import Sword
from Player import Player
from Monster_speed import Monster_speed


class Board:
    def __init__(self, s, s1):
        self.width = 10
        self.height = 10
        self.board = [[1, 10, 10, 10, 10, 10, 10, 1, 10, 10],
                      [1, 10, 1, 10, 10, 10, 10, 10, 10, 10],
                      [1, 10, 10, 10, 10, 1, 10, 1, 10, 10],
                      [1, 1, 1, 1, 1, 1, 1, 1, 10, 10],
                      [1, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                      [1, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                      [1, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                      [1, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                      [1, 10, 10, 10, 10, 10, 10, 10, 10, 10],
                      [1, 10, 10, 10, 10, 10, 10, 10, 10, 10]]
        self.monsters = [Monster_speed(4, 4)]
        self.items = [Sword(2, 0)]
        self.player = Player(1, 0, 3)
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
        for i in self.items:
            if not any(i.get_coord()):
                continue
            x = self.cell_size * i.get_coord()[0] + self.left
            y = self.cell_size * i.get_coord()[1] + self.top
            pygame.draw.rect(sc, (0, 255, 0), ((x, y), (self.cell_size, self.cell_size)))

    def move_player(self, x, y):
        x = self.player.get_coord()[0] + x
        y = self.player.get_coord()[1] + y
        if 0 <= x < self.width and 0 <= y < self.height and self.board[y][x] == 0:
            self.player.set_coord(x, y)

    def move_monsters(self):
        for i in self.monsters:
            if not i.can_move(self.player.get_coord(), self.board):
                continue
            move = i.move(self.player.get_coord(), self.board)
            if move:
                for j in range(i.get_speed()):
                    if not move:
                        break
                    i.set_move(move.pop(0))

    def interact_monsters(self):
        for i in self.monsters:
            if abs(i.get_coord()[0] - self.player.get_coord()[0]) <= 1 and\
               abs(i.get_coord()[1] - self.player.get_coord()[1]) <= 1:
                self.player.damage(i.get_damage())
                print(self.player.heal())
                if self.player.heal() <= 0:
                    END()

    def interact_items(self):
        for i in self.items:
            if not any(i.get_coord()):
                continue
            if abs(i.get_coord()[0] - self.player.get_coord()[0]) <= 1 and\
               abs(i.get_coord()[1] - self.player.get_coord()[1]) <= 1:
                old = self.player.chang_weapon(i)
                x, y = i.get_coord()
                i.set_coord(None, None)
                if old:
                    old.set_coord(x, y)

    def attack(self, pos):
        weapon = self.player.get_weapon()
        if not weapon:
            return None
        cell = self.get_cell(pos)
        print(weapon.can_atack(self.player.get_coord(), cell, self.board))
        if not weapon.can_atack(self.player.get_coord(), cell, self.board):
            return None
        for i in self.monsters:
            if i.get_coord() == cell:
                i.set_hp(weapon.get_damage())
                if i.get_hp() <= 0:
                    self.monsters.pop(self.monsters.index(i))
                return None

    def get_cell(self, m_pos):
        x, y = m_pos
        if not self.left < x < self.left + self.width * self.cell_size:
            return None
        if not self.top < y < self.top + self.height * self.cell_size:
            return None
        cell = ((x - self.left) // self.cell_size,
                (y - self.top) // self.cell_size)
        return cell
