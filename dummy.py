import pygame
import math

import settings
import utils
from utils import display, player_y, player_x, handle_damage, give_damage, display_scroll
from item import Item

dummy_texture = pygame.image.load("textures\\Dummy.xcf")


class Dummy:
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height
        self.size = width/2
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.damage_flick_cooldown = 0
        self.damaged = False
        self.damage_flick_dir = 0
        self.hp = settings.dummy_hp
        self.protected = False
        self.movement_blockade = [0, 0]

    def main(self):
        handle_damage(self)
        self.hit_box = pygame.Rect(self.x - self.size + 5 + display_scroll[0],
                                   self.y - self.size + 5 + display_scroll[1], self.width - 10, self.height - 10)
        if settings.enable_hit_boxes:
            pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        self.render()

    def render(self):
        angle = (180 / math.pi) * -math.atan2(player_y - self.y - display_scroll[1], player_x - self.x - display_scroll[0])
        dummy_copy = pygame.transform.rotate(dummy_texture, angle)
        display.blit(dummy_copy,
                     (self.x - dummy_copy.get_width()/2 + display_scroll[0],
                      self.y - dummy_copy.get_height()/2 + display_scroll[1]))

    def attack(self, game):
        self.hp = self.hp
        # print(enemy_bullets)
        # print("Dummy attacked!")

    def die(self, game):
        self.hp = self.hp
        print("Dummy died!")
        game.enemies.remove(self)
        game.solids.remove(self)
        if utils.gamemode != 1:
            game.items.append(Item(self.x, self.y, Item.game_won, Item.item_textures[3]))

    def damage(self, damage):
        if not self.protected and not utils.tutorial_running:
            give_damage(self, damage)
        return True

    def render_solid(self): # needs to be implemented to enable collision, subject to change
        self.hp = self.hp
