from items.item import Item

class ArmorUpgrade(Item):
    def apply_effect(self, player):
        player.armor += 10  # Increase player armor by 10
        print("Player armor increased by 10.")
