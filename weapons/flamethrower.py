from weapons.weapon import Weapon
class Flamethrower(Weapon):
    def __init__(self):
        super().__init__(name="Flamethrower", base_damage=5, fire_rate=100, projectile_speed=5, shape='square', color=(255, 0, 255))
