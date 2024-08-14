import pygame
import math
from entities.xp import XP

class Enemy:
    def __init__(self, x, y, image_path, speed):
        try:
            self.image = pygame.image.load(f'assets/images/{image_path}')
        except pygame.error as e:
            print(f"Error loading enemy image: {e}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))

        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = 50  # Initial health for the enemy
        self.damage = 10  # Damage the enemy deals to the player on collision

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move_towards_player(self, player, enemies):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.rect.topleft = (self.x, self.y)

        # Prevent overlapping with other enemies
        self.avoid_overlapping(enemies)

    def avoid_overlapping(self, enemies):
        repulsion_strength = 0.5  # Lower value for smoother movement

        for other in enemies:
            if other is not self:
                dx = self.rect.centerx - other.rect.centerx
                dy = self.rect.centery - other.rect.centery
                distance = math.hypot(dx, dy)
                min_distance = self.rect.width / 2 + other.rect.width / 2

                if distance < min_distance and distance > 0:
                    # Apply a repulsive force to move them apart
                    overlap = min_distance - distance
                    dx /= distance
                    dy /= distance
                    self.x += dx * overlap * repulsion_strength
                    self.y += dy * overlap * repulsion_strength
                    self.rect.topleft = (self.x, self.y)

    def take_damage(self, amount):
        if self.health <= 0:
            return  # Prevent further damage if the enemy is already dead

        self.health -= amount
        if self.health <= 0:
            self.health = 0  # Prevent health from going negative
            self.die()

    def die(self):
        print("Enemy died")
        xp_value = 50  # Example value, adjust as necessary
        xp_orb = XP(self.rect.centerx, self.rect.centery, xp_value)
        return xp_orb  # Return the created XP orb

    def is_dead(self):
        return self.health <= 0
