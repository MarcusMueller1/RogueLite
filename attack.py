import pygame
import math

class Attack:
    def __init__(self, x, y, target, speed, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'images/{image_path}')
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.target = target
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

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
