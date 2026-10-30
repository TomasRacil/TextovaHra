"""Příkaz `verze` – ukázkový PR pro výuku.

Slouží k předvedení celého cyklu: issue → větev → změna → test → PR → review → merge.
Je záměrně malý (jeden soubor + jeden test), aby bylo na projektoru vidět,
že PR má dělat jednu věc.
"""

from __future__ import annotations

from .. import __version__
from ..registry import command


@command("verze", "vypíše verzi hry")
def version_command(game, argument: str) -> str:
    """Vrátí název hry a aktuální verzi."""
    return f"Textová hra, verze {__version__}"
