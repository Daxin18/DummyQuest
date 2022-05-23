import pygame
import math
import random

import settings
from utils import display


class Bullet:
    def __init__(self, x, y, dest_x, dest_y, size, ttl, damage, texture):
        self.dmg = damage
        self.size = size
        self.x = x
        self.y = y
        self.mouse_x = dest_x
        self.mouse_y = dest_y
        self.speed = settings.bullet_speed
        self.angle = math.atan2(y - dest_y, x - dest_x)
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        self.TTL = ttl
        self.texture = texture

    def main(self):
        self.x -= self.vel_x
        self.y -= self.vel_y
        self.TTL -= 1
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size*2, self.size*2)
        # pygame.draw.rect(display, (0, 255, 0), self.hit_box)
        display.blit(pygame.transform.scale(self.texture, (self.size * 2, self.size * 2)),
                     (self.x - self.size, self.y - self.size))

    def damage(self, entity):
        if entity.damageable:
            if not entity.damaged:
                entity.damage_flick_dir = random.randint(0, 3)
                if entity.damage_flick_dir == 0:
                    entity.x -= settings.damage_flick
                elif entity.damage_flick_dir == 1:
                    entity.y -= settings.damage_flick
                elif entity.damage_flick_dir == 2:
                    entity.x += settings.damage_flick
                else:
                    entity.y += settings.damage_flick
                entity.damaged = True
                entity.damage_flick_cooldown = settings.damage_flick_cooldown
            entity.hp -= self.dmg
        return entity.damageable
