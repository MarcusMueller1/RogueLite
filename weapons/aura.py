import pygame
import random
from game_logic.ui import DamageText
from weapons.weapon import Weapon

class Aura(Weapon):
    def __init__(self):
        super().__init__(name="Aura", base_damage=1, fire_rate=0, projectile_speed=0, shape='circle',
                         color=(255, 223, 128))  # Soft golden color for the holy aura
        self.radius = 50  # Initial radius of the aura
        self.damage_interval = 50  # Time in milliseconds between damage applications
        self.last_damage_time = 0  # Tracks the last time damage was applied
        self.initial_damage = self.base_damage  # Store the initial base damage
        self.particles = []  # For storing particles
        self.max_layers = 10  # Number of glow layers for smooth effect

    def apply_modifiers(self, damage_modifier, radius_modifier):
        self.damage = self.base_damage * damage_modifier
        self.radius *= radius_modifier  # Apply radius modifier
        self.initial_damage = self.damage  # Store the modified damage as the new initial damage

    def level_up(self):
        self.level += 1
        self.damage = self.initial_damage * (1 + 0.2 * (self.level - 1))
        self.radius += 20  # Increase the radius by 20 units per level

    def add_particle(self):
        # Cast self.radius to int to avoid TypeError
        inner_radius_int = int(self.radius * 0.5)  # Particles stay within the inner 50% of the radius
        if random.random() < 0.2:  # Lower probability to reduce the number of particles
            particle = {
                'x': random.randint(-inner_radius_int, inner_radius_int),
                'y': random.randint(-inner_radius_int, inner_radius_int),
                'size': random.randint(1, 2),  # Smaller size for subtler effect
                'alpha': random.randint(50, 100)  # Lower alpha for barely visible particles
            }
            self.particles.append(particle)

    def update_particles(self):
        # Update particle positions and fade them out
        for particle in self.particles[:]:
            particle['y'] -= 0.5  # Particles move up more slowly
            particle['alpha'] -= 1  # Particles fade out more slowly
            if particle['alpha'] <= 0:
                self.particles.remove(particle)

    def draw_particles(self, screen, player_x, player_y, camera_x=0, camera_y=0):
        for particle in self.particles:
            particle_color = (*self.color[:3], particle['alpha'])  # Particle color with alpha
            pygame.draw.circle(screen, particle_color,
                               (player_x + particle['x'] - camera_x,
                                player_y + particle['y'] - camera_y),
                               particle['size'])

    def draw(self, screen, player_x, player_y, camera_x=0, camera_y=0):
        # Draw the optimized glow with a smooth transition
        for i in range(self.max_layers, 0, -1):
            glow_radius = self.radius + i * 5  # Smaller radius increments for smoother effect
            alpha = int(50 / (i + 1))  # Keep alpha values low to prevent full opacity

            glow_color = (*self.color[:3], alpha)  # RGBA color with calculated alpha
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (player_x - glow_radius - camera_x, player_y - glow_radius - camera_y))

        # Draw particles
        self.draw_particles(screen, player_x, player_y, camera_x, camera_y)

        # Update particles each frame
        self.update_particles()
        self.add_particle()  # Continuously add new particles for a dynamic effect

    def apply_damage(self, enemies, player, damage_texts):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_damage_time < self.damage_interval:
            return  # Not enough time has passed since the last damage application

        for enemy in enemies:
            if not enemy.is_dead():  # Only apply damage if the enemy is alive
                distance = ((enemy.rect.centerx - player.rect.centerx) ** 2 + (
                        enemy.rect.centery - player.rect.centery) ** 2) ** 0.5
                if distance <= self.radius:
                    enemy.take_damage(self.damage)
                    damage_text = DamageText(enemy.rect.centerx, enemy.rect.centery, self.damage)
                    damage_texts.append(damage_text)

        self.last_damage_time = current_time  # Update the last damage time after applying damage
