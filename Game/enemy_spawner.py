import pygame.image

from GameObject import *
import random
from world_generator import WORLD_LENGTH
from Block import ROZMIAR_BLOKU


running = True
enemies = []
enemy_imgs = [pygame.image.load('black_slime.png'), pygame.image.load('hiesenberg_Slime.png')]


def spawn():
    enemies.append(Enemy(random.randrange(0, WORLD_LENGTH * ROZMIAR_BLOKU), 0, 16, 16, random.choice(enemy_imgs), 20, 5))
    enemies[-1].phys_enabled = True
    if len(enemies) > 100:
        del enemies[0]


def update_objects(obj_list):
    for obj in enemies:
        if obj not in obj_list:
            obj_list.append(obj)


def stop():
    running = False