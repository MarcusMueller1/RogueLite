import pygame
import math

class Enemy:
    def __init__(self, x, y, image_path, speed):
        try:
            self.image = pygame.image.load(f'images/{image_path}')
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

    def move_towards_player(self, player):
        dx = player.x - self.x
        dy = player.y - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            dx /= distance
            dy /= distance
            self.x += dx * self.speed
            self.y += dy * self.speed
            self.rect.topleft = (self.x, self.y)

    def take_damage(self, amount):
        self.health -= amount
        print(f"Enemy took {amount} damage, health is now {self.health}")  # Debugging output
        if self.health <= 0:
            self.die()

    def die(self):
        print("Enemy died")
        # Handle enemy death (e.g., remove from game, drop XP, etc.)

    def is_dead(self):
        return self.health <= 0
