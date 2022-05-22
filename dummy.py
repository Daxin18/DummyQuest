import pygame

import settings
from utils import display

dummy_texture = pygame.image.load("textures\\Dummy.xcf")


class Dummy:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.size = width/2
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.damage_flick_cooldown = 0
        self.damaged = False
        self.damage_flick_dir = 0
        self.hp = 10000

    def main(self):
        if self.damage_flick_cooldown != 0:
            self.damage_flick_cooldown -= 1
        elif self.damaged:
            self.damaged = False
            if self.damage_flick_dir == 0:
                self.x += settings.damage_flick
            elif self.damage_flick_dir == 1:
                self.y += settings.damage_flick
            elif self.damage_flick_dir == 2:
                self.x -= settings.damage_flick
            else:
                self.y -= settings.damage_flick

        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.width, self.height)
        # pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        # pygame.draw.circle(display, (160, 90, 80), (self.x, self.y), self.width/2)
        display.blit(dummy_texture, (self.x - self.size, self.y - self.size))

    def attack(self, enemy_bullets):
        self.hp = self.hp
        # print(enemy_bullets)
        # print("Dummy attacked!")

    def die(self):
        self.hp = self.hp
        print("Dummy died!")
