import pygame

from utils import display, display_scroll


class Tree:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

    def render_asset(self):
        pygame.draw.circle(display, (40, 200, 40), (self.x + display_scroll[0], self.y + display_scroll[1]), self.size)
