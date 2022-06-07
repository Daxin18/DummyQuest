import pygame

dummy_hp = 100

player_hp = 100
player_health_cap = 1000  # maximum health a player can have
player_base_health_cap = 1000   # same as above, but the one above is changing if a player picks up an item,
                                # this one is constant so it is used to set parameters
walking_speed = 3
sprinting_boost = 3
shooting_penalty = 1
shooting_penalty_time = 20
shotgun_shooting_penalty = 2
shotgun_shooting_penalty_time = 10
dash_speed = 15
dash_duration = 10
dash_cooldown = 60
crosshair_size = 3
crosshair_dot = True
dev_keys = True
bullet_speed = 10
bullet_size = 6
bullet_TTL = 90
base_bullet_damage = 2
damage_flick = 5
damage_flick_cooldown = 5
shotgun_cooldown = 60
shotgun_pellets = 12
shotgun_pellet_damage = 1
shotgun_pellet_size = 4
shotgun_pellet_speed = 10
shotgun_spread = 6  # the higher the value, the more accurate the shotgun is
base_bonus_damage = 0
base_bonus_shotgun_damage = 0

slime_speed = 2
slime_size = 15
slime_wandering_range = 100
slime_wander_off_probability = 20   # slime has 1/[slime_wander_off_probability] chance to wander off
slime_behaviour_change = 60
slime_attack_cooldown = 180
slime_bullet_speed = 6
slime_bullet_size = 10
slime_bullet_TTL = 90
slime_death_bullet_TTL = 180
slime_bullet_dmg = 1
slime_death_bullet_dmg = 2
slime_hp = 30
slime_sight_range = 600
spawn_cd = 10

guardian_width = 30
guardian_height = 80
guardian_speed = 1
guardian_idle_time = 300
guardian_buried_time = 160
guardian_attack_cast_time = 120
guardian_min_deviation_range = 50
guardian_max_deviation_range = 100
guardian_sight_range = 800
guardian_hp = 150
guardian_bullet_speed = 20
guardian_bullet_size = 15
guardian_bullet_TTL = 120
guardian_bullet_damage = 15

enable_hit_boxes = False
enable_bullet_hit_boxes = False

collision_tolerance = dash_speed + sprinting_boost + walking_speed + 10

rock_number = 25

tmap_x_offset = 26
tmap_y_offset = 28

spawner_width = 256
spawner_height = 192
spawner_hp = 1000
spawner_spawn_cd = 600
spawner_enraged_spawn_cd = 180
spawner_spawn_amount = 3
spawner_death_spawn_amount = 8
spawner_enrage_hp_ratio = 0.5
spawner_spawn_distance = 200  # not really a distance but whatever
spawner_spawn_deviation = 150
spawner_sight_range = 1200
spawner_amount = 4

item_hover_time = 60
item_hover_amount = 0.25
pizza_heal = 25
item_pickup_radius = 100

spawner_coordinates = [[-1150, 3150], [3400, -2500], [3200, 3300], [-2300, -2200]]
pizza_coordinates = [[-1690, -1565], [3690, -1430], [2855, 2275], [-1048, 2137]]
curse_coordinates = [[-2580, 3550]]
base_boost_coordinates = [[-2520, -2710], [3690, 3500]]
shotgun_boost_coordinates = [[3690, -2710]]

pickup_key = pygame.K_e
sprinting_button = pygame.K_LSHIFT
dash_button = pygame.K_SPACE

difficulty_level = 1
