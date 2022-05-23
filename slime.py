import pygame
import math
import random

import settings
import utils
from utils import display
from bullet import Bullet

slime_bullet_texture = pygame.image.load("textures\\Slime_bullet.xcf")
still_animation = [pygame.image.load("textures\\Slime_still_0.xcf"), pygame.image.load("textures\\Slime_still_1.xcf"),
                   pygame.image.load("textures\\Slime_still_2.xcf"), pygame.image.load("textures\\Slime_still_3.xcf"),
                   pygame.image.load("textures\\Slime_still_0.xcf")]


class Slime:
    def __init__(self, x, y):
        self.size = settings.slime_size
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size*2, self.size*2)
        self.damage_flick_cooldown = 0
        self.damaged = False
        self.damage_flick_dir = 0
        self.speed = settings.slime_speed
        self.angle = math.atan2(y - utils.player_y, x - utils.player_x)
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.behaviour_change_timer = 0
        self.attack_cooldown = settings.slime_attack_cooldown
        self.hp = settings.slime_hp
        self.damageable = True
        self.animation_counter = 0

    def main(self):
        self.handle_damage()
        self.behaviour()
        self.x -= self.vel_x
        self.y -= self.vel_y
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

        texture = int(self.animation_counter/12) - 1
        if self.animation_counter == 60:
            self.animation_counter = 0
        else:
            self.animation_counter += 1
        # pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        display.blit(pygame.transform.scale(still_animation[texture], (self.size*2, self.size*2)),
                     (self.x - self.size, self.y - self.size))

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
        if self.behaviour_change_timer == 0:
            if self.player_in_range() and random.randint(0, settings.slime_wander_off_probability) != 0:
                self.follow_player()
            else:
                self.wander()
            self.vel_x = math.cos(self.angle) * self.speed
            self.vel_y = math.sin(self.angle) * self.speed
            self.behaviour_change_timer = settings.slime_behaviour_change
        else:
            self.behaviour_change_timer -= 1

    def player_in_range(self):
        return math.sqrt((self.x - utils.player_x) ** 2 + (self.y - utils.player_y) ** 2) <= settings.slime_sight_range

    def follow_player(self):
        deviation_x = random.randint(-settings.slime_min_wandering_range, settings.slime_max_wandering_range)
        deviation_y = random.randint(-settings.slime_min_wandering_range, settings.slime_max_wandering_range)
        self.angle = math.atan2(self.y - utils.player_y - deviation_y, self.x - utils.player_x - deviation_x)

    def wander(self):
        deviation_x = random.randint(-settings.slime_min_wandering_range, settings.slime_max_wandering_range)
        deviation_y = random.randint(-settings.slime_min_wandering_range, settings.slime_max_wandering_range)
        self.angle = math.atan2(self.y + deviation_y, self.x + deviation_x)

    def attack(self, enemy_bullets):
        if self.attack_cooldown == 0 and self.player_in_range():
            enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y, settings.slime_bullet_size,
                                        settings.slime_bullet_TTL, settings.slime_bullet_dmg, slime_bullet_texture))
            enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y, settings.slime_bullet_size,
                                        settings.slime_bullet_TTL, settings.slime_bullet_dmg, slime_bullet_texture))
            enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y + 2, settings.slime_bullet_size,
                                        settings.slime_bullet_TTL, settings.slime_bullet_dmg, slime_bullet_texture))
            enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y + 2, settings.slime_bullet_size,
                                        settings.slime_bullet_TTL, settings.slime_bullet_dmg, slime_bullet_texture))
            enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y - 2, settings.slime_bullet_size,
                                        settings.slime_bullet_TTL, settings.slime_bullet_dmg, slime_bullet_texture))
            enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y - 2, settings.slime_bullet_size,
                                        settings.slime_bullet_TTL, settings.slime_bullet_dmg, slime_bullet_texture))
            self.attack_cooldown = settings.slime_attack_cooldown
        elif self.attack_cooldown != 0:
            self.attack_cooldown -= 1

    def die(self, enemy_bullets):
        enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x - 2, self.y + 1, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x + 2, self.y + 1, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x - 2, self.y - 1, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x + 2, self.y - 1, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y + 2, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y + 2, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y - 2, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y - 2, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x, self.y + 1, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
        enemy_bullets.append(Bullet(self.x, self.y, self.x, self.y - 1, settings.slime_bullet_size,
                                    settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                    slime_bullet_texture))
