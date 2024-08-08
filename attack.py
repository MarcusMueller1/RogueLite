import pygame
import math

class Attack:
    def __init__(self, x, y, target, speed, image_path, damage, min_distance=30):
        try:
            self.image = pygame.image.load(f'images/{image_path}')
        except pygame.error as e:
            print(f"Error loading attack image: {e}")
            self.image = pygame.Surface((20, 20))
            self.image.fill((255, 255, 0))

        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.target = target
        self.damage = damage
        self.dx, self.dy = 0, 0

        # Ensure that the attack does not spawn too close to the target
        self.adjust_position(min_distance)
        self.calculate_direction()

    def adjust_position(self, min_distance):
        dx = self.target.rect.centerx - self.x
        dy = self.target.rect.centery - self.y
        distance = math.hypot(dx, dy)

        if distance < min_distance:
            if distance != 0:
                # Adjust position to be min_distance away from the target
                self.x = self.target.rect.centerx - (dx / distance * min_distance)
                self.y = self.target.rect.centery - (dy / distance * min_distance)
                self.rect.center = (self.x, self.y)

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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def hit_target(self):
        return self.rect.colliderect(self.target.rect)
