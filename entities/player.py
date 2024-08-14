import random
import pygame
from typing import TYPE_CHECKING
from entities.character import Character

from weapons.attack import Attack
from weapons.aura import Aura
from weapons.flamethrower import Flamethrower
from weapons.pistol import Pistol
from weapons.rifle import Rifle
from weapons.rocket_launcher import RocketLauncher
from weapons.shotgun import Shotgun
from weapons.sniper import Sniper


def display_weapon_choices(screen, choices):
    font = pygame.font.Font(None, 30)  # Reduce font size
    rect_width, rect_height = 200, 60
    padding = 20
    start_x = (screen.get_width() - (rect_width * len(choices) + padding * (len(choices) - 1))) // 2
    start_y = (screen.get_height() - rect_height) // 2

    rects = []
    for i, weapon in enumerate(choices):
        rect_x = start_x + i * (rect_width + padding)
        rect_y = start_y
        rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)
        rects.append(rect)

        # Draw the rectangle
        pygame.draw.rect(screen, (0, 0, 0), rect)
        pygame.draw.rect(screen, (255, 255, 255), rect, 2)

        # Draw the weapons name and level
        text = font.render(f"{weapon.name} (Lvl. {weapon.level})", True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    pygame.display.flip()
    return rects


def die():
    print("Player has died")
    # Handle player's death


class Player:

    def __init__(self, game, x, y, image_path, character: Character):
        self.game = game
        self.character = character
        self.image = pygame.image.load(f'assets/images/{image_path}')
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

        # Apply character stats to the player
        character.apply_to_player(self)

        # Initialize player-specific attributes
        self.health = character.health
        self.max_health = character.health
        self.armor = character.armor
        self.speed = character.speed
        self.invincible = False
        self.invincible_time = 0
        self.invincible_duration = 1000
        self.is_alive = True

        # Initialize XP and level attributes
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 200  # XP required to reach the next level

        # Initialize weapons list
        self.weapons = []
        starting_weapon = character.starting_weapon
        self.add_or_level_up_weapon(starting_weapon)

        # Apply character modifiers to the starting weapon if it's an Aura
        if isinstance(starting_weapon, Aura):
            starting_weapon.apply_modifiers(character.damage, character.radius)

    def add_or_level_up_weapon(self, new_weapon):
        for weapon in self.weapons:
            if weapon.name == new_weapon.name:
                weapon.level_up()
                return
        self.weapons.append(new_weapon)

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

    def attack(self, attacks, target=None, enemies=None, damage_texts=None):
        for weapon in self.weapons:
            if isinstance(weapon, Aura):
                weapon.apply_damage(enemies, self, damage_texts)  # Pass the damage_texts list
            else:
                if weapon.can_shoot() and target is not None:
                    attack = Attack(self.rect.centerx, self.rect.centery, target, weapon.projectile_speed, weapon.shape,
                                    weapon.color, weapon.damage, 100)
                    attacks.append(attack)

    def draw(self, screen, camera_x, camera_y):
        screen.blit(self.image, (self.x - camera_x, self.y - camera_y))
        self.draw_health_bar(screen, camera_x, camera_y)
        self.draw_xp_bar(screen)

        for weapon in self.weapons:
            if isinstance(weapon, Aura):
                weapon.draw(screen, self.rect.centerx, self.rect.centery, camera_x, camera_y)


    def draw_health_bar(self, screen, camera_x=0, camera_y=0):
        bar_width = 100
        bar_height = 10
        health_ratio = self.health / self.max_health
        health_bar_width = int(bar_width * health_ratio)

        health_bar_x = self.rect.centerx - (bar_width // 2) - camera_x
        health_bar_y = self.rect.top - 25 - camera_y

        pygame.draw.rect(screen, (255, 0, 0), (health_bar_x, health_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (health_bar_x, health_bar_y, health_bar_width, bar_height))

        font = pygame.font.Font(None, 24)
        health_text = f"{int(self.health)}/{self.max_health}"
        text = font.render(health_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx - camera_x, health_bar_y - 10))
        screen.blit(text, text_rect)

    def draw_xp_bar(self, screen, camera_x=0, camera_y=0):
        bar_width = screen.get_width()
        bar_height = 20
        xp_ratio = self.xp / self.xp_to_next_level
        xp_bar_width = int(bar_width * xp_ratio)

        xp_bar_x = 0  # The XP bar usually spans the full width, so no camera offset is needed horizontally
        xp_bar_y = 10 - camera_y

        pygame.draw.rect(screen, (50, 50, 50), (xp_bar_x, xp_bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 0, 255), (xp_bar_x, xp_bar_y, xp_bar_width, bar_height))

        font = pygame.font.Font(None, 36)
        xp_text = f"Level {self.level}"
        text = font.render(xp_text, True, (255, 255, 255))
        text_rect = text.get_rect(center=(bar_width // 2, xp_bar_y + bar_height // 2))
        screen.blit(text, text_rect)

    def collect_xp(self, amount, screen):
        self.xp += amount
        if self.xp >= self.xp_to_next_level:
            self.level_up(screen)

    def level_up(self, screen):
        self.level += 1
        self.xp = 0
        self.xp_to_next_level = int(self.xp_to_next_level * 1.5)  # Increase XP required for the next level
        self.max_health += 10  # Increase player's max health as an example
        self.health = self.max_health  # Heal the player to full health
        self.choose_new_weapon(screen)  # Allow the player to choose a new weapon

    # In the choose_new_weapon method (in player.py)

    def choose_new_weapon(self, screen):
        # Preserve the current game state before showing the weapon selection screen
        current_camera_x = self.game.camera_x
        current_camera_y = self.game.camera_y

        self.game.paused = True  # Pause the game

        available_weapons = [Pistol(), Rifle(), Shotgun(), Sniper(), RocketLauncher(), Flamethrower(), Aura()]
        random.shuffle(available_weapons)
        choices = available_weapons[:3]

        rects = display_weapon_choices(screen, choices)

        chosen_weapon = None
        while not chosen_weapon:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(mouse_pos):
                            chosen_weapon = choices[i]
                            self.add_or_level_up_weapon(chosen_weapon)
                            break

            # Instead of redrawing the background, just draw the current state
            self.draw(screen, current_camera_x,
                      current_camera_y)  # Draw the player and other entities in their last known positions
            self.game.draw_pause_menu(screen, choices, rects)  # Overlay the weapon selection screen

            pygame.display.flip()  # Update the full display surface to the screen

        # Restore the camera position after selecting the weapon
        self.game.camera_x = current_camera_x
        self.game.camera_y = current_camera_y

        self.game.paused = False  # Unpause the game

    def add_or_level_up_weapon(self, new_weapon):
        self.character.apply_to_weapon(new_weapon)
        for weapon in self.weapons:
            if weapon.name == new_weapon.name:
                weapon.level_up()
                return
        self.weapons.append(new_weapon)



    def draw_weapon_box(self, screen):
        font = pygame.font.Font(None, 24)  # Font size adjusted to fit within the box
        box_width, box_height = 150, 30
        padding = 5
        start_x = 10  # Position near the top left corner
        start_y = 40  # Position just below the XP bar

        for i, weapon in enumerate(self.weapons):
            rect_x = start_x
            rect_y = start_y + i * (box_height + padding)
            rect = pygame.Rect(rect_x, rect_y, box_width, box_height)

            # Draw the box
            pygame.draw.rect(screen, (0, 0, 0), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)

            # Draw the weapon's name and level
            text = font.render(f"{weapon.name} (Lvl. {weapon.level})", True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

    def choose_starting_weapon(self, screen):
        available_weapons = [Pistol(), Rifle(), Shotgun(), Sniper(), RocketLauncher(), Flamethrower(), Aura()]
        random.shuffle(available_weapons)
        choices = available_weapons[:3]

        rects = display_weapon_choices(screen, choices)

        chosen_weapon = None
        while not chosen_weapon:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(rects):
                        if rect.collidepoint(mouse_pos):
                            chosen_weapon = choices[i]
                            self.add_or_level_up_weapon(chosen_weapon)
                            break

            # Use the dedicated drawing function for the pause menu
            self.game.draw_pause_menu(screen, choices, rects)

    def take_damage(self, damage):
        if not self.invincible:
            effective_damage = max(damage - self.armor, 0)
            self.health -= effective_damage
            self.invincible = True
            self.invincible_time = pygame.time.get_ticks()

            if self.health <= 0:
                self.health = 0
                self.is_alive = False  # Player is dead

            return effective_damage
        return 0

    def update_invincibility(self):
        if self.invincible:
            current_time = pygame.time.get_ticks()
            if current_time - self.invincible_time > self.invincible_duration:
                self.invincible = False  # End invincibility
