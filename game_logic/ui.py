import pygame


class DamageText:
    def __init__(self, x, y, damage, font_size=20, color=(255, 0, 0), duration=1000):
        self.x = x
        self.y = y
        self.damage = damage
        self.font_size = font_size
        self.color = color
        self.duration = duration  # Duration in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, self.font_size)
        self.text = self.font.render(str(self.damage), True, self.color)
        self.rect = self.text.get_rect(center=(self.x, self.y))

    def update(self):
        # Move the text up slightly
        self.y -= 1
        self.rect.y = self.y

    def draw(self, screen):
        screen.blit(self.text, self.rect)

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration
