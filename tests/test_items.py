"""KONTRAKT: předměty, batoh a jejich použití.

Přeskočené testy = zadání. Odstraňte @unittest.skip, až funkci doplníte.
Soubor vlastní tým "předměty a inventář".
"""

from __future__ import annotations

import unittest

from game.cli import build_game
from game.engine import Item, Player


@unittest.skip("TODO: implementuj předměty – odstraň skip, až bude hotovo")
class TestItems(unittest.TestCase):
    def setUp(self) -> None:
        self.game = build_game()

    def test_take_item_from_room(self) -> None:
        room = self.game.room
        item = room.items[0]

        self.game.handle(f"vezmi {item.name}")

        self.assertIn(item.name, [i.name for i in self.game.player.inventory])
        self.assertNotIn(item.name, [i.name for i in room.items])

    def test_take_missing_item(self) -> None:
        output = self.game.handle("vezmi drak")
        self.assertIn("není", output.lower())

    def test_drop_item_returns_it_to_room(self) -> None:
        room = self.game.room
        item = room.items[0]
        self.game.handle(f"vezmi {item.name}")
        self.game.handle(f"polož {item.name}")

        self.assertNotIn(item.name, [i.name for i in self.game.player.inventory])
        self.assertIn(item.name, [i.name for i in room.items])

    def test_inventory_command_lists_items(self) -> None:
        room = self.game.room
        item = room.items[0]
        self.game.handle(f"vezmi {item.name}")
        output = self.game.handle("batoh")
        self.assertIn(item.name, output)


class TestPlayerModel(unittest.TestCase):
    """Čisté unit testy modelu – bez hry, jen třída Player."""

    @unittest.skip("TODO: implementuj Player – odstraň skip, až bude hotovo")
    def test_damage_reduces_hp(self) -> None:
        player = Player()
        player.damage(30)
        self.assertEqual(player.hp, 70)

    @unittest.skip("TODO: implementuj Player – odstraň skip, až bude hotovo")
    def test_hp_never_below_zero(self) -> None:
        player = Player()
        player.damage(999)
        self.assertEqual(player.hp, 0)
        self.assertFalse(player.is_alive())

    @unittest.skip("TODO: implementuj Player – odstraň skip, až bude hotovo")
    def test_heal_never_above_max(self) -> None:
        player = Player(hp=90, max_hp=100)
        player.heal(50)
        self.assertEqual(player.hp, 100)

    @unittest.skip("TODO: implementuj Player – odstraň skip, až bude hotovo")
    def test_inventory_is_not_shared_between_players(self) -> None:
        # Klasická chyba: mutable default argument.
        a, b = Player(), Player()
        a.inventory.append(Item(name="klíč"))
        self.assertEqual(b.inventory, [])


if __name__ == "__main__":
    unittest.main()
