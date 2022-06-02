import pygame
import sys

import utils
import settings
from utils import display
from game import Game

menuu = pygame.image.load("textures\\menuu.0001.jpg")


class Menu:
    def __init__(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.buttons = []
        self.initialize_buttons()
        self.game = Game()
        self.death_screen = Death_screen(self.game)
        self.paused = Pause()
        self.win = Win_screen(self.game)
        self.settings = Settings()

    def main(self):
        self.manage_display()
        self.update_mouse()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 600, 400, 400, 80, "Play", self.play))
        self.buttons.append(Button(self, 600, 500, 400, 80, "Settings", self.open_settings))
        self.buttons.append(Button(self, 600, 600, 400, 80, "Quit", self.quit))

    def update_mouse(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def play(self):
        utils.choose_game_mode = True

    @staticmethod
    def open_settings():
        utils.open_settings = True

    @staticmethod
    def quit():
        utils.game_running = False
        utils.running = False
        pygame.quit()
        sys.exit()

    def manage_display(self):
        display.fill((39, 142, 183))
        display.blit(menuu, (0, 0))
        for button in self.buttons:
            button.render()
        title1 = utils.title_font.render("Dummy", True, (0, 0, 0))
        title2 = utils.title_font.render("Quest", True, (0, 0, 0))
        display.blit(title1, (365, 50))
        display.blit(title2, (400, 180))
        pygame.display.update()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


class Button:
    base = pygame.image.load("textures\\Button_base.xcf")
    click = pygame.image.load("textures\\Button_click.xcf")

    def __init__(self, menu, x, y, width, height, name, function):
        self.menu = menu
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = name
        self.name = utils.font_buttons.render(name, True, (0, 0, 0))
        self.function = function
        self.hit_box = pygame.Rect(x - width/2, y - height/2, width, height)
        self.clicked = False
        self.texture = Button.base

    def render(self):
        self.choose_texture()
        pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        texture_copy = pygame.transform.scale(self.texture, (self.width, self.height))
        display.blit(texture_copy, (self.x - self.width/2, self.y - self.height/2))
        display.blit(self.name,
                     (self.x - self.name.get_width()/2, self.y - self.name.get_height()/2))

    def choose_texture(self):
        if self.hit_box.x < self.menu.mouse_x < self.hit_box.x + self.hit_box.width and\
           self.hit_box.y < self.menu.mouse_y < self.hit_box.y + self.hit_box.height:
            self.texture = Button.click
            self.clicked = True
        else:
            self.texture = Button.base
            self.clicked = False

    def do_sth(self):
        if self.clicked:
            self.function()


class Death_screen:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.initialize_buttons()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def main(self):
        pygame.mouse.set_visible(True)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.manage_display()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 600, 500, 400, 80, "Menu", self.go_back))
        self.buttons.append(Button(self, 600, 600, 400, 80, "Quit", Menu.quit))

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def manage_display(self):
        message = utils.font_death.render("You're dead!", True, (150, 15, 15))
        display.blit(message, (350, 100))
        for button in self.buttons:
            button.render()
        pygame.display.update()

    def go_back(self):
        utils.game_running = False
        utils.dead = False

class Pause:
    def __init__(self):
        self.buttons = []
        self.initialize_buttons()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def main(self):
        pygame.mouse.set_visible(True)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.manage_display()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 600, 500, 400, 80, "Resume", self.resume))
        self.buttons.append(Button(self, 600, 600, 400, 80, "Menu", self.menu))

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def manage_display(self):
        message = utils.font_death.render("Paused", True, (0, 60, 60))
        display.blit(message, (450, 100))
        for button in self.buttons:
            button.render()
        pygame.display.update()

    @staticmethod
    def menu():
        utils.game_running = False
        utils.paused = False

    @staticmethod
    def resume():
        pygame.mouse.set_visible(False)
        utils.paused = False

