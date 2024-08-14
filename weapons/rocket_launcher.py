from weapons.weapon import Weapon

class RocketLauncher(Weapon):
    def __init__(self):
        super().__init__(name="Rocket Launcher", base_damage=50, fire_rate=3000, projectile_speed=8, shape='circle', color=(255, 165, 0))
