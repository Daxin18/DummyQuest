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


class Game:
    def __init__(self):
        utils.set_game_parameters()

        self.player_bullets = []
        self.enemies = []
        self.enemy_bullets = []
        self.solids = []  # aka things you can collide with
        self.assets = []
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
            pygame.mouse.set_visible(True)
            utils.game_running = False

    def reset_parameters(self):
        display.fill((105, 105, 105))
        collision_table[0] = 0
        collision_table[1] = 0

        utils.clock.tick(60)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.environment_speed = settings.walking_speed

    def handle_collisions(self):
        for bullet in self.player_bullets:
            for entity in [*self.enemies, *self.solids]:
                if bullet.hit_box.colliderect(entity.hit_box):
                    try:  # if a bullet hits 2 things at once (rare occurance) it will throw ValueError
                        if bullet.damage(entity):
                            self.player_bullets.remove(bullet)
                    except ValueError:
                        0

        for bullet in self.enemy_bullets:
            for entity in [self.player, *self.solids]:
                if bullet.hit_box.colliderect(entity.hit_box):
                    try:  # if a bullet hits 2 things at once (rare occurance) it will throw ValueError
                        if bullet.damage(entity):
                            self.enemy_bullets.remove(bullet)
                    except ValueError:
                        0

        for solid in self.solids:
            utils.check_player_collision(solid, self.player)

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
        if keys[pygame.K_LCTRL]:
            display.blit(utils.font_health.render("HP: " + str(self.player.hp), True, (255, 255, 255)),
                         (self.player.x, self.player.y + self.player.height / 2))
            for enemy in self.enemies:
                display.blit(utils.font_health.render("HP: " + str(enemy.hp), True, (255, 255, 255)),
                             (enemy.x + display_scroll[0], enemy.y + enemy.size + display_scroll[1]))

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
            enemy.attack(self.enemy_bullets)
            if enemy.hp <= 0:
                self.enemies.remove(enemy)
                enemy.die(self.enemy_bullets)
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
        display.blit(utils.font_enemies.render("Enemies alive: " + str(len(self.enemies) - 1), True, (255, 255, 255)),
                     (display.get_width() - 190, 10))
        self.player.show_dash_cooldown()

    def initialize_map(self):
        sheet = SpriteSheet('textures\\tiles\\spritesheet.png')
        tilemap = TileMap(tmapPath, sheet)
        return tilemap

