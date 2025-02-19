import pygame.font
from pygame import image, K_UP, K_DOWN, K_LEFT, K_RIGHT

from exceptions import NotDrawnError, KeyNotSupportedError
from objectdata import UNIT_SIZE
from gameobject import GameObject

import datetime


class ObjectType:
    sprite = None
    rect = None
    data_points = ()
    data_defaults = ()
    solid = True

    @classmethod
    def draw(cls, sur, dest, ui_surface, data):
        if not cls.sprite:
            raise NotDrawnError
        sur.blit(cls.sprite, dest)

    @classmethod
    def on_key_pressed(cls, key, data):
        raise KeyNotSupportedError(key)

    @classmethod
    def on_update(cls, data):
        raise NotImplementedError

    @classmethod
    def setup(cls, data):
        raise NotImplementedError

    @classmethod
    def on_mouse_button_down(self, data):
        raise NotImplementedError


class Movable(ObjectType):
    sprite = image.load('placeholder.png')
    rect = sprite.get_rect()
    data_points = 'x', 'y', 'can_move'
    data_defaults = 0, 0, True

    @classmethod
    def can_move(cls, data, offset, stack=0):
        if stack > 1:
            return False
        obj = GameObject.get_solid_object_by_position(data['x'] + offset[0], data['y'] - offset[1])
        try:
            if not obj.get_type().solid:
                return True
            return obj.get_type().can_move(obj.get_data(), offset, stack + 1)
        except AttributeError:
            if obj is None:
                return True
            return False

    @classmethod
    def move(cls, data, offset):
        obj = GameObject.get_solid_object_by_position(data['x'] + offset[0], data['y'] - offset[1])
        if cls.can_move(data, offset):
            data['can_move'] = True
            data['x'] += offset[0]
            data['y'] -= offset[1]
            if obj is not None and issubclass(obj.get_type(), Movable):
                obj.get_type().move(obj.get_data(),  offset)
        else:
            data['can_move'] = False
        return data


class UIObject(ObjectType):
    data_points = 'x', 'y', 'font', 'font_size', 'text', 'color', 'text_color', 'padding', 'width', 'height'
    data_defaults = 0, 0, None, 25, 'Abc', (0, 0, 0, 0), (255, 255, 255, 255), 10, None, None
    solid = False

    @classmethod
    def draw(cls, sur, dest, ui_surface, data):
        text = data['font'].render(data['text'], True, data['text_color'])
        text_rect = text.get_rect()
        if data['width']:
            text_rect.width = data['width'] - data['padding'] * 2
        if data['height']:
            text_rect.height = data['height'] - data['padding'] * 2
        pygame.draw.rect(ui_surface, data['color'], pygame.Rect(data['x'], data['y'], text_rect.width + data['padding'] * 2, text_rect.height + data['padding'] * 2))
        ui_surface.blit(text, pygame.Rect(data['x'] + data['padding'], data['y'] + data['padding'], text_rect.width, text_rect.height))


class Player(Movable):
    sprite = image.load('player.png')
    rect = sprite.get_rect()
    data_points = 'x', 'y', 'can_move'
    data_defaults = 0, 0, True

    @classmethod
    def on_key_pressed(cls, key, data):
        if key == K_UP:
            offset = 0, UNIT_SIZE
        elif key == K_DOWN:
            offset = 0, -UNIT_SIZE
        elif key == K_LEFT:
            offset = -UNIT_SIZE, 0
        elif key == K_RIGHT:
            offset = UNIT_SIZE, 0
        else:
            raise KeyNotSupportedError(key)

        cls.move(data, offset)
        return data


class Box(Movable):
    sprite = image.load('box.png')
    rect = sprite.get_rect()
    data_points = 'x', 'y', 'can_move'
    data_defaults = 0, 0, True


class Wall(ObjectType):
    sprite = image.load('wall.png')
    rect = sprite.get_rect()
    data_points = 'x', 'y'
    data_defaults = 0, 0


class Floor(ObjectType):
    sprite = image.load('floor.png')
    rect = sprite.get_rect()
    data_points = 'x', 'y'
    data_defaults = 0, 0
    solid = False


class Goal(ObjectType):
    sprite_set = image.load('goal_set.png')
    sprite = image.load('goal.png')
    rect = sprite.get_rect()
    data_points = 'x', 'y', 'set'
    data_defaults = 0, 0, False
    solid = False

    @classmethod
    def on_update(cls, data):
        obj = GameObject.get_solid_object_by_position(data['x'], data['y'])
        if obj is not None:
            data['set'] = obj.get_type() is Box
        else:
             data['set'] = False

        return data

    @classmethod
    def draw(cls, sur, dest, ui_surface, data):
        sur.blit(cls.sprite, dest)
        if data['set']:
            ui_surface.blit(cls.sprite_set, dest)


class Timer(UIObject):
    data_points = 'x', 'y', 'font', 'font_size', 'text', 'color', 'text_color', 'padding', 'width', 'height', 'start_time'
    data_defaults = 0, 0, None, 25, 'Abc', (0, 0, 0, 0), (255, 255, 255, 255), 10, None, None, datetime.datetime.now()
    solid = False

    @classmethod
    def setup(cls, data):
        data['start_time'] = datetime.datetime.now()
        data['font'] = pygame.font.Font('NotoSans-Regular.ttf', data['font_size'])
        return data

    @classmethod
    def on_update(cls, data):
        data['text'] = str(datetime.datetime.now() - data['start_time'])[2:7]
        return data


class Button(UIObject):
    data_points = 'x', 'y', 'font', 'font_size', 'text', 'color', 'text_color', 'padding', 'width', 'height', 'on_press', 'rect', 'color_default', 'color_hover'
    data_defaults = 0, 0, None, 25, 'Abc', (255, 255, 255, 200), (0, 0, 0, 255), 5, None, None, None, pygame.Rect(0, 0, 0, 0), (255, 255, 255, 200), (195, 215, 255, 200)
    solid = False

    @classmethod
    def setup(cls, data):
        data['font'] = pygame.font.Font('NotoSans-Regular.ttf', data['font_size'])
        text = data['font'].render(data['text'], True, data['text_color'])
        text_rect = text.get_rect()
        if data['width']:
            text_rect.width = data['width'] - data['padding'] * 2
        if data['height']:
            text_rect.height = data['height'] - data['padding'] * 2
        data['rect'] = pygame.Rect(data['x'], data['y'], text_rect.width + data['padding'] * 2, text_rect.height + data['padding'] * 2)
        return data

    @classmethod
    def on_update(cls, data):
        mouse_pos = pygame.mouse.get_pos()
        if data['rect'].x < mouse_pos[0] < data['rect'].x + data['rect'].width and data['rect'].y < mouse_pos[1] < data['rect'].y + data['rect'].height:
            data['color'] = data['color_hover']
        else:
            data['color'] = data['color_default']
        return data

    @classmethod
    def on_mouse_button_down(cls, data):
        mouse_pos = pygame.mouse.get_pos()
        if data['rect'].x < mouse_pos[0] < data['rect'].x + data['rect'].width and data['rect'].y < mouse_pos[1] < data['rect'].y + data['rect'].height:
            data['on_press']()
        return data


class Label(UIObject):
    @classmethod
    def setup(cls, data):
        data['font'] = pygame.font.Font('NotoSans-Regular.ttf', data['font_size'])
        return data
