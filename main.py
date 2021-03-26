import random

from classes.game import Person, bcolors
from classes.magic import Spell
from classes.inventory import Item

###
# Create magic
###
# Create black magic
fire = Spell(name="Fire", cost=10, damage=100, type="black")
thunder = Spell(name="Thunder", cost=10, damage=100, type="black")
blizzard = Spell(name="Blizzard", cost=10, damage=100, type="black")
meteor = Spell(name="Meteor", cost=20, damage=200, type="black")
quake = Spell(name="Quake", cost=14, damage=140, type="black")

# Create white magic
cure = Spell(name="Cure", cost=12, damage=120, type="white")
cura = Spell(name="Cura", cost=18, damage=200, type="white")

###
# Create some item
###
potion = Item(name="Potion", type="potion", description="Heals 50 HP", prop=50)
hi_potion = Item(name="Hi-Potion", type="potion",
                 description="Heals 100 HP", prop=100)
super_potion = Item(name="Super Potion", type="potion",
                    description="Heals 500 HP", prop=500)
elixir = Item(name="Elixir", type="elixir",
              description="Fully restores HP and MP", prop=9999)
mega_elixir = Item(name="Mega Elixir", type="elixir",
                   description="Fully restores HP and MP for all party member", prop=9999)
grenade = Item(name="Grenade", type="attack",
               description="Deals 500 damages", prop=500)

###
# Instance Persons
###
# Players
player1 = Person(name="Valos", hp=460, mp=35, attack=80, defense=34,
                 magic=[fire, thunder, blizzard, cure, cura],
                 items=[{"item": potion, "quantity": 15},
                        {"item": hi_potion, "quantity": 5}])
player2 = Person(name="Nick ", hp=340, mp=85, attack=20, defense=34,
                 magic=[fire, thunder, blizzard, cure, cura],
                 items=[{"item": potion, "quantity": 15},
                        {"item": super_potion, "quantity": 3},
                        {"item": elixir, "quantity": 5}])
player3 = Person(name="Robot", hp=800, mp=65, attack=100, defense=34,
                 magic=[fire, thunder, blizzard, cure, cura],
                 items=[{"item": grenade, "quantity": 2}])

# Enemies
enemy1 = Person(name="Imp 1", hp=400, mp=35, attack=25, defense=15,
                magic=[], items=[])
enemy2 = Person(name="Magna ", hp=1200, mp=155, attack=105, defense=35,
                magic=[meteor, quake], items=[])
enemy3 = Person(name="Imp 2", hp=400, mp=35, attack=25, defense=15,
                magic=[], items=[])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

###
# Main loop
###
running = True

print(bcolors.FAIL + bcolors.BOLD + "AN ENEMY ATTACKS" + bcolors.ENDC)

while running:
    print("==============================")
    print("\n")
    print("NAME                  HP                                      MP")
    for player in players:
        player.get_stats()

    print("\n")
    for enemy in enemies:
        enemy.get_enemy_stats()

    for player in players:
        player.choose_action()
        choice = input("\nChose action: ")
        index = int(choice) - 1

        # Attack
        if index == 0:
            damage = player.generate_damage()
            enemy = player.choose_target(enemies)
            enemies[enemy].take_damage(damage)
            print("\nYou attacked " +
                  enemies[enemy].name + "for", damage, "points of damage.")
            enemies[enemy].get_enemy_stats()

            if enemies[enemy].get_hp() == 0:
                del(enemies[enemy])
        # Magic
        elif index == 1:
            player.choose_magic()
            magic_choice = int(input("\nChoose magic: ")) - 1

            if magic_choice == -1:
                continue

            spell = player.magic[magic_choice]

            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNot enough MP\n" + bcolors.ENDC)
                continue

            player.reduce_mp(spell.cost)
            magic_damage = spell.generate_damage()

            if spell.type == "white":
                player.heal(magic_damage)
                print(bcolors.OKGREEN + spell.name, "heals",
                      str(magic_damage), "HP." + bcolors.ENDC)
            elif spell.type == "black":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(magic_damage)
                print(bcolors.OKBLUE + spell.name, "deals",
                      str(magic_damage), "points of damage." + bcolors.ENDC)
                enemies[enemy].get_enemy_stats()

                if enemies[enemy].get_hp() == 0:
                    del(enemies[enemy])
        # Items
        elif index == 2:
            player.choose_item()
            item_choice = int(input("\nChoose item: ")) - 1

            if item_choice == -1:
                continue

            item = player.items[item_choice]["item"]

            if player.items[item_choice]["quantity"] == 0:
                print(bcolors.FAIL + "None left..." + bcolors.ENDC)
                continue

            player.items[item_choice]["quantity"] -= 1

            if item.type == "potion":
                player.heal(item.prop)
                print(bcolors.OKGREEN + item.name, "heals",
                      str(item.prop), "HP." + bcolors.ENDC)
            elif item.type == "elixir":
                if item.name == "Mega Elixir":
                    for p in players:
                        p.hp = p.max_hp
                        p.mp = p.max_mp
                        print(bcolors.OKGREEN + item.name,
                              "fully restored HP and MP for the entire team" + bcolors.ENDC)
                else:
                    player.hp = player.max_hp
                    player.mp = player.max_mp
                    print(bcolors.OKGREEN + item.name,
                          "fully restored HP and MP" + bcolors.ENDC)
            elif item.type == "attack":
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + item.name + " deals",
                      str(item.prop), "points of damage" + bcolors.ENDC)
                enemies[enemy].get_enemy_stats()

                if enemies[enemy].get_hp() == 0:
                    del(enemies[enemy])
        else:
            continue

        endGame = True
        for enemy in enemies:
            if enemy.get_hp() != 0:
                endGame = False

        if endGame:
            print(bcolors.OKGREEN + "You win!" + bcolors.ENDC)
            running = False
            break

    if running:
        for enemy in enemies:
            enemy_choice = random.randrange(0, 3)
            target = random.randrange(0, len(players))

            if enemy_choice == 1:
                if len(enemy.magic) == 0:
                    print(enemy.name + " does nothing")
                else:
                    spell = enemy.choose_enemy_spell()
                    magic_damage = spell.generate_damage()
                    players[target].take_damage(magic_damage)
                    print(bcolors.FAIL + spell.name, "deals",
                          str(magic_damage), "points of damage to " + players[target].name + "." + bcolors.ENDC)
            else:
                enemy_damage = enemy.generate_damage()
                players[target].take_damage(enemy_damage)
                print(enemy.name + " attacks " +
                      players[target].name + " for " + str(enemy_damage) + " damages")

            endGame = True
            for p in players:
                if p.get_hp() != 0:
                    endGame = False

            if endGame:
                print(bcolors.FAIL + "Your enemies have defeated you!" + bcolors.ENDC)
                running = False
                break
