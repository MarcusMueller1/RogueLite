from weapons.weapon import Weapon

class Shotgun(Weapon):
    def __init__(self):
        super().__init__(name="Shotgun", base_damage=25, fire_rate=1000, projectile_speed=10, shape='circle', color=(0, 0, 255))
