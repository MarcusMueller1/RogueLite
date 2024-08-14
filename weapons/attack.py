import math
import pygame

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
        self.active = True  # Add an active state to control damage application

    def calculate_direction(self):
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.dx = dx / distance * self.speed
            self.dy = dy / distance * self.speed

    def update(self):
        if not self.active:
            return  # Do nothing if the projectile is inactive

        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)

        if self.hit_target():
            self.hit_time = pygame.time.get_ticks()
            self.active = False  # Deactivate after hitting the target

    def draw(self, screen, camera_x=0, camera_y=0):
        if not self.active:
            return  # Do not draw inactive projectiles

        if self.shape == 'circle':
            pygame.draw.circle(screen, self.color, (self.rect.centerx - camera_x, self.rect.centery - camera_y), 10)
        elif self.shape == 'square':
            rect_with_offset = self.rect.move(-camera_x, -camera_y)
            pygame.draw.rect(screen, self.color, rect_with_offset)

    def hit_target(self):
        return self.rect.colliderect(self.target.rect)

    def can_apply_damage(self):
        if self.hit_time and not self.active:
            return True
        return False


