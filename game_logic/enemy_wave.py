# enemy_wave.py
import random
import pygame

class Wave:
    def __init__(self, enemy_configs):
        self.enemy_configs = enemy_configs
        self.total_enemies = sum(count for _, count, _, _ in enemy_configs)
        self.spawned_enemies = 0
        self.remaining_enemies = self._expand_enemy_list()

    def _expand_enemy_list(self):
        enemy_list = []
        for enemy_class, count, image_path, speed in self.enemy_configs:
            enemy_list.extend([(enemy_class, image_path, speed)] * count)
        random.shuffle(enemy_list)
        return enemy_list

    def spawn(self, game):
        # Spawn all enemies at once
        while self.spawned_enemies < self.total_enemies:
            if self.remaining_enemies:
                enemy_class, image_path, speed = self.remaining_enemies.pop()
                x, y = self.get_spawn_position(game.screen_width, game.screen_height)
                game.enemies.append(enemy_class(x, y, image_path, speed, game))
                self.spawned_enemies += 1
                print(f"Spawned enemy {self.spawned_enemies}/{self.total_enemies} in wave.")
            else:
                break

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
