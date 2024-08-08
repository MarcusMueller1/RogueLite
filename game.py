import pygame
import random
from player import Player
from item import Item
from enemy import Enemy
from attack import Attack
from damage_text import DamageText

class Game:
    def __init__(self):
        pygame.init()
        self.fullscreen = False
        self.windowed_size = (1280, 720)
        self.screen_width, self.screen_height = self.windowed_size
        self.screen = pygame.display.set_mode(self.windowed_size)
        pygame.display.set_caption("2D Roguelite")

        self.player = Player(self.screen_width // 2, self.screen_height // 2, 'player.png', 5)
        self.item = Item(random.randint(0, self.screen_width - 30),
                         random.randint(0, self.screen_height - 30),
                         'item.png')

        self.enemies = []
        self.attacks = []
        self.damage_texts = []

        self.clock = pygame.time.Clock()
        self.running = True
        self.spawn_interval = 3000  # Spawn every 3 seconds
        self.last_spawn_time = pygame.time.get_ticks()
        self.shoot_interval = 1000  # Shoot every second
        self.last_shoot_time = pygame.time.get_ticks()

    def game_over(self):
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('Game Over', True, (255, 0, 0))
        restart_text = font.render('Restart', True, (255, 255, 255))
        quit_text = font.render('Quit', True, (255, 255, 255))

        game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        restart_rect = restart_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
        quit_rect = quit_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 150))

        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(restart_text, restart_rect)
        self.screen.blit(quit_text, quit_rect)
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    waiting = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                        waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if restart_rect.collidepoint(mouse_pos):
                        self.__init__()  # Restart the game
                        waiting = False
                    elif quit_rect.collidepoint(mouse_pos):
                        self.running = False
                        waiting = False

    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = self.screen.get_size()
        else:
            self.screen = pygame.display.set_mode(self.windowed_size)
            self.screen_width, self.screen_height = self.windowed_size

    def find_nearest_enemy(self):
        if self.enemies:
            return min(self.enemies, key=lambda enemy: self.get_distance(self.player, enemy))
        return None

    def get_distance(self, entity1, entity2):
        dx = entity1.rect.centerx - entity2.rect.centerx
        dy = entity1.rect.centery - entity2.rect.centery
        return (dx ** 2 + dy ** 2) ** 0.5

    def spawn_enemy(self, count=3):
        for _ in range(count):
            x = random.randint(0, self.screen_width - 50)
            y = random.randint(0, self.screen_height - 50)
            new_enemy = Enemy(x, y, 'enemy.png', 2)
            self.enemies.append(new_enemy)

    def handle_collisions(self):
        for enemy in self.enemies:
            enemy.move_towards_player(self.player)
            if self.player.rect.colliderect(enemy.rect):
                effective_damage = self.player.take_damage(enemy.damage)
                if effective_damage > 0:
                    damage_text = DamageText(self.player.rect.centerx, self.player.rect.centery - 20, effective_damage)
                    self.damage_texts.append(damage_text)

    def handle_attacks(self):
        current_time = pygame.time.get_ticks()
        if self.player.can_shoot:
            if current_time - self.last_shoot_time > self.shoot_interval:
                nearest_enemy = self.find_nearest_enemy()
                if nearest_enemy:
                    attack = Attack(self.player.rect.centerx,
                                    self.player.rect.centery,
                                    nearest_enemy, 10, 'fireball.png', 20)
                    self.attacks.append(attack)
                    self.last_shoot_time = current_time

        for attack in self.attacks:
            attack.update()
            if attack.hit_target():
                attack.target.take_damage(attack.damage)
                damage_text = DamageText(attack.target.rect.centerx, attack.target.rect.centery - 20, attack.damage)
                self.damage_texts.append(damage_text)
                if attack.target.is_dead():
                    self.enemies.remove(attack.target)
                self.attacks.remove(attack)

    def update_and_draw(self):
        for text in self.damage_texts:
            text.update()
            if text.is_expired():
                self.damage_texts.remove(text)

        self.screen.fill((0, 0, 0))
        self.player.draw(self.screen)
        if not self.item.collected:
            self.item.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for attack in self.attacks:
            attack.draw(self.screen)
        for text in self.damage_texts:
            text.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
                    self.toggle_fullscreen()

            keys = pygame.key.get_pressed()
            self.player.move(keys, self.screen_width, self.screen_height)

            self.player.update_invincibility()  # Ensure this is called to manage invincibility

            if not self.item.collected:
                self.item.check_pickup(self.player)

            if current_time - self.last_spawn_time > self.spawn_interval:
                self.spawn_enemy(count=5)
                self.last_spawn_time = current_time

            self.handle_collisions()
            self.handle_attacks()
            self.update_and_draw()
            if not self.player.is_alive:
                self.game_over()

            self.clock.tick(60)

        pygame.quit()
