from items.item import Item

class SpeedBoost(Item):
    def apply_effect(self, player):
        player.speed += 2  # Increase player speed by 2
        print("Player speed increased by 2.")
