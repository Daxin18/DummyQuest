import pygame
import math
import random

import settings
import utils
from utils import display, handle_damage, give_damage, display_scroll
from bullet import Bullet
from item import Item

slime_bullet_texture = pygame.image.load("textures\\Slime_bullet.xcf")
still_animation = [pygame.image.load("textures\\Slime_still_0.xcf"), pygame.image.load("textures\\Slime_still_1.xcf"),
                   pygame.image.load("textures\\Slime_still_2.xcf"), pygame.image.load("textures\\Slime_still_3.xcf"),
                   pygame.image.load("textures\\Slime_still_0.xcf")]


class Slime:
    def __init__(self, x, y):
        self.size = settings.slime_size
        self.width = self.size*2
        self.height = self.size*2
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
        self.protected = False
        self.animation_counter = 0
        self.movement_blockade = [0, 0]

    def main(self):
        handle_damage(self)
        self.behaviour()
        self.x -= self.vel_x
        self.y -= self.vel_y
        self.hit_box = pygame.Rect(self.x - self.size + display_scroll[0],
                                   self.y - self.size + display_scroll[1], self.size * 2, self.size * 2)

        texture = int(self.animation_counter/12) - 1
        if self.animation_counter == 60:
            self.animation_counter = 0
        else:
            self.animation_counter += 1
        if settings.enable_hit_boxes:
            pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        display.blit(pygame.transform.scale(still_animation[texture], (self.size*2, self.size*2)),
                     (self.x - self.size + display_scroll[0], self.y - self.size + display_scroll[1]))

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
        return math.sqrt((self.x + display_scroll[0] - utils.player_x) ** 2 +
                         (self.y + display_scroll[1] - utils.player_y) ** 2)\
               <= settings.slime_sight_range

    def follow_player(self):
        deviation_x = random.randint(-settings.slime_wandering_range, settings.slime_wandering_range)
        deviation_y = random.randint(-settings.slime_wandering_range, settings.slime_wandering_range)
        self.angle = math.atan2(self.y + display_scroll[1] - utils.player_y - deviation_y,
                                self.x + display_scroll[0] - utils.player_x - deviation_x)

    def wander(self):
        deviation_x = random.randint(-settings.slime_wandering_range, settings.slime_wandering_range)
        deviation_y = random.randint(-settings.slime_wandering_range, settings.slime_wandering_range)
        self.angle = math.atan2(self.y + display_scroll[1] + deviation_y - self.y - display_scroll[1],
                                self.x + display_scroll[0] + deviation_x - self.x - display_scroll[0])

    def attack(self, game):
        if self.attack_cooldown == 0 and self.player_in_range():
            game.enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y, settings.slime_bullet_size,
                                             settings.slime_bullet_TTL, settings.slime_bullet_dmg,
                                             settings.slime_bullet_speed, slime_bullet_texture))
            game.enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y, settings.slime_bullet_size,
                                             settings.slime_bullet_TTL, settings.slime_bullet_dmg,
                                             settings.slime_bullet_speed, slime_bullet_texture))
            game.enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y + math.sqrt(3),
                                             settings.slime_bullet_size,
                                             settings.slime_bullet_TTL, settings.slime_bullet_dmg,
                                             settings.slime_bullet_speed, slime_bullet_texture))
            game.enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y + math.sqrt(3),
                                             settings.slime_bullet_size,
                                             settings.slime_bullet_TTL, settings.slime_bullet_dmg,
                                             settings.slime_bullet_speed, slime_bullet_texture))
            game.enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y - math.sqrt(3),
                                             settings.slime_bullet_size,
                                             settings.slime_bullet_TTL, settings.slime_bullet_dmg,
                                             settings.slime_bullet_speed, slime_bullet_texture))
            game.enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y - math.sqrt(3),
                                             settings.slime_bullet_size,
                                             settings.slime_bullet_TTL, settings.slime_bullet_dmg,
                                             settings.slime_bullet_speed, slime_bullet_texture))
            self.attack_cooldown = settings.slime_attack_cooldown
        elif self.attack_cooldown != 0:
            self.attack_cooldown -= 1

    def die(self, game):
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x - math.sqrt(3), self.y + 1, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x + math.sqrt(3), self.y + 1, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x - math.sqrt(3), self.y - 1, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x + math.sqrt(3), self.y - 1, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y + math.sqrt(3), settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y + math.sqrt(3), settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x - 1, self.y - math.sqrt(3), settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x + 1, self.y - math.sqrt(3), settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x, self.y + 1, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemy_bullets.append(Bullet(self.x, self.y, self.x, self.y - 1, settings.slime_bullet_size,
                                         settings.slime_death_bullet_TTL, settings.slime_death_bullet_dmg,
                                         settings.slime_bullet_speed, slime_bullet_texture))
        game.enemies.remove(self)
        if random.randint(0, game.player.hp - 1) == 0:
            game.items.append(Item(self.x, self.y, Item.pizza, Item.item_textures[0]))


    def damage(self, damage):
        if not self.protected:
            give_damage(self, damage)
        return True
