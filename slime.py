
class Slime:
    def __init__(self, x, y, size):
        self.size = size
        self.x = x
        self.y = y
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size*2, self.size*2)
        self.damage_flick_cooldown = 0
        self.damaged = False
        self.damage_flick_dir = 0
        self.speed = slime_speed
        self.angle = math.atan2(y - player.y, x - player.x)
        self.vel_x = math.cos(self.angle) * self.speed
        self.vel_y = math.sin(self.angle) * self.speed
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)
        self.behaviour_change_timer = 0
        self.attack_cooldown = slime_attack_cooldown
        self.hp = slime_hp

        self.animation_counter = 0
        self.still_animation = [pygame.image.load("Slime_still_0.xcf"), pygame.image.load("Slime_still_1.xcf"),
                                pygame.image.load("Slime_still_2.xcf"), pygame.image.load("Slime_still_3.xcf"),
                                pygame.image.load("Slime_still_0.xcf")]

    def main(self):
        if self.damage_flick_cooldown != 0:
            self.damage_flick_cooldown -= 1
        elif self.damaged:
            self.damaged = False
            if self.damage_flick_dir == 0:
                self.x += damage_flick
            elif self.damage_flick_dir == 1:
                self.y += damage_flick
            elif self.damage_flick_dir == 2:
                self.x -= damage_flick
            else:
                self.y -= damage_flick

        self.behaviour()
        self.x -= self.vel_x
        self.y -= self.vel_y
        self.hit_box = pygame.Rect(self.x - self.size, self.y - self.size, self.size * 2, self.size * 2)

        texture = int(self.animation_counter/12) - 1
        if self.animation_counter == 60:
            self.animation_counter = 0
        else:
            self.animation_counter += 1
        #pygame.draw.rect(display, (255,0,0), self.hit_box)
        display.blit(pygame.transform.scale(self.still_animation[texture],
                                            (self.size*2, self.size*2)), (self.x - self.size, self.y - self.size))
        # pygame.draw.circle(display, (255, 140, 0), (self.x, self.y), self.size)

    def behaviour(self):
        if self.behaviour_change_timer == 0:
            if self.player_in_range() and random.randint(0, slime_wander_off_probability) != 0:
                self.follow_player()
            else:
                self.wander()
            self.vel_x = math.cos(self.angle) * self.speed
            self.vel_y = math.sin(self.angle) * self.speed
            self.behaviour_change_timer = slime_behaviour_change
        else:
            self.behaviour_change_timer -= 1

    def player_in_range(self):
        return math.sqrt((self.x - player.x) ** 2 + (self.y - player.y) ** 2) <= slime_sight_range

    def follow_player(self):
        deviation_x = random.randint(-slime_min_wandering_range, slime_max_wandering_range)
        deviation_y = random.randint(-slime_min_wandering_range, slime_max_wandering_range)
        self.angle = math.atan2(self.y - player.y - deviation_y, self.x - player.x - deviation_x)

    def wander(self):
        deviation_x = random.randint(-slime_min_wandering_range, slime_max_wandering_range)
        deviation_y = random.randint(-slime_min_wandering_range, slime_max_wandering_range)
        self.angle = math.atan2(self.y + deviation_y, self.x + deviation_x)

    def attack(self, enemy_bullets):
        if self.attack_cooldown == 0 and self.player_in_range():
            enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi, slime_bullet_size, slime_bullet_TTL, slime_bullet_dmg))
            enemy_bullets.append(SlimeBullet(self.x, self.y, 0, slime_bullet_size, slime_bullet_TTL, slime_bullet_dmg))
            enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi*1/3, slime_bullet_size, slime_bullet_TTL, slime_bullet_dmg))
            enemy_bullets.append(SlimeBullet(self.x, self.y, -math.pi*1/3, slime_bullet_size, slime_bullet_TTL, slime_bullet_dmg))
            enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi*2/3, slime_bullet_size, slime_bullet_TTL, slime_bullet_dmg))
            enemy_bullets.append(SlimeBullet(self.x, self.y, -math.pi*2/3, slime_bullet_size, slime_bullet_TTL, slime_bullet_dmg))
            self.attack_cooldown = slime_attack_cooldown
        elif self.attack_cooldown != 0:
            self.attack_cooldown -= 1

    def die(self):
        enemy_bullets.append(SlimeBullet(self.x, self.y, 0, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi * 1 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi * 2 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi * 3 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi * 4 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, math.pi * 5 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, -math.pi * 1 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, -math.pi * 2 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, -math.pi * 3 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, -math.pi * 4 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))
        enemy_bullets.append(SlimeBullet(self.x, self.y, -math.pi * 5 / 6, slime_bullet_size, slime_death_bullet_TTL, slime_death_bullet_dmg))

