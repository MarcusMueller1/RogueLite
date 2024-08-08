import pygame
import math

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
        self.calculate_direction()

    def calculate_direction(self):
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

        # Set hit time if projectile hits the target
        if self.hit_target() and self.hit_time is None:
            self.hit_time = pygame.time.get_ticks()

    def draw(self, screen):
        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, self.rect.center, 10)
        elif self.shape == 'square':
            pygame.draw.rect(screen, self.color, self.rect)

    def hit_target(self):
        return self.rect.colliderect(self.target.rect)

    def can_apply_damage(self):
        if self.hit_time:
            return pygame.time.get_ticks() - self.hit_time >= self.delay
        return False
