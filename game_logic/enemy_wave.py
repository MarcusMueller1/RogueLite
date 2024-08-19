# enemy_wave.py
import random
import pygame


class Wave:
    def __init__(self, enemy_configs, spawn_delay):
        """
        :param enemy_configs: List of tuples containing (Enemy class, count, image_path, speed)
                              e.g., [(FastEnemy, 5, 'fast_enemy.png', 4), (TankEnemy, 3, 'tank_enemy.png', 1)]
        :param spawn_delay: Delay in milliseconds between spawning each enemy.
        """
        self.enemy_configs = enemy_configs
        self.spawn_delay = spawn_delay
        self.total_enemies = sum(count for _, count, _, _ in enemy_configs)
        self.spawned_enemies = 0
        self.last_spawn_time = pygame.time.get_ticks()
        self.remaining_enemies = self._expand_enemy_list()

    def _expand_enemy_list(self):
        """
        Expands the enemy configuration into a flat list of tuples (enemy_class, image_path, speed).
        """
        enemy_list = []
        for enemy_class, count, image_path, speed in self.enemy_configs:
            enemy_list.extend([(enemy_class, image_path, speed)] * count)
        random.shuffle(enemy_list)  # Randomize the spawn order
        return enemy_list

    def spawn(self, game):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time >= self.spawn_delay and self.spawned_enemies < self.total_enemies:
            self.last_spawn_time = current_time
            enemy_class, image_path, speed = self.remaining_enemies.pop()
            x, y = self.get_spawn_position(game.screen_width, game.screen_height)
            game.enemies.append(enemy_class(x, y, image_path, speed, game))
            self.spawned_enemies += 1

    @staticmethod
    def get_spawn_position(screen_width, screen_height):
        edge = random.choice(['top', 'bottom', 'left', 'right'])
        if edge == 'top':
            return random.randint(0, screen_width - 50), 0
        elif edge == 'bottom':
            return random.randint(0, screen_width - 50), screen_height - 50
        elif edge == 'left':
            return 0, random.randint(0, screen_height - 50)
        elif edge == 'right':
            return screen_width - 50, random.randint(0, screen_height - 50)
