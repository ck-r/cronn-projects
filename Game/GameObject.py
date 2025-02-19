import pygame.draw
from pygame import draw
import Block


class Objekt:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.x_blok = x // Block.ROZMIAR_BLOKU
        self.y_blok = y // Block.ROZMIAR_BLOKU
        self.__width = width
        self.__height = height
        self.phys_enabled = False

    def get_width(self):
        return self.__width

    def get_height(self):
        return self.__height

    def update(self, gravity, delta_time):
        self.x_blok = self.x // Block.ROZMIAR_BLOKU
        self.y_blok = self.y // Block.ROZMIAR_BLOKU

    def draw(self, surface, scroll_x, scroll_y):
        pass

class Pleyer(Objekt):
    def __init__(self, x, y, width, height, image, health, damage, speed):
        super().__init__(x, y, width, height)
        self.image = image
        self.__max_health = health
        self.__health = health
        self.damage = damage
        self.speed = speed
        self.velocity_x = 0
        self.velocity_y = 0
        self.grounded = False
        self.can_jump = True

    def update(self, gravity, delta_time):
        super().update(gravity, delta_time)
        self.x += self.velocity_x
        self.y += self.velocity_y
        if not self.grounded:
            self.velocity_y += gravity * delta_time
        if Block.znajdz_blok(self.x_blok, self.y_blok + 2) is not None or Block.znajdz_blok(self.x_blok + 1, self.y_blok + 2) is not None:
            if self.grounded:
                self.y = self.y_blok * Block.ROZMIAR_BLOKU
            self.grounded = True
            self.velocity_y = 0
        else:
            self.grounded = False
        if Block.znajdz_blok(self.x_blok, self.y_blok - 1) is not None or Block.znajdz_blok(self.x_blok + 1, self.y_blok - 1) is not None:
            self.can_jump = False
            self.velocity_y = 0
        else:
            self.can_jump = True

    def draw(self, surface, scroll_x, scroll_y):
        surface.blit(self.image, (self.x - scroll_x, self.y - scroll_y, self.image.get_rect()[2], self.image.get_rect()[3]))
        pygame.draw.rect(surface, (255, 0, 0), (self.x - scroll_x, self.y - scroll_y - 10, round(self.image.get_rect()[2] * (self.__health / self.__max_health)),3))

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def jump(self, force):
        if self.grounded and self.can_jump:
            self.grounded = False
            self.velocity_y = -force

    def attack(self, target):
        target.get_damage(self.damage)

    def is_alive(self):
        return self.__health > 0

    def get_damage(self, damage):
        self.__health -= damage
        if not self.is_alive():
            self.x = 0
            self.y = 0
            self.__health = self.__max_health


class Enemy(Objekt):
    def __init__(self, x, y, width, height, image, health, damage):
        super().__init__(x, y, width, height)
        self.image = image
        self.max_health = health
        self.__health = health
        self.damage = damage
        self.grounded = False
        self.velocity_x = 0
        self.velocity_y = 0
        self.zablokowany_lewo = False
        self.zablokowany_prawo = False

    def draw(self, surface, scroll_x, scroll_y):
        if self.is_alive():
            surface.blit(self.image, (self.x - scroll_x, self.y - scroll_y, self.image.get_rect()[2], self.image.get_rect()[3]))
            pygame.draw.rect(surface, (255, 0, 0), (self.x - scroll_x, self.y - scroll_y - 10, round(self.image.get_rect()[2] * (self.__health / self.max_health)), 3))

    def jump(self, force, direction):
        if self.grounded and self.can_jump:
            self.grounded = False
            self.velocity_y = -force
            self.velocity_x = force * direction

    def update(self, gravity, delta_time):
        super().update(gravity, delta_time)
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.is_alive():
            if not self.grounded:
                self.velocity_y += gravity * delta_time
            if Block.znajdz_blok(self.x_blok, self.y_blok + 1) is not None or Block.znajdz_blok(self.x_blok + 1, self.y_blok + 1) is not None:
                if self.grounded:
                    self.y = self.y_blok * Block.ROZMIAR_BLOKU
                self.grounded = True
                self.velocity_y = 0
            else:
                self.grounded = False
            if Block.znajdz_blok(self.x_blok, self.y_blok - 1) is not None or Block.znajdz_blok(self.x_blok + 1, self.y_blok - 1) is not None:
                self.can_jump = False
                self.velocity_y = 0
            else:
                self.can_jump = True

            if Block.znajdz_blok(self.x_blok, self.y_blok) is not None:
                self.zablokowany_lewo = False
                self.velocity_x = 0
            else:
                self.zablokowany_lewo = True
            if Block.znajdz_blok(self.x_blok + 1, self.y_blok) is not None:
                self.zablokowany_lewo = False
                self.velocity_x = 0
            else:
                self.zablokowany_lewo = True

    def attack(self, target):
        target.get_damage(self.damage)

    def is_alive(self):
        return self.__health > 0

    def get_damage(self, damage):
        self.__health -= damage
        if not self.is_alive():
            print(self)
            del self