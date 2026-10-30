"""Testy pro ukázkový příkaz `verze`.

Vzor pro studenty: test ověřuje chování (co hráč uvidí), ne implementaci.
"""

from __future__ import annotations

import unittest

from game import __version__
from game.cli import build_game
from game.registry import COMMANDS


class TestVersionCommand(unittest.TestCase):
    def setUp(self) -> None:
        self.game = build_game()

    def test_command_is_registered(self) -> None:
        self.assertIn("verze", COMMANDS)

    def test_version_is_in_output(self) -> None:
        output = self.game.handle("verze")
        self.assertIn(__version__, output)

    def test_command_needs_no_argument(self) -> None:
        self.assertEqual(self.game.handle("verze"), self.game.handle("verze cokoli"))


if __name__ == "__main__":
    unittest.main()
