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
                menu.death_screen.main()
            while utils.paused:
                menu.paused.main()
            while utils.win:
                menu.win.main()
        while utils.open_settings:
            menu.settings.main()