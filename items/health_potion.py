from items.item import Item

class HealthPotion(Item):
    def apply_effect(self, player):
        player.health = min(player.max_health, player.health + 20)  # Heal the player by 20 points
        print("Player healed by 20 health points.")
