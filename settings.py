import pygame

pygame.init()

player_hp = 100
walking_speed = 3
sprinting_boost = 3
shooting_penalty = 1
shooting_penalty_time = 20
shotgun_shooting_penalty = 1.5
shotgun_shooting_penalty_time = 10
dash_speed = 15
dash_duration = 10
dash_cooldown = 60
crosshair_size = 3
crosshair_dot = True
dev_keys = True
bullet_speed = 10
bullet_size = 5
bullet_TTL = 90
base_bullet_damage = 2
damage_flick = 5
damage_flick_cooldown = 5
shotgun_cooldown = 60
shotgun_pellets = 12
shotgun_pellet_damage = 1
shotgun_pellet_size = 2
shotgun_spread = 6  # the higher the value, the more accurate the shotgun is
slime_speed = 2
slime_size = 15
slime_min_wandering_range = 50
slime_max_wandering_range = 100
slime_wander_off_probability = 20   # slime has 1/[slime_wander_off_probability] to wander off
slime_behaviour_change = 60
slime_attack_cooldown = 180
slime_bullet_speed = 6
slime_bullet_size = 10
slime_bullet_TTL = 90
slime_death_bullet_TTL = 180
slime_bullet_dmg = 1
slime_death_bullet_dmg = 3
slime_bullet_texture = pygame.image.load("textures\\Slime_bullet.xcf")
player_still = pygame.image.load("textures\\Player_still.xcf")
player_running = [pygame.image.load("textures\\Player_running_0.xcf"), pygame.image.load("textures\\Player_running_1.xcf")]
player_bullet_texture = pygame.image.load("textures\\Player_bullet.xcf")
dash_trail = pygame.image.load("textures\\dash_trail.xcf")
slime_hp = 30
slime_sight_range = 450

display = pygame.display.set_mode((1200, 700))
clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 32)
font_health = pygame.font.Font('freesansbold.ttf', 12)
font_enemies = pygame.font.Font('freesansbold.ttf', 20)
