import pygame
from datetime import datetime
from Gauss_noize import GaussNoize

from Player import Player
from Monster import Monster
from Monster_speed import Monster_speed
from Sword import Sword
from Bow import Bow
from Chest import Chest
from Healing_potion import Healing_potion

from END import END
from Weapon import Weapon
from Load_image import load_image


class Board:
    # создание поля
    def __init__(self, board_width, board_height, map_save=False):
        self.width = board_width
        self.height = board_height
        # значения по умолчанию
        self.items_group = pygame.sprite.Group()
                
        self.left = 20
        self.top = 20
        self.cell_size = 30

        self.map_save = map_save

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

    def render(self, screen, can_move):
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
                for item in self.items:
                    if not all(item.get_coord()):
                        continue
                    pygame.draw.rect(field, (255, 255, 255), (item.y * self.cell_size, item.x * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)

                pygame.draw.rect(field, (128, 64, 48), (self.chest.y * self.cell_size, self.chest.x * self.cell_size,
                                                        self.cell_size, self.cell_size), 0)

                count = 0
                for item in self.items:
                    if not all(item.get_coord()):
                        continue
                    if count < 2:
                        pygame.draw.rect(field, (255, 255, 0), (item.y * self.cell_size, item.x * self.cell_size,
                                                                self.cell_size, self.cell_size), 0)
                    else:
                        pygame.draw.rect(field, (210, 210, 210), (item.y * self.cell_size, item.x * self.cell_size,
                                                                  self.cell_size, self.cell_size), 0)
                    if isinstance(item, Sword):
                        color_item = pygame.Color(10, 10, 255)
                    elif isinstance(item, Bow):
                        color_item = pygame.Color(128, 64, 48)

                    pygame.draw.rect(field, color_item, (item.y * self.cell_size + 5, item.x * self.cell_size + 5,
                                                         self.cell_size - 10, self.cell_size - 10), 0)
                    count += 1

                # игрок
                if can_move:
                    pygame.draw.rect(field, (100, 255, 100), (self.player.y * self.cell_size, self.player.x * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)
                else:
                    pygame.draw.rect(field, (100, 100, 255), (self.player.y * self.cell_size, self.player.x * self.cell_size,
                                                              self.cell_size, self.cell_size), 0)

        screen.blit(field, (self.left, self.top))

    def draw_interface(self, sc, x=25, y=25, s_h=50):
        # draw heart (рисование сердец)
        hearts_group = pygame.sprite.Group()
        hp = self.player.hp
        false_hp = self.player.get_max_heal() - self.player.hp
        for i in range(hp):
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.transform.scale(load_image("heart_1.png"), (50, 50))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = x + s_h * i
            sprite.rect.y = y
            hearts_group.add(sprite)
        for i in range(false_hp):
            sprite = pygame.sprite.Sprite()
            sprite.image = pygame.transform.scale(load_image("false_heart.png"), (50, 50))
            sprite.rect = sprite.image.get_rect()
            sprite.rect.x = x + s_h * (hp + i)
            sprite.rect.y = y
            hearts_group.add(sprite)
        hearts_group.draw(sc)
        # draw wepon (рисование оружия)
        weapon_group = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(load_image("window_2.png"), (120, 105))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x
        sprite.rect.y = y + s_h + 10
        weapon_group.add(sprite)
        sprite = pygame.sprite.Sprite()
        if self.player.active_weapon:
            sprite.image = pygame.transform.scale(self.player.active_weapon.image, (90, 77))
        else:
            sprite.image = pygame.transform.scale(load_image("empty_weapon.png"), (70, 70))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x + 5
        sprite.rect.y = y + s_h + 25
        weapon_group.add(sprite)
        weapon_group.draw(sc)

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
        next_num = str(sum([int(num1, 2), int(num2, 2), int(num3, 2)]))[5:26]
        if num == next_num:
            next_num = self.randomize(num + '01100000000')
        return next_num

    def create_map(self):
        self.board = [[0] * self.width for _ in range(self.height)]
        self.items = []
        self.set_start_finish_points()

        # рандомная карта и точки спавна
        Done = False
        while not Done:
            self.paint_start_finish_points()
            # генерация стен с помощью шума Гауса
            self.board = GaussNoize(self.board, self.width, self.map_save, self.seed)

            Done = self.check_rightness(self.board)
            if not Done:
                self.board = [[0] * self.width for _ in range(self.height)]

        # рандомный сундук
        Done = False
        while not Done:
            new_board, chest_coords = self.set_structure()
            Done = self.check_rightness(new_board)

        self.board = new_board
        self.chest = Chest(chest_coords, self.seed)

        # генерация предметов на земле
        self.set_items()

        # размещение сущностей
        self.set_entities()

        # delete
        for i in range(self.width):
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
                if 0 <= self.start_coords[0] + range_y < self.width and 0 <= self.start_coords[1] + range_x < self.height:
                    self.board[self.start_coords[0] + range_y][self.start_coords[1] + range_x] = 11
                    self.start_cells.append((self.start_coords[0] + range_y, self.start_coords[1] + range_x))

                if 0 <= self.finish_coords[0] + range_y < self.width and 0 <= self.finish_coords[1] + range_x < self.height:
                    self.board[self.finish_coords[0] + range_y][self.finish_coords[1] + range_x] = 12

    def set_structure(self):
        structure = [[10, 10, 20, 10, 10],
                     [20, 10, 10, 10, 20],
                     [20, 10, 'Chest', 10, 20],
                     [20, 10, 10, 10, 20],
                     [10, 10, 20, 10, 10]]
        second_board = self.board
        self.seed = self.randomize(self.seed)

        coord = int(self.seed[2:4])
        coord2 = int(self.seed[4:6])
        while coord >= self.width - 5:
            coord -= 10
        while coord2 >= self.width - 5:
            coord2 -= 10

        for x in range(5):
            for y in range(5):
                if second_board[coord + x][coord2 + y] in [11, 12]:
                    continue
                second_board[coord + x][coord2 + y] = structure[x][y]
                if structure[x][y] == 'Chest':
                    chest = (coord + x, coord2 + y)

        # for i in range(self.width):
        #     print(second_board[i])

        return second_board, chest
    # cоздание случайной карты

    def set_items(self):
        # предметы на спавне
        if self.start_coords[0] == 0 and self.start_coords[1] == self.width - 1:  # right top
            self.items.append(Sword(1, self.width - 1, self.items_group))
            self.items.append(Bow(0, self.width - 2, self.items_group))
            
        elif self.start_coords[0] == 0 and self.start_coords[1] == 0:  # left top
            self.items.append(Sword(1, 0, self.items_group))
            self.items.append(Bow(0, 1, self.items_group))
            
        elif self.start_coords[0] == 0:  # top
            self.items.append(Sword(0, self.start_coords[1] + 1, self.items_group))
            self.items.append(Bow(0, self.start_coords[1] - 1, self.items_group))
            
        elif self.start_coords[0] == self.width - 1 and self.start_coords[1] == 0:  # left bottom
            self.items.append(Sword(self.width - 1, 1, self.items_group))
            self.items.append(Bow(self.width - 2, 0, self.items_group))
            
        elif self.start_coords[1] == 0:  # left
            self.items.append(Sword(self.start_coords[0] + 1, 0, self.items_group))
            self.items.append(Bow(self.start_coords[0] - 1, 0, self.items_group))

        elif self.start_coords[0] == self.width - 1 and self.start_coords[1] == self.width - 1:  # right bottom
            self.items.append(Sword(self.width - 2, self.width - 1, self.items_group))
            self.items.append(Bow(self.width - 1, self.width - 2, self.items_group))

        elif self.start_coords[0] == self.width - 1:  # bottom
            self.items.append(Sword(self.width - 1, self.start_coords[1] + 1, self.items_group))
            self.items.append(Bow(self.width - 1, self.start_coords[1] - 1, self.items_group))

        elif self.start_coords[1] == self.width - 1:  # right
            self.items.append(Sword(self.start_coords[0] - 1, self.width - 1, self.items_group))
            self.items.append(Bow(self.start_coords[0] + 1, self.width - 1, self.items_group))

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
                coord = sum([int(i) for i in self.seed[11:14]])
                coord2 = sum([int(i) for i in self.seed[5:8]])
                while coord >= self.width:
                    coord -= 15
                while coord2 >= self.height:
                    coord2 -= 15
                # if self.has_path(coord2, coord, self.start_coords[1], self.start_coords[0]) or\
                #         (coord, coord2) in to_check or self.board[coord][coord2] == 20:

                if (coord, coord2) in to_check or self.board[coord][coord2] in [20, 11]:
                    Right_pos = False

            to_check.append((coord, coord2))
            if i > 6:
                monster = Monster_speed(coord, coord2)
            else:
                monster = Monster(coord, coord2)
            all_monsters.append(monster)

        self.monsters = all_monsters

    def check_rightness(self, board):
        for x in range(self.height):
            for y in range(self.width):
                if board[x][y] in [10, 12]:
                    if not self.has_path(x, y, self.start_coords[1], self.start_coords[0]):
                        return False

        if not self.has_path(self.finish_coords[0], self.finish_coords[1], self.start_coords[0], self.start_coords[1]):
                return False

        return True

    # def move(self, entity, x, y):  # entity - сущность(игрок, монстр)
    #     entity.x += x
    #     entity.y += y

    def move_player(self, x, y):
        x = self.player.get_coord()[0] + x
        y = self.player.get_coord()[1] + y
        for i in self.monsters:
            if i.x == x and i.y == y:
                return None
        for i in self.items:
            if i.x == x and i.y == y and i.__class__.__name__ == "Chest":
                return None
        if 0 <= x < self.width and 0 <= y < self.height and self.board[x][y] in [10, 11, 12]:
            self.player.set_coord(x, y)

    def move_monsters(self):
        for i in self.monsters:
            if not i.can_move(self.player.get_coord(), self.board):
                continue
            move = i.move(self.player.get_coord(), self.board, self.monsters, self.items)
            print(move)
            if move:
                for j in range(i.get_speed()):
                    if not move:
                        break
                    i.set_move(move.pop(0))
                # raise Exception('I know Python!')

    def interact_monsters(self):
        for i in self.monsters:
            x = abs(i.get_coord()[0] - self.player.get_coord()[0])
            y = abs(i.get_coord()[1] - self.player.get_coord()[1])
            if x <= 1 and y <= 1 and y * x == 0:
                self.player.damage(i.get_damage())
                print(self.player.hp)
                if self.player.hp <= 0:
                    print(self.player.get_exp())
                    END()

    def interact_items(self):
        print(self.items)
        for i in self.items:
            if not all(i.get_coord()):
                continue
            if issubclass(i.__class__, Weapon):
                print("weapon")
                x = i.get_coord()[0] == self.player.get_coord()[0]
                y = i.get_coord()[1] == self.player.get_coord()[1]
                if x and y:
                    old = self.player.chang_weapon(i)
                    x, y = i.get_coord()
                    i.set_coord(None, None)
                    if old:
                        old.set_coord(x, y)
                    return None
            if issubclass(i.__class__, Chest):
                print("chest")
                x = abs(i.get_coord()[0] - self.player.get_coord()[0])
                y = abs(i.get_coord()[1] - self.player.get_coord()[1])
                if x <= 1 and y <= 1 and x * y == 0:
                    # открытие сундука
                    # self.player.set_loot(i.open())
                    '''
                    old = self.player.chang_weapon(i)
                    x, y = i.get_coord()
                    i.set_coord(None, None)
                    if old:
                        old.set_coord(x, y)
                    '''

    def attack(self, pos):
        weapon = self.player.get_weapon()
        if not weapon:
            return None
        cell = self.get_cell(pos)
        print(self.player.can_attack(cell, self.board, self.items), "###############################")
        # raise Exception('I know Python!')
        if not self.player.can_attack(cell, self.board, self.items):
            return None
        for i in self.monsters:
            if i.get_coord() == cell[::-1]:
                i.set_hp(weapon.get_damage())
                if i.get_hp() <= 0:
                    self.player.set_loot(i.get_loot())
                    self.player.set_exp(i.get_exp())
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


# if __name__ == '__main__':
#     pygame.init()
#     s = 22
#     size = width, height = s * 30 + 40, s * 30 + 40
#     screen = pygame.display.set_mode(size)
#
#     board = Board(s, s)
#     running = True
#     while running:
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 board.get_click(event.pos)
#         screen.fill((0, 0, 0))
#         board.render(screen)
#         pygame.display.flip()
