import pygame
import sys
import random

import settings
import utils
from utils import display, display_scroll, move, collision_table, game_tmap_path
from slime import Slime
from guardian import Guardian
from player import Player
from dummy import Dummy
from rock import Rock
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
        Game.reset_parameters(self)
        Game.handle_collisions(self)
        self.tmap.draw_map()
        Game.render_stuff(self)
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
        if utils.gamemode != 1:
            for coordinates in settings.curse_coordinates:
                self.items.append(Item(coordinates[0], coordinates[1], Item.cursed_boost, Item.item_textures[4]))
        for coordinates in settings.base_boost_coordinates:
            self.items.append(Item(coordinates[0], coordinates[1], Item.base_damage_boost, Item.item_textures[1]))
        for coordinates in settings.shotgun_boost_coordinates:
            self.items.append(Item(coordinates[0], coordinates[1], Item.shotgun_damage_boost, Item.item_textures[2]))

    def generate_random_terrain(self):
        for i in range(settings.rock_number):
            r_x = random.randint(self.player.x - 2700, self.player.x + 2700)
            r_y = random.randint(self.player.y - 2700, self.player.y + 2700)
            while 451 < r_x < 750 and 150 < r_y < 449:
                r_x = random.randint(self.player.x - 2700, self.player.x + 2700)
                r_y = random.randint(self.player.y - 2700, self.player.y + 2700)
            r_w = random.randint(45, 70)
            r_h = random.randint(45, 70)
            self.solids.append(Rock(r_x, r_y, r_w, r_h))

    def check_for_end(self):
        if self.player.hp <= 0:
            utils.dead = True
        utils.check_for_player_kill_zone(self)
        for enemy in self.enemies:
            utils.check_kill_zone(self, enemy)

        if utils.gamemode == 1 and self.player.hp >= settings.player_health_cap:
                utils.win = True
                utils.game_running = False
                print("WTF")

    @staticmethod
    def reset_parameters(game_class):
        display.fill((187, 63, 63))
        collision_table[0] = 0
        collision_table[1] = 0
        for enemy in game_class.enemies:
            enemy.movement_blockade[0] = 0
            enemy.movement_blockade[1] = 0

        utils.clock.tick(60)
        game_class.mouse_x, game_class.mouse_y = pygame.mouse.get_pos()
        game_class.environment_speed = settings.walking_speed

    @staticmethod
    def handle_collisions(game_class):
        for bullet in game_class.player_bullets:
            if Game.check_bullet_to_enemy(game_class, bullet):
                Game.check_bullet_to_solid(game_class, bullet)

        for bullet in game_class.enemy_bullets:
            if bullet.hit_box.colliderect(game_class.player.hit_box):
                try:  # if a bullet hits 2 things at once (rare occurance) it will throw ValueError
                    if bullet.damage(game_class.player):
                        game_class.enemy_bullets.remove(bullet)
                except ValueError:
                    pass
            Game.check_enemy_bullet_to_solid(game_class, bullet)

        for solid in game_class.solids:
            utils.check_player_collision(solid, game_class.player)
            for enemy in game_class.enemies:
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

    @staticmethod
    def render_stuff(game_class):
        for solid in game_class.solids:
            solid.render_solid()
        game_class.player.main(game_class.mouse_x, game_class.mouse_y)
        for enemy in game_class.enemies:
            enemy.main()
            enemy.attack(game_class)
            if enemy.hp <= 0:
                enemy.die(game_class)
                game_class.SCORE += 1
        # bullets
        for bullet in game_class.player_bullets:
            if bullet.TTL != 0:
                bullet.main()
            else:
                game_class.player_bullets.remove(bullet)
        for bullet in game_class.enemy_bullets:
            if bullet.TTL != 0:
                bullet.main()
            else:
                game_class.enemy_bullets.remove(bullet)
        # items
        for item in game_class.items:
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

        display.blit(utils.font.render("KILLS: " + str(self.SCORE), True, (0, 0, 255)), (display.get_width() / 2 - 70, 20))
        display.blit(utils.font.render("TIME: " + str(int(self.time/3600)) + "min " + str(int((self.time/60)%60)) + "s", True, (0, 0, 255)),
                     (10, 20))
        display.blit(utils.font_enemies.render("Enemies alive: " + str(len(self.enemies) - 1), True, (255, 255, 255)),
                     (display.get_width() - 190, 10))
        self.player.show_dash_cooldown()

    def initialize_map(self):
        sheet = SpriteSheet('textures\\tiles\\spritesheet.png')
        tilemap = TileMap(game_tmap_path, sheet)
        return tilemap

    @staticmethod
    def check_bullet_to_enemy(game, bullet):
        for enemy in game.enemies:
            if bullet.hit_box.colliderect(enemy.hit_box):
                try:
                    if bullet.damage(enemy):
                        game.player_bullets.remove(bullet)
                        return False
                except ValueError:
                    pass
        return True

    @staticmethod
    def check_bullet_to_solid(game, bullet):
        for solid in game.solids:
            if bullet.hit_box.colliderect(solid.hit_box) and not game.enemies.__contains__(solid):
                try:
                    if bullet.damage(solid):
                        game.player_bullets.remove(bullet)
                        break
                except ValueError:
                    pass

    @staticmethod
    def check_enemy_bullet_to_solid(game, bullet):
        for solid in game.solids:
            if bullet.hit_box.colliderect(solid.hit_box) and not game.enemies.__contains__(solid):
                try:
                    if bullet.damage(solid):
                        game.enemy_bullets.remove(bullet)
                        break
                except ValueError:
                    pass
