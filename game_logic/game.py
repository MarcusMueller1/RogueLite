import random
import pygame

from entities.enemy import Enemy
from game_logic.ui import DamageText
from game_logic.utils import get_distance
from items.armor_upgrade import ArmorUpgrade
from items.health_potion import HealthPotion
from items.speed_boost import SpeedBoost
from entities.character import Character
from entities.player import Player
from weapons.pistol import Pistol
from weapons.aura import Aura
from weapons.flamethrower import Flamethrower


def display_character_choices(screen, characters):
    font = pygame.font.Font(None, 30)
    rect_width, rect_height = 200, 60
    padding = 20
    start_x = (screen.get_width() - (rect_width * len(characters) + padding * (len(characters) - 1))) // 2
    start_y = (screen.get_height() - rect_height) // 2

    rects = []
    for i, character in enumerate(characters):
        rect_x = start_x + i * (rect_width + padding)
        rect_y = start_y
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        rects.append(rect)

        pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        text = font.render(f"{character.name}", True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()
    return rects


def choose_character(screen):
    characters = [
        Character("Warrior", health=150, armor=10, speed=5.0, damage=1.2, attack_speed=0.9, radius=1.0,
                  starting_weapon=Pistol()),
        Character("Mage", health=100, armor=5, speed=5, damage=1.5, attack_speed=1.1, radius=1.5,
                  starting_weapon=Aura()),
        Character("Rogue", health=80, armor=3, speed=5, damage=1.3, attack_speed=1.5, radius=1.0,
                  starting_weapon=Flamethrower()),
    ]

    rects = display_character_choices(screen, characters)

    chosen_character = None
    while not chosen_character:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i, rect in enumerate(rects):
                    if rect.collidepoint(mouse_pos):
                        chosen_character = characters[i]
                        break

    return chosen_character


class Game:
    def __init__(self):
        pygame.init()
        self.map_width = 2560  # Larger map width
        self.map_height = 1440  # Larger map height
        self.camera_x = 0
        self.camera_y = 0
        self.fullscreen = False
        self.windowed_size = (1280, 720)
        self.screen_width, self.screen_height = self.windowed_size

        self.screen = pygame.display.set_mode(self.windowed_size, pygame.DOUBLEBUF)
        pygame.display.set_caption("2D Roguelite")

        self.background_image = pygame.image.load('assets/images/background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.map_width, self.map_height))

        self.enemies = []
        self.items = []
        self.attacks = []
        self.damage_text = []
        self.xp_orbs = []

        self.items = [
            HealthPotion(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                         'health_potion.png'),
            SpeedBoost(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                       'speed_boost.png'),
            ArmorUpgrade(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                         'armor_upgrade.png')
        ]

        self.clock = pygame.time.Clock()
        self.running = True
        self.spawn_interval = 10000
        self.last_spawn_time = pygame.time.get_ticks()

        character = choose_character(self.screen)
        self.player = Player(self, self.screen_width // 2, self.screen_height // 2, 'player.png', character)

        self.spawn_enemy(count=5)

        self.paused = False

    def toggle_fullscreen(self):
        if self.fullscreen:
            # Switch to windowed mode
            pygame.display.set_mode(self.windowed_size)
            self.screen_width, self.screen_height = self.windowed_size
            self.fullscreen = False
        else:
            # Switch to fullscreen mode
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = self.screen.get_size()
            self.fullscreen = True

        # Rescale the background image to fit the new screen size
        self.background_image = pygame.transform.scale(self.background_image, (self.map_width, self.map_height))

        # Recalculate the camera position to ensure it stays within the map boundaries
        self.update_camera()

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

    def handle_attacks(self):
        nearest_enemy = self.find_nearest_enemy()
        if nearest_enemy and self.player.is_alive:
            self.player.attack(self.attacks, nearest_enemy, self.enemies, self.damage_text)

        attacks_to_remove = []

        for attack in self.attacks:
            attack.update(self.enemies, self.damage_text)  # Pass in the list of damage_texts
            if not attack.active:
                attacks_to_remove.append(attack)

        for attack in attacks_to_remove:
            if attack in self.attacks:
                self.attacks.remove(attack)

        # Update and draw damage texts
        for text in self.damage_text[:]:
            text.update()
            if text.is_expired():
                self.damage_text.remove(text)
            else:
                text.draw(self.screen, self.camera_x, self.camera_y)

    def find_nearest_enemy(self):
        if self.enemies:
            return min(self.enemies, key=lambda enemy: get_distance(self.player, enemy))
        return None

    def update_camera(self):
        half_screen_width = self.screen_width // 2
        half_screen_height = self.screen_height // 2

        # Update camera position to follow the player
        self.camera_x = self.player.rect.centerx - half_screen_width
        self.camera_y = self.player.rect.centery - half_screen_height

        # Ensure the camera doesn't move out of the map boundaries
        self.camera_x = max(0, min(self.camera_x, self.map_width - self.screen_width))
        self.camera_y = max(0, min(self.camera_y, self.map_height - self.screen_height))

        # Debugging the camera position

    def spawn_enemy(self, count=3):
        for _ in range(count):
            edge = random.choice(['top', 'bottom', 'left', 'right'])

            if edge == 'top':
                x = random.randint(0, self.screen_width - 50)
                y = 0
            elif edge == 'bottom':
                x = random.randint(0, self.screen_width - 50)
                y = self.screen_height - 50
            elif edge == 'left':
                x = 0
                y = random.randint(0, self.screen_height - 50)
            elif edge == 'right':
                x = self.screen_width - 50
                y = random.randint(0, self.screen_height - 50)

            new_enemy = Enemy(x, y, 'enemy.png', 2, self)
            self.enemies.append(new_enemy)

    def handle_collisions(self):
        for enemy in self.enemies:
            enemy.move_towards_player(self.player, self.enemies)

            collision_distance = 10
            if self.player.rect.inflate(collision_distance, collision_distance).colliderect(enemy.rect):
                effective_damage = self.player.take_damage(enemy.damage)
                if effective_damage > 0:
                    damage_text = DamageText(self.player.rect.centerx, self.player.rect.centery - 20, effective_damage)
                    self.damage_text.append(damage_text)

    def update_and_draw(self):
        self.screen.blit(self.background_image, (-self.camera_x, -self.camera_y))

        for text in self.damage_text[:]:
            text.update()
            if text.is_expired():
                self.damage_text.remove(text)
            else:
                text.draw(self.screen, self.camera_x, self.camera_y)

        xp_orbs_to_remove = []
        for xp_orb in self.xp_orbs[:]:
            if xp_orb.update(self.player, self.screen):
                xp_orbs_to_remove.append(xp_orb)
            else:
                # Pass the camera offsets to the draw method
                xp_orb.draw(self.screen, self.camera_x, self.camera_y)

        for xp_orb in xp_orbs_to_remove:
            if xp_orb in self.xp_orbs:
                self.xp_orbs.remove(xp_orb)

        self.player.draw(self.screen, self.camera_x, self.camera_y)
        self.player.draw_weapon_box(self.screen)

        for item in self.items:
            if not item.collected:
                item.draw(self.screen, self.camera_x, self.camera_y)

        for enemy in self.enemies:
            enemy.draw(self.screen, self.camera_x, self.camera_y)
        for attack in self.attacks:
            attack.draw(self.screen, self.camera_x, self.camera_y)

        pygame.display.flip()

    def draw_pause_menu(self, screen, choices, rects):
        # Draw the weapon selection menu (this will be on top of everything else)
        for rect, weapon in zip(rects, choices):
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            font = pygame.font.Font(None, 30)
            text = font.render(f"{weapon.name}", True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        while self.running:
            current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
                    self.toggle_fullscreen()

            if not self.paused:
                keys = pygame.key.get_pressed()
                self.player.move(keys, self.map_width, self.map_height)

                self.update_camera()

                self.player.update_invincibility()

                for item in self.items:
                    if not item.collected:
                        item.check_pickup(self.player)

                if current_time - self.last_spawn_time > self.spawn_interval:
                    self.spawn_enemy(count=10)
                    self.last_spawn_time = current_time

                self.handle_collisions()
                self.handle_attacks()

            self.update_and_draw()

            if not self.player.is_alive:
                self.game_over()

            self.clock.tick(60)

        pygame.quit()
