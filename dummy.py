import pygame
import math
import random

import settings
from utils import display, player_y, player_x

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
        self.protected = False

    def main(self):
        self.handle_damage()
        self.hit_box = pygame.Rect(self.x - self.size + 5, self.y - self.size + 5, self.width - 10, self.height - 10)
        if settings.enable_hit_boxes:
            pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        self.render()

    def handle_damage(self):
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

    def render(self):
        angle = (180 / math.pi) * -math.atan2(player_y - self.y, player_x - self.x)
        dummy_copy = pygame.transform.rotate(dummy_texture, angle)
        display.blit(dummy_copy,
                     (self.x - dummy_copy.get_width()/2, self.y - dummy_copy.get_height()/2))

    def attack(self, enemy_bullets):
        self.hp = self.hp
        # print(enemy_bullets)
        # print("Dummy attacked!")

    def die(self):
        self.hp = self.hp
        print("Dummy died!")

    def damage(self, damage):
        if not self.protected and not self.damaged:
            self.damage_flick_dir = random.randint(0, 3)
            if self.damage_flick_dir == 0:
                self.x -= settings.damage_flick
            elif self.damage_flick_dir == 1:
                self.y -= settings.damage_flick
            elif self.damage_flick_dir == 2:
                self.x += settings.damage_flick
            else:
                self.y += settings.damage_flick
            self.damaged = True
            self.damage_flick_cooldown = settings.damage_flick_cooldown
            self.hp -= damage
        return True
