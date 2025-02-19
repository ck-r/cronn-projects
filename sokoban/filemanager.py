import json

import pygame.mixer

from objectdata import UNIT_SIZE
from gameobject import GameObject, create_object_at
from objecttype import Wall, Floor, Player, Box, Goal, Timer, Button, Label
from exceptions import FunctionDoesNotExistsError
from soundmanager import sound_redo, sound_button, sound_load

import cv2
import json
import os

WALL_COL = 255, 0, 0
FLOOR_COL = 255, 255, 255
PLAYER_COL = 0, 0, 255
BOX_COL = 0, 255, 0
GOAL_COL = 255, 0, 255
SET_GOAL_COL = 255, 255, 0

TYPES = {'Label': Label, 'Button': Button}

with open('times.json', 'r') as file:
    times = json.load(file)

loaded_level = 1


def get_loaded_level():
    return loaded_level


def load_level(level_number, play_sound=True):
    global loaded_level
    loaded_level = level_number
    if play_sound:
        pygame.mixer.Sound.play(sound_button)
    create_object_at(Timer, 0, 0)
    with open('reset_button.json', 'r') as file:
        reset_btn_data = json.load(file)
    with open('back_button.json', 'r') as file:
        back_btn_data = json.load(file)
    create_object_from_data(reset_btn_data)
    create_object_from_data(back_btn_data)
    try:
        img = cv2.imread(os.path.join('levels', f'level{level_number}.png'), cv2.IMREAD_UNCHANGED)
        rows, cols, _ = img.shape

        for x in range(rows):
            for y in range(cols):
                b, g, r, _ = (img[x, y])
                if (r, g, b) == WALL_COL:
                    create_object_at(Wall, x * UNIT_SIZE, y * UNIT_SIZE)
                elif (r, g, b) == FLOOR_COL:
                    create_object_at(Floor, x * UNIT_SIZE, y * UNIT_SIZE)
                elif (r, g, b) == PLAYER_COL:
                    create_object_at(Floor, x * UNIT_SIZE, y * UNIT_SIZE)
                    create_object_at(Player, x * UNIT_SIZE, y * UNIT_SIZE, -1)
                elif (r, g, b) == BOX_COL:
                    create_object_at(Floor, x * UNIT_SIZE, y * UNIT_SIZE)
                    create_object_at(Box, x * UNIT_SIZE, y * UNIT_SIZE, -1)
                elif (r, g, b) == GOAL_COL:
                    create_object_at(Goal, x * UNIT_SIZE, y * UNIT_SIZE)
                elif (r, g, b) == SET_GOAL_COL:
                    create_object_at(Goal, x * UNIT_SIZE, y * UNIT_SIZE)
                    create_object_at(Box, x * UNIT_SIZE, y * UNIT_SIZE, -1)
        [i.setup() for i in GameObject.objects]
    except AttributeError:
        load_menu(2)


def create_object_from_data(data):
    obj = create_object_at(TYPES[data['type']], data['x'], data['y'])
    for attr in tuple(data)[3:]:
        try:
            obj.get_data()[attr] = data[attr]
        except LookupError:
            obj.get_data()['on_press'] = get_button_function(data[attr])
    obj.setup()


def load_menu(menu_id):
    with open(os.path.join('menus', f'menu{menu_id}.json')) as file:
        data = json.load(file)
    if data['unload_level']:
        GameObject.objects.clear()
    for attrs in tuple(data.values()):
        if type(attrs) is not dict:
            break
        create_object_from_data(attrs)


def save_time(level, time):
    saved_data = times[level - 1] = str(time)[2:7]
    with open('times.json', 'r+') as times_file:
        time_data = json.load(times_file)
        time_data[level - 1] = saved_data
        times_file.seek(0)
        json.dump(time_data, times_file)
        times_file.truncate()
        with open(os.path.join('menus', 'menu2.json'), 'r+') as menu:
            menu_data = json.load(menu)
            for i in range(15):
                menu_data[f'label_l{i + 1}']['text'] = f'{i + 1}: --:--' if times[i] is None else f'{i + 1}: {times[i]}'
            menu.seek(0)
            json.dump(menu_data, menu)
            menu.truncate()


def reset_times():
    with open('times.json', 'w') as times_file:
        times_file.seek(0)
        json.dump([None] * 15, times_file)
        times_file.truncate()
        with open(os.path.join('menus', 'menu2.json'), 'r+') as menu:
            menu_data = json.load(menu)
            for i in range(15):
                menu_data[f'label_l{i + 1}']['text'] = f'{i + 1}: --:--'
            menu.seek(0)
            json.dump(menu_data, menu)
            menu.truncate()
    load_menu(2)


def get_button_function(func_data):
    if func_data[0] == 'load_level':
        def func():
            GameObject.objects.clear()
            if func_data[1] == 'current':
                pygame.mixer.Sound.play(sound_redo)
                load_level(loaded_level, play_sound=False)
            else:
                load_level(func_data[1])
    elif func_data[0] == 'load_menu':
        def func():
            pygame.mixer.Sound.play(sound_button)
            load_menu(func_data[1])
    elif func_data[0] == 'reset_times':
        def func():
            pygame.mixer.Sound.play(sound_redo)
            reset_times()
    else:
        raise FunctionDoesNotExistsError(func_data[0])
    return func
