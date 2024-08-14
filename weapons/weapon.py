import pygame


class Weapon:
    def __init__(self, name, base_damage, fire_rate, projectile_speed, shape, color):
        self.name = name
        self.base_damage = base_damage
        self.damage = base_damage
        self.fire_rate = fire_rate
        self.projectile_speed = projectile_speed
        self.shape = shape  # Shape of the projectile ('circle' or 'square')
        self.color = color  # Color of the projectile (RGB tuple)
        self.level = 1
        self.last_shoot_time = 0

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.fire_rate:
            self.last_shoot_time = current_time
            return True
        return False

    def level_up(self):
        self.level += 1
        self.damage = self.base_damage * (1 + 0.2 * self.level)  # Increase damage by 20% per level
        print(f"{self.name} leveled up to level {self.level}. Damage is now {self.damage}.")
