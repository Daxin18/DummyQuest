import pygame
import math
import random

import settings
from utils import display, font
from bullet import Bullet

player_still = pygame.image.load("textures\\Player_still.xcf")
player_running = [pygame.image.load("textures\\Player_running_0.xcf"),
                  pygame.image.load("textures\\Player_running_1.xcf")]
player_bullet_texture = pygame.image.load("textures\\Player_bullet.xcf")
dash_trail = pygame.image.load("textures\\dash_trail.xcf")


class Player:
    def __init__(self, x, y, width, height):
        self.hp = settings.player_hp
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dash_cooldown = 0
        self.dash_remaining = settings.dash_duration
        self.dashing = False
        self.running = False
        self.shotgun_cooldown = 0
        self.shotgun_penalty = 0
        self.shooting_penalty = 0
        self.damage_flick_cooldown = 0
        self.damaged = False
        self.damage_flick_dir = 0
        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.running_animation_timer = 0
        self.last_dash_activation_x = self.x
        self.last_dash_activation_y = self.y
        self.dash_trail_copy = dash_trail
        self.dash_offset_x = 96
        self.dash_offset_y = 96
        self.damageable = True

    def main(self, mouse_x, mouse_y):
        if self.dash_cooldown != 0:
            self.dash_cooldown -= 1
        if self.shotgun_cooldown != 0:
            self.shotgun_cooldown -= 1
        if self.shotgun_penalty != 0:
            self.shotgun_penalty -= 1
        if self.shooting_penalty != 0:
            self.shooting_penalty -= 1
        self.handle_damage()
        self.draw_player(mouse_x, mouse_y)

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

    def dash(self, keys):
        if self.dash_remaining == settings.dash_duration:
            self.determine_dash_direction(keys)
        self.dash_remaining -= 1
        self.dashing = True
        if self.dash_remaining == 0:
            self.dash_cooldown = settings.dash_cooldown
            self.dash_remaining = settings.dash_duration
            self.dashing = False
            self.last_dash_activation_x = self.x
            self.last_dash_activation_y = self.y

    def determine_dash_direction(self, keys):
        if keys[pygame.K_a]:
            self.last_dash_activation_x = self.x + 10
        if keys[pygame.K_w]:
            self.last_dash_activation_y = self.y + 10
        if keys[pygame.K_s]:
            self.last_dash_activation_y = self.y - 10
        if keys[pygame.K_d]:
            self.last_dash_activation_x = self.x - 10

        angle = (180/math.pi) * -math.atan2(self.last_dash_activation_y - self.y, self.last_dash_activation_x - self.x)
        match angle:
            case num if num > 170 or num < -170 or -10 < num < 10:  # aka going E or W
                self.dash_offset_x = 96
                self.dash_offset_y = 18
            case num if 80 < num < 100 or -100 < num < -80:     # aka going N or S
                self.dash_offset_x = 16
                self.dash_offset_y = 96
            case num if -150 < num < -130 or 40 < num < 60:     # aka going SW or NEs
                self.dash_offset_x = 78
                self.dash_offset_y = 80
            case num if 130 < num < 150 or -60 < num < -40:     # aka going SE or NW
                self.dash_offset_x = 76
                self.dash_offset_y = 76
        self.dash_trail_copy = pygame.transform.rotate(dash_trail, angle)

    def reset_dash(self):
        if self.dashing:
            self.dash_cooldown = settings.dash_cooldown
            self.dash_remaining = settings.dash_duration
            self.dashing = False
            self.last_dash_activation_x = self.x
            self.last_dash_activation_y = self.y

    def draw_player(self, mouse_x, mouse_y):
        angle = (180/math.pi) * -math.atan2(mouse_y - self.y, mouse_x - self.x) - 90

        if self.running:
            if self.running_animation_timer < 30:
                player_copy = pygame.transform.rotate(player_running[0], angle)
                self.running_animation_timer += 1
            elif self.running_animation_timer < 59:
                player_copy = pygame.transform.rotate(player_running[1], angle)
                self.running_animation_timer += 1
            else:
                player_copy = pygame.transform.rotate(player_running[1], angle)
                self.running_animation_timer = 0
        else:
            player_copy = pygame.transform.rotate(player_still, angle)
            if self.running_animation_timer < 30:
                self.running_animation_timer = 30
            else:
                self.running_animation_timer = 0

        if self.dashing:
            display.blit(self.dash_trail_copy, (self.x - self.dash_offset_x, self.y - self.dash_offset_y))

        correction = 6 * abs(math.sin(2 * math.radians(angle)))
        display.blit(player_copy,
                     (self.x - self.width / 2 - correction, self.y - self.height / 2 - correction))

    def show_dash_cooldown(self):
        if self.dash_cooldown != 0:
            cd = font.render("Dash: on cooldown (" + str(round(self.dash_cooldown/60, 1)) + "s)", True, (255, 0, 0))
        else:
            cd = font.render("Dash: Ready", True, (0, 255, 0))
        display.blit(cd, (5, display.get_height() - 35))

    def distance_to_crosshair(self, mouse_x, mouse_y):
        return math.sqrt((self.x - mouse_x) ** 2 + (self.y - mouse_y) ** 2)

    def primary_fire(self, mouse_x, mouse_y, player_bullets):
        player_bullets.append(Bullet(self.x, self.y, mouse_x, mouse_y, settings.bullet_size,
                                     settings.bullet_TTL, settings.base_bullet_damage,
                                     player_bullet_texture))
        self.shooting_penalty = settings.shooting_penalty_time

    def shotgun(self, mouse_x, mouse_y, player_bullets):
        if self.shotgun_cooldown == 0:
            spread = int(self.distance_to_crosshair(mouse_x, mouse_y) / settings.shotgun_spread)
            i = 0
            while i < settings.shotgun_pellets:
                mouse_x_1 = mouse_x + random.randint(-spread, spread)
                mouse_y_1 = mouse_y + random.randint(-spread, spread)
                player_bullets.append(Bullet(self.x, self.y, mouse_x_1, mouse_y_1, settings.shotgun_pellet_size,
                                             settings.bullet_TTL, settings.shotgun_pellet_damage,
                                             player_bullet_texture))
                i += 1
            self.shotgun_cooldown = settings.shotgun_cooldown
            self.shotgun_penalty = settings.shotgun_shooting_penalty_time

    def damage(self, damage):
        if not self.dashing and not self.damaged:
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
