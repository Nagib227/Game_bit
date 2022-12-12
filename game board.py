import pygame
from datetime import datetime
from Gauss_noize import GaussNoize


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
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # 0 - пустые клетки
    # 1 - группа клеток по которым можно ходить: 10 - земля. 11 - клетки спавна. 12 - клетки выхода. 13 - середина тропы
    # 20 - клетки стен. 21 - середина стены

    def render(self, screen):
        field = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 0:
                    pygame.draw.rect(field, (255, 255, 255), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 1)
                elif self.board[j][i] == 11:
                    pygame.draw.rect(field, (255, 255, 100), (i * self.cell_size, j * self.cell_size,
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
                elif self.board[j][i] == 21:
                    pygame.draw.rect(field, (90, 90, 90), (i * self.cell_size, j * self.cell_size,
                                                        self.cell_size, self.cell_size), 0)
                elif self.board[j][i] == 13:
                    pygame.draw.rect(field, (220, 220, 220), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)

        screen.blit(field, (self.left, self.top))

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        self.on_click(cell_coords)

    def get_cell(self, mouse_pos):
        coords = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.left) // self.cell_size)
        return coords

    def on_click(self, cell_coords):
        if 0 <= cell_coords[0] < self.width and 0 <= cell_coords[1] < self.height:
            print(cell_coords)
            self.board[cell_coords[1]][cell_coords[0]] = 20
        else:
            print('None')

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
        next_num = str(sum([int(num1, 2), int(num2, 2), int(num3, 2)]))[:20]
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

            if not Done:
                self.board = [[0] * self.width for _ in range(self.height)]

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
    size = width, height = 701, 701
    screen = pygame.display.set_mode(size)

    board = Board(22, 22)
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