import pygame
import sys
import random

import settings
import utils
from utils import display, display_scroll, move
from slime import Slime
from player import Player
from dummy import Dummy

pygame.init()

player = Player(display.get_width()/2, display.get_height()/2, 32, 32)
dummy = Dummy(600, 300, 40, 40)
player_bullets = []
enemies = []
enemy_bullets = []
enemies.append(dummy)

spawn_cd = settings.spawn_cd
SCORE = 0

while True:
    if player.hp <= 0:
        break   # subject to change

    display.fill((105, 105, 105))
    entity_scroll = [0, 0]

    utils.clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    environment_speed = settings.walking_speed

    # collisions
    for bullet in player_bullets:
        for enemy in enemies:
            if bullet.hit_box.colliderect(enemy.hit_box):
                try:    # if a bullet hits 2 enemies at once (rare occurance) it will throw ValueError
                    player_bullets.remove(bullet)
                except ValueError:
                    0
                bullet.damage(enemy)

    for bullet in enemy_bullets:
        if bullet.hit_box.colliderect(player.hit_box):
            bullet.damage(player)
            enemy_bullets.remove(bullet)

    # controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not player.running:
            if event.button == 1:
                player.primary_fire(mouse_x, mouse_y, player_bullets)
            if event.button == 3:
                player.shotgun(mouse_x, mouse_y, player_bullets)

    keys = pygame.key.get_pressed()

    # speed
    if player.shooting_penalty != 0:
        environment_speed -= settings.shooting_penalty
    if player.shotgun_penalty != 0:
        environment_speed -= settings.shotgun_shooting_penalty
    if keys[pygame.K_SPACE] and player.dash_cooldown == 0:
        environment_speed += settings.dash_speed
        player.dash(keys)
    if not keys[pygame.K_SPACE]:
        player.reset_dash()
    if keys[pygame.K_LSHIFT]:
        environment_speed += settings.sprinting_boost
        player.running = True
    if not keys[pygame.K_LSHIFT]:
        player.running = False

    # movement
    if keys[pygame.K_a]:
        move(display_scroll, player_bullets, enemy_bullets, enemies, environment_speed, 0)
    if keys[pygame.K_w]:
        move(display_scroll, player_bullets, enemy_bullets, enemies, 0, environment_speed)
    if keys[pygame.K_s]:
        move(display_scroll, player_bullets, enemy_bullets, enemies, 0, -environment_speed)
    if keys[pygame.K_d]:
        move(display_scroll, player_bullets, enemy_bullets, enemies, -environment_speed, 0)
    if keys[pygame.K_LCTRL]:
        display.blit(utils.font_health.render("HP: " + str(player.hp), True, (255, 255, 255)),
                                              (player.x, player.y + player.height/2))
        for enemy in enemies:
            display.blit(utils.font_health.render("HP: " + str(enemy.hp), True, (255, 255, 255)),
                               (enemy.x, enemy.y + enemy.size))

    # developer keys
    if settings.dev_keys:
        if spawn_cd != 0:
            spawn_cd -= 1
        elif keys[pygame.K_p]:
            enemies.append(Slime(random.randint(0, 600), random.randint(0, 800), settings.slime_size))
            spawn_cd = settings.spawn_cd

    # entities
    player.main(mouse_x, mouse_y)
    for enemy in enemies:
        enemy.main()
        enemy.attack(enemy_bullets)
        if enemy.hp <= 0:
            enemies.remove(enemy)
            enemy.die(enemy_bullets)
            SCORE += 1
    # bullets
    for bullet in player_bullets:
        if bullet.TTL != 0:
            bullet.main()
        else:
            player_bullets.remove(bullet)
    for bullet in enemy_bullets:
        if bullet.TTL != 0:
            bullet.main()
        else:
            enemy_bullets.remove(bullet)
    # assets
    pygame.draw.circle(display, (40, 200, 40), (200 + display_scroll[0], 300 + display_scroll[1]), 30)
    pygame.draw.circle(display, (40, 200, 40), (600 + display_scroll[0], 135 + display_scroll[1]), 30)
    pygame.draw.circle(display, (40, 200, 40), (124 + display_scroll[0], 347 + display_scroll[1]), 30)
    pygame.draw.circle(display, (40, 200, 40), (423 + display_scroll[0], 564 + display_scroll[1]), 30)
    pygame.draw.circle(display, (40, 200, 40), (96 + display_scroll[0], 15 + display_scroll[1]), 30)
    # crosshair
    pygame.draw.rect(display, (255, 255, 255), (mouse_x-1, mouse_y + settings.crosshair_size + 5, 2, 5))
    pygame.draw.rect(display, (255, 255, 255), (mouse_x-1, mouse_y - settings.crosshair_size - 10, 2, 5))
    pygame.draw.rect(display, (255, 255, 255), (mouse_x + settings.crosshair_size + 4, mouse_y-1, 5, 2))
    pygame.draw.rect(display, (255, 255, 255), (mouse_x - settings.crosshair_size - 10, mouse_y-1, 5, 2))
    if settings.crosshair_dot:
        pygame.draw.circle(display, (255, 255, 255), (mouse_x, mouse_y), 1)
    if player.running:
        no_shooting = utils.font.render("X", True, (255, 0, 0))
        display.blit(no_shooting, (mouse_x - 11, mouse_y - 15))
    if player.shotgun_cooldown == 0:
        pygame.draw.rect(display, (0, 0, 255), (mouse_x + settings.crosshair_size,
                                                mouse_y + settings.crosshair_size + 5, 3, 4))
        pygame.draw.rect(display, (0, 0, 255), (mouse_x + settings.crosshair_size + 4,
                                                mouse_y + settings.crosshair_size + 5, 3, 4))
        pygame.draw.rect(display, (0, 0, 255), (mouse_x + settings.crosshair_size + 8,
                                                mouse_y + settings.crosshair_size + 5, 3, 4))

    display.blit(utils.font.render("SCORE: " + str(SCORE), True, (0, 0, 255)), (display.get_width()/2 - 70, 20))
    display.blit(utils.font_enemies.render("Enemies alive: " + str(len(enemies)-1), True, (255, 255, 255)),
                 (display.get_width() - 190, 10))
    pygame.display.update()

