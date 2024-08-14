import pygame
from game_logic.ui import DamageText
from weapons.weapon import Weapon

class Aura(Weapon):
    def __init__(self):
        super().__init__(name="Aura", base_damage=1, fire_rate=0, projectile_speed=0, shape='circle',
                         color=(255, 255, 0))
        self.radius = 125  # Initial radius of the aura
        self.damage_interval = 50  # Time in milliseconds between damage applications
        self.last_damage_time = 0  # Tracks the last time damage was applied
        self.initial_damage = self.base_damage  # Store the initial base damage

    def apply_modifiers(self, damage_modifier, radius_modifier):
        self.damage = self.base_damage * damage_modifier
        self.radius *= radius_modifier  # Apply radius modifier
        self.initial_damage = self.damage  # Store the modified damage as the new initial damage

    def level_up(self):
        self.level += 1
        self.damage = self.initial_damage * (1 + 0.2 * (self.level - 1))
        self.radius += 20  # Increase the radius by 20 units per level
        print(f"{self.name} leveled up to level {self.level}. Damage is now {self.damage}.")

    def draw(self, screen, player):
        pygame.draw.circle(screen, self.color, player.rect.center, self.radius, 2)

    def apply_damage(self, enemies, player, damage_texts):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time < self.damage_interval:
            return  # Not enough time has passed since the last damage application

        for enemy in enemies:
            if not enemy.is_dead():  # Only apply damage if the enemy is alive
                distance = ((enemy.rect.centerx - player.rect.centerx) ** 2 + (
                        enemy.rect.centery - player.rect.centery) ** 2) ** 0.5
                if distance <= self.radius:
                    print(f"Applying {self.damage} damage to enemy at distance {distance}")  # Debug statement
                    enemy.take_damage(self.damage)
                    damage_text = DamageText(enemy.rect.centerx, enemy.rect.centery, self.damage)
                    damage_texts.append(damage_text)

        self.last_damage_time = current_time  # Update the last damage time after applying damage

