import pygame

class XP:
    def __init__(self, x, y, amount, color=(0, 255, 0)):
        self.x = x
        self.y = y
        self.amount = amount
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, 10, 10)  # XP orbs will be small squares

    def update(self, player, screen):
        if self.rect.colliderect(player.rect):
            player.collect_xp(self.amount, screen)  # Pass the screen argument
            return True
        return False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
