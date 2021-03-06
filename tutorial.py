import pygame
import sys
import random

import settings
import utils
from utils import display, display_scroll, move, collision_table, tutorial_tmap_path
from slime import Slime
from guardian import Guardian
from player import Player
from dummy import Dummy
from map import TileMap, SpriteSheet
from item import Item
from game import Game

dummy_text = pygame.image.load("textures\\Dummy_dialogue.xcf")


class Tutorial:
    def __init__(self):
        utils.set_game_parameters()
        utils.paused = False
        utils.win = False
        utils.dead = False
        utils.message_break = False

        self.message = MessageBreak(Message("XD", 0), self)
        # stage controls what a player can do during a tutorial
        self.stage = 0
        # 0 - no control
        # 1 - AWSD movement
        # 2 - shooting1 (primary fire)
        # 3 - shooting2 (secondary fire)
        # 4 - sprinting
        # 5 - dashing
        # 6 - fight

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

        self.tmap = self.initialize_map()

        self.cutscene = False
        self.next_dialogue_in = 0
        self.current_dialogue = 0
        self.dialogue_items = []
        self.initialize_items()

        def initial_condition(table):
            return True
        self.dialogue_condition = initial_condition
        self.condition_table = [0, 0, 0, 0]

        self.condition_update = initial_condition

    def main(self):

        self.time += 1
        if self.next_dialogue_in > 0:
            self.next_dialogue_in -= 1
        else:
            self.spawn_dialogue_item()

        self.check_for_end()
        Game.reset_parameters(self)
        Game.handle_collisions(self)
        self.tmap.draw_map()
        Game.render_stuff(self)
        self.handle_controls()
        self.render_hud()

        if self.cutscene:
            self.stage = 0
            self.message.main()
        else:
            self.condition_update(self.condition_table)

        pygame.display.update()
        # print("x: " + str(display_scroll[0]) + ", y: " + str(display_scroll[1]))  # to get coordinates for placement

    def initialize_items(self):
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width/2, self.dummy.y - self.dummy.height/6,
                                   Tutorial.intro, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.movement, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.shooting1, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.shooting2, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.sprinting, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.dashing, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.fight, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.go_explore, Item.item_textures[5]))
        self.dialogue_items.append(Item(self.dummy.x - self.dummy.width / 2, self.dummy.y - self.dummy.height / 6,
                                        Tutorial.end, Item.item_textures[5]))

    def spawn_dialogue_item(self):
        if self.dialogue_condition(self.condition_table) and len(self.items) < 1:
            self.items.append(self.dialogue_items[self.current_dialogue])

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

    def handle_controls(self):
        # controls
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not self.player.running:
                if self.cutscene:
                    if event.button == 1:
                        self.cutscene = False
                        self.stage = self.message.mess.return_stage
                elif self.stage >= 2:
                    if event.button == 1:
                        self.player.primary_fire(self.mouse_x, self.mouse_y, self.player_bullets)
                        if self.stage == 2:
                            self.condition_table[0] += 1
                    if self.stage >= 3 and event.button == 3:
                        if self.stage == 3 and self.player.shotgun_cooldown == 0:
                            self.condition_table[0] += 1
                        self.player.shotgun(self.mouse_x, self.mouse_y, self.player_bullets)

        keys = pygame.key.get_pressed()

        # speed
        if self.player.shooting_penalty != 0:
            self.environment_speed -= settings.shooting_penalty
        if self.player.shotgun_penalty != 0:
            self.environment_speed -= settings.shotgun_shooting_penalty
        if self.stage >= 5 and keys[settings.dash_button] and self.player.dash_cooldown == 0:
            self.environment_speed += settings.dash_speed
            self.player.dash(keys)
            if self.stage == 5:
                self.condition_table[0] += 1
        if not keys[settings.dash_button]:
            self.player.reset_dash()
        if self.stage >= 4 and keys[settings.sprinting_button]:
            self.environment_speed += settings.sprinting_boost
            self.player.running = True
        if not keys[settings.sprinting_button]:
            self.player.running = False

        # movement
        if self.stage >= 1 and keys[pygame.K_a]:
            if collision_table[0] >= 0:
                move(self.environment_speed, 0)
        if self.stage >= 1 and keys[pygame.K_w]:
            if collision_table[1] <= 0:
                move(0, self.environment_speed)
        if self.stage >= 1 and keys[pygame.K_s]:
            if collision_table[1] >= 0:
                move(0, -self.environment_speed)
        if self.stage >= 1 and keys[pygame.K_d]:
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
            if self.hit_box_cd != 0:
                self.hit_box_cd -= 1
            elif keys[pygame.K_h]:
                settings.enable_hit_boxes = not settings.enable_hit_boxes
                self.hit_box_cd = 20

    def render_hud(self):
        if self.stage >= 1:
            pygame.draw.rect(display, (255, 255, 255), (self.mouse_x - 1, self.mouse_y + settings.crosshair_size + 5, 2, 5))
            pygame.draw.rect(display, (255, 255, 255), (self.mouse_x - 1, self.mouse_y - settings.crosshair_size - 10, 2, 5))
            pygame.draw.rect(display, (255, 255, 255), (self.mouse_x + settings.crosshair_size + 4, self.mouse_y - 1, 5, 2))
            pygame.draw.rect(display, (255, 255, 255), (self.mouse_x - settings.crosshair_size - 10, self.mouse_y - 1, 5, 2))
            if settings.crosshair_dot:
                pygame.draw.circle(display, (255, 255, 255), (self.mouse_x, self.mouse_y), 1)
            if self.player.running:
                no_shooting = utils.font.render("X", True, (255, 0, 0))
                display.blit(no_shooting, (self.mouse_x - 11, self.mouse_y - 15))
            if self.player.shotgun_cooldown == 0 and self.stage >= 3:
                pygame.draw.rect(display, (0, 0, 255), (self.mouse_x + settings.crosshair_size,
                                                        self.mouse_y + settings.crosshair_size + 5, 3, 4))
                pygame.draw.rect(display, (0, 0, 255), (self.mouse_x + settings.crosshair_size + 4,
                                                        self.mouse_y + settings.crosshair_size + 5, 3, 4))
                pygame.draw.rect(display, (0, 0, 255), (self.mouse_x + settings.crosshair_size + 8,
                                                        self.mouse_y + settings.crosshair_size + 5, 3, 4))
        if self.stage >= 6:
            display.blit(utils.font.render("Kills: " + str(self.SCORE), True, (0, 0, 255)),
                         (display.get_width() / 2 - 70, 20))
            display.blit(
                utils.font_enemies.render("Enemies alive: " + str(len(self.enemies) - 1), True, (255, 255, 255)),
                (display.get_width() - 190, 10))
        display.blit(utils.font.render("TIME: " + str(int(self.time/3600)) + "min " + str(int((self.time/60)%60)) + "s", True, (0, 0, 255)),
                     (10, 20))
        if self.stage >= 4:
            self.player.show_dash_cooldown()

    def initialize_map(self):
        sheet = SpriteSheet('textures\\tiles\\spritesheet.png')
        tilemap = TileMap(tutorial_tmap_path, sheet)
        return tilemap

    @staticmethod
    def intro(tutorial):
        tutorial.cutscene = True
        tutorial.player.hp = 10
        tutorial.condition_table = [0, 0, 0, 0]
        tutorial.message.set_message(Message([" ",
                                              " ",
                                              "Hello there! You look exhausted!",
                                              "Better check your HP by pressing [Left_ctrl]"], 0))
        def new_cond(table):
            return table[0] >= 60

        tutorial.dialogue_condition = new_cond

        def new_update(table):
            if table[0] < 60:
                mess = utils.font_enemies.render(f"HP viewed for: {table[0]}/60", True, (255, 255, 255))
            else:
                mess = utils.font_enemies.render(f"HP viewed for: {table[0]}/60", True, (30, 255, 30))
            pygame.draw.rect(display, (50, 50, 50), pygame.Rect(0, 660, 1200, 40))
            display.blit(mess, (500, 670))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                table[0] += 1

        tutorial.condition_update = new_update

        tutorial.next_dialogue_in = 60
        tutorial.current_dialogue += 1

    @staticmethod
    def movement(tutorial):
        tutorial.cutscene = True
        tutorial.condition_table = [0, 0, 0, 0]
        tutorial.message.set_message(Message(["You don't look so well, let's get moving, use:",
                                              "A  - to move left",
                                              "W - to move up",
                                              "S - to move down",
                                              "D - to move right"], 1))
        def new_cond(table):
            for x in table:
                if x < 60:
                    return False
            return True

        tutorial.dialogue_condition = new_cond

        def new_update(table):
            if table[0] < 60:
                A = utils.font_enemies.render(f"Left: {table[0]}/60", True, (255, 255, 255))
            else:
                A = utils.font_enemies.render(f"Left: {table[0]}/60", True, (30, 255, 30))
            if table[1] < 60:
                W = utils.font_enemies.render(f"Top: {table[1]}/60", True, (255, 255, 255))
            else:
                W = utils.font_enemies.render(f"Top: {table[1]}/60", True, (30, 255, 30))
            if table[2] < 60:
                S = utils.font_enemies.render(f"Down: {table[2]}/60", True, (255, 255, 255))
            else:
                S = utils.font_enemies.render(f"Down: {table[2]}/60", True, (30, 255, 30))
            if table[3] < 60:
                D = utils.font_enemies.render(f"Right: {table[3]}/60", True, (255, 255, 255))
            else:
                D = utils.font_enemies.render(f"Right: {table[3]}/60", True, (30, 255, 30))
            pygame.draw.rect(display, (50, 50, 50), pygame.Rect(0, 660, 1200, 40))
            display.blit(A, (250, 670))
            display.blit(W, (450, 670))
            display.blit(S, (650, 670))
            display.blit(D, (850, 670))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                table[0] += 1
            if keys[pygame.K_w]:
                table[1] += 1
            if keys[pygame.K_s]:
                table[2] += 1
            if keys[pygame.K_d]:
                table[3] += 1

        tutorial.condition_update = new_update
        tutorial.next_dialogue_in = 120
        tutorial.current_dialogue += 1

    @staticmethod
    def shooting1(tutorial):
        tutorial.cutscene = True
        tutorial.condition_table = [0, 0, 0, 0]
        tutorial.message.set_message(Message([" ",
                                              "Now, let's learn how to shoot! Press:",
                                              " ",
                                              "LMB - primary fire, single bullet"], 2))
        def new_cond(table):
            return table[0] >= 20

        tutorial.dialogue_condition = new_cond

        def new_update(table):
            if table[0] < 20:
                mess = utils.font_enemies.render(f"Shots fired: {table[0]}/20", True, (255, 255, 255))
            else:
                mess = utils.font_enemies.render(f"Shots fired: {table[0]}/20", True, (30, 255, 30))
            pygame.draw.rect(display, (50, 50, 50), pygame.Rect(0, 660, 1200, 40))
            display.blit(mess, (500, 670))

        tutorial.condition_update = new_update


        tutorial.next_dialogue_in = 120
        tutorial.current_dialogue += 1

    @staticmethod
    def shooting2(tutorial):
        tutorial.cutscene = True
        tutorial.condition_table = [0, 0, 0, 0]
        tutorial.message.set_message(Message(["If you need more firepower you can use:",
                                              "RMB - secondary fire, multiple bullets on a short cooldown",
                                              "Note, that there is an indicator on your crosshair that "
                                              "tells you when you can shoot secondary fire again"], 3))
        def new_cond(table):
            return table[0] >= 5

        tutorial.dialogue_condition = new_cond

        def new_update(table):
            if table[0] < 5:
                mess = utils.font_enemies.render(f"Secondary shots fired: {table[0]}/5", True, (255, 255, 255))
            else:
                mess = utils.font_enemies.render(f"Secondary shots fired: {table[0]}/5", True, (30, 255, 30))
            pygame.draw.rect(display, (50, 50, 50), pygame.Rect(0, 660, 1200, 40))
            display.blit(mess, (450, 670))

        tutorial.condition_update = new_update
        tutorial.next_dialogue_in = 120
        tutorial.current_dialogue += 1

    @staticmethod
    def sprinting(tutorial):
        tutorial.cutscene = True
        tutorial.message.set_message(Message(["You might have noticed, that you move pretty slow",
                                              "Especially when shooting... but there is a solution, just press ",
                                              f"[{str.upper(pygame.key.name(settings.sprinting_button))}] "
                                              "to sprint and move faster",
                                              "Note, that you cannot shoot while sprinting"], 4))

        tutorial.condition_table = [0, 0, 0, 0]
        def new_cond(table):
            return table[0] >= 120

        tutorial.dialogue_condition = new_cond

        def new_update(table):
            if table[0] < 120:
                mess = utils.font_enemies.render(f"Sprinted for: {table[0]}/120", True, (255, 255, 255))
            else:
                mess = utils.font_enemies.render(f"Sprinted for: {table[0]}/120", True, (30, 255, 30))
            pygame.draw.rect(display, (50, 50, 50), pygame.Rect(0, 660, 1200, 40))
            display.blit(mess, (450, 670))
            keys = pygame.key.get_pressed()
            if keys[settings.sprinting_button]:
                table[0] += 1

        tutorial.condition_update = new_update

        tutorial.next_dialogue_in = 120
        tutorial.current_dialogue += 1

    @staticmethod
    def dashing(tutorial):
        tutorial.cutscene = True
        tutorial.message.set_message(Message([" ",
                                              "I think we all know, you won't stop there...",
                                              f"Use [{str.upper(pygame.key.name(settings.dash_button))}] to dash!",
                                              "It makes you super fast and invincible for a short period"], 5))
        tutorial.condition_table = [0, 0, 0, 0]
        def new_cond(table):
            return table[0] >= 50

        tutorial.dialogue_condition = new_cond

        def new_update(table):
            if table[0] < 50:
                mess = utils.font_enemies.render(f"Dashes: {table[0]//10}/5", True, (255, 255, 255))
            else:
                mess = utils.font_enemies.render(f"Dashes: {table[0]//10}/5", True, (30, 255, 30))
            pygame.draw.rect(display, (50, 50, 50), pygame.Rect(1000, 660, 200, 40))
            display.blit(mess, (1050, 670))

        tutorial.condition_update = new_update

        tutorial.next_dialogue_in = 120
        tutorial.current_dialogue += 1

    @staticmethod
    def fight(tutorial):
        tutorial.cutscene = True
        tutorial.condition_table = [0, 0, 0, 0]
        tutorial.message.set_message(Message(["",
                                              "Now, let's put your skills to a test and kill that Slime!",
                                              "",
                                              "Don't talk to me unless it's gone!"], 6))

        def new_cond(table):
            return table[0] == 1

        tutorial.dialogue_condition = new_cond

        tutorial.condition_update = tutorial.fight_update
        tutorial.next_dialogue_in = 120
        tutorial.current_dialogue += 1

    def fight_update(self, table):
        if not self.cutscene and len(self.enemies) < 2 and self.SCORE != 1:
            self.enemies.append(Slime(self.player.x + 300 + display_scroll[0],
                                      self.player.y + 10 + display_scroll[1]))
        if self.SCORE == 1:
            table[0] = 1

    @staticmethod
    def go_explore(tutorial):
        tutorial.cutscene = True
        tutorial.condition_table = [0, 0, 0, 0]
        tutorial.message.set_message(Message(["Well done! In a normal fight there's going to be way more of them though!",
                                              "You gotta know your surroundings...",
                                              "Go explore a little and talk to me when you're done",
                                              "and we're gonna get you out of this boring tutorial!",
                                              ""], 6))

        def new_cond(table):
            sum = 0
            for x in table:
                sum += x
            return sum >= 600

        tutorial.dialogue_condition = new_cond

        def new_update(table):
            tmp = table[0] + table[1] + table[2] + table[3]
            if tmp < 600:
                mess = utils.font_enemies.render(f"Time walking: {tmp}/600", True, (255, 255, 255))
            else:
                mess = utils.font_enemies.render(f"Time walking: {tmp}/600", True, (30, 255, 30))
            pygame.draw.rect(display, (50, 50, 50), pygame.Rect(900, 660, 300, 40))
            display.blit(mess, (950, 670))
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:    # this time we return so count time spent walking
                table[0] += 1
                return True
            if keys[pygame.K_w]:
                table[1] += 1
                return True
            if keys[pygame.K_s]:
                table[2] += 1
                return True
            if keys[pygame.K_d]:
                table[3] += 1
                return True
            return True

        tutorial.condition_update = new_update
        tutorial.next_dialogue_in = 120
        tutorial.current_dialogue += 1

    @staticmethod
    def end(tutorial):
        utils.win = True

class MessageBreak:
    def __init__(self, message, tutorial):
        self.mess = message
        self.tutorial = tutorial

    def main(self):
        self.mess.main()
        self.handle_clicks()
        pygame.display.update()

    def set_message(self, mess):
        self.mess = mess

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.tutorial.cutscene = False
                    print("Hello world")
                    self.tutorial.stage = self.mess.return_stage


class Message:

    # continue_mess = utils.font_items.render(f"Press [{pygame.key.name(settings.pickup_key)}] to continue", True, (255, 255, 255))
    continue_mess = utils.font_dialogue.render(f"Press [LMB] to continue", True, (255, 255, 255))

    def __init__(self, text, return_stage):
        self.mess = []
        for text in text:
            self.mess.append(utils.font_dialogue.render(text, True, (255, 255, 255)))
        self.return_stage = return_stage

    def main(self):
        pygame.draw.rect(display, (50, 50, 50), pygame.Rect(0, 580, 1200, 120))
        display.blit(dummy_text, (30, 500))
        for i in range(0, len(self.mess)):
            display.blit(self.mess[i], (display.get_width()/2 - self.mess[i].get_width()/2, 590 + i*21))
        display.blit(Message.continue_mess, (1000, 675))
