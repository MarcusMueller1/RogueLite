import pygame

class XP:
    def __init__(self, x, y, amount, color=(0, 255, 0)):
        # Store world position (x, y) without camera influence
        self.world_x = x
        self.world_y = y
        self.amount = amount
        self.color = color
        self.rect = pygame.Rect(self.world_x, self.world_y, 10, 10)  # XP orbs will be small squares

    def update(self, player, screen):
        # Only detect collision with player, do not modify world_x, world_y
        if self.rect.colliderect(player.rect):
            player.collect_xp(self.amount, screen)
            return True
        return False

    def draw(self, screen, camera_x=0, camera_y=0):
        screen_x = self.world_x - camera_x
        screen_y = self.world_y - camera_y
        pygame.draw.rect(screen, self.color, pygame.Rect(screen_x, screen_y, 10, 10))


