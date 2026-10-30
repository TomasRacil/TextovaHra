import json
from pathlib import Path

from game.core import Item


def save_game(game, path):


    data = {
        "player": {
            "name": game.player.name,
            "room_key": game.player.room_key,
            "inventory": [
                {
                    "name": item.name,
                    "description": item.description
                }
                for item in game.player.inventory
            ],
            "hp": game.player.hp,
            "max_hp": game.player.max_hp
        },
        "finished": game.finished,
    }

    with Path(path).open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_game(game, path):


    try:
        with Path(path).open("r", encoding="utf-8") as file:
            data = json.load(file)

    except json.JSONDecodeError as error:
        raise ValueError("Uložená hra obsahuje neplatný JSON.") from error

    if not isinstance(data, dict):
        raise ValueError("Uložená hra má neplatný formát.")

    if not all(key in data for key in ("player", "finished")):
        raise ValueError("V uložené hře chybí potřebné údaje.")

    player = data["player"]

    if not isinstance(player, dict):
        raise ValueError("Neplatná data hráče.")

    required_keys = ("name", "room_key", "inventory", "hp", "max_hp")

    if not all(key in player for key in required_keys):
        raise ValueError("V uloženém hráči chybí potřebné údaje.")

    if not isinstance(player["name"], str) or not player["name"].strip():
        raise ValueError("Neplatné jméno hráče.")

    if not isinstance(player["room_key"], str):
        raise ValueError("Neplatná místnost hráče.")

    if player["room_key"] not in game.world.rooms:
        raise ValueError("Uložená místnost ve světě neexistuje.")

    if not isinstance(player["inventory"], list):
        raise ValueError("Neplatný inventář.")

    if not isinstance(player["hp"], int) or isinstance(player["hp"], bool):
        raise ValueError("Neplatné HP.")

    if not isinstance(player["max_hp"], int) or isinstance(player["max_hp"], bool):
        raise ValueError("Neplatné maximální HP.")

    if player["max_hp"] <= 0:
        raise ValueError("Maximální HP musí být větší než nula.")

    if not 0 <= player["hp"] <= player["max_hp"]:
        raise ValueError("HP je mimo povolený rozsah.")

    if not isinstance(data["finished"], bool):
        raise ValueError("Neplatný stav dokončení hry.")


    inventory = []

    for item_data in player["inventory"]:
        if not isinstance(item_data, dict):
            raise ValueError("Neplatný předmět v inventáři.")

        if not isinstance(item_data.get("name"), str):
            raise ValueError("Předmět nemá platný název.")

        description = item_data.get("description", "")

        if not isinstance(description, str):
            raise ValueError("Neplatný popis předmětu.")

        inventory.append(
            Item(
                name=item_data["name"],
                description=description
            )
        )

    # Data jsou ověřena, můžeme obnovit stav hry.
    game.player.name = player["name"]
    game.player.room_key = player["room_key"]
    game.player.inventory = inventory
    game.player.hp = player["hp"]
    game.player.max_hp = player["max_hp"]
    game.finished = data["finished"]
    game.turn = data["turn"]