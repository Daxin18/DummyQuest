import pygame

import settings
from utils import display, display_scroll

texture = pygame.image.load("textures\\Rock.xcf")

"""
Rock is the basic solid

To be included in:
- solids    (for collision)

Behaviour/ attack patterns:
- behaviour - none
- attack pattern - none

Special properties:
--> stops the player and few entities movement
--> collision can be skipped if player is dashing
"""


class Rock:
    def __init__(self, x, y, width, height):
        self.hp = 0
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hit_box = pygame.Rect(self.x - self.width/2, self.y - self.height/2,
                                   self.width, self.height)

    def render_solid(self):
        self.hit_box = pygame.Rect(self.x - self.width/2 + display_scroll[0],
                                   self.y - self.height/2 + display_scroll[1], self.width, self.height)
        if settings.enable_hit_boxes:
            pygame.draw.rect(display, (255, 0, 0), self.hit_box)
        display.blit(pygame.transform.scale(texture, (self.width, self.height)),
                     (self.x - self.width/2 + display_scroll[0], self.y - self.height/2 + display_scroll[1]))

    def damage(self, damage):
        self.hp += damage
        return True
