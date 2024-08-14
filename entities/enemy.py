import math

import pygame

from entities.xp import XP


class Enemy:
    def __init__(self, x, y, image_path, speed, game):
        self.game = game
        try:
            self.image = pygame.image.load(f'assets/images/{image_path}')
        except pygame.error as e:
            print(f"Error loading enemy image: {e}")
            self.image = pygame.Surface((50, 50))
            self.image.fill((255, 0, 0))

        self.dead = False
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.health = 50
        self.damage = 10

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

                if min_distance > distance > 0:
                    # Apply a repulsive force to move them apart
                    overlap = min_distance - distance
                    dx /= distance
                    dy /= distance
                    self.x += dx * overlap * repulsion_strength
                    self.y += dy * overlap * repulsion_strength
                    self.rect.topleft = (self.x, self.y)

    def take_damage(self, amount):
        if self.health > 0 and not self.dead:
            self.health -= amount
            print(f"Enemy took {amount} damage, health is now {self.health}")  # Debug statement
            if self.health <= 0:
                self.health = 0
                self.die()

    def die(self):
        if not self.dead:
            self.dead = True
            print("Enemy died")
            xp_value = 50
            xp_orb = XP(self.rect.centerx, self.rect.centery, xp_value)
            self.game.xp_orbs.append(xp_orb)
            self.game.enemies.remove(self)  # Remove the enemy from the game's enemy list

    def is_dead(self):
        return self.dead
