import pygame
import sys
import random

import settings
import utils
from utils import display, display_scroll, move, collision_table, tmapPath
from slime import Slime
from guardian import Guardian
from player import Player
from dummy import Dummy
from rock import Rock
from tree import Tree
from map import TileMap, SpriteSheet
from spawner import Spawner
from item import Item


class Game:
    def __init__(self):
        utils.set_game_parameters()
        utils.paused = False
        utils.win = False
        utils.dead = False

        self.player_bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.solids = []  # aka things you can collide with
        self.assets = []
        self.items = []
        self.time = 0

        self.player = Player(utils.player_x, utils.player_y, 32, 32)
        self.dummy = Dummy(600, 300, 40, 40)
        self.enemies.append(self.dummy)
        self.solids.append(self.dummy)

        self.spawn_cd = 0
        self.hit_box_cd = 0
        self.SCORE = 0

        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.environment_speed = settings.walking_speed

        self.generate_random_terrain()
        self.tmap = self.initialize_map()
        self.generate_spawners()
        self.generate_items()

    def main(self):
        self.time += 1
        self.check_for_end()
        self.reset_parameters()
        self.handle_collisions()
        self.tmap.draw_map()
        self.render_stuff()
        self.handle_controls()
        self.render_hud()
        pygame.display.update()
        # print("x: " + str(display_scroll[0]) + ", y: " + str(display_scroll[1]))  # to get coordinates for placement

    def generate_spawners(self):
        for i in range(0, settings.spawner_amount):
            spawn = Spawner(settings.spawner_coordinates[i][0], settings.spawner_coordinates[i][1],
                            settings.spawner_height, settings.spawner_width, self)
            self.enemies.append(spawn)
            self.solids.append(spawn)

    def generate_items(self):
        for coordinates in settings.pizza_coordinates:
            self.items.append(Item(coordinates[0], coordinates[1], Item.pizza, Item.item_textures[0]))
        for coordinates in settings.curse_coordinates:
            self.items.append(Item(coordinates[0], coordinates[1], Item.cursed_boost, Item.item_textures[4]))
        for coordinates in settings.base_boost_coordinates:
            self.items.append(Item(coordinates[0], coordinates[1], Item.base_damage_boost, Item.item_textures[1]))
        for coordinates in settings.shotgun_boost_coordinates:
            self.items.append(Item(coordinates[0], coordinates[1], Item.shotgun_damage_boost, Item.item_textures[2]))

    def generate_random_terrain(self):
        for i in range(settings.rock_number):
            r_x = random.randint(self.player.x - 1000, self.player.x + 1000)
            r_y = random.randint(self.player.y - 1000, self.player.y + 1000)
            while 550 < r_x < 650 and 250 < r_y < 350:
                r_x = random.randint(self.player.x - 1000, self.player.x + 1000)
                r_y = random.randint(self.player.y - 1000, self.player.y + 1000)
            r_w = random.randint(45, 70)
            r_h = random.randint(45, 70)
            self.solids.append(Rock(r_x, r_y, r_w, r_h))
        for i in range(settings.tree_number):
            r_x = random.randint(self.player.x - 1000, self.player.x + 1000)
            r_y = random.randint(self.player.y - 1000, self.player.y + 1000)
            while 550 < r_x < 650 and 250 < r_y < 350:
                r_x = random.randint(self.player.x - 1000, self.player.x + 1000)
                r_y = random.randint(self.player.y - 1000, self.player.y + 1000)
            r_s = random.randint(25, 40)
            self.assets.append(Tree(r_x, r_y, r_s))

    def check_for_end(self):
        if self.player.hp <= 0:
            utils.dead = True
        utils.check_for_player_kill_zone(self)
        for enemy in self.enemies:
            utils.check_kill_zone(self, enemy)

    def reset_parameters(self):
        # display.fill((105, 105, 105))
        display.fill((150, 15, 15))
        collision_table[0] = 0
        collision_table[1] = 0
        for enemy in self.enemies:
            enemy.movement_blockade[0] = 0
            enemy.movement_blockade[1] = 0

        utils.clock.tick(60)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.environment_speed = settings.walking_speed

    def handle_collisions(self):
        for bullet in self.player_bullets:
            if self.check_bullet_to_enemy(bullet):
                self.check_bullet_to_solid(bullet)

        for bullet in self.enemy_bullets:
            if bullet.hit_box.colliderect(self.player.hit_box):
                try:  # if a bullet hits 2 things at once (rare occurance) it will throw ValueError
                    if bullet.damage(self.player):
                        self.enemy_bullets.remove(bullet)
                except ValueError:
                    0
            self.check_enemy_bullet_to_solid(bullet)

        for solid in self.solids:
            utils.check_player_collision(solid, self.player)
            for enemy in self.enemies:
                utils.check_entity_collision(solid, enemy)

    def handle_controls(self):
        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.player.running:
                if event.button == 1:
                    self.player.primary_fire(self.mouse_x, self.mouse_y, self.player_bullets)
                if event.button == 3:
                    self.player.shotgun(self.mouse_x, self.mouse_y, self.player_bullets)

        keys = pygame.key.get_pressed()

        # speed
        if self.player.shooting_penalty != 0:
            self.environment_speed -= settings.shooting_penalty
        if self.player.shotgun_penalty != 0:
            self.environment_speed -= settings.shotgun_shooting_penalty
        if keys[pygame.K_SPACE] and self.player.dash_cooldown == 0:
            self.environment_speed += settings.dash_speed
            self.player.dash(keys)
        if not keys[pygame.K_SPACE]:
            self.player.reset_dash()
        if keys[pygame.K_LSHIFT]:
            self.environment_speed += settings.sprinting_boost
            self.player.running = True
        if not keys[pygame.K_LSHIFT]:
            self.player.running = False

        # movement
        if keys[pygame.K_a]:
            if collision_table[0] >= 0:
                move(self.environment_speed, 0)
        if keys[pygame.K_w]:
            if collision_table[1] <= 0:
                move(0, self.environment_speed)
        if keys[pygame.K_s]:
            if collision_table[1] >= 0:
                move(0, -self.environment_speed)
        if keys[pygame.K_d]:
            if collision_table[0] <= 0:
                move(-self.environment_speed, 0)

        # utilities
        if keys[pygame.K_LCTRL]:
            display.blit(utils.font_health.render("HP: " + str(self.player.hp), True, (255, 255, 255)),
                         (self.player.x, self.player.y + self.player.height / 2))
            for enemy in self.enemies:
                display.blit(utils.font_health.render("HP: " + str(enemy.hp), True, (255, 255, 255)),
                             (enemy.x + display_scroll[0], enemy.y + 7*enemy.height/16 + display_scroll[1]))
        if keys[pygame.K_ESCAPE]:
            utils.paused = True
        if keys[settings.pickup_key]:
            for item in self.items:
                item.use_item(self)

        # developer keys
        if settings.dev_keys:
            if self.spawn_cd != 0:
                self.spawn_cd -= 1
            elif keys[pygame.K_p]:
                self.enemies.append(Slime(random.randint(0 - display_scroll[0], display.get_width() - display_scroll[0]),
                                          random.randint(0 - display_scroll[1], display.get_height() - display_scroll[1])))
                self.enemies.append(Guardian(random.randint(0 - display_scroll[0], display.get_width() - display_scroll[0]),
                                             random.randint(0 - display_scroll[1], display.get_height() - display_scroll[1]),
                                             self.enemies[0]))
                self.spawn_cd = settings.spawn_cd
            if self.hit_box_cd != 0:
                self.hit_box_cd -= 1
            elif keys[pygame.K_h]:
                settings.enable_hit_boxes = not settings.enable_hit_boxes
                self.hit_box_cd = 20

    def render_stuff(self):
        for solid in self.solids:
            solid.render_solid()
        # assets
        for asset in self.assets:
            asset.render_asset()
        self.player.main(self.mouse_x, self.mouse_y)
        for enemy in self.enemies:
            enemy.main()
            enemy.attack(self)
            if enemy.hp <= 0:
                enemy.die(self)
                self.SCORE += 1
        # bullets
        for bullet in self.player_bullets:
            if bullet.TTL != 0:
                bullet.main()
            else:
                self.player_bullets.remove(bullet)
        for bullet in self.enemy_bullets:
            if bullet.TTL != 0:
                bullet.main()
            else:
                self.enemy_bullets.remove(bullet)
        # items
        for item in self.items:
            item.main()

    def render_hud(self):
        pygame.draw.rect(display, (255, 255, 255), (self.mouse_x - 1, self.mouse_y + settings.crosshair_size + 5, 2, 5))
        pygame.draw.rect(display, (255, 255, 255), (self.mouse_x - 1, self.mouse_y - settings.crosshair_size - 10, 2, 5))
        pygame.draw.rect(display, (255, 255, 255), (self.mouse_x + settings.crosshair_size + 4, self.mouse_y - 1, 5, 2))
        pygame.draw.rect(display, (255, 255, 255), (self.mouse_x - settings.crosshair_size - 10, self.mouse_y - 1, 5, 2))
        if settings.crosshair_dot:
            pygame.draw.circle(display, (255, 255, 255), (self.mouse_x, self.mouse_y), 1)
        if self.player.running:
            no_shooting = utils.font.render("X", True, (255, 0, 0))
            display.blit(no_shooting, (self.mouse_x - 11, self.mouse_y - 15))
        if self.player.shotgun_cooldown == 0:
            pygame.draw.rect(display, (0, 0, 255), (self.mouse_x + settings.crosshair_size,
                                                    self.mouse_y + settings.crosshair_size + 5, 3, 4))
            pygame.draw.rect(display, (0, 0, 255), (self.mouse_x + settings.crosshair_size + 4,
                                                    self.mouse_y + settings.crosshair_size + 5, 3, 4))
            pygame.draw.rect(display, (0, 0, 255), (self.mouse_x + settings.crosshair_size + 8,
                                                    self.mouse_y + settings.crosshair_size + 5, 3, 4))

        display.blit(utils.font.render("SCORE: " + str(self.SCORE), True, (0, 0, 255)), (display.get_width() / 2 - 70, 20))
        display.blit(utils.font.render("TIME: " + str(int(self.time/3600)) + "min " + str(int((self.time/60)%60)) + "s", True, (0, 0, 255)),
                     (10, 20))
        display.blit(utils.font_enemies.render("Enemies alive: " + str(len(self.enemies) - 1), True, (255, 255, 255)),
                     (display.get_width() - 190, 10))
        self.player.show_dash_cooldown()

    def initialize_map(self):
        sheet = SpriteSheet('textures\\tiles\\spritesheet.png')
        tilemap = TileMap(tmapPath, sheet)
        return tilemap

    def check_bullet_to_enemy(self, bullet):
        for enemy in self.enemies:
            if bullet.hit_box.colliderect(enemy.hit_box):
                try:
                    if bullet.damage(enemy):
                        self.player_bullets.remove(bullet)
                        return False
                except ValueError:
                    0
        return True

    def check_bullet_to_solid(self, bullet):
        for solid in self.solids:
            if bullet.hit_box.colliderect(solid.hit_box) and not self.enemies.__contains__(solid):
                try:
                    if bullet.damage(solid):
                        self.player_bullets.remove(bullet)
                        break
                except ValueError:
                    0

    def check_enemy_bullet_to_solid(self, bullet):
        for solid in self.solids:
            if bullet.hit_box.colliderect(solid.hit_box) and not self.enemies.__contains__(solid):
                try:
                    if bullet.damage(solid):
                        self.enemy_bullets.remove(bullet)
                        break
                except ValueError:
                    0
