import pygame
import math

import settings
import utils
from utils import display, display_scroll, player_x, player_y, font_items


class Item:
    item_textures = [pygame.image.load("textures\\pizza.xcf"), pygame.image.load("textures\\bullet_boost.xcf"),
                     pygame.image.load("textures\\shotgun_boost.xcf"), pygame.image.load("textures\\Player_bullet.xcf")]

    def __init__(self, x, y, function, texture):
        self.x = x
        self.y = y
        self.texture = texture
        self.function = function
        self.hover_counter = -settings.item_hover_time
        self.hover_amount = settings.item_hover_amount

    def main(self):
        self.render_item()

    def render_item(self):
        if self.hover_counter == settings.item_hover_time:
            self.hover_counter = -settings.item_hover_time
        elif self.hover_counter < 0:
            self.y -= self.hover_amount
            self.hover_counter += 1
        else:
            self.y += self.hover_amount
            self.hover_counter += 1
        display.blit(self.texture, (self.x + display_scroll[0], self.y + display_scroll[1]))
        if self.player_in_range():
            display.blit(font_items.render("Press [" + str(pygame.key.name(settings.pickup_key)) + "] to use",
                                           True, (255, 255, 255)),
                         (self.x + display_scroll[0] - 32, self.y + display_scroll[1] + 32))

    def player_in_range(self):
        return math.sqrt((self.x + display_scroll[0] - player_x) ** 2 +
                         (self.y + display_scroll[1] - player_y) ** 2) \
               <= settings.item_pickup_radius

    def use_item(self, game):
        if self.player_in_range():
            self.function(game)
            game.items.remove(self)

    @staticmethod
    def health_potion(game):
        game.player.hp += settings.health_potion_heal

    @staticmethod
    def base_damage_boost(game):
        game.player.base_bonus_damage += 1

    @staticmethod
    def shotgun_damage_boost(game):
        game.player.shotgun_bonus_damage += 1

    @staticmethod
    def game_won(game):
        utils.win = True
