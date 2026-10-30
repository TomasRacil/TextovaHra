import unittest
import json
import tempfile
from pathlib import Path

from game.core import Game, World, Room, Player, Item
from game.systems.save import save_game, load_game


class TestSaveSystem(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.filename = Path(self.temp_dir.name) / "savegame.json"

        world = World(
            rooms={
                "start": Room(key="start", name="Start"),
                "forest": Room(key="forest", name="Forest")
            },
            start_room="start"
        )

        self.game = Game(
            world=world,
            player=Player(
                name="Warrior",
                room_key="forest",
                inventory=[
                    Item("sword", "Ostrý meč."),
                    Item("potion", "Lektvar života.")
                ],
                hp=75,
                max_hp=100
            ),
            finished=False,
        )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_save_and_load(self):
        save_game(self.game, self.filename)

        self.game.player.name = "Changed"
        self.game.player.inventory = []
        self.game.player.hp = 10

        load_game(self.game, self.filename)

        self.assertEqual(self.game.player.name, "Warrior")
        self.assertEqual(self.game.player.room_key, "forest")
        self.assertEqual(self.game.player.hp, 75)
        self.assertEqual(self.game.player.max_hp, 100)
        self.assertEqual(len(self.game.player.inventory), 2)
        self.assertIsInstance(self.game.player.inventory[0], Item)
        self.assertEqual(
            self.game.player.inventory[0].description,
            "Ostrý meč."
        )

    def test_game_save_and_load(self):
        self.game.save(self.filename)

        self.game.player.hp = 10
        self.game.load(self.filename)

        self.assertEqual(self.game.player.hp, 75)

    def test_missing_file(self):
        with self.assertRaises(FileNotFoundError):
            load_game(self.game, self.filename)

    def test_corrupted_file(self):
        self.filename.write_text("Neplatny JSON", encoding="utf-8")

        with self.assertRaises(ValueError):
            load_game(self.game, self.filename)

    def test_missing_data(self):
        self.filename.write_text(
            json.dumps({"player": {}, "finished": False, "turn": 0}),
            encoding="utf-8"
        )

        with self.assertRaises(ValueError):
            load_game(self.game, self.filename)

    def test_invalid_inventory(self):
        data = {
            "player": {
                "name": "Warrior",
                "room_key": "forest",
                "inventory": "sword",
                "hp": 75,
                "max_hp": 100
            },
            "finished": False,
        }

        self.filename.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(ValueError):
            load_game(self.game, self.filename)

    def test_negative_hp(self):
        data = {
            "player": {
                "name": "Warrior",
                "room_key": "forest",
                "inventory": [],
                "hp": -10,
                "max_hp": 100
            },
            "finished": False,
        }

        self.filename.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(ValueError):
            load_game(self.game, self.filename)

    def test_hp_above_max(self):
        data = {
            "player": {
                "name": "Warrior",
                "room_key": "forest",
                "inventory": [],
                "hp": 150,
                "max_hp": 100
            },
            "finished": False,
        }

        self.filename.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(ValueError):
            load_game(self.game, self.filename)

    def test_invalid_room(self):
        data = {
            "player": {
                "name": "Warrior",
                "room_key": "unknown",
                "inventory": [],
                "hp": 75,
                "max_hp": 100
            },
            "finished": False,
        }

        self.filename.write_text(json.dumps(data), encoding="utf-8")

        with self.assertRaises(ValueError):
            load_game(self.game, self.filename)


if __name__ == "__main__":
    unittest.main(verbosity=2)