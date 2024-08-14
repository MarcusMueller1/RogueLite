import pygame
import random

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

# Define specific weapons
class Pistol(Weapon):
    def __init__(self):
        super().__init__(name="Pistol", base_damage=10, fire_rate=500, projectile_speed=15, shape='circle', color=(255, 0, 0))

class Rifle(Weapon):
    def __init__(self):
        super().__init__(name="Rifle", base_damage=8, fire_rate=300, projectile_speed=20, shape='square', color=(0, 255, 0))

class Shotgun(Weapon):
    def __init__(self):
        super().__init__(name="Shotgun", base_damage=15, fire_rate=1000, projectile_speed=10, shape='circle', color=(0, 0, 255))

class Sniper(Weapon):
    def __init__(self):
        super().__init__(name="Sniper", base_damage=25, fire_rate=2000, projectile_speed=30, shape='square', color=(255, 255, 0))

class RocketLauncher(Weapon):
    def __init__(self):
        super().__init__(name="Rocket Launcher", base_damage=50, fire_rate=3000, projectile_speed=8, shape='circle', color=(255, 165, 0))

class Flamethrower(Weapon):
    def __init__(self):
        super().__init__(name="Flamethrower", base_damage=5, fire_rate=100, projectile_speed=5, shape='square', color=(255, 0, 255))
class Aura(Weapon):
    def __init__(self):
        super().__init__(name="Aura", base_damage=1, fire_rate=0, projectile_speed=0, shape='circle', color=(255, 255, 0))
        self.radius = 200  # Initial radius of the aura

    def level_up(self):
        super().level_up()
        self.radius += 20  # Increase the radius by 20 units per level

    def draw(self, screen, player):
        pygame.draw.circle(screen, self.color, player.rect.center, self.radius, 2)

    def apply_damage(self, enemies, player):
        for enemy in enemies:
            if not enemy.is_dead():  # Only apply damage if the enemy is alive
                distance = ((enemy.rect.centerx - player.rect.centerx) ** 2 + (
                            enemy.rect.centery - player.rect.centery) ** 2) ** 0.5
                if distance <= self.radius:
                    enemy.take_damage(self.damage)

