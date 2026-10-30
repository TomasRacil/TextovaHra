
import unittest
import json
import os

from save_system import save_game, load_game


class TestSaveSystem(unittest.TestCase):

    def setUp(self):
        self.filename = "savegame.json"

        self.player = {
            "name": "Warrior",
            "room_key": "forest",
            "inventory": ["sword", "potion"],
            "hp": 75,
            "max_hp": 100,
            "damage": 20
        }

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    # Test uložení a načtení hry
    def test_save_and_load(self):
        save_game(self.player)

        loaded_player = load_game()

        self.assertEqual(loaded_player, self.player)

    # Test neexistujícího souboru
    def test_missing_file(self):
        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test poškozeného JSON
    def test_corrupted_file(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            file.write("Toto neni platny JSON")

        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test chybějících údajů
    def test_missing_data(self):
        player = {
            "name": "Warrior",
            "room_key": "forest",
            "inventory": ["sword"],
            "hp": 75,
            "max_hp": 100
        }

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(player, file)

        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test nesprávného datového typu
    def test_invalid_data_types(self):
        player = self.player.copy()
        player["inventory"] = "sword"

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(player, file)

        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test záporného HP
    def test_negative_hp(self):
        player = self.player.copy()
        player["hp"] = -10

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(player, file)

        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test HP vyššího než max_hp
    def test_hp_above_max(self):
        player = self.player.copy()
        player["hp"] = 150

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(player, file)

        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test nulového nebo záporného max_hp
    def test_invalid_max_hp(self):
        player = self.player.copy()
        player["max_hp"] = 0

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(player, file)

        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test záporného damage
    def test_negative_damage(self):
        player = self.player.copy()
        player["damage"] = -5

        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump(player, file)

        loaded_player = load_game()

        self.assertIsNone(loaded_player)

    # Test správného damage
    def test_valid_damage(self):
        save_game(self.player)

        loaded_player = load_game()

        self.assertEqual(loaded_player["damage"], 20)


if __name__ == "__main__":
    unittest.main(verbosity=2)
