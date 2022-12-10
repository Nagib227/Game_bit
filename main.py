import pygame


if __name__ == '__main__':
    time = 1000
    time_Move = 1000
    s = 20
    #######
    size = width, height = s * 25 + 10 * 2, s * 25 + 10 * 2
    sc = pygame.display.set_mode(size)
    NOT_MOVE = pygame.USEREVENT + 1
    MOVE = pygame.USEREVENT + 2
    # board = Board(s, s)
    # board.set_view(10, 10, 25)
    clock = pygame.time.Clock()
    fps = 10
    move = False
    move_P = False
    move_M = False
    end = True
    start = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == NOT_MOVE:
                move = True
                move_P = True
                move_M = True
                start = True
                print("Начало тайминга хода")
            if event.type == MOVE:
                move = False
                end = True
                print("Конец тайминга хода")
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if move and move_P:
                        move_P = False
                        print("W")
                if event.key == pygame.K_s:
                    if move and move_P:
                        move_P = False
                        print("S")
                if event.key == pygame.K_a:
                    if move and move_P:
                        move_P = False
                        print("A")
                if event.key == pygame.K_d:
                    if move and move_P:
                        move_P = False
                        print("D")
        if move_M:
            move_M = False
            print("Ход Монсра")
        if move and start:
            start = False
            pygame.time.set_timer(NOT_MOVE, 0)
            pygame.time.set_timer(MOVE, time_Move)
        elif end:
            end = False
            pygame.time.set_timer(MOVE, 0)
            pygame.time.set_timer(NOT_MOVE, time)
        sc.fill((0, 0, 0))
        # board.render(sc)
        pygame.display.flip()
        clock.tick(fps)
