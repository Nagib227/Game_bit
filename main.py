import pygame

from END import END
from Board import Board


if __name__ == '__main__':
    time = 1000
    time_Move = 1000
    s = 20
    #######
    size = width, height = s * 25 + 10 * 2, s * 25 + 10 * 2
    sc = pygame.display.set_mode(size)
    NOT_MOVE = pygame.USEREVENT + 1
    MOVE = pygame.USEREVENT + 2
    board = Board()
    clock = pygame.time.Clock()
    fps = 10
    move = False
    move_P = False
    end = True
    start = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                END() # !!!!!!!!!!!!!!
            if event.type == NOT_MOVE:
                move = True
                move_P = True
                start = True
                print("Начало тайминга хода")
                print("Ход Монсра")
                board.move_monsters()
            if event.type == MOVE:
                move = False
                end = True
                print("Конец тайминга хода")
                board.interact_monsters()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if move and move_P:
                        move_P = False
                        print("W")
                        board.move_player(0, -1)
                if event.key == pygame.K_s:
                    if move and move_P:
                        move_P = False
                        board.move_player(0, 1)
                        print("S")
                if event.key == pygame.K_a:
                    if move and move_P:
                        move_P = False
                        print("A")
                        board.move_player(-1, 0)
                if event.key == pygame.K_d:
                    if move and move_P:
                        move_P = False
                        print("D")
                        board.move_player(1, 0)
                if event.key == pygame.K_e:
                    print("E")
                    board.interact_items()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if move and move_P:
                        move_P = False
                        print("atack")
                        board.atack(event.pos)
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
        pygame.display.flip()
        clock.tick(fps)
