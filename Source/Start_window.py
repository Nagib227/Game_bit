import pygame
import os

from END import END
from VARIABLES import *
from Load_image import load_image


os.environ['SDL_VIDEO_WINDOW_POS'] = '%i,%i' % (800, 100)
pygame.init()
sc = pygame.display.set_mode((1, 1))


class Fon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('fon_1.png'), (S * CELL_SIZE + 40, S * CELL_SIZE + 40))
    
    def __init__(self, size, *group):
        super().__init__(*group)
        self.image = Fon.image
        self.rect = self.image.get_rect()
        self.size = size
        self.rect.x = 0
        self.rect.y = 0
        self.fon = 1

    def update(self):
        if self.fon == 1:
            self.image = pygame.transform.scale(load_image('fon_2.png'), (S * CELL_SIZE + 40, S * CELL_SIZE + 40))
            self.fon = 2
            return None
        if self.fon == 2:
            self.image = pygame.transform.scale(load_image('fon_1.png'), (S * CELL_SIZE + 40, S * CELL_SIZE + 40))
            self.fon = 1


def start_window():
    pygame.init()
    s = S
    size = WIDTH, HEIGHT = s * CELL_SIZE + 40, s * CELL_SIZE + 40
    sc = pygame.display.set_mode(size)
    intro_text = ["                                                              Игра \"БИТ\"",
                  "",
                  "    Правила игры:",
                  "Вы появляетесь в точке спавна, клетки спавна полностью безопасны. Для перехода на",
                  "следущую карту необходимо собрать 3 ключа с особых монстров и дойти до клетки",
                  "выхода.",
                  "Ходить и бить вы можете только под бит фоновой музыки.",
                  "",
                  '',
                  '    Управление:',
                  "Передвижение игрока: \"W\", \"A\", \"S\", \"D\"",
                  "Взаимодействие с предметами/сундуками/финишом: \"Е\"",
                  "Использование зелья лечения: \"1\"",
                  "Атаковать монстров: ЛКМ.",
                  "",
                  "",
                  "    Игра автоматически сохраняется при закрытии, если вы находитесь в процессе",
                  "прохождения карты. Продолжить можно нажав \"CONTINUE\"."]
    all_sprites = pygame.sprite.Group()
    Fon(size, all_sprites)
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, (200, 225, 200))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)
    btn = pygame.transform.scale(load_image('btn_start.png'), (150, 75))
    sc.blit(btn, (200, 450))
    clock = pygame.time.Clock()
    FPS = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 150 < event.pos[0] < 150 + 200 and\
                   600 < event.pos[1] < 600 + 100:
                    return "new"
                elif 550 < event.pos[0] < 550 + 245 and\
                     610 < event.pos[1] < 610 + 75:
                    return "continue"
        for i in all_sprites:
            i.update()
        all_sprites.draw(sc)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, True, (200, 225, 200))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            sc.blit(string_rendered, intro_rect)
        btn = pygame.transform.scale(load_image('btn_start.png'), (200, 100))
        sc.blit(btn, (150, 600))
        btn = pygame.transform.scale(load_image('continue.png'), (245, 75))
        sc.blit(btn, (550, 610))
        pygame.display.flip()
        clock.tick(FPS)
