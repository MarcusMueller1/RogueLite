import pygame
import math
from weapons.weapon import Weapon
from weapons.attack import Attack


class Flamethrower(Weapon):
    def __init__(self):
        super().__init__(name="Flamethrower", base_damage=1, fire_rate=150, projectile_speed=1, shape='circle',
                         color=(255, 140, 0))
        self.spread_angle = 30  # Spread angle for the flame spray (in degrees)
        self.num_flames = 5  # Number of flames emitted in each spray burst
        self.range = 300  # Maximum range of the flames in pixels

    def shoot(self, player, direction, attacks):
        if self.can_shoot():
            # Calculate the base angle based on player's direction of movement
            if direction == (0, 0):
                return  # No direction given, do not shoot

            player_direction = math.atan2(direction[1], direction[0])

            # Generate multiple flames within the spread angle
            for i in range(self.num_flames):
                # Calculate the angle for each flame based on the spread
                angle_offset = math.radians(self.spread_angle * (i / (self.num_flames - 1) - 0.5))
                flame_angle = player_direction + angle_offset
                dx = math.cos(flame_angle) * self.projectile_speed
                dy = math.sin(flame_angle) * self.projectile_speed

                # Create a flame attack projectile
                flame_attack = Attack(
                    player.rect.centerx,
                    player.rect.centery,
                    None,  # No specific target, just move in the direction
                    self.projectile_speed,
                    self.shape,
                    self.color,
                    self.damage
                )
                flame_attack.dx = dx
                flame_attack.dy = dy
                flame_attack.range = self.range
                flame_attack.max_distance = self.range  # Set the range for the flame

                # Add each flame to the attacks list
                attacks.append(flame_attack)
