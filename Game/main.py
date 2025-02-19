import random

import niebo
from niebo import *
import pygame
import world_generator
from GameObject import *
import Block
import enemy_spawner

pygame.init()

Pleyer_img = pygame.image.load('postac.png')
Pleyer2_img = pygame.image.load('postac2.png')

screen = pygame.display.set_mode((1024, 1024))

scroll_x = 0
scroll_y = 0

delta_time = 0
ticks_last_frame = 0
last_enemy_spawn = 0
enemy_spawn_delta = 0

player = Pleyer(world_generator.WORLD_LENGTH // 2, 0,
                24, 48,
                Pleyer_img, 50, 1, 0.2)

player2 = Pleyer(world_generator.WORLD_LENGTH // 2, 0,
                24, 48,
                Pleyer2_img, 50, 1, 0.2)

player.phys_enabled = True
player2.phys_enabled = True
objects = [player, player2]
GRAVITY = 0.01
JUMP_FORCE = 2


def znajdz_object(x, y):
    for obj in objects:
        if int(obj.x_blok) == x and int(obj.y_blok) == y:
            return obj
    return None


world_generator.generate_world()

attacked = None
running = True
while running:
    ticks = pygame.time.get_ticks()
    delta_time = ticks - ticks_last_frame
    ticks_last_frame = pygame.time.get_ticks()

    enemy_spawn_delta = last_enemy_spawn - pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    player_zablokowany_lewo = Block.znajdz_blok(player.x_blok, player.y_blok) is not None or Block.znajdz_blok(player.x_blok, player.y_blok + 1) is not None
    player_zablokowany_prawo = Block.znajdz_blok(player.x_blok + 1, player.y_blok) is not None or Block.znajdz_blok(player.x_blok + 1, player.y_blok + 1) is not None
    player2_zablokowany_lewo = Block.znajdz_blok(player2.x_blok, player2.y_blok) is not None or Block.znajdz_blok(player2.x_blok, player2.y_blok + 1) is not None
    player2_zablokowany_prawo = Block.znajdz_blok(player2.x_blok + 1, player2.y_blok) is not None or Block.znajdz_blok(player2.x_blok + 1, player2.y_blok + 1) is not None
    if keys[pygame.K_LEFT] and not player_zablokowany_lewo:
        player.move(-player.speed * delta_time, 0)
    if keys[pygame.K_RIGHT] and not player_zablokowany_prawo:
        player.move(player.speed * delta_time, 0)
    if keys[pygame.K_UP]:
        player.jump(JUMP_FORCE)

    if keys[pygame.K_a] and not player2_zablokowany_lewo:
        player2.move(-player.speed * delta_time, 0)
    if keys[pygame.K_d] and not player2_zablokowany_prawo:
        player2.move(player.speed * delta_time, 0)
    if keys[pygame.K_w]:
        player2.jump(JUMP_FORCE)

    wybrany_blok_x = (pygame.mouse.get_pos()[0] + scroll_x) // Block.ROZMIAR_BLOKU
    wybrany_blok_y = (pygame.mouse.get_pos()[1] + scroll_y) // Block.ROZMIAR_BLOKU

    in_range = (abs(player.x_blok - wybrany_blok_x) < 5 or abs(player2.x_blok - wybrany_blok_x) < 5) and (abs(player.y_blok - wybrany_blok_y) < 5 or abs(player2.y_blok - wybrany_blok_y) < 5)

    if pygame.mouse.get_pressed()[0]:
        blok = Block.znajdz_blok(wybrany_blok_x, wybrany_blok_y)
        attacked = znajdz_object(wybrany_blok_x, wybrany_blok_y)
        if blok is not None and in_range:
            blok.damage -= 0.08
            if blok.damage < 0:
                Block.usun_blok(wybrany_blok_x, wybrany_blok_y)
        if attacked is not None and in_range:
            player.attack(attacked)
            if not in_range:
                attacked = None

    if pygame.mouse.get_pressed()[2]:
        Block.postaw_blok(Block.ZIEMIA, wybrany_blok_x, wybrany_blok_y)

    scroll_x = player.x - screen.get_width() // 2
    scroll_y = player.y - screen.get_height() // 2

    screen.fill((33, 162, 211))
    niebo.draw(screen, scroll_y)
    Block.draw_bloki(screen, scroll_x, scroll_y)

    if enemy_spawn_delta < -2000:
        enemy_spawner.spawn()
        last_enemy_spawn = pygame.time.get_ticks()
        for enemy in enemy_spawner.enemies:
            enemy.jump(12, random.choice([-0.3, 0.3]))
        if random.randrange(1, 4) == 1:
            chmura_spawn(screen)

        for attacker in enemy_spawner.enemies:
            if in_range:
                if (attacker.x - player.x) ** 2 + (attacker.y - player.y) ** 2 < 30000 and (attacker.x - player.x) ** 2 + (attacker.y - player.y) < (attacker.x - player2.x) ** 2 + (attacker.y - player2.y) ** 2:
                    attacker.attack(player)
                elif (attacker.x - player2.x) ** 2 + (attacker.y - player2.y) ** 2 < 30000:
                    attacker.attack(player2)

    enemy_spawner.update_objects(objects)
    for obj in objects:
        if -obj.get_width() <= obj.x - scroll_x <= screen.get_width() and -obj.get_height() <= obj.y - scroll_y <= screen.get_height():
            obj.draw(screen, scroll_x, scroll_y)
        if obj.phys_enabled:
            obj.update(GRAVITY, delta_time)
    if len(objects) > 100:
        del objects[2]

    if player2.x > player.x + screen.get_width() // 2:
        pygame.draw.polygon(screen, (255, 255, 255), ((screen.get_width() - 25, screen.get_height() // 2 - 25),(screen.get_width() - 25, screen.get_height() // 2 + 25),(screen.get_width(), screen.get_height() // 2)))
    elif player2.x < player.x - screen.get_width() // 2:
        pygame.draw.polygon(screen, (255, 255, 255), ((25, screen.get_height() // 2 - 25),(25, screen.get_height() // 2 + 25),(0, screen.get_height() // 2)))

    pygame.display.flip()
enemy_spawner.stop()