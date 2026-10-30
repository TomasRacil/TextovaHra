"""Základní příkazy: help, rozhledni, konec.

Tenhle soubor berte jako vzor. Je krátký, otestovaný a ukazuje, jak má
vypadat příkaz: dekorátor @command, návratový text místo print(), žádná
globální proměnná.
"""

from __future__ import annotations

from ..registry import COMMANDS, command


@command("help", "vypíše seznam dostupných příkazů")
def help_command(game, argument: str) -> str:
    lines = ["Dostupné příkazy:"]
    for name in sorted(COMMANDS):
        lines.append(f"  {name:<12} {COMMANDS[name].help}")
    lines.append("")
    lines.append("Napiš 'rozhledni' pro popis místnosti.")
    return "\n".join(lines)


@command("rozhledni", "popíše místnost, východy a předměty")
def look_command(game, argument: str) -> str:
    room = game.room
    lines = [f"== {room.name} =="]
    if room.description:
        lines.append(room.description)
    if room.exits:
        lines.append("Východy: " + ", ".join(sorted(room.exits)))
    else:
        lines.append("Odsud se nedá nikam jít.")
    if room.items:
        lines.append("Předměty: " + ", ".join(item.name for item in room.items))
    return "\n".join(lines)


@command("konec", "ukončí hru")
@command("quit", "ukončí hru (anglicky)")
def quit_command(game, argument: str) -> str:
    game.finished = True
    return "Hra ukončena. Na shledanou!"
