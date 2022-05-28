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

    def main(self):
        self.manage_display()
        self.update_mouse()
        self.handle_clicks()

    def initialize_buttons(self):
        self.buttons.append(Button(self, 300, 500, 200, 40, "Start", self.start_game))
        self.buttons.append(Button(self, 300, 550, 200, 40, "Settings", self.open_settings))
        self.buttons.append(Button(self, 300, 600, 200, 40, "Quit", self.quit))

    def update_mouse(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()

    def start_game(self):
        self.game = Game()
        utils.game_running = True

    def open_settings(self):
        self.buttons = self.buttons

    def quit(self):
        utils.game_running = False
        utils.running = False
        sys.exit()

    def manage_display(self):
        display.fill((39, 142, 183))
        for button in self.buttons:
            button.render()
        pygame.display.update()

    def handle_clicks(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for button in self.buttons:
                        button.do_sth()
                        break


class Button:
    base = pygame.image.load("textures\\Button_base.xcf")
    click = pygame.image.load("textures\\Button_click.xcf")

    def __init__(self, menu, x, y, width, height, name, function):
        self.menu = menu
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = utils.font_enemies.render(name, True, (0, 0, 0))
        self.function = function
        self.hit_box = pygame.Rect(x - width/2, y - width/2, width, height)
        self.clicked = False
        self.texture = Button.base

    def render(self):
        self.choose_texture()
        pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        display.blit(self.texture, (self.x - self.width/2, self.y - self.height * 2.5))
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
