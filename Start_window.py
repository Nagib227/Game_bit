import pygame

from END import END
from VARIABLES import *
from Load_image import load_image


pygame.init()
sc = pygame.display.set_mode((1, 1))


class Fon(pygame.sprite.Sprite):
    image = pygame.transform.scale(load_image('fon_1.png'), (S * 30 + 40, S * 30 + 40))
    
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
            self.image = pygame.transform.scale(load_image('fon_2.png'), (S * 30 + 40, S * 30 + 40))
            self.fon = 2
            return None
        if self.fon == 2:
            self.image = pygame.transform.scale(load_image('fon_1.png'), (S * 30 + 40, S * 30 + 40))
            self.fon = 1

def start_window():
    pygame.init()
    s = S
    size = WIDTH, HEIGHT = s * 30 + 40, s * 30 + 40
    sc = pygame.display.set_mode(size)
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    all_sprites = pygame.sprite.Group()
    Fon(size, all_sprites)
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)
    btn = pygame.transform.scale(load_image('btn_start.png'), (150, 75))
    sc.blit(btn, (200, 450))
    clock = pygame.time.Clock()
    FPS = 1.5
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                if 150 < event.pos[0] < 300 and\
                   450 < event.pos[1] < 525:
                    return "new"
                elif 375 < event.pos[0] < 560 and\
                     455 < event.pos[1] < 515:
                    return "continue"
        for i in all_sprites:
            i.update()
        all_sprites.draw(sc)
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('white'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            sc.blit(string_rendered, intro_rect)
        btn = pygame.transform.scale(load_image('btn_start.png'), (150, 75))
        sc.blit(btn, (150, 450))
        btn = pygame.transform.scale(load_image('continue.png'), (185, 60))
        sc.blit(btn, (375, 455))
        pygame.display.flip()
        clock.tick(FPS)
