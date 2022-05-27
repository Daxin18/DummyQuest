import pygame

import settings
from utils import display, collision_table, display_scroll

texture = pygame.image.load("textures\\Rock.xcf")


class Rock:
    def __init__(self, x, y, width, height):
        self.hp = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hit_box = pygame.Rect(self.x - 3 * self.width/8, self.y - 3 * self.height/8,
                                   3 * self.width/4, 3 * self.height/4)

    def render_solid(self):
        self.hit_box = pygame.Rect(self.x - 3 * self.width/8 + display_scroll[0],
                                   self.y - 3 * self.height/8 + display_scroll[1], 3 * self.width/4, 3 * self.height/4)
        if settings.enable_hit_boxes:
            pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        display.blit(pygame.transform.scale(texture, (self.width, self.height)),
                     (self.x - self.width/2 + display_scroll[0], self.y - self.height/2 + display_scroll[1]))

    def check_player_collision(self, player):
        if self.hit_box.colliderect(player.hit_box):
            top = player.hit_box.top - self.hit_box.bottom
            bottom = player.hit_box.bottom - self.hit_box.top
            right = player.hit_box.right - self.hit_box.left
            left = player.hit_box.left - self.hit_box.right
            if abs(top) < settings.rock_collision_tolerance:   # top collision
                collision_table[1] = 1
                print("top collision")
            if abs(bottom) < settings.rock_collision_tolerance:  # bottom collision
                collision_table[1] = -1
                print("bottom collision")
            if abs(right) < settings.rock_collision_tolerance:  # right collision
                collision_table[0] = 1
                print("right collision")
            if abs(left) < settings.rock_collision_tolerance:  # left collision
                collision_table[0] = -1
                print("left collision")

    def damage(self, damage):
        self.hp += damage
        return True
