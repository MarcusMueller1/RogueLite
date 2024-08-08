import pygame

class Item:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(f'images/{image_path}')
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))

    def check_pickup(self, player):
        if self.rect.colliderect(player.rect):
            self.collected = True
            player.can_shoot = True  # Set the player's ability to shoot
            return True
        return False
