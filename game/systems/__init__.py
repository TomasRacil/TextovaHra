"""Systémy hry – složitější logika oddělená od příkazů.

Příkaz v game/commands/ má být tenký: přečte argument, zavolá systém,
vrátí text. Systém je třída, která se dá otestovat samostatně, bez hry.

Příklad:

    # game/systems/combat.py
    class Combat:
        def __init__(self, player, enemy):
            self.player = player
            self.enemy = enemy

        def attack(self) -> str:
            ...

    # game/commands/boj.py
    from ..registry import command
    from ..systems.combat import Combat

    @command("bojuj", "zaútočí na protivníka")
    def fight(game, argument: str) -> str:
        ...

Každý tým vlastní své soubory (viz ZADANI.md, kapitola 4).
"""
