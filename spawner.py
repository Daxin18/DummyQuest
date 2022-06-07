import pygame
import math
import random

import settings
from utils import display, player_y, player_x, handle_damage, give_damage, display_scroll
from slime import Slime
from guardian import Guardian
from item import Item

spawner_texture = pygame.image.load("textures\\Spawner.xcf")

"""
Spawner is the enemy that summons new enemies, has a lot of health

To be included in:
- enemies   (for attack, death, damage etc.)
- solids    (for collision)

Behaviour/ attack patterns:
- behaviour - stands in one place
- attack pattern - spawns 3 Slimes near it, in the direction of a player every few seconds

Special properties:
--> always spawns in with 4 Guardians, giving it "protected"* status
--> drops one pizza, base_damage_boost and shotgun_damage_boost + spawns 10 Slimes upon death
--> when HP falls below certain threshhold (depending on difficulty level) it starts spawning enemies significantly faster
--> gives Dummy invisible** "protected" status when present

* "protected" status - grants an enemy invincibility, while also making them stop all the bullets
** invisible - there is no visual indicator that enemy is protected
"""


class Spawner:
    def __init__(self, x, y, width, height, game):
        self.width = width
        self.height = height
        self.size = height/2
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2, self.width, self.height)
        self.damage_flick_cooldown = 0
        self.damaged = False
        self.damage_flick_dir = 0
        self.hp = settings.spawner_hp
        self.protected = False
        self.attack_cd = settings.spawner_spawn_cd
        self.enraged = False
        self.movement_blockade = [0, 0]

        game.enemies.append(Guardian(self.x - self.width, self.y - self.height, self))
        game.enemies.append(Guardian(self.x - self.width, self.y + self.height, self))
        game.enemies.append(Guardian(self.x + self.width, self.y + self.height, self))
        game.enemies.append(Guardian(self.x + self.width, self.y - self.height, self))

    def main(self):
        handle_damage(self)
        self.hit_box = pygame.Rect(self.x + display_scroll[0] - self.width/2,
                                   self.y + display_scroll[1] - self.height/2, self.height, self.width)
        if settings.enable_hit_boxes:
            pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        self.render()

    def render(self):
        texture_copy = pygame.transform.scale(spawner_texture, (self.height, self.width))
        display.blit(texture_copy,
                     (self.x + display_scroll[0] - self.width/2,
                      self.y + display_scroll[1] - self.height/2))
        if self.enraged:
            pygame.draw.circle(display, (255, 0, 0), (self.x, self.y), 15)

    def attack(self, game):
        game.enemies[0].protected = True    # Dummy is always the enemy with the index of 0
        if self.attack_cd == 0 and self.player_in_range():
            self.spawn_slimes(game, settings.spawner_spawn_amount)
            if self.enraged:
                self.attack_cd = settings.spawner_enraged_spawn_cd
            else:
                self.attack_cd = settings.spawner_spawn_cd
        elif self.attack_cd > 0:
            self.attack_cd -= 1

    def player_in_range(self):
        return math.sqrt((self.x + display_scroll[0] - player_x) ** 2 +
                         (self.y + display_scroll[1] - player_y) ** 2) \
                   <= settings.spawner_sight_range

    def die(self, game):
        game.enemies[0].protected = False   # Dummy is always the enemy with the index of 0
        self.spawn_slimes(game, settings.spawner_death_spawn_amount)
        game.enemies.remove(self)
        game.solids.remove(self)
        game.items.append(Item(self.x - 50, self.y, Item.pizza, Item.item_textures[0]))
        game.items.append(Item(self.x, self.y, Item.base_damage_boost, Item.item_textures[1]))
        game.items.append(Item(self.x + 50, self.y, Item.shotgun_damage_boost, Item.item_textures[2]))

    def damage(self, damage):
        if not self.protected:
            give_damage(self, damage)
            if self.hp <= settings.spawner_hp * settings.spawner_enrage_hp_ratio:
                self.enraged = True
        return True

    def render_solid(self):  # needs to be implemented to enable collision, subject to change
        self.hp = self.hp

    def spawn_slimes(self, game, amount):
        deviation_x = random.randint(-settings.spawner_spawn_deviation, settings.spawner_spawn_deviation)
        deviation_y = random.randint(-settings.spawner_spawn_deviation, settings.spawner_spawn_deviation)
        angle = math.atan2(self.y + display_scroll[1] - player_y - deviation_y,
                           self.x + display_scroll[0] - player_x - deviation_x)
        dist_x = self.x - (math.cos(angle) * settings.spawner_spawn_distance)
        dist_y = self.y - (math.sin(angle) * settings.spawner_spawn_distance)
        game.enemies.append(Slime(dist_x, dist_y))
        for i in range(0, amount - 1):
            deviation_x = random.randint(-settings.spawner_spawn_deviation, settings.spawner_spawn_deviation)
            deviation_y = random.randint(-settings.spawner_spawn_deviation, settings.spawner_spawn_deviation)
            game.enemies.append(Slime(dist_x + deviation_x, dist_y + deviation_y))
