import math
import pygame
from game_logic.ui import DamageText  # Adjust the path based on your project structure

class Attack:
    def __init__(self, x, y, target, speed, shape, color, damage, delay=100):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 20, 20)  # Default size for projectiles
        self.speed = speed
        self.target = target
        self.shape = shape
        self.color = color
        self.damage = damage
        self.delay = delay  # Delay before applying damage in milliseconds
        self.hit_time = None  # Time when the projectile hits the target
        self.dx, self.dy = 0, 0

        if self.target:
            self.calculate_direction()
        else:
            self.dx = 0
            self.dy = 0

        self.active = True  # Add an active state to control damage application
        self.distance_traveled = 0  # To track how far the projectile has traveled
        self.max_distance = 300  # Default max distance for a projectile

    def calculate_direction(self):
        if self.target:
            dx = self.target.rect.centerx - self.x
            dy = self.target.rect.centery - self.y
            distance = math.hypot(dx, dy)
            if distance != 0:
                self.dx = dx / distance * self.speed
                self.dy = dy / distance * self.speed

    def update(self, enemies, damage_texts):
        if not self.active:
            return  # Do nothing if the projectile is inactive

        # Move the projectile
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

        self.distance_traveled += self.speed

        # Check if the projectile has exceeded its range
        if self.distance_traveled >= self.max_distance:
            self.active = False
            return

        # Check for collisions with enemies and apply damage
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                damage_text = DamageText(self.rect.centerx, self.rect.centery, self.damage)
                damage_texts.append(damage_text)
                self.active = False  # Deactivate after hitting an enemy
                return  # Stop checking further once damage is applied

    def draw(self, screen, camera_x=0, camera_y=0):
        if not self.active:
            return  # Do not draw inactive projectiles

        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (self.rect.centerx - camera_x, self.rect.centery - camera_y), 10)
        elif self.shape == 'square':
            rect_with_offset = self.rect.move(-camera_x, -camera_y)
            pygame.draw.rect(screen, self.color, rect_with_offset)

    def can_apply_damage(self):
        if self.hit_time and not self.active:
            return True
        return False
