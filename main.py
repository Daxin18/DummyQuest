import pygame
import sys
import random

import settings
import utils
from utils import display, display_scroll, move, enemies, enemy_bullets, player_bullets, solids, collision_table, assets
from slime import Slime
from guardian import Guardian
from player import Player
from dummy import Dummy
from rock import Rock
from tree import Tree

pygame.init()
pygame.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0), (0, 0, 0, 0, 0, 0, 0, 0))

player = Player(utils.player_x, utils.player_y, 32, 32)

dummy = Dummy(600, 300, 40, 40)
enemies.append(dummy)
solids.append(dummy)
for i in range(25):
    r_x = random.randint(player.x - 1000, player.x + 1000)
    r_y = random.randint(player.y - 1000, player.y + 1000)
    while 550 < r_x < 650 and 250 < r_y < 350:
        r_x = random.randint(player.x - 1000, player.x + 1000)
        r_y = random.randint(player.y - 1000, player.y + 1000)
    r_w = random.randint(45, 70)
    r_h = random.randint(45, 70)
    solids.append(Rock(r_x, r_y, r_w, r_h))
for i in range(40):
    r_x = random.randint(player.x - 1000, player.x + 1000)
    r_y = random.randint(player.y - 1000, player.y + 1000)
    while 550 < r_x < 650 and 250 < r_y < 350:
        r_x = random.randint(player.x - 1000, player.x + 1000)
        r_y = random.randint(player.y - 1000, player.y + 1000)
    r_s = random.randint(25, 40)
    assets.append(Tree(r_x, r_y, r_s))

spawn_cd = 0
hit_box_cd = 0
SCORE = 0

while True:
    if player.hp <= 0:
        break   # subject to change

    display.fill((105, 105, 105))
    collision_table[0] = 0
    collision_table[1] = 0

    utils.clock.tick(60)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    environment_speed = settings.walking_speed

    # collisions
    for bullet in player_bullets:
        for entity in [*enemies, *solids]:
            if bullet.hit_box.colliderect(entity.hit_box):
                try:    # if a bullet hits 2 enemies at once (rare occurance) it will throw ValueError
                    if bullet.damage(entity):
                        player_bullets.remove(bullet)
                except ValueError:
                    0

    for bullet in enemy_bullets:
        for entity in [player, *solids]:
            if bullet.hit_box.colliderect(entity.hit_box):
                if bullet.damage(entity):
                    enemy_bullets.remove(bullet)

    for solid in solids:
        utils.check_player_collision(solid, player)
        solid.render_solid()

    # controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not player.running:
            if event.button == 1:
                player.primary_fire(mouse_x, mouse_y)
            if event.button == 3:
                player.shotgun(mouse_x, mouse_y)

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
        if collision_table[0] >= 0:
            move(environment_speed, 0)
    if keys[pygame.K_w]:
        if collision_table[1] <= 0:
            move(0, environment_speed)
    if keys[pygame.K_s]:
        if collision_table[1] >= 0:
            move(0, -environment_speed)
    if keys[pygame.K_d]:
        if collision_table[0] <= 0:
            move(-environment_speed, 0)
    if keys[pygame.K_LCTRL]:
        display.blit(utils.font_health.render("HP: " + str(player.hp), True, (255, 255, 255)),
                     (player.x, player.y + player.height/2))
        for enemy in enemies:
            display.blit(utils.font_health.render("HP: " + str(enemy.hp), True, (255, 255, 255)),
                         (enemy.x + display_scroll[0], enemy.y + enemy.size + display_scroll[1]))

    # developer keys
    if settings.dev_keys:
        if spawn_cd != 0:
            spawn_cd -= 1
        elif keys[pygame.K_p]:
            enemies.append(Slime(random.randint(0, display.get_width()), random.randint(0, display.get_height())))
            enemies.append(Guardian(random.randint(0, display.get_width()), random.randint(0, display.get_height()),
                                    enemies[0]))
            spawn_cd = settings.spawn_cd
        if hit_box_cd != 0:
            hit_box_cd -= 1
        elif keys[pygame.K_h]:
            settings.enable_hit_boxes = not settings.enable_hit_boxes
            hit_box_cd = 20

    # entities
    player.main(mouse_x, mouse_y)
    for enemy in enemies:
        enemy.main()
        enemy.attack()
        if enemy.hp <= 0:
            enemies.remove(enemy)
            enemy.die()
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
    for asset in assets:
        asset.render_asset()

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
    player.show_dash_cooldown()
    pygame.display.update()
