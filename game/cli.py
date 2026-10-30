"""Konzolové rozhraní hry – načtení světa, smyčka vstupů, výpis odpovědí.

Tento soubor je hotový a obvykle ho není potřeba měnit. Pokud potřebuješ
jiné uvítání nebo jiný vstup (např. načtení uložené hry), domluv se
s projekt leadem – je to sdílený soubor, tedy místo možných konfliktů.
"""

from __future__ import annotations

import sys
from pathlib import Path

from .engine import Game, World
from .registry import load_commands

DATA_FILE = Path(__file__).parent / "data" / "world.json"


def build_game(data_file: Path = DATA_FILE) -> Game:
    """Připraví hru: zaregistruje příkazy a načte svět."""
    load_commands()
    return Game(world=World.from_json(data_file))


def main(argv: list[str] | None = None) -> int:
    game = build_game()

    print("=" * 60)
    print("TEXTOVÁ HRA")
    print("=" * 60)
    print("Napiš 'help' pro seznam příkazů, 'konec' pro ukončení.\n")
    print(game.handle("rozhledni"))
    print()

    while not game.finished:
        try:
            line = input("> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break

        output = game.handle(line)
        if output:
            print(output)

    print("\nDěkujeme za hraní.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
