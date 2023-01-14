import pygame

from Game_Board import Board
from Bit import Bit
from Heart_bit import Heart_bit

from END import END
from Load_image import load_image
from VARIABLES import *


def main(btn="new", exp=None, hp=None):
    time = TIME
    time_Move = TIME_MOVE
    pygame.init()
    s = S
    size = width, height = s * 40 + 40, s * 40 + 40
    sc = pygame.display.set_mode(size)

    if btn == 'continue':
        board = Board(s, s, load_game=True)
    elif exp is None or hp is None:
        board = Board(s, s)
    else:
        board = Board(s, s, map_save=False, exp=exp, hp=hp)

    NOT_MOVE = pygame.USEREVENT + 1
    MOVE = pygame.USEREVENT + 2
    BIT = pygame.USEREVENT + 3
    pygame.time.set_timer(BIT, 8)
    clock = pygame.time.Clock()
    fps = 244
    move = False
    move_P = False
    end = True
    start = False
    bits_group = pygame.sprite.Group()
    Bit(-30, height - 110, round((width - 40) / round(time / 10 * 3.05)), (width - 40) // 2, bits_group, rot=False)
    Bit(width + 0, height - 110, -round((width - 40) / round(time / 10 * 3.05)), (width - 40) // 2, bits_group, rot=True)
    Heart_bit((width - 110) // 2, height - 120, bits_group)
    pygame.mixer.music.load('data/01 - Tombtorial (Tutorial).mp3')
    pygame.mixer.music.play(-1)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                board.save_game()
                END()  # !!!!!!!!!!!!!!
            if event.type == BIT:
                for i in bits_group:
                    if issubclass(i.__class__, Heart_bit):
                        i.update(move)
                    else:
                        i.update()
            if event.type == NOT_MOVE:
                move = True
                move_P = True
                start = True
                print("Начало тайминга хода")
                for i in bits_group:
                    if issubclass(i.__class__, Bit):
                        i.set_start()
            if event.type == MOVE:
                move = False
                end = True
                print("Конец тайминга хода")
                if "kill" == board.interact_monsters():
                    return "kill"
                print("Ход Монсра")
                board.move_monsters()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    if move and move_P:
                        move_P = False
                        print("A")
                        board.move_player(0, -1)
                if event.key == pygame.K_d:
                    if move and move_P:
                        move_P = False
                        board.move_player(0, 1)
                        print("D")
                if event.key == pygame.K_w:
                    if move and move_P:
                        move_P = False
                        print("W")
                        board.move_player(-1, 0)
                if event.key == pygame.K_s:
                    if move and move_P:
                        move_P = False
                        print("S")
                        board.move_player(1, 0)
                if event.key == pygame.K_e:
                    print("E")
                    exp = board.interact_items()
                    if type(exp) == list:
                        return exp
                    board.interact_chest()
                if event.key == pygame.K_1:
                    print("1")
                    board.healing()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if move and move_P:
                        move_P = False
                        print("attack")
                        board.attack(event.pos)
        if move and start:
            start = False
            pygame.time.set_timer(NOT_MOVE, 0)
            pygame.time.set_timer(MOVE, time_Move)
        elif end:
            end = False
            pygame.time.set_timer(MOVE, 0)
            pygame.time.set_timer(NOT_MOVE, time)
        sc.fill((0, 0, 0))
        board.render(sc)
        board.draw_interface(sc)
        bits_group.draw(sc)
        pygame.display.flip()
        clock.tick(fps)
