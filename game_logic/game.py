import random
import pygame

from game_logic.wave_config import wave_data  # Import wave configurations
from entities.enemy_types import FastEnemy, TankEnemy  # Import custom enemy types
from game_logic.enemy_wave import Wave  # Import the Wave class
from entities.character import Character
from entities.player import Player
from items.armor_upgrade import ArmorUpgrade
from items.health_potion import HealthPotion
from items.speed_boost import SpeedBoost
from weapons.pistol import Pistol
from weapons.aura import Aura
from weapons.flamethrower import Flamethrower
from game_logic.ui import DamageText
from game_logic.utils import get_distance


class Game:
    def __init__(self):
        pygame.init()
        self.map_width = 2560
        self.map_height = 1440
        self.camera_x = 0
        self.camera_y = 0
        self.fullscreen = False
        self.windowed_size = (1280, 720)
        self.screen_width, self.screen_height = self.windowed_size

        self.screen = pygame.display.set_mode(self.windowed_size, pygame.DOUBLEBUF)
        pygame.display.set_caption("2D Roguelite")

        self.background_image = pygame.image.load('assets/images/background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.map_width, self.map_height))

        # Game entities
        self.enemies = []
        self.items = []
        self.attacks = []
        self.damage_text = []
        self.xp_orbs = []

        # Initialize game state
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialize waves
        self.waves = []
        self.current_wave_index = 0
        self.load_waves_from_config()  # Load waves from the external config

        # Wave timer
        self.time_between_waves = 10000  # 10 seconds between waves
        self.last_wave_time = pygame.time.get_ticks()

        # Spawn initial items
        self.spawn_items()

        # Character selection and player initialization
        character = self.choose_character()
        self.player = Player(self, self.screen_width // 2, self.screen_height // 2, 'player.png', character)

        self.paused = False

    def load_waves_from_config(self):
        for wave_info in wave_data:
            wave = Wave(enemy_configs=wave_info["enemy_configs"])
            self.waves.append(wave)

    def initialize_waves(self):
        wave1 = Wave(enemy_configs=[(FastEnemy, 5, 'fast_enemy.png', 4), (TankEnemy, 3, 'tank_enemy.png', 1)],
                     spawn_delay=800)
        wave2 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)
        wave3 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)
        wave4 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)
        wave5 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)
        wave6 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)
        wave7 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)
        wave8 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)
        wave9 = Wave(enemy_configs=[(TankEnemy, 2, 'tank_enemy.png', 1), (FastEnemy, 4, 'fast_enemy.png', 4)],
                     spawn_delay=1000)

        self.waves.extend([wave1, wave2, wave3, wave4, wave5, wave6, wave7, wave8, wave9])

    def spawn_items(self):
        self.items = [
            HealthPotion(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                         'health_potion.png'),
            SpeedBoost(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                       'speed_boost.png'),
            ArmorUpgrade(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                         'armor_upgrade.png')
        ]

    def choose_character(self):
        characters = [
            Character("Warrior", health=150, armor=10, speed=5.0, damage=1.2, attack_speed=0.9, radius=1.0,
                      starting_weapon=Pistol()),
            Character("Mage", health=100, armor=5, speed=5, damage=1.5, attack_speed=1.1, radius=1.5,
                      starting_weapon=Aura()),
            Character("Rogue", health=80, armor=3, speed=5, damage=1.3, attack_speed=1.5, radius=1.0,
                      starting_weapon=Flamethrower()),
        ]

        rects = self.display_character_choices(characters)
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

    def display_character_choices(self, characters):
        font = pygame.font.Font(None, 30)
        rect_width, rect_height = 200, 60
        padding = 20
        start_x = (self.screen.get_width() - (rect_width * len(characters) + padding * (len(characters) - 1))) // 2
        start_y = (self.screen.get_height() - rect_height) // 2

        rects = []
        for i, character in enumerate(characters):
            rect_x = start_x + i * (rect_width + padding)
            rect_y = start_y
            rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
            rects.append(rect)

            pygame.draw.rect(self.screen, (0, 0, 0), rect)
            pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)

            text = font.render(f"{character.name}", True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)

        pygame.display.flip()
        return rects

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

        # Update and draw game entities like damage text, xp orbs, player, enemies, etc.
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

        # Time-based wave spawning logic
        current_time = pygame.time.get_ticks()
        if self.current_wave_index < len(self.waves):
            current_wave = self.waves[self.current_wave_index]
            current_wave.spawn(self)

            # Start next wave based on time, without affecting existing enemies
            if current_time - self.last_wave_time >= self.time_between_waves:
                print(f"Wave {self.current_wave_index + 1} completed. Moving to next wave.")
                self.current_wave_index += 1
                self.last_wave_time = current_time

        pygame.display.flip()

    def draw_pause_menu(self, screen, choices, rects):
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

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_F12:
                    self.toggle_fullscreen()

            if not self.paused:
                # Handle player movement, collision, and other game logic
                keys = pygame.key.get_pressed()
                self.player.move(keys, self.map_width, self.map_height)
                self.update_camera()
                self.player.update_invincibility()
                for item in self.items:
                    if not item.collected:
                        item.check_pickup(self.player)
                self.handle_collisions()
                self.handle_attacks()

            # Call update_and_draw every frame
            self.update_and_draw()

            # Check for game over
            if not self.player.is_alive:
                self.game_over()

            # Cap the frame rate
            self.clock.tick(60)

        pygame.quit()
