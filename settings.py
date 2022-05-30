import pygame

player_hp = 100
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
bullet_size = 5
bullet_TTL = 90
base_bullet_damage = 2
damage_flick = 5
damage_flick_cooldown = 5
shotgun_cooldown = 60
shotgun_pellets = 12
shotgun_pellet_damage = 1
shotgun_pellet_size = 2
shotgun_pellet_speed = 10
shotgun_spread = 6  # the higher the value, the more accurate the shotgun is
slime_speed = 2
slime_size = 15
slime_wandering_range = 100
slime_wander_off_probability = 20   # slime has 1/[slime_wander_off_probability] to wander off
slime_behaviour_change = 60
slime_attack_cooldown = 180
slime_bullet_speed = 6
slime_bullet_size = 10
slime_bullet_TTL = 90
slime_death_bullet_TTL = 180
slime_bullet_dmg = 1
slime_death_bullet_dmg = 3
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
guardian_bullet_damage = 15
guardian_bullet_speed = 20
guardian_bullet_size = 15
guardian_bullet_TTL = 120

enable_hit_boxes = False
enable_bullet_hit_boxes = False

collision_tolerance = dash_speed + sprinting_boost + walking_speed + 10

tree_number = 40
rock_number = 25

tmap_x_offset = 26
tmap_y_offset = 28

spawner_width = 30
spawner_height = 80
spawner_hp = 1000
spawner_spawn_cd = 600
spawner_enraged_spawn_cd = 180
spawner_spawn_amount = 3
spawner_death_spawn_amount = 8
spawner_enrage_hp_ratio = 0.5
spawner_spawn_distance = 200  # not really a distance but whatever
spawner_spawn_deviation = 150
spawner_guardians = 3
spawner_sight_range = 1000

item_hover_time = 60
item_hover_amount = 0.25
health_potion_heal = 25
item_pickup_radius = 100

pickup_key = pygame.K_e
