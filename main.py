import pygame
import random
import math

# Define the Player class
class Player:
    def __init__(self, x, y, image_path, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def move(self, keys, screen_width, screen_height):
        if keys[pygame.K_a] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_d] and self.x < screen_width - self.rect.width:
            self.x += self.speed
        if keys[pygame.K_w] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_s] and self.y < screen_height - self.rect.height:
            self.y += self.speed
        self.rect.topleft = (self.x, self.y)

# Define the Item class
class Item:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, (self.x, self.y))

    def check_pickup(self, player):
        if self.rect.colliderect(player.rect):
            self.collected = True
            return True
        return False

# Define the Enemy class
class Enemy:
    def __init__(self, x, y, image_path, speed):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
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

# Define the Game class
class Game:
    def __init__(self):
        pygame.init()
        self.fullscreen = False
        self.windowed_size = (1280, 720)
        self.screen_width, self.screen_height = self.windowed_size
        self.screen = pygame.display.set_mode(self.windowed_size)
        pygame.display.set_caption("2D Roguelite")

        # Player
        self.player = Player(self.screen_width // 2, self.screen_height // 2, 'player.png', 5)

        # Item
        self.item = Item(random.randint(0, self.screen_width - 30),
                         random.randint(0, self.screen_height - 30),
                         'item.png')

        # Enemy
        self.enemy = Enemy(random.randint(0, self.screen_width - 50),
                           random.randint(0, self.screen_height - 50),
                           'enemy.png', 2)

        self.clock = pygame.time.Clock()
        self.running = True

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode(self.windowed_size)
            self.screen_width, self.screen_height = self.windowed_size

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
                    self.toggle_fullscreen()

            keys = pygame.key.get_pressed()
            self.player.move(keys, self.screen_width, self.screen_height)

            if not self.item.collected:
                self.item.check_pickup(self.player)

            self.enemy.move_towards_player(self.player)

            self.screen.fill((0, 0, 0))
            self.player.draw(self.screen)
            if not self.item.collected:
                self.item.draw(self.screen)
            self.enemy.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

# Main execution
if __name__ == "__main__":
    game = Game()
    game.run()
