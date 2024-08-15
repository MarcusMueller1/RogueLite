from weapons.weapon import Weapon

class Pistol(Weapon):
    def __init__(self):
        super().__init__(name="Pistol", base_damage=15, fire_rate=500, projectile_speed=5, shape='circle', color=(255, 0, 0))
