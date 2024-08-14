from weapons.weapon import Weapon

class Sniper(Weapon):
    def __init__(self):
        super().__init__(name="Sniper", base_damage=25, fire_rate=2000, projectile_speed=30, shape='square', color=(255, 255, 0))
