from weapons.weapon import Weapon

class Sniper(Weapon):
    def __init__(self):
        super().__init__(name="Sniper", base_damage=40, fire_rate=1800, projectile_speed=10, shape='square', color=(255, 255, 0))
