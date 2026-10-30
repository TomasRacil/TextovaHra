from __future__ import annotations

import unittest

from game.cli import build_game

def test_rozhledni_vypise_spravny_text(self) -> None:
        vysledek = self.game.handle("rozhledni")
        
        self.assertIn("==", vysledek)
        self.assertIn("Východy:", vysledek)
        self.assertIn("Předměty:", vysledek)

if __name__ == "__main__":
    unittest.main()
