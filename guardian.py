import pygame
import math
import random

import settings
import utils
from utils import display, player_x, player_y
from bullet import Bullet

texture = pygame.image.load("textures\\drawing.png")
player_still = pygame.image.load("textures\\Player_still.xcf")
standing = [pygame.image.load("textures\\Guardian_standing_0.xcf"),
            pygame.image.load("textures\\Guardian_standing_1.xcf"),
            pygame.image.load("textures\\Guardian_standing_2.xcf"),
            pygame.image.load("textures\\Guardian_standing_3.xcf")]
buried = [pygame.image.load("textures\\Guardian_buried_0.xcf"),
          pygame.image.load("textures\\Guardian_buried_1.xcf"),
          pygame.image.load("textures\\Guardian_buried_2.xcf")]
shield = pygame.image.load("textures\\Guardian_protection.xcf")


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
        self.guarding.protected = True
        self.animation_counter = 0

    def main(self):
        self.handle_damage()
        # pygame.draw.rect(display, (255, 0, 0), self.hit_box)
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
        self.guarding.protected = True
        if self.buried:  # buried aka moving
            bur = int(self.animation_counter / 20) - 1
            if self.animation_counter == 60:
                self.animation_counter = 0
            else:
                self.animation_counter += 1
            self.texture = buried[bur]
            if self.behaviour_change_timer != 0:
                self.behaviour_change_timer -= 1
                self.x -= self.vel_x
                self.y -= self.vel_y
            else:
                self.buried = False
                self.behaviour_change_timer = settings.guardian_idle_time
        else:
            sta = int(self.animation_counter / 15) - 1
            if self.animation_counter == 60:
                self.animation_counter = 0
            else:
                self.animation_counter += 1
            self.texture = standing[sta]
            if self.behaviour_change_timer != 0:
                self.behaviour_change_timer -= 1
            else:
                self.buried = True
                self.behaviour_change_timer = settings.guardian_buried_time
                deviation_x = random.randint(-settings.guardian_min_deviation_range,
                                             settings.guardian_max_deviation_range)
                deviation_y = random.randint(-settings.guardian_min_deviation_range,
                                             settings.guardian_max_deviation_range)
                angle = math.atan2(self.y - self.guarding.y - deviation_y, self.x - self.guarding.x - deviation_x)
                self.vel_x = math.cos(angle) * self.speed
                self.vel_y = math.sin(angle) * self.speed

        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        display.blit(shield, (self.guarding.x - self.guarding.size, self.guarding.y +5))
        display.blit(self.texture, (self.x - self.width/2, self.y - self.height/2))

    def player_in_range(self):
        return math.sqrt((self.x - utils.player_x) ** 2 + (self.y - utils.player_y) ** 2) <= settings.guardian_sight_range

    def attack(self, enemy_bullets):
        0

    def die(self, enemy_bullets):
        self.guarding.protected = False

    def damage(self, damage):
        if not self.buried and not self.damaged:
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
        return not self.buried
