"""Základní testy šablony – tyhle MUSÍ procházet pořád.

Když jeden z nich spadne, rozbili jste kostru hry, ne svoji funkci.
Spuštění:

    python -m unittest discover -s tests -v
"""

from __future__ import annotations

import unittest

from game.cli import DATA_FILE, build_game
from game.engine import Item, Room, World
from game.registry import COMMANDS


class TestSkeleton(unittest.TestCase):
    """Ověřuje, že šablona drží pohromadě."""

    def setUp(self) -> None:
        self.game = build_game()

    def test_world_loads(self) -> None:
        self.assertGreaterEqual(len(self.game.world.rooms), 3)

    def test_start_room_exists(self) -> None:
        self.assertIn(self.game.world.start_room, self.game.world.rooms)

    def test_player_starts_in_start_room(self) -> None:
        self.assertEqual(self.game.player.room_key, self.game.world.start_room)

    def test_all_exits_point_to_existing_rooms(self) -> None:
        for key, room in self.game.world.rooms.items():
            for direction, target in room.exits.items():
                with self.subTest(room=key, direction=direction):
                    self.assertIn(
                        target,
                        self.game.world.rooms,
                        f"Místnost '{key}' vede na neexistující '{target}'",
                    )

    def test_data_file_exists(self) -> None:
        self.assertTrue(DATA_FILE.is_file(), f"Chybí {DATA_FILE}")

    def test_commands_registered(self) -> None:
        for name in ("help", "rozhledni", "konec"):
            self.assertIn(name, COMMANDS)

    def test_help_lists_commands(self) -> None:
        output = self.game.handle("help")
        self.assertIn("help", output)
        self.assertIn("rozhledni", output)

    def test_unknown_command_is_polite(self) -> None:
        output = self.game.handle("tancuj")
        self.assertIn("Neznámý příkaz", output)

    def test_empty_line_returns_nothing(self) -> None:
        self.assertEqual(self.game.handle("   "), "")

    def test_look_describes_current_room(self) -> None:
        output = self.game.handle("rozhledni")
        self.assertIn(self.game.room.name, output)

    def test_quit_finishes_game(self) -> None:
        self.game.handle("konec")
        self.assertTrue(self.game.finished)

    def test_unimplemented_command_does_not_crash(self) -> None:
        # Příkaz, který ještě není hotový, nesmí shodit celou hru.
        # Test si registruje vlastní dočasný příkaz, takže nezávisí na tom,
        # co už je v engine.py implementované.
        from game.registry import COMMANDS, command

        @command("__test_nehotovo", "dočasný testovací příkaz")
        def _boom(game, argument: str) -> str:
            raise NotImplementedError("test")

        try:
            output = self.game.handle("__test_nehotovo")
        finally:
            COMMANDS.pop("__test_nehotovo", None)

        self.assertIn("není hotový", output)


class TestModel(unittest.TestCase):
    """Datové třídy – po doplnění logiky sem přidejte další testy."""

    def test_room_str(self) -> None:
        room = Room(key="a", name="Síň")
        self.assertEqual(str(room), "Síň")

    def test_item_str(self) -> None:
        item = Item(name="klíč")
        self.assertEqual(str(item), "klíč")

    def test_world_from_json(self) -> None:
        world = World.from_json(DATA_FILE)
        self.assertTrue(world.rooms)
        first = next(iter(world.rooms.values()))
        self.assertIsInstance(first, Room)


if __name__ == "__main__":
    unittest.main()
