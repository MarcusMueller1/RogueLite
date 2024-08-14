import pygame

class Item:
    def __init__(self, x, y, image_path):
        try:
            self.image = pygame.image.load(f'assets/images/{image_path}')
        except pygame.error as e:
            print(f"Error loading item image: {e}")
            self.image = pygame.Surface((30, 30))
            self.image.fill((0, 255, 0))

        self.x = x
        self.y = y
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
