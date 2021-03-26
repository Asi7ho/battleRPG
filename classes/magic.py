import random


class Spell:
    def __init__(self, name, cost, damage, type):
        self.name = name
        self.cost = cost
        self.damage = damage
        self.type = type

    def generate_damage(self):
        damage_low = self.damage - 15
        damage_high = self.damage + 15
        return random.randrange(damage_low, damage_high)