class Win_screen:
    def __init__(self, game):
        self.game = game
        self.buttons = []
        self.initialize_buttons()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def main(self):
        pygame.mouse.set_visible(True)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.manage_display()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 600, 500, 400, 80, "Menu", self.go_back))
        self.buttons.append(Button(self, 600, 600, 400, 80, "Quit", Menu.quit))

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                sys.exit()

    def manage_display(self):
        message = utils.font_death.render("You've won!", True, (138, 238, 255))
        display.blit(message, (330, 100))
        for button in self.buttons:
            button.render()
        pygame.display.update()

    @staticmethod
    def go_back():
        utils.game_running = False
        utils.win = False


class Settings:
    def __init__(self):
        self.buttons = []
        self.initialize_buttons()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def main(self):
        pygame.mouse.set_visible(True)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.manage_display()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 600, 300, 400, 80, "Difficulty level", Settings.toggle_difficulty))
        self.buttons.append(Button(self, 600, 400, 400, 80, "Crosshair dot", Settings.toggle_crosshair))
        self.buttons.append(Button(self, 600, 600, 400, 80, "<-- Back", Settings.go_back))

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                sys.exit()

    def manage_display(self):
        display.fill((39, 142, 183))
        message = utils.font_death.render("Settings", True, (156, 183, 50))
        display.blit(message, (430, 100))
        for button in self.buttons:
            button.render()
        Settings.manage_settings()
        pygame.display.update()

    @staticmethod
    def go_back():
        utils.open_settings = False
        utils.set_difficulty()

    @staticmethod
    def toggle_crosshair():
        settings.crosshair_dot = not settings.crosshair_dot

    @staticmethod
    def toggle_difficulty():
        settings.difficulty_level += 1
        if settings.difficulty_level > 2:
            settings.difficulty_level = -1
        utils.set_difficulty()

    @staticmethod
    def manage_settings():
        if settings.crosshair_dot:
            display.blit(utils.font_buttons.render("ON", True, (0, 255, 0)), (820, 380))
        else:
            display.blit(utils.font_buttons.render("OFF", True, (255, 0, 0)), (820, 380))

        if settings.difficulty_level == -1:
            display.blit(utils.font_buttons.render("BABY", True, (0, 255, 0)), (820, 280))
        elif settings.difficulty_level == 0:
            display.blit(utils.font_buttons.render("EASY", True, (200, 255, 28)), (820, 280))
        elif settings.difficulty_level == 1:
            display.blit(utils.font_buttons.render("NORMAL", True, (249, 200, 30)), (820, 280))
        else:
            display.blit(utils.font_buttons.render("HARD", True, (255, 0, 0)), (820, 280))


class Choice:
    def __init__(self, menu):
        self.menu = menu
        self.buttons = []
        self.initialize_buttons()
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def main(self):
        pygame.mouse.set_visible(True)
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.manage_display()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 600, 300, 400, 80, "Normal", self.normal))
        self.buttons.append(Button(self, 300, 450, 400, 80, "Tutorial (W.I.P.)", self.tutorial))
        self.buttons.append(Button(self, 900, 450, 400, 80, "Pizza hunt (W.I.P.)", self.pizza))
        self.buttons.append(Button(self, 600, 600, 400, 80, "<-- Back", self.go_back))

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()

            if event.type == pygame.QUIT:
                sys.exit()

    def manage_display(self):
        display.fill((39, 142, 183))
        message = utils.font_death.render("Choose game mode", True, (138, 238, 255))
        display.blit(message, (180, 100))
        for button in self.buttons:
            button.render()
        pygame.display.update()

    def normal(self):
        pygame.mouse.set_visible(False)
        self.menu.game = Game()
        utils.game_running = True
        utils.choose_game_mode = False

    def tutorial(self):
        utils.choose_game_mode = False

    def pizza(self):
        utils.choose_game_mode = False

    @staticmethod
    def go_back():
        utils.choose_game_mode = False
