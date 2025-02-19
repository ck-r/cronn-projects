from pygame import draw
import pygame
import random

chmury_img = [pygame.image.load('chmura.png'), pygame.image.load('chmura1.png'), pygame.image.load('chmura2.png')]
chmury = []


class Chmura:
    def __init__(self, speed, x, y):
        self.speed = speed
        self.x = x
        self.y = y
        self.image = random.choice(chmury_img)

    def draw(self, surface, scroll_y):
        surface.blit(self.image, (self.x, self.y - scroll_y / 2, self.image.get_rect()[2], self.image.get_rect()[3]))
        self.x += self.speed


def chmura_spawn(surface):
    chmury.append(Chmura(random.random() / 7 + 0.1, -210, random.randrange(-700, 700)))
    for _ in chmury:
        if _.x > surface.get_width():
            del _


def draw(surface, scroll_y):
    for _ in chmury:
        _.draw(surface, scroll_y)
