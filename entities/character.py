
class Character:
    def __init__(self, name, health, armor, speed, damage, attack_speed, radius, starting_weapon):
        self.name = name
        self.health = health
        self.armor = armor
        self.speed = speed
        self.damage = damage
        self.attack_speed = attack_speed
        self.radius = radius
        self.starting_weapon = starting_weapon

    def apply_to_player(self, player):
        player.health = self.health
        player.max_health = self.health
        player.armor = self.armor
        player.speed = self.speed

    def apply_to_weapon(self, weapon):
        weapon.damage *= self.damage
        weapon.fire_rate /= self.attack_speed
        if hasattr(weapon, 'radius'):
            weapon.radius *= self.radius
        if hasattr(weapon, 'projectile_speed'):
            weapon.projectile_speed *= self.speed

    def __str__(self):
        return (f"{self.name}: Health={self.health}, Armor={self.armor}, Speed={self.speed}, "
                f"Damage={self.damage}, Attack Speed={self.attack_speed}, Radius={self.radius}, "
                f"Starting Weapon={self.starting_weapon.name}")
