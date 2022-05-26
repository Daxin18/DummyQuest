import pygame
import math
import random

import settings
import utils
from utils import display, player_x, player_y, handle_damage, give_damage, enemy_bullets
from bullet import Bullet

standing = [pygame.image.load("textures\\Guardian_standing_0.xcf"),
            pygame.image.load("textures\\Guardian_standing_1.xcf"),
            pygame.image.load("textures\\Guardian_standing_2.xcf"),
            pygame.image.load("textures\\Guardian_standing_3.xcf")]
buried = [pygame.image.load("textures\\Guardian_buried_0.xcf"),
          pygame.image.load("textures\\Guardian_buried_1.xcf"),
          pygame.image.load("textures\\Guardian_buried_2.xcf")]
shield = pygame.image.load("textures\\Guardian_protection.xcf")
bullet = pygame.image.load("textures\\Guardian_bullet.xcf")


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
        handle_damage(self)
        if settings.enable_hit_boxes:
            pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        self.behaviour()

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
        display.blit(shield, (self.guarding.x - self.guarding.size, self.guarding.y + 5))
        display.blit(self.texture, (self.x - self.width/2, self.y - self.height/2))

    def player_in_range(self):
        return math.sqrt((self.x - utils.player_x) ** 2 + (self.y - utils.player_y) ** 2) <= settings.guardian_sight_range

    def attack(self):
        timer = settings.guardian_attack_cast_time + self.behaviour_change_timer == settings.guardian_idle_time
        if not self.buried and timer and self.player_in_range():
            enemy_bullets.append(Bullet(self.x, self.y - self.height/2 + 10, player_x, player_y,
                                        settings.guardian_bullet_size, settings.guardian_bullet_TTL,
                                        settings.guardian_bullet_damage, settings.guardian_bullet_speed, bullet))

    def die(self):
        self.guarding.protected = False

    def damage(self, damage):
        if not self.buried:
            give_damage(self, damage)
        return not self.buried
