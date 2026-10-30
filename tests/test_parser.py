"""KONTRAKT: parser příkazů a nápověda.

Tyto testy jsou zatím PŘESKOČENÉ (@unittest.skip). To je záměr: jsou to
zadání v podobě testu. Až funkci naprogramujete, odstraňte skip a test
musí projít. Tím máte důkaz, že práce je hotová.

Tento soubor vlastní tým, který dělá parser (rozpoznávání příkazů,
zkratky, práci s diakritikou a velikostí písmen). Ostatní ho neupravují.
"""

from __future__ import annotations

import unittest

from game.cli import build_game


@unittest.skip("TODO: implementuj parser – odstraň skip, až bude hotovo")
class TestParser(unittest.TestCase):
    def setUp(self) -> None:
        self.game = build_game()

    def test_verb_is_case_insensitive(self) -> None:
        self.assertEqual(self.game.handle("ROZHLEDNI"), self.game.handle("rozhledni"))

    def test_whitespace_is_ignored(self) -> None:
        self.assertEqual(self.game.handle("  rozhledni  "), self.game.handle("rozhledni"))

    def test_rozhledni_vypise_spravny_text(self) -> None:
        vysledek = self.game.handle("rozhledni")
        
        self.assertIn("==", vysledek)
        self.assertIn("Východy:", vysledek)
        self.assertIn("Předměty:", vysledek)

    def test_argument_is_passed_to_command(self) -> None:
        # Příkaz 'jdi sever' musí dostat argument 'sever'.
        output = self.game.handle("jdi sever")
        self.assertNotIn("Neznámý příkaz", output)

    def test_alias_works(self) -> None:
        # Např. 'jdi' a 'j' musí dělat totéž.
        self.assertEqual(self.game.handle("jdi sever"), self.game.handle("j sever"))


if __name__ == "__main__":
    unittest.main()
