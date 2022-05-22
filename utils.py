import pygame

pygame.init()

display = pygame.display.set_mode((1200, 700))
display_scroll = [0, 0]

clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
font_health = pygame.font.Font('freesansbold.ttf', 12)
font_enemies = pygame.font.Font('freesansbold.ttf', 20)
player_x = display.get_width()/2
player_y = display.get_height()/2


def move(d_scroll, p_bul, e_bul, e, x, y):
    d_scroll[0] += x
    d_scroll[1] += y
    for bullet in p_bul:
        bullet.x += x
        bullet.y += y
    for bullet in e_bul:
        bullet.x += x
        bullet.y += y
    for enemy in e:
        enemy.x += x
        enemy.y += y
