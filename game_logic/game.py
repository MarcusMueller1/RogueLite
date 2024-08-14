import random
import pygame

from entities.enemy import Enemy
from game_logic.ui import DamageText
from game_logic.utils import get_distance
from items.armor_upgrade import ArmorUpgrade
from items.health_potion import HealthPotion
from items.speed_boost import SpeedBoost


class Game:
    def __init__(self):
        pygame.init()
        self.fullscreen = False
        self.windowed_size = (1280, 720)
        self.screen_width, self.screen_height = self.windowed_size

        # Set up the display with double buffering enabled
        self.screen = pygame.display.set_mode(self.windowed_size, pygame.DOUBLEBUF)
        pygame.display.set_caption("2D Roguelite")

        # Load and set up the background image
        self.background_image = pygame.image.load('assets/images/background.png').convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        # Initialize game elements
        self.enemies = []  # Initialize enemies list
        self.items = []  # Initialize items list
        self.attacks = []  # Initialize attacks list
        self.damage_text = []  # Initialize damage text list
        self.xp_orbs = []  # Initialize XP orbs list

        self.items = [
            HealthPotion(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                         'health_potion.png'),
            SpeedBoost(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                       'speed_boost.png'),
            ArmorUpgrade(random.randint(0, self.screen_width - 30), random.randint(0, self.screen_height - 30),
                         'armor_upgrade.png')
        ]

        # Initialize other game-related attributes
        self.clock = pygame.time.Clock()
        self.running = True  # Ensure this is initialized before using it in the run method
        self.spawn_interval = 10000  # Spawn every 10 seconds
        self.last_spawn_time = pygame.time.get_ticks()

        # Initialize the player after initializing the game elements
        from entities.player import Player  # Importing here to avoid circular dependency
        self.player = Player(self, self.screen_width // 2, self.screen_height // 2, 'player.png', 5)

        # Now that all game elements are initialized, choose starting weapon
        self.player.choose_starting_weapon(self.screen)

        # Trigger the first wave spawn immediately
        self.spawn_enemy(count=5)  # Adjust the count as necessary

        self.paused = False

    def toggle_fullscreen(self):
        if self.fullscreen:
            pygame.display.set_mode(self.windowed_size)
            self.screen_width, self.screen_height = self.windowed_size
            self.fullscreen = False
        else:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.screen_width, self.screen_height = self.screen.get_size()
            self.fullscreen = True

        # Resize the background image to fit the new screen size
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

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

        enemies_to_remove = []
        attacks_to_remove = []

        for attack in self.attacks:
            attack.update()
            if attack.can_apply_damage():
                if attack.target.is_dead():
                    attacks_to_remove.append(attack)
                    continue  # Skip this attack if the target is already dead

                # Apply damage to the target
                attack.target.take_damage(attack.damage)

                # Add the creation of DamageText
                damage_text = DamageText(attack.target.rect.centerx, attack.target.rect.centery, attack.damage)
                self.damage_text.append(damage_text)

                if attack.target.is_dead() and attack.target not in enemies_to_remove:
                    enemies_to_remove.append(attack.target)

                attacks_to_remove.append(attack)  # Mark the attack for removal after it hits

        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                enemy.die()  # This will now automatically add the XP orb to the game's xp_orbs list
                self.enemies.remove(enemy)  # Ensure enemy is removed from the list

        for attack in attacks_to_remove:
            if attack in self.attacks:
                self.attacks.remove(attack)

    def find_nearest_enemy(self):
        if self.enemies:
            return min(self.enemies, key=lambda enemy: get_distance(self.player, enemy))
        return None

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

            new_enemy = Enemy(x, y, 'enemy.png', 2, self)  # Pass the game instance
            self.enemies.append(new_enemy)

    def handle_collisions(self):
        for enemy in self.enemies:
            enemy.move_towards_player(self.player, self.enemies)

            # Check for collision with player and apply damage
            collision_distance = 10  # Distance in pixels to buffer the collision
            if self.player.rect.inflate(collision_distance, collision_distance).colliderect(enemy.rect):
                effective_damage = self.player.take_damage(enemy.damage)
                if effective_damage > 0:
                    damage_text = DamageText(self.player.rect.centerx, self.player.rect.centery - 20, effective_damage)
                    self.damage_text.append(damage_text)

    def update_and_draw(self):
        # Draw the background image first
        self.screen.blit(self.background_image, (0, 0))

        # Update and draw damage texts
        for text in self.damage_text[:]:
            text.update()
            if text.is_expired():
                self.damage_text.remove(text)
            else:
                text.draw(self.screen)

        # Collect XP orbs to remove after the loop
        xp_orbs_to_remove = []
        for xp_orb in self.xp_orbs[:]:
            if xp_orb.update(self.player, self.screen):  # Pass the screen argument
                xp_orbs_to_remove.append(xp_orb)  # Mark for removal
            else:
                xp_orb.draw(self.screen)

        # Remove XP orbs outside of the loop
        for xp_orb in xp_orbs_to_remove:
            if xp_orb in self.xp_orbs:
                self.xp_orbs.remove(xp_orb)

        # Draw the player and their weapon
        self.player.draw(self.screen)
        self.player.draw_weapon_box(self.screen)  # Draw the weapon box here

        # Update and draw items
        for item in self.items:
            if not item.collected:
                item.draw(self.screen)

        # Draw enemies and attacks
        for enemy in self.enemies:
            enemy.draw(self.screen)
        for attack in self.attacks:
            attack.draw(self.screen)

        pygame.display.flip()

    def draw_pause_menu(self, screen, choices, rects):
        # Draw the background image first
        screen.blit(self.background_image, (0, 0))

        # Draw the player, enemies, and items (static elements)
        self.player.draw(screen)
        for enemy in self.enemies:
            enemy.draw(screen)
        for item in self.items:
            if not item.collected:
                item.draw(screen)

        # Draw the weapon choice boxes
        for rect, weapon in zip(rects, choices):
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)
            font = pygame.font.Font(None, 30)
            text = font.render(f"{weapon.name} (Lvl. {weapon.level})", True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        # Finally, update the display
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
                self.player.move(keys, self.screen_width, self.screen_height)

                self.player.update_invincibility()

                for item in self.items:
                    if not item.collected:
                        item.check_pickup(self.player)

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
