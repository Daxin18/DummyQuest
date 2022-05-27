import pygame
import random
from settings import damage_flick, damage_flick_cooldown, collision_tolerance

pygame.init()

display = pygame.display.set_mode((1200, 700))
display_scroll = [0, 0]
collision_table = [0, 0]    # collision on x, collision on y

player_x = display.get_width()/2
player_y = display.get_height()/2

player_bullets = []
enemies = []
enemy_bullets = []
solids = []  # aka things you can collide with
assets = []

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
font_health = pygame.font.Font('freesansbold.ttf', 12)
font_enemies = pygame.font.Font('freesansbold.ttf', 20)

game_running = False
running = True


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


def check_player_collision(solid, player):
    if solid.hit_box.colliderect(pygame.Rect(player.x - player.width / 2 - 10, player.y - player.height / 2 - 10,
                                             player.width + 20, player.height + 20)):
        top = player.hit_box.top - solid.hit_box.bottom
        bottom = player.hit_box.bottom - solid.hit_box.top
        right = player.hit_box.right - solid.hit_box.left
        left = player.hit_box.left - solid.hit_box.right
        if abs(top) < collision_tolerance:   # top collision
            collision_table[1] = 1
            print("top collision")
        if abs(bottom) < collision_tolerance:  # bottom collision
            collision_table[1] = -1
            print("bottom collision")
        if abs(right) < collision_tolerance:  # right collision
            collision_table[0] = 1
            print("right collision")
        if abs(left) < collision_tolerance:  # left collision
            collision_table[0] = -1
            print("left collision")
