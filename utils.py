import pygame
import random
from settings import damage_flick, damage_flick_cooldown

pygame.init()

display = pygame.display.set_mode((1200, 700))
display_scroll = [0, 0]

player_x = display.get_width()/2
player_y = display.get_height()/2

player_bullets = []
enemies = []
enemy_bullets = []

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
font_health = pygame.font.Font('freesansbold.ttf', 12)
font_enemies = pygame.font.Font('freesansbold.ttf', 20)


def move(x, y):
    display_scroll[0] += x
    display_scroll[1] += y


def handle_damage(self):
    if self.damage_flick_cooldown != 0:
        self.damage_flick_cooldown -= 1
    elif self.damaged:
        self.damaged = False
        if self.damage_flick_dir == 0:
            self.x += damage_flick
        elif self.damage_flick_dir == 1:
            self.y += damage_flick
        elif self.damage_flick_dir == 2:
            self.x -= damage_flick
        else:
            self.y -= damage_flick


def give_damage(self, damage):
    if not self.damaged:
        self.damage_flick_dir = random.randint(0, 3)
        if self.damage_flick_dir == 0:
            self.x -= damage_flick
        elif self.damage_flick_dir == 1:
            self.y -= damage_flick
        elif self.damage_flick_dir == 2:
            self.x += damage_flick
        else:
            self.y += damage_flick
        self.damaged = True
        self.damage_flick_cooldown = damage_flick_cooldown
    self.hp -= damage
