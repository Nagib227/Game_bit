import pygame
import sqlite3
from datetime import datetime
from Gauss_noize import GaussNoize

from Player import Player
from Monster_default import Monster_default
from Monster_speed import Monster_speed
from Sword import Sword
from Bow import Bow
from Chest import Chest
from Healing_potion import Healing_potion
from Lose import Lose

from Weapon import Weapon
from Load_image import load_image


class Board:
    # создание поля
    def __init__(self, board_width, board_height, map_save=False, load_game=False):
        self.width = board_width
        self.height = board_height
        # значения по умолчанию
        self.all_sprites = pygame.sprite.Group()

        self.left = 20
        self.top = 20
        self.cell_size = 40

        self.floor = pygame.transform.scale(load_image("ground.png"), (self.cell_size, self.cell_size))
        self.start = pygame.transform.scale(load_image("spawn.png"), (self.cell_size, self.cell_size))
        self.finish = pygame.transform.scale(load_image("exit_1.png"), (self.cell_size, self.cell_size))
        self.exit = pygame.transform.scale(load_image("exit_2.png"), (self.cell_size, self.cell_size))
        
        # self.wall_1 = pygame.transform.scale(load_image("wall_1.png"), (self.cell_size, self.cell_size))
        # self.wall_2 = pygame.transform.scale(load_image("wall_2.png"), (self.cell_size, self.cell_size))
        # self.wall_3 = pygame.transform.scale(load_image("wall_3.png"), (self.cell_size, self.cell_size))
        self.wall_floor = pygame.transform.scale(load_image("wall_floor.png"), (self.cell_size, self.cell_size))

        self.items = []
        self.monsters = []

        if load_game:
            self.load_game()
        else:
            self.map_save = map_save

            self.seed = self.get_seed()
            self.create_map()

    # 0 - пустые клетки
    # 1 - группа клеток по которым можно ходить: 10 - земля. 11 - клетки спавна. 12 - клетки выхода
    # 20 - клетки стен

    def render(self, screen):
        field = pygame.Surface((self.width * self.cell_size, self.height * self.cell_size))
        floor_group = pygame.sprite.Group()
        for j in range(self.height):
            for i in range(self.width):
                if self.board[j][i] == 11:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = self.start
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = i * self.cell_size
                    sprite.rect.y = j * self.cell_size
                    floor_group.add(sprite)

                elif self.board[j][i] == 12:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = self.finish
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = i * self.cell_size
                    sprite.rect.y = j * self.cell_size
                    floor_group.add(sprite)

                elif self.board[j][i] == 10:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = self.floor
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = i * self.cell_size
                    sprite.rect.y = j * self.cell_size
                    floor_group.add(sprite)

                elif self.board[j][i] == 20:
                    sprite = pygame.sprite.Sprite()
                    sprite.image = self.wall_floor
                    sprite.rect = sprite.image.get_rect()
                    sprite.rect.x = i * self.cell_size
                    sprite.rect.y = j * self.cell_size
                    floor_group.add(sprite)

                    # sprite.image = self.wall_3
                    # sprite.rect = sprite.image.get_rect()
                    # sprite.rect.x = i * self.cell_size
                    # sprite.rect.y = j * self.cell_size
                    # floor_group.add(sprite)
                    
        sprite = pygame.sprite.Sprite()
        sprite.image = self.exit
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = self.finish_coords[1] * self.cell_size
        sprite.rect.y = self.finish_coords[0] * self.cell_size
        floor_group.add(sprite)
        
        floor_group.draw(field)
        self.all_sprites.draw(field)

        screen.blit(field, (self.left, self.top))

    def draw_interface(self, sc, x=25, y=25, s_h=50):
        # draw hearts (рисование сердец)
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
            sprite.image = pygame.transform.scale(self.player.active_weapon.get_img(), (90, 77))
        else:
            sprite.image = pygame.transform.scale(load_image("empty_weapon.png"), (70, 70))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x + 5
        sprite.rect.y = y + s_h + 25
        weapon_group.add(sprite)
        weapon_group.draw(sc)
        # draw healing_potion (рисование зелья здоровья)
        healing_potion_group = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(load_image("health_potion.png"), (60, 75))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x
        y_hp = y + s_h + 20 + 105
        sprite.rect.y = y_hp
        
        font = pygame.font.Font(None, 50)
        string_rendered = font.render("x", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = y_hp + 42
        intro_rect.x = x + 60
        sc.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 70)
        string_rendered = font.render(str(len(self.player.get_hp_potion())), 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = y_hp + 30
        intro_rect.x = x + 85
        sc.blit(string_rendered, intro_rect)
        
        healing_potion_group.add(sprite)
        healing_potion_group.draw(sc)
        # draw key (рисование ключа)
        key_group = pygame.sprite.Group()
        sprite = pygame.sprite.Sprite()
        sprite.image = pygame.transform.scale(load_image("key.png"), (60, 75))
        sprite.rect = sprite.image.get_rect()
        sprite.rect.x = x
        y_hp = y + s_h + 220
        sprite.rect.y = y_hp
        
        font = pygame.font.Font(None, 50)
        string_rendered = font.render("x", 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = y_hp + 42
        intro_rect.x = x + 60
        sc.blit(string_rendered, intro_rect)

        font = pygame.font.Font(None, 70)
        string_rendered = font.render(str(self.player.get_key()), 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.y = y_hp + 30
        intro_rect.x = x + 85
        sc.blit(string_rendered, intro_rect)
        
        key_group.add(sprite)
        key_group.draw(sc)

    def get_click(self, mouse_pos):
        cell_coords = self.get_cell(mouse_pos)
        print(cell_coords)

    def get_cell(self, mouse_pos):
        coords = ((mouse_pos[0] - self.left) // self.cell_size, (mouse_pos[1] - self.left) // self.cell_size)
        return coords

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
        try:
            num2 += '0' * int(num[-5])
            num3 += '0' * int(num[-5:-3])
        except Exception:
            num2 += '0' * 8
            num3 += '0' * 25

        next_num = str(sum([int(num1, 2), int(num2, 2), int(num3, 2)]))[5:26]
        if num == next_num:
            next_num = self.randomize(num + '01100000000')
        return next_num

    def create_map(self):
        self.board = [[0] * self.width for _ in range(self.height)]
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
        self.chest = Chest(chest_coords, self.all_sprites, size=self.cell_size)

        # генерация предметов на земле
        self.set_items()

        # размещение сущностей
        self.set_entities()

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
        self.start_cells = []
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

        return second_board, chest

    def set_items(self):
        # предметы на спавне
        if self.start_coords[0] == 0 and self.start_coords[1] == self.width - 1:  # right top
            self.items.append(Sword(1, self.width - 1, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(0, self.width - 2, self.all_sprites, size=self.cell_size))
            
        elif self.start_coords[0] == 0 and self.start_coords[1] == 0:  # left top
            self.items.append(Sword(1, 0, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(0, 1, self.all_sprites, size=self.cell_size))
            
        elif self.start_coords[0] == 0:  # top
            self.items.append(Sword(0, self.start_coords[1] + 1, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(0, self.start_coords[1] - 1, self.all_sprites, size=self.cell_size))
            
        elif self.start_coords[0] == self.width - 1 and self.start_coords[1] == 0:  # left bottom
            self.items.append(Sword(self.width - 1, 1, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(self.width - 2, 0, self.all_sprites, size=self.cell_size))
            
        elif self.start_coords[1] == 0:  # left
            self.items.append(Sword(self.start_coords[0] + 1, 0, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(self.start_coords[0] - 1, 0, self.all_sprites, size=self.cell_size))

        elif self.start_coords[0] == self.width - 1 and self.start_coords[1] == self.width - 1:  # right bottom
            self.items.append(Sword(self.width - 2, self.width - 1, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(self.width - 1, self.width - 2, self.all_sprites, size=self.cell_size))

        elif self.start_coords[0] == self.width - 1:  # bottom
            self.items.append(Sword(self.width - 1, self.start_coords[1] + 1, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(self.width - 1, self.start_coords[1] - 1, self.all_sprites, size=self.cell_size))

        elif self.start_coords[1] == self.width - 1:  # right
            self.items.append(Sword(self.start_coords[0] - 1, self.width - 1, self.all_sprites, size=self.cell_size))
            self.items.append(Bow(self.start_coords[0] + 1, self.width - 1, self.all_sprites, size=self.cell_size))

        print(self.items)

    # размещение сущностей
    def set_entities(self):
        self.player = Player(self.start_coords[0], self.start_coords[1], self.all_sprites, size=self.cell_size)


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

                if (coord, coord2) in to_check or self.board[coord][coord2] in [20, 11] or self.chest.x == coord and self.chest.y == coord2:
                    Right_pos = False

            to_check.append((coord, coord2))
            if i > 6:
                monster = Monster_speed(coord, coord2, self.all_sprites, size=self.cell_size)
            else:
                monster = Monster_default(coord, coord2, self.all_sprites, size=self.cell_size)
            all_monsters.append(monster)

        self.monsters = all_monsters
        # cоздание случайного хлеба

    def check_rightness(self, board):
        for x in range(self.height):
            for y in range(self.width):
                if board[x][y] in [10, 12]:
                    if not self.has_path(x, y, self.start_coords[1], self.start_coords[0]):
                        return False

        if not self.has_path(self.finish_coords[0], self.finish_coords[1], self.start_coords[0], self.start_coords[1]):
                return False

        return True

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
                if self.player.hp <= 0:
                    return Lose(self.player.get_exp())

    def interact_items(self):
        for i in self.items:
            if i.get_coord()[0] is None:
                continue
            if issubclass(i.__class__, Weapon):
                print("weapon")
                x = i.get_coord()[0] == self.player.get_coord()[0]
                y = i.get_coord()[1] == self.player.get_coord()[1]
                if x and y:
                    old = self.player.chang_weapon(i)
                    x, y = i.get_coord()
                    i.set_coord(None, None)
                    i.none_draw()
                    if old:
                        old.set_coord(x, y)
                        old.true_draw(x, y)
                    return None
            elif issubclass(i.__class__, Chest):
                print("chest")
                x = abs(i.get_coord()[0] - self.player.get_coord()[0])
                y = abs(i.get_coord()[1] - self.player.get_coord()[1])
                if x <= 1 and y <= 1 and x * y == 0 and not i.is_opened:
                    hp = self.open_chest(i)
                    self.items.append(hp)
            if issubclass(i.__class__, Healing_potion):
                x = i.get_coord()[0] == self.player.get_coord()[0]
                y = i.get_coord()[1] == self.player.get_coord()[1]
                if x and y:
                    print("potion")
                    self.player.set_loot([i])
                    del self.items[self.items.index(i)]
                    sp = list(self.all_sprites)
                    sp.pop(sp.index(i))
                    self.all_sprites = pygame.sprite.Group()
                    for i in sp:
                        self.all_sprites.add(i)

    def healing(self):
        self.player.healing()

    def interact_chest(self):
        x = abs(self.chest.get_coord()[0] - self.player.get_coord()[0])
        y = abs(self.chest.get_coord()[1] - self.player.get_coord()[1])
        if x <= 1 and y <= 1 and x * y == 0 and not self.chest.is_opened:
            print("chest")
            self.open_chest(self.chest)

    def open_chest(self, chest):
        chest.is_opened = True
        self.items.append(chest.get_item(self.all_sprites))
        self.player.set_exp(chest.exp)
        print('opened')

    def attack(self, pos):
        weapon = self.player.get_weapon()
        if not weapon:
            return None
        cell = self.get_cell(pos)
        print(self.player.can_attack(cell, self.board, self.items), "###############################")
        if not self.player.can_attack(cell, self.board, self.items):
            return None
        for i in self.monsters:
            if i.get_coord() == cell[::-1]:
                i.set_hp(weapon.get_damage())
                if i.get_hp() <= 0:
                    self.player.set_loot(i.get_loot())
                    self.player.set_exp(i.get_exp())
                    self.monsters.pop(self.monsters.index(i))
                    sp = list(self.all_sprites)
                    sp.pop(sp.index(i))
                    self.all_sprites = pygame.sprite.Group()
                    for i in sp:
                        self.all_sprites.add(i)
                return None

    def save_game(self):
        # хлеб, точка старта/финиша, игрок, сундук, предметы, монстры

        # карта:
        board_in_string = ''
        for i in range(self.height):
            row = ', '.join([str(j) for j in self.board[i]])
            board_in_string += row + "."
        board_in_string = board_in_string[:-1]
        start = f'{self.start_coords[0]}, {self.start_coords[1]}'
        finish = f'{self.finish_coords[0]}, {self.finish_coords[1]}'

        # игрок
        potions = ''
        for potion in self.player.get_hp_potion():
            potions += f'{str(potion.x)}, {str(potion.y)}' + '.'
        potions = potions[: -1]

        weapon = None
        if self.player.active_weapon is not None:
            weapon = self.player.active_weapon
            weapon = f'{str(weapon.x)}, {str(weapon.y)}, {str(weapon.damage)}, {str(weapon.field_attack)}'

        player = f'{str(self.player.x)}, {str(self.player.y)}, {str(self.player.hp)}, {str(self.player.key)}, ' \
                 f'{weapon}, {str(potions)}, {str(self.player.get_exp())}'

        # сундук
        chest = f'{self.chest.x}, {self.chest.y}, {self.chest.is_opened}'

        # предметы
        weapons = ''
        potions = ''
        for item in self.items:
            if isinstance(item, Weapon):
                weapons += f'{str(item.x)}, {str(item.y)}, {str(item.damage)}, {str(item.field_attack)}' + '.'
            elif isinstance(item, Healing_potion):
                potions += f'{str(item.x)}, {str(item.y)}, {str(item.heal)}'
        weapons = weapons[:-1]

        # монстры
        monsters = ''
        for monster in self.monsters:
            monsters += f'{str(monster.x)}, {str(monster.y)}, {str(monster.hp)}, {str(monster.speed)}' + '.'
        monsters = monsters[:-1]

        print(board_in_string)
        print(start, finish)
        print(player)
        print(chest)
        print(weapons)
        print(potions)
        print(monsters)

        bd = sqlite3.connect('data/Game_save.db')
        cur = bd.cursor()

        cur.execute(f"""INSERT INTO Saved_data(data, type) VALUES ('{board_in_string}', 1)""")
        cur.execute(f"""INSERT INTO Saved_data(data, type) VALUES ('{start}', 2), ('{finish}', 3), ('{player}', 4), 
        ('{chest}', 5), ('{weapons}', 6), ('{potions}', 7), ('{monsters}', 8)""")
        bd.commit()

    def load_game(self):
        bd = sqlite3.connect('data/Game_save.db')
        cur = bd.cursor()

        # карта:
        board = []
        pre_board = cur.execute("""SELECT data FROM Saved_data WHERE type = 1""").fetchone()[0].split('.')
        for row in pre_board:
            new_row = []
            for i in row.split(', '):
                if i != 'Chest':
                    new_row.append(int(i))
                else:
                    new_row.append(i)
            board.append(new_row)

        # игрок:
        pre_player = cur.execute("""SELECT data FROM Saved_data WHERE type = 4""").fetchone()[0].split(', ')
        potions = []
        if pre_player[5] != '':
            for potion in pre_player[5].split('.'):
                potion = potion.split(', ')
                potions.append(Healing_potion(int(potion[0]), int(potion[1]), self.all_sprites))

        weapon = None
        if pre_player[4] != 'None':
            weapon = pre_player[4].split(', ')
            if weapon[3] == 1:
                weapon = Bow(int(weapon[0]), int(weapon[1]), self.all_sprites)
            elif weapon[3] == 2:
                weapon = Sword(int(weapon[0]), int(weapon[1]), self.all_sprites)

        player = Player(int(pre_player[0]), int(pre_player[1]), self.all_sprites, hp=int(pre_player[2]),
                        weapon=weapon, keys=int(pre_player[3]), potion=potions)

        # сундук:
        pre_chest = cur.execute("""SELECT data FROM Saved_data WHERE type = 5""").fetchone()[0].split(', ')
        if pre_chest[-1] == 'False':
            pre_chest[-1] = False
        else:
            pre_chest[-1] = True
        print(pre_chest)

        # предметы:
        weapons = cur.execute("""SELECT data FROM Saved_data WHERE type = 6""").fetchone()[0].split('.')
        for weapon in weapons:
            if weapon[3] == 1:
                self.items.append(Bow(int(weapon[0]), int(weapon[1]), self.all_sprites))
            elif weapon[3] == 2:
                self.items.append(Sword(int(weapon[0]), int(weapon[1]), self.all_sprites))

        potion = cur.execute("""SELECT data FROM Saved_data WHERE type = 7""").fetchone()[0].split(', ')
        print(potion)
        if potion[0] != '':
            self.items.append(Healing_potion(int(potion[0]), int(potion[1]), self.all_sprites, heal=int(potion[2])))

        # монстров определять по speed!
        monsters = cur.execute("""SELECT data FROM Saved_data WHERE type = 8""").fetchone()[0].split('.')
        if monsters:
            for monster in monsters:
                monster = monster.split(', ')
                if monster[-1] == '1':
                    self.monsters.append(
                        Monster_default(int(monster[0]), int(monster[1]), self.all_sprites, hp=int(monster[2])))
                elif monster[-1] == '2':
                    self.monsters.append(
                        Monster_speed(int(monster[0]), int(monster[1]), self.all_sprites, hp=int(monster[2])))


        self.board = board
        self.start_coords = tuple(int(i) for i in cur.execute("""SELECT data FROM Saved_data WHERE type = 2""").fetchone()[0].split(', '))
        self.finish_coords = tuple(int(i) for i in cur.execute("""SELECT data FROM Saved_data WHERE type = 3""").fetchone()[0].split(', '))
        self.player = player
        self.chest = Chest((int(pre_chest[0]), int(pre_chest[0])), self.all_sprites, is_opened=pre_chest[-1])

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
