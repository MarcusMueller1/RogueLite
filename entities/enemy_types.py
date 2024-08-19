# enemy_types.py
from entities.enemy import Enemy


class FastEnemy(Enemy):
    def __init__(self, x, y, image_path, speed, game):
        super().__init__(x, y, image_path, speed, game)
        self.health = 30
        self.damage = 15


class TankEnemy(Enemy):
    def __init__(self, x, y, image_path, speed, game):
        super().__init__(x, y, image_path, speed, game)
        self.health = 150
        self.damage = 20
