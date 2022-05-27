import pygame

import utils
from game import Game

if __name__ == '__main__':
    pygame.init()
    game = Game()
    utils.game_running = True
    while utils.game_running:
        game.main()
