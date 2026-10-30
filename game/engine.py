"""Jádro hry: svět, místnosti, postavy, předměty a samotná hra.

Tady je HOTOVÁ JEN KOSTRA. Třídy mají atributy (datové položky) a prázdné
metody, které vyhazují NotImplementedError. Logiku doplňují studenti –
nejlépe v nových modulech, ne úpravou tohoto souboru (viz ZADANI.md,
kapitola "Vlastnictví souborů").

Co v tomto souboru hotové je:
  * datové třídy Item, Room, Player, World (atributy + __str__),
  * načtení světa z JSON (World.from_json) – jde o "instalatérství",
  * Game.handle() – rozparsuje řádek a zavolá příkaz z registru.

Co hotové není (a je na vás):
  * pohyb hráče, předměty, souboj, ukládání hry, dialogy, podmínky výhry.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Item:
    """Předmět, který může ležet v místnosti nebo v batohu."""

    name: str
    description: str = ""
    # TODO: další atributy podle vaší hry (váha, účinek, přenosnost, ...)

    def __str__(self) -> str:
        return self.name


@dataclass
class Room:
    """Místnost, po které se hráč pohybuje."""

    key: str
    name: str
    description: str = ""
    exits: dict[str, str] = field(default_factory=dict)  # směr -> klíč místnosti
    items: list[Item] = field(default_factory=list)

    def __str__(self) -> str:
        return self.name

    def add_item(self, item: Item) -> None:
        """Položí předmět do místnosti."""
        raise NotImplementedError("Room.add_item")

    def remove_item(self, name: str) -> Item | None:
        """Odebere předmět podle jména; None = v místnosti není."""
        raise NotImplementedError("Room.remove_item")


@dataclass
class Player:
    """Hráč – jeho stav, batoh a poloha."""

    name: str = "Hráč"
    room_key: str = "start"
    inventory: list[Item] = field(default_factory=list)
    hp: int = 100
    max_hp: int = 100

    def is_alive(self) -> bool:

        if not isinstance(self.hp, int):
            raise NotImplementedError()
            return False
        if(self.hp>0):
            
            return True
        else: 
            
            return False

    def take(self, item: Item) -> None:
        """Přesune předmět do batohu."""
        raise NotImplementedError("Player.take")

    def drop(self, name: str) -> Item | None:
        """Vyndá předmět z batohu podle jména; None = nemá ho."""
        raise NotImplementedError("Player.drop")

    def damage(self, amount: int) -> None:
        if amount<0:
            amount = 0
        self.hp -=amount
        if self.hp<0:
            self.hp = 0
        
        """Ubere zdraví (ne pod nulu)."""
        

    def heal(self, amount: int) -> None:
        """Přidá zdraví (maximálně do max_hp)."""
        raise NotImplementedError("Player.heal")


@dataclass
class World:
    """Mapa hry – slovník místností a informace, kde hráč začíná."""

    rooms: dict[str, Room] = field(default_factory=dict)
    start_room: str = "start"

    def room(self, key: str) -> Room:
        """Vrátí místnost podle klíče. KeyError = taková místnost neexistuje."""
        return self.rooms[key]

    @classmethod
    def from_json(cls, path: str | Path) -> "World":
        """Načte svět z JSON souboru (viz game/data/world.json)."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        rooms: dict[str, Room] = {}
        for key, raw in data.get("rooms", {}).items():
            rooms[key] = Room(
                key=key,
                name=raw.get("name", key),
                description=raw.get("description", ""),
                exits=dict(raw.get("exits", {})),
                items=[
                    Item(name=item["name"], description=item.get("description", ""))
                    for item in raw.get("items", [])
                ],
            )
        return cls(rooms=rooms, start_room=data.get("start_room", "start"))


@dataclass
class Game:
    """Stav jednoho rozehraného příběhu."""

    world: World
    player: Player = field(default_factory=Player)
    finished: bool = False
    turn: int = 0

    def __post_init__(self) -> None:
        # Hráč začíná tam, kde to říká svět.
        self.player.room_key = self.world.start_room

    @property
    def room(self) -> Room:
        """Místnost, ve které hráč právě je."""
        return self.world.room(self.player.room_key)

    def handle(self, line: str) -> str:
        """Zpracuje jeden řádek od hráče a vrátí text odpovědi.

        Tohle je jediné "spojení" mezi vstupem a příkazy – hotové.
        Neznámý příkaz nespadne, jen slušně odmítne.
        """
        from .registry import COMMANDS

        line = line.strip()
        if not line:
            return ""

        verb, _, rest = line.partition(" ")
        verb = verb.lower()
        argument = rest.strip()

        cmd = COMMANDS.get(verb)
        if cmd is None:
            return f"Neznámý příkaz: '{verb}'. Napiš 'help' pro seznam příkazů."

        self.turn += 1
        try:
            return cmd.handler(self, argument)
        except NotImplementedError as exc:
            # Rozepsaná funkce nemá shodit celou hru.
            return f"Příkaz '{verb}' ještě není hotový ({exc})."
