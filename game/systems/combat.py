def boj(Player, Monster) -> bool:
    """Funkce pro boj mezi hráčem a monstry. Vrací False, pokud hráč zemřel, jinak True."""
    print(f"Potkal jsi {Monster.name} připrav se na boj!")

    is_alive = True

    while is_alive:
        print(f"{Monster.name} má {Monster.hp} HP a ty máš {Player.hp} HP.")
        volba = int(input("Jakou akci chceš provést? 1 - Útok | 2 - Rozdejchat to "))
        if volba == 1:
            Monster.hp -= Player.dmg
            print(f"Útočíš na {Monster.name} a zraníš ho o {Player.dmg} HP!")
        elif volba == 2:
            print(f"Rozdejcháváš se a a doplňuješ síly na další útok!")
            Player.hp += 15
        else:
            print("Neplatná volba, promeškals.")

        print(f"{Monster.name} útočí na tebe a zraní tě o {Monster.dmg} HP!")
        Player.hp -= Monster.dmg

        if Player.hp <= 0:
            Player.hp = 0
            print("Bohužel jsi prohrál a zemřel.")
            is_alive = False
            return False
        elif Monster.hp <= 0:
            Monster.hp = 0
            print(f"Gratulace! Porazil jsi {Monster.name}!")
            is_alive = False
            Player.setdmg(5)
            return True
