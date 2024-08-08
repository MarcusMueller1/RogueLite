import pygame
import random
from player import Player
from item import Item
from enemy import Enemy
from attack import Attack

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

        self.attacks = []
        self.shoot_interval = 1000  # Shoot every second
        self.last_shoot_time = pygame.time.get_ticks()

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode(self.windowed_size)
            self.screen_width, self.screen_height = self.windowed_size

    def find_nearest_enemy(self):
        # For now, we have only one enemy, so return it
        return self.enemy

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

            if self.player.can_shoot:
                current_time = pygame.time.get_ticks()
                if current_time - self.last_shoot_time > self.shoot_interval:
                    nearest_enemy = self.find_nearest_enemy()
                    attack = Attack(self.player.rect.centerx,
                                    self.player.rect.centery,
                                    nearest_enemy, 10, '/fireball.png')

                    self.attacks.append(attack)
                    self.last_shoot_time = current_time

            for attack in self.attacks:
                attack.update()

            self.screen.fill((0, 0, 0))
            self.player.draw(self.screen)
            if not self.item.collected:
                self.item.draw(self.screen)
            self.enemy.draw(self.screen)
            for attack in self.attacks:
                attack.draw(self.screen)
            pygame.display.flip()

            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
wwwww