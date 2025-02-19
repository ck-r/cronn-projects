import pygame.image
from pygame import draw

ROZMIAR_BLOKU = 24
bloki = dict()

stone_img = pygame.image.load('Stone_Block.png')
dirt_img = pygame.image.load('Dirt_Block.png')
grass_img = pygame.image.load('trawa.png')


class TypBloku:
    def __init__(self, image, wytrzymalosc):
        self.image = image
        self.wytrzymalosc = wytrzymalosc


TRAWA = TypBloku(grass_img, 2)
ZIEMIA = TypBloku(dirt_img, 2)
KAMIEN = TypBloku(stone_img, 6)
BEDROCK = TypBloku(stone_img, 999999999)


class Blok:
    def __init__(self, typ, x, y):
        self.typ = typ
        self.damage = typ.wytrzymalosc
        self.x = x
        self.y = y

    def draw(self, surface, scroll_x, scroll_y):
        draw.rect(surface, self.typ.kolor, (self.x * ROZMIAR_BLOKU - scroll_x, self.y * ROZMIAR_BLOKU - scroll_y, ROZMIAR_BLOKU, ROZMIAR_BLOKU))


def postaw_blok(typ, x, y):
    bloki[(x, y)] = Blok(typ, x, y)


def znajdz_blok(x, y):
    try:
        return bloki[(x, y)]
    except KeyError:
        return None


def znajdz_typ_bloku(x, y):
    try:
        return bloki[(x, y)].typ
    except KeyError:
        return None


def usun_blok(x, y):
    try:
        del bloki[(x, y)]
    except KeyError:
        pass


def draw_bloki(surface, scroll_x, scroll_y):
    for blok in bloki.values():
        if scroll_x - surface.get_width() // 2 <= blok.x * ROZMIAR_BLOKU <= scroll_x + surface.get_width():
            surface.blit(blok.typ.image, ((blok.x * ROZMIAR_BLOKU) - scroll_x, (blok.y * ROZMIAR_BLOKU) - scroll_y, blok.typ.image.get_rect()[2], blok.typ.image.get_rect()[3]))