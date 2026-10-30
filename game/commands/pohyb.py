from __future__ import annotations

from ..registry import command
from .basic import look_command  # Import pro automatické rozhlédnutí po vstupu do místnosti


@command("jdi", "posune hráče do zvoleného směru")
def jdi_command(game, argument: str) -> str:
    
    if not argument:
        return "Kam chceš jít? Zadej směr."
    

    if argument not in game.room.exits:
        return f"Tamtudy ('{argument}') se jít nedá."
    
    # Získání klíče nové místnosti a aktualizace pozice hráče
    game.player.room_key = game.room.exits[argument]
    
    # Vrátíme rovnou popis nové místnosti (využijeme existující příkaz 'rozhledni')
    return game.handle("rozhledni")