import pygame

class Weapon:
    def __init__(self, name, damage, fire_rate, projectile_speed, shape, color):
        self.name = name
        self.damage = damage
        self.fire_rate = fire_rate  # In milliseconds
        self.projectile_speed = projectile_speed
        self.shape = shape  # Shape of the projectile ('circle' or 'square')
        self.color = color  # Color of the projectile (RGB tuple)
        self.last_shoot_time = 0

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shoot_time >= self.fire_rate:
            self.last_shoot_time = current_time
            return True
        return False
