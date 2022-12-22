import pygame
from datetime import datetime
from Gauss_noize import GaussNoize

from Player import Player
from Monster import Monster
from Monster_speed import Monster_speed

from END import END


class Board:
    # создание поля
    def __init__(self, board_width, board_height):
        self.width = board_width
        self.height = board_height
        # значения по умолчанию
        self.left = 20
        self.top = 20
        self.cell_size = 30

        self.seed = self.get_seed()
        self.create_map()
        
    # настройка внешнего вида
    # def set_view(self, left, top, cell_size):
    #     self.left = left
    #     self.top = top
    #     self.cell_size = cell_size

    # 0 - пустые клетки
    # 1 - группа клеток по которым можно ходить: 10 - земля. 11 - клетки спавна. 12 - клетки выхода
    # 20 - клетки стен

    def render(self, screen):

        field = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 0:
                    pygame.draw.rect(field, (255, 0, 255), (i * self.cell_size, j * self.cell_size,
                                                            self.cell_size, self.cell_size), 1)
                elif self.board[j][i] == 11:
                    pygame.draw.rect(field, (255, 255, 0), (i * self.cell_size, j * self.cell_size,
                                                            self.cell_size, self.cell_size), 0)
                elif self.board[j][i] == 12:
                    pygame.draw.rect(field, (255, 100, 100), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)
                elif self.board[j][i] == 10:
                    pygame.draw.rect(field, (210, 210, 210), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)

                elif self.board[j][i] == 20:
                    pygame.draw.rect(field, (100, 100, 100), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)
                for monster in self.monsters:
                    pygame.draw.rect(field, (0, 0, 0), (monster.y * self.cell_size, monster.x * self.cell_size,
                                                        self.cell_size, self.cell_size), 0)

                pygame.draw.rect(field, (0, 255, 0), (self.player.y * self.cell_size, self.player.x * self.cell_size,
                                                      self.cell_size, self.cell_size), 0)

        screen.blit(field, (self.left, self.top))

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        print(cell_coords)
        # self.on_click(cell_coords)

    def get_cell(self, mouse_pos):
        coords = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.left) // self.cell_size)
        return coords

    # def on_click(self, cell_coords):
    #     if 0 <= cell_coords[0] < self.width and 0 <= cell_coords[1] < self.height:
    #         print(cell_coords)
    #         self.board[cell_coords[1]][cell_coords[0]] = 20
    #     else:
    #         print('None')

    # cоздание случайной карты
    def get_seed(self):
        current_time = datetime.now()

        date, time = str(current_time).split()
        date = ''.join(date.split('-'))
        time = ''.join(''.join(time.split(':')).split('.'))
        seed = date + time
        seed = self.randomize(seed)
        return seed

    def randomize(self, num):
        num1 = bin(int(num))[2:]
        num3 = num2 = str(num1)
        num2 += '0' * int(num[-5])
        num3 += '0' * int(num[-8: -6])
        next_num = str(sum([int(num1, 2), int(num2, 2), int(num3, 2)]))[:21]
        if num == next_num:
            next_num = self.randomize(num + '011000')
        return next_num

    def create_map(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.set_start_finish_points()
        Done = False
        while not Done:
            Done = True
            self.paint_start_finish_points()
        # генерация стен с помощью шума Гауса
            self.board = GaussNoize(self.board)

            for x in range(self.height):
                for y in range(self.width):
                    if self.board[x][y] in [10, 12]:
                        if not self.has_path(x, y, self.start_coords[1], self.start_coords[0]):
                            Done = False

            if not self.has_path(self.finish_coords[0], self.finish_coords[1], self.start_coords[0], self.start_coords[1]):
                Done = False

            if not Done:
                self.board = [[0] * self.width for _ in range(self.height)]
        self.set_entities()

        for i in range(22):
            print(i, self.board[i])

    def set_start_finish_points(self):
        self.seed = self.randomize(self.seed)
        print(self.seed)

        self.start_cells = []
        # чёт и чёт - верх
        # чёт и нечёт - право
        # нечёт и чёт - лево
        # нечёт и нечёт - низ
        start_pos = ''
        num = int(self.seed[:2])
        if num // 10 % 2 == 0 and num % 2 == 0:
            start_pos = 'up'
        elif num // 10 % 2 == 0 and num % 2 != 0:
            start_pos = 'right'
        elif num // 10 % 2 != 0 and num % 2 == 0:
            start_pos = 'left'
        elif num // 10 % 2 != 0 and num % 2 != 0:
            start_pos = 'down'

        coord = int(self.seed[2:4])
        coord2 = int(self.seed[4:6])
        while coord >= self.width:
            coord -= 10
        while coord2 >= self.width:
            coord2 -= 10

        if start_pos == 'up':
            self.start_coords = (0, coord)
            self.finish_coords = (self.height - 1, coord2)
        elif start_pos == 'down':
            self.start_coords = (self.height - 1, coord)
            self.finish_coords = (0, coord2)
        elif start_pos == 'right':
            self.start_coords = (coord, self.width - 1)
            self.finish_coords = (coord2, 0)
        elif start_pos == 'left':
            self.start_coords = (coord, 0)
            self.finish_coords = (coord2, self.width - 1)

        print(self.start_coords, self.finish_coords)

    def paint_start_finish_points(self):
        for range_y in range(-1, 2):  # перебор клетор 3х3 с данной клеткой в центре
            for range_x in range(-1, 2):
                if 0 <= self.start_coords[0] + range_y < 22 and 0 <= self.start_coords[1] + range_x < 22:
                    self.board[self.start_coords[0] + range_y][self.start_coords[1] + range_x] = 11
                    self.start_cells.append((self.start_coords[0] + range_y, self.start_coords[1] + range_x))

                if 0 <= self.finish_coords[0] + range_y < 22 and 0 <= self.finish_coords[1] + range_x < 22:
                    self.board[self.finish_coords[0] + range_y][self.finish_coords[1] + range_x] = 12
    # cоздание случайной карты

    # размещение сущностей
    def set_entities(self):
        self.player = Player(self.start_coords[0], self.start_coords[1])


        all_monsters = []
        to_check = []
        for i in range(10):
            Right_pos = False  # цикл создающий и располагающий монстров
            while not Right_pos:  # цикл, который проверяет правильность расположения монстров
                Right_pos = True
                self.seed = self.randomize(self.seed)
                print(self.seed)

                coord = sum([int(i) for i in self.seed[11:14]])
                coord2 = sum([int(i) for i in self.seed[5:8]])
                print(coord, coord2)
                while coord >= self.width:
                    coord -= 15
                while coord2 >= self.height:
                    coord2 -= 15
                print(coord, coord2)
                if self.has_path(coord2, coord, self.start_coords[1], self.start_coords[0]) or\
                        (coord, coord2) in to_check or self.board[coord][coord2] == 20:
                    Right_pos = False

            to_check.append((coord, coord2))
            if i > 4:
                monster = Monster_speed(coord, coord2)
            else:
                monster = Monster(coord, coord2)
            all_monsters.append(monster)

        self.monsters = all_monsters

    # def move(self, entity, x, y):  # entity - сущность(игрок, монстр) (взято из майнкрафта)
    #     entity.x += x
    #     entity.y += y

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
            if abs(i.get_coord()[0] - self.player.get_coord()[0]) <= 1 and \
                    abs(i.get_coord()[1] - self.player.get_coord()[1]) <= 1:
                self.player.damage(i.get_damage())
                print(self.player.heal())
                if self.player.heal() <= 0:
                    END()

    def interact_items(self):
        for i in self.items:
            if not any(i.get_coord()):
                continue
            if abs(i.get_coord()[0] - self.player.get_coord()[0]) <= 1 and \
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


    def has_path(self, x1, y1, x2, y2):
        """Метод для определения доступности из клетки (x1, y1)
         клетки (x2, y2) по волновому методу"""
        # словарь расстояний
        d = {(x1, y1): 0}
        v = [(x1, y1)]
        while len(v) > 0:
            x, y = v.pop(0)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx * dy != 0:
                        continue
                    if x + dx < 0 or x + dx >= self.width or y + dy < 0 or y + dy >= self.height:
                        continue
                    if self.board[x + dx][y + dy] in [10, 11, 12]:
                        dn = d.get((x + dx, y + dy), -1)
                        if dn == -1:
                            d[(x + dx, y + dy)] = d.get((x, y), -1) + 1
                            v.append((x + dx, y + dy))
        dist = d.get((x2, y2), -1)
        return dist >= 0


if __name__ == '__main__':
    pygame.init()
    s = 22
    size = width, height = s * 30 + 40, s * 30 + 40
    screen = pygame.display.set_mode(size)

    board = Board(s, s)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        screen.fill((0, 0, 0))
        board.render(screen)
        pygame.display.flip()