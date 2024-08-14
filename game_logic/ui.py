import pygame


class DamageText:
    def __init__(self, x, y, damage, font_size=20, color=(255, 0, 0), duration=1000):
        self.x = x
        self.y = y
        self.damage = round(damage, 2)  # Round the damage to 2 decimal places
        self.font_size = font_size
        self.color = color
        self.duration = duration  # Duration in milliseconds
        self.start_time = pygame.time.get_ticks()
        self.font = pygame.font.Font(None, self.font_size)
        self.text = self.font.render(str(self.damage), True, self.color)
        self.rect = self.text.get_rect(center=(self.x, self.y))

   # weapon.draw(screen, self.rect.centerx, self.rect.centery, camera_x, camera_y)
    def update(self):
        # Move the text up slightly
        self.y -= 1
        self.rect.y = self.y

    def draw(self, screen, camera_x=0, camera_y=0):
        screen.blit(self.text, (self.x - camera_x, self.y - camera_y))

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.duration
