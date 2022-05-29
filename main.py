import pygame

import utils
from menu import Menu

if __name__ == '__main__':
    pygame.init()
    menu = Menu()
    while utils.running:
        menu.main()
        while utils.game_running:
            menu.game.main()
            while utils.dead:
                print("true")
