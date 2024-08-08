import pygame
import math

class Enemy:
    def __init__(self, x, y, image_path, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'images/{image_path}')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

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
