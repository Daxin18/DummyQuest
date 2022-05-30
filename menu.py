import pygame
import sys

import utils
from utils import display
from game import Game


class Menu:
    def __init__(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        self.buttons = []
        self.initialize_buttons()
        self.game = Game()
        self.death_screen = Death_screen(self.game)
        self.paused = Pause()
        self.win = Win_screen(self.game)

    def main(self):
        self.manage_display()
        self.update_mouse()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 600, 500, 400, 80, "Start", self.start_game))
        self.buttons.append(Button(self, 600, 600, 400, 80, "Settings", self.open_settings))
        self.buttons.append(Button(self, 600, 700, 400, 80, "Quit", self.quit))

    def update_mouse(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def start_game(self):
        pygame.mouse.set_visible(False)
        self.game = Game()
        utils.game_running = True

    def open_settings(self):
        True

    @staticmethod
    def quit():
        utils.game_running = False
        utils.running = False
        pygame.quit()
        sys.exit()

    def manage_display(self):
        display.fill((39, 142, 183))
        for button in self.buttons:
            button.render()
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
        self.hit_box = pygame.Rect(x - width/2, y - width/2, width, height)
        self.clicked = False
        self.texture = Button.base

    def render(self):
        self.choose_texture()
        pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        texture_copy = pygame.transform.scale(self.texture, (self.width, self.height))
        display.blit(texture_copy, (self.x - self.width/2, self.y - self.height * 2.5))
        display.blit(self.name,
                     (self.x - self.name.get_width()/2, self.y - self.height * 2.25))

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
        self.buttons.append(Button(self, 600, 600, 400, 80, "Menu", self.go_back))
        self.buttons.append(Button(self, 600, 700, 400, 80, "Quit", Menu.quit))

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
        self.buttons.append(Button(self, 600, 600, 400, 80, "Resume", self.resume))
        self.buttons.append(Button(self, 600, 700, 400, 80, "Menu", self.menu))

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

    def menu(self):
        utils.game_running = False
        utils.paused = False

    def resume(self):
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
        self.buttons.append(Button(self, 600, 600, 400, 80, "Menu", self.go_back))
        self.buttons.append(Button(self, 600, 700, 400, 80, "Quit", Menu.quit))

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
        message = utils.font_death.render("You won!", True, (138, 238, 255))
        display.blit(message, (400, 100))
        for button in self.buttons:
            button.render()
        pygame.display.update()

    def go_back(self):
        utils.game_running = False
        utils.win = False
