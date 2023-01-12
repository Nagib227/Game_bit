# Lose
import pygame

from END import END
from VARIABLES import *
from Load_image import load_image


pygame.init()
sc = pygame.display.set_mode((1, 1))


def Lose(exp):
    pygame.init()
    s = S
    size = WIDTH, HEIGHT = s * 30 + 40, s * 30 + 40
    sc = pygame.display.set_mode(size)
    intro_text = [f"Вы набрали {exp} очков", 
                  "Для продолжения нажмите кнопку мышки"]
    fon = pygame.transform.scale(load_image('lose_3.png'), (WIDTH, HEIGHT))
    sc.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('#8b0000'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        sc.blit(string_rendered, intro_rect)
    clock = pygame.time.Clock()
    FPS = 1.5
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                END()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return "kill"
        pygame.display.flip()
        clock.tick(FPS)
