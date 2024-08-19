# enemy_types.py
from entities.enemy import Enemy


class FastEnemy(Enemy):
    def __init__(self, x, y, image_path, speed, game):
        super().__init__(x, y, image_path, speed, game)
        self.health = 15
        self.damage = 15


class TankEnemy(Enemy):
    def __init__(self, x, y, image_path, speed, game):
        super().__init__(x, y, image_path, speed, game)
        self.health = 10
        self.damage = 20
