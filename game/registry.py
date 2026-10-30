"""Registr příkazů – srdce rozšiřitelnosti hry.

Každý příkaz je funkce ozdobená dekorátorem @command. Funkce dostane
instanci hry a zbytek řádku za příkazem, vrátí text pro hráče.

Díky registru platí: kdo chce přidat příkaz, založí NOVÝ soubor
v game/commands/ a nesahá do cizího kódu. Tím se vyhnete konfliktům
ve společných souborech.

Postup pro nový příkaz:

    # game/commands/mluv.py
    from ..registry import command

    @command("mluv", "promluví s postavou v místnosti")
    def mluv(game, argument):
        if not argument:
            return "S kým chceš mluvit?"
        return f"Zkusíš promluvit s: {argument}"
"""

from __future__ import annotations

import importlib
import pkgutil
from dataclasses import dataclass
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:  # jen pro typovou nápovědu, ne kvůli importu za běhu
    from .engine import Game


@dataclass(frozen=True)
class Command:
    """Jeden příkaz hry."""

    name: str
    help: str
    handler: Callable[["Game", str], str]


#: Všechny zaregistrované příkazy: název -> Command
COMMANDS: dict[str, Command] = {}


def command(name: str, help: str = "") -> Callable[[Callable], Callable]:
    """Zaregistruje funkci jako příkaz hry pod daným jménem."""

    def decorator(func: Callable[["Game", str], str]) -> Callable[["Game", str], str]:
        COMMANDS[name.lower()] = Command(name=name.lower(), help=help, handler=func)
        return func

    return decorator


def load_commands() -> None:
    """Naimportuje všechny moduly v game/commands/, čímž se příkazy zaregistrují.

    Volá se jednou při startu hry (viz game/cli.py) a v testech.
    """
    from . import commands as package

    for module in pkgutil.iter_modules(package.__path__):
        if module.name.startswith("_"):
            continue
        importlib.import_module(f"{package.__name__}.{module.name}")
