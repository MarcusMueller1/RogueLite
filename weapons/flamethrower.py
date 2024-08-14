from weapons.weapon import Weapon


class Flamethrower(Weapon):
    def __init__(self):
        super().__init__(name="Flamethrower", base_damage=2, fire_rate=80, projectile_speed=4, shape='square', color=(255, 0, 255))
