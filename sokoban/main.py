import datetime

from exceptions import KeyNotSupportedError, NotDrawnError
from gameobject import GameObject, clear_gameobjects
from objecttype import Goal, Button, Timer
from objectdata import SCREEN_WIDTH, SCREEN_HEIGHT
from filemanager import load_level, load_menu, save_time, get_loaded_level, times
from soundmanager import sound_load, sound_redo, sound_button
import pygame

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Sokoban')
ui = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
ui = ui.convert_alpha(ui)

running = True

load_menu(0)

while running:
    # event collection
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key not in [pygame.K_SPACE, pygame.K_0, pygame.K_ESCAPE]:
                for i in GameObject.objects:
                    try:
                        i.on_key_pressed(event.key)
                    except KeyNotSupportedError:
                        pass

            elif event.key == pygame.K_SPACE:
                clear_gameobjects()
                pygame.mixer.Sound.play(sound_redo)
                load_level(get_loaded_level(), play_sound=False)

            elif event.key == pygame.K_ESCAPE:
                pygame.mixer.Sound.play(sound_button)
                load_menu(1)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for obj in [i for i in GameObject.objects if i.get_type() is Button]:
                obj.on_mouse_button_down()

    # update
    for i in GameObject.objects:
        i.on_update()

    # drawing
    screen.fill((0, 0, 0))
    ui.fill((0, 0, 0, 0))
    for i in GameObject.objects:
        try:
            i.draw(screen, ui)
        except NotDrawnError:
            pass
    screen.blit(ui, (0, 0))
    pygame.display.flip()

    # late update
    goals = [i for i in GameObject.objects if i.get_type() is Goal]
    progress = bool(goals)
    for i in goals:
        progress = progress and i['set']
    if progress:
        timer = [i for i in GameObject.objects if i.get_type() is Timer][0]
        time = datetime.datetime.now() - timer.get_data()['start_time']
        if times[get_loaded_level() - 1] is None or time.total_seconds() < int(times[get_loaded_level() - 1][:2]) * 60 + int(times[get_loaded_level() - 1][3:5]):
            save_time(get_loaded_level(), time)

        clear_gameobjects()
        pygame.mixer.Sound.play(sound_load)
        next_level = get_loaded_level() + 1
        load_level(next_level, play_sound=False)
    progress = True
pygame.quit()
