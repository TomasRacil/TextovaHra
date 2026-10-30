
import json


def save_game(player):
    with open("savegame.json", "w", encoding="utf-8") as file:
        json.dump(player, file, indent=4, ensure_ascii=False)


def load_game():
    try:
        with open("savegame.json", "r", encoding="utf-8") as file:
            player = json.load(file)

 
        if not isinstance(player, dict):
            print("Uložená hra má neplatný formát.")
            return None

        required_keys = ("name", "room_key", "inventory", "hp", "max_hp", "damage")

        if not all(key in player for key in required_keys):
            print("V uložené hře chybí potřebné údaje.")
            return None


        if not isinstance(player["name"], str) or not player["name"].strip():
            print("Neplatné jméno hráče.")
            return None

        if not isinstance(player["room_key"], str) or not player["room_key"].strip():
            print("Neplatná místnost v uložené hře.")
            return None


        if not isinstance(player["inventory"], list):
            print("Neplatný batoh v uložené hře.")
            return None

        if not isinstance(player["hp"], int) or isinstance(player["hp"], bool):
            print("Neplatný počet životů v uložené hře.")
            return None

 
        if not isinstance(player["max_hp"], int) or isinstance(player["max_hp"], bool):
            print("Neplatná maximální hodnota HP.")
            return None


        if player["max_hp"] <= 0:
            print("Maximální HP musí být větší než nula.")
            return None

        if player["hp"] < 0 or player["hp"] > player["max_hp"]:
            print("HP je mimo povolený rozsah.")
            return None

        if not isinstance(player["damage"], int) or isinstance(player["damage"], bool):
            print("Neplatná hodnota damage.")
            return None

        if player["damage"] < 0:
            print("Damage nemůže být záporný.")
            return None

        return player

    except FileNotFoundError:
        print("Nebyla nalezena žádná uložená hra.")
        return None

    except json.JSONDecodeError:
        print("Uložená hra je poškozená.")
        return None
