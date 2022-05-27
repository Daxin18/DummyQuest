import pygame
import math

import settings
from utils import display, display_scroll


class Bullet:
    def __init__(self, x, y, dst_x, dst_y, size, ttl, damage, speed, texture, player_bullet=False):
        self.dmg = damage
        self.size = size
        self.x = x
        self.y = y
        self.mouse_x = dst_x
        self.mouse_y = dst_y
        self.speed = speed
        self.angle = math.atan2(y - dst_y, x - dst_x)
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        self.TTL = ttl
        self.texture = texture

        self.corr = [0, 0]
        if player_bullet:
            self.corr[0] += display_scroll[0]
            self.corr[1] += display_scroll[1]

    def main(self):
        self.x -= self.vel_x
        self.y -= self.vel_y
        self.TTL -= 1
        self.hit_box = pygame.Rect(self.x - self.size + display_scroll[0] - self.corr[0],
                                   self.y - self.size + display_scroll[1] - self.corr[1],
                                   self.size*2, self.size*2)
        if settings.enable_bullet_hit_boxes:
            pygame.draw.rect(display, (0, 255, 0), self.hit_box)
        display.blit(pygame.transform.scale(self.texture, (self.size * 2, self.size * 2)),
                     (self.x - self.size + display_scroll[0] - self.corr[0],
                      self.y - self.size + display_scroll[1] - self.corr[1]))

    def damage(self, entity):
        return entity.damage(self.dmg)
