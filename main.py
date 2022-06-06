import pygame

import utils
import menu

if __name__ == '__main__':
    pygame.init()
    main_menu = menu.Menu()
    settings_screen = menu.Settings()
    pause_overlay = menu.Pause()
    choice_screen = menu.Choice(main_menu)
    while utils.running:
        main_menu.main()
        while utils.choose_game_mode:
            choice_screen.main()
        while utils.game_running:
            main_menu.game.main()
            while utils.dead:
                main_menu.death_screen.main()
            while utils.paused:
                pause_overlay.main()
            while utils.win:
                main_menu.win.main()
        while utils.open_settings:
            settings_screen.main()
        while utils.tutorial_running:
            main_menu.tutorial.main()
            while utils.dead:
                main_menu.death_screen.main()
            while utils.paused:
                pause_overlay.main()
            while utils.win:
                main_menu.win.main()

