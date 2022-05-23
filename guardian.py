import pygame
import math
import random

import settings
import utils
from utils import display, player_x, player_y
from bullet import Bullet

texture = pygame.image.load("textures\\drawing.png")
player_still = pygame.image.load("textures\\Player_still.xcf")


class Guardian:
    def __init__(self, x, y, guarding):
        self.width = settings.guardian_width
        self.height = settings.guardian_height
        self.size = self.height/2
        self.guarding = guarding
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.damage_flick_cooldown = 0
        self.damaged = False
        self.damage_flick_dir = 0
        self.speed = settings.guardian_speed
        self.behaviour_change_timer = 0
        self.hp = settings.guardian_hp
        self.buried = False
        self.vel_x = 0
        self.vel_y = 0
        self.texture = pygame.image.load("textures\\drawing.png")
        self.damageable = True
        self.guarding.damageable = False

    def main(self):
        self.handle_damage()
        self.behaviour()

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

    def behaviour(self):
        if self.buried: # buried aka moving
            self.texture = texture
            if self.behaviour_change_timer != 0:
                self.behaviour_change_timer -= 1
                self.x -= self.vel_x
                self.y -= self.vel_y
            else:
                self.buried = False
                self.damageable = True
                self.behaviour_change_timer = settings.guardian_idle_time
        else:
            self.texture = player_still
            if self.behaviour_change_timer != 0:
                self.behaviour_change_timer -= 1
            else:
                self.buried = True
                self.damageable = False
                self.behaviour_change_timer = settings.guardian_buried_time
                deviation_x = random.randint(-settings.guardian_min_deviation_range,
                                             settings.guardian_max_deviation_range)
                deviation_y = random.randint(-settings.guardian_min_deviation_range,
                                             settings.guardian_max_deviation_range)
                angle = math.atan2(self.guarding.y + deviation_y, self.guarding.x + deviation_x)
                self.vel_x = math.cos(angle) * self.speed
                self.vel_y = math.sin(angle) * self.speed

        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        display.blit(self.texture, (self.x, self.y))

    def player_in_range(self):
        return math.sqrt((self.x - utils.player_x) ** 2 + (self.y - utils.player_y) ** 2) <= settings.guardian_sight_range

    def attack(self, enemy_bullets):
        0

    def die(self, enemy_bullets):
        self.guarding.damageable = True
