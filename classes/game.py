import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, attack, defense, magic, items):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.max_mp = mp
        self.mp = mp
        self.attack_high = attack + 10
        self.attack_low = attack - 10
        self.defense = defense
        self.magic = magic
        self.items = items
        self.actions = ["Attack", "Magic", "Items"]

    def generate_damage(self):
        return random.randrange(self.attack_low, self.attack_high)

    def heal(self, hp):
        self.hp += hp

        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp < 0:
            self.hp = 0

        return self.hp

    def reduce_mp(self, cost):
        self.mp -= cost

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.max_hp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.max_mp

    def choose_action(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD +
              "ACTIONS (" + self.name + "): " + bcolors.ENDC)
        for action in self.actions:
            print("    " + str(i) + ": ", action)
            i += 1

    def choose_magic(self):
        i = 1
        print("\n" + bcolors.OKBLUE + bcolors.BOLD + "MAGIC: " + bcolors.ENDC)
        for spell in self.magic:
            print("    " + str(i) + ": ", spell.name,
                  "(cost: " + str(spell.cost) + ")")
            i += 1

    def choose_item(self):
        i = 1
        print("\n" + bcolors.OKGREEN + bcolors.BOLD + "ITEMS: " + bcolors.ENDC)
        for item in self.items:
            print("    " + str(i) + ":", item["item"].name,
                  "-", str(item["item"].description), "(x" + str(item["quantity"]) + ")")
            i += 1

    def choose_target(self, enemies):
        i = 1
        print("\n" + bcolors.FAIL + bcolors.BOLD + "TARGETS: " + bcolors.ENDC)
        for enemy in enemies:
            if enemy.get_hp() != 0:
                print("    " + str(i) + ":", enemy.name)
                i += 1

        choice = int(input("\nChoose target: ")) - 1
        return choice

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        if spell.cost > self.get_mp():
            self.choose_enemy_spell()
        else:
            return spell

    def get_stats(self):
        bar_hp = ""
        bar_ticks_hp = (self.hp / self.max_hp) * 24

        bar_mp = ""
        bar_ticks_mp = (self.mp / self.max_mp) * 10

        while bar_ticks_hp > 0:
            bar_hp += "█"
            bar_ticks_hp -= 1

        while len(bar_hp) < 24:
            bar_hp += " "

        while bar_ticks_mp > 0:
            bar_mp += "█"
            bar_ticks_mp -= 1

        while len(bar_mp) < 10:
            bar_mp += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""

        if len(hp_string) < 2 * len(str(self.max_hp)) + 1:
            decreased = 2 * len(str(self.max_hp)) + 1 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string

        mp_string = str(self.mp) + "/" + str(self.max_mp)
        current_mp = ""

        if len(mp_string) < 2 * len(str(self.max_mp)) + 1:
            decreased = 2 * len(str(self.max_mp)) + 1 - len(mp_string)
            while decreased > 0:
                current_mp += " "
                decreased -= 1
            current_mp += mp_string
        else:
            current_mp = mp_string

        print(bcolors.BOLD + self.name + "        " + current_hp + " |" + bcolors.OKGREEN +
              bar_hp + bcolors.ENDC + bcolors.BOLD + "|        " + current_mp + " |" + bcolors.OKBLUE + bar_mp + bcolors.ENDC + "|" + "\n")

    def get_enemy_stats(self):
        bar_hp = ""
        bar_ticks_hp = (self.hp / self.max_hp) * 50

        while bar_ticks_hp > 0:
            bar_hp += "█"
            bar_ticks_hp -= 1

        while len(bar_hp) < 50:
            bar_hp += " "

        hp_string = str(self.hp) + "/" + str(self.max_hp)
        current_hp = ""

        if len(hp_string) < 2 * len(str(self.max_hp)) + 1:
            decreased = 2 * len(str(self.max_hp)) + 1 - len(hp_string)
            while decreased > 0:
                current_hp += " "
                decreased -= 1
            current_hp += hp_string
        else:
            current_hp = hp_string

        print(bcolors.BOLD + self.name + "        " + current_hp + " |" + bcolors.FAIL +
              bar_hp + bcolors.ENDC + bcolors.BOLD + "|" + bcolors.ENDC + "\n")
