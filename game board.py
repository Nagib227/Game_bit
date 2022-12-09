import pygame
from datetime import datetime


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.seed = self.get_seed()
        self.create_map()
        # значения по умолчанию
        self.left = 20
        self.top = 20
        self.cell_size = 30

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    # 0 - клетки, по которым можно ходить
    # 10 - клетки спавна
    # 20 - клетки выхода
    # 1 - клетки препятствий

    def render(self, screen):
        field = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 0:
                    pygame.draw.rect(field, (255, 255, 255), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 1)
                elif self.board[j][i] == 10:
                    pygame.draw.rect(field, (255, 255, 100), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)
                elif self.board[j][i] == 20:
                    pygame.draw.rect(field, (255, 100, 100), (i * self.cell_size, j * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)

                elif self.board[j][i] == 1:
                    pygame.draw.rect(field, (200, 200, 200), (i * self.cell_size, j * self.cell_size,
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
            self.board[cell_coords[1]][cell_coords[0]] = 1
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
        self.set_start_finish_points()

    def set_start_finish_points(self):
        self.seed = self.randomize(self.seed)
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

        for range_y in range(-1, 2):  # перебор клетор 3х3 с данной клеткой в центре
            for range_x in range(-1, 2):
                if 0 <= self.start_coords[0] + range_x < 22 and 0 <= self.start_coords[1] + range_y < 22:
                    self.board[self.start_coords[0] + range_x][self.start_coords[1] + range_y] = 10

                if 0 <= self.finish_coords[0] + range_x < 22 and 0 <= self.finish_coords[1] + range_y < 22:
                    self.board[self.finish_coords[0] + range_x][self.finish_coords[1] + range_y] = 20


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