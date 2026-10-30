"""KONTRAKT: pohyb mezi místnostmi.

Přeskočené testy = zadání. Odstraňte @unittest.skip, až funkci doplníte.
Soubor vlastní tým "pohyb a mapa".
"""

from __future__ import annotations

import unittest

from game.cli import build_game


@unittest.skip("TODO: implementuj pohyb – odstraň skip, až bude hotovo")
class TestMovement(unittest.TestCase):
    def setUp(self) -> None:
        self.game = build_game()

    def test_move_to_neighbour_room(self) -> None:
        start = self.game.player.room_key
        room = self.game.world.room(start)
        direction, target = next(iter(room.exits.items()))

        self.game.handle(f"jdi {direction}")

        self.assertEqual(self.game.player.room_key, target)

    def test_move_back(self) -> None:
        room = self.game.room
        direction, target = next(iter(room.exits.items()))
        self.game.handle(f"jdi {direction}")

        back = self.game.world.room(target)
        opposite = next(d for d, k in back.exits.items() if k == room.key)
        self.game.handle(f"jdi {opposite}")

        self.assertEqual(self.game.player.room_key, room.key)

    def test_unknown_direction_is_refused(self) -> None:
        before = self.game.player.room_key
        output = self.game.handle("jdi nahoru")
        self.assertEqual(self.game.player.room_key, before)
        self.assertIn("nelze", output.lower())

    def test_look_after_move_shows_new_room(self) -> None:
        direction, target = next(iter(self.game.room.exits.items()))
        self.game.handle(f"jdi {direction}")
        output = self.game.handle("rozhledni")
        self.assertIn(self.game.world.room(target).name, output)


if __name__ == "__main__":
    unittest.main()
