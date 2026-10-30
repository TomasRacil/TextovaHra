"""KONTRAKT: ukládání a načtení rozehrané hry.

Přeskočené testy = zadání. Odstraňte @unittest.skip, až funkci doplníte.
Soubor vlastní tým "ukládání a infrastruktura".
"""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from game.cli import build_game


@unittest.skip("TODO: implementuj ukládání – odstraň skip, až bude hotovo")
class TestSaveLoad(unittest.TestCase):
    def setUp(self) -> None:
        self.game = build_game()
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.save_path = Path(self.tmpdir.name) / "save.json"

    def test_save_creates_file(self) -> None:
        self.game.save(self.save_path)
        self.assertTrue(self.save_path.is_file())

    def test_save_is_valid_json(self) -> None:
        self.game.save(self.save_path)
        data = json.loads(self.save_path.read_text(encoding="utf-8"))
        self.assertIn("player", data)

    def test_load_restores_position(self) -> None:
        direction, target = next(iter(self.game.room.exits.items()))
        self.game.handle(f"jdi {direction}")
        self.game.save(self.save_path)

        loaded = build_game()
        loaded.load(self.save_path)
        self.assertEqual(loaded.player.room_key, target)

    def test_load_missing_file_raises(self) -> None:
        with self.assertRaises(FileNotFoundError):
            self.game.load(Path(self.tmpdir.name) / "neexistuje.json")


if __name__ == "__main__":
    unittest.main()
