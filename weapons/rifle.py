from weapons.weapon import Weapon


class Rifle(Weapon):
    def __init__(self):
        super().__init__(name="Rifle", base_damage=8, fire_rate=300, projectile_speed=5, shape='square', color=(0, 255, 0))
