# Koncepty použité v šabloně

Tohle je čtení pro chvíli, kdy v kódu narazíš na něco, co jsi ještě neviděl.
Není to učebnice Pythonu – je to vysvětlení **těch konkrétních věcí, které v této šabloně
opravdu jsou**, s odkazem na místo v projektu.

Pořadí odpovídá tomu, jak na ně narazíš při čtení `game/engine.py` shora dolů.

---

## 1. Modul, balíček a `python -m game`

**Modul** = jeden soubor `.py`. **Balíček** = složka s `__init__.py`, tedy skupina modulů.

```
game/                 ← balíček
├── __init__.py       ← označuje složku za balíček (může být prázdný)
├── engine.py         ← modul game.engine
└── commands/
    ├── __init__.py   ← balíček game.commands
    └── basic.py      ← modul game.commands.basic
```

Import z jiného modulu ve stejném balíčku se píše **relativně** – tečka znamená „odtud“:

```python
from ..registry import command      # .. = o úroveň výš (game/), pak registry
from .engine import Game            # .  = tady v této složce
```

`python -m game` znamená „spusť balíček `game` jako program“. Python hledá `game/__main__.py`
a spustí ho. Proto existuje soubor `game/__main__.py` – je to vstupní bod.

> **Kde to uvidíš:** `game/__main__.py`, `game/commands/__init__.py`, importy v `registry.py`.

---

## 2. Třída, instance, `self`

Třída je předpis, instance je konkrétní objekt vytvořený podle předpisu.

```python
class Player:
    def __init__(self, name: str = "Hráč"):
        self.name = name        # atribut instance

hráč = Player("Tomáš")           # instance
print(hráč.name)                 # Tomáš
```

`self` je **odkaz na konkrétní instanci**. Díky němu ví metoda, se kterou instancí pracuje.
`__init__` se zavolá automaticky při vytvoření (`Player("Tomáš")`).

**Atribut** = data (`self.hp`). **Metoda** = funkce, která s nimi pracuje (`player.damage(10)`).

> **Kde to uvidíš:** `Item`, `Room`, `Player`, `World`, `Game` v `engine.py`.

---

## 3. `@dataclass` – co to je a proč to tam je

`@dataclass` je **dekorátor z knihovny `dataclasses`**, který za tebe vygeneruje „ukecaný“ kód
pro třídu, která hlavně drží data.

```python
from dataclasses import dataclass

@dataclass
class Item:
    name: str
    description: str = ""
```

Tohle je **funkčně stejné** jako:

```python
class Item:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

    def __repr__(self) -> str:
        return f"Item(name={self.name!r}, description={self.description!r})"

    def __eq__(self, other) -> bool:
        return (self.name, self.description) == (other.name, other.description)
```

`@dataclass` ti tedy ušetří tři věci:

| Co vygeneruje | K čemu je |
|---|---|
| `__init__` | nemusíš psát `def __init__(self, ...)` a přiřazování |
| `__repr__` | `print(item)` vypíše `Item(name='klíč', ...)` – skvělé na ladění |
| `__eq__` | `item_a == item_b` porovná hodnoty, ne identitu objektů |

**Důležité:** `@dataclass` je jen zkratka pro data. Metody si do třídy normálně přidáváš sám:

```python
@dataclass
class Item:
    name: str
    description: str = ""

    def __str__(self) -> str:      # vlastní metoda – dataclass ji nechá být
        return self.name
```

**Kdy `@dataclass` použít:** třída je hlavně „taška na data“ (předmět, místnost, uložená hra).
**Kdy ne:** třída má složitou logiku a stav se mění mnoha způsoby – pak je čitelnější
obyčejná třída s `__init__`.

> **Kde to uvidíš:** `Item`, `Room`, `Player`, `World`, `Game` v `engine.py`.

---

## 4. `field(default_factory=list)` – past s mutable argumentem

Tohle je nejčastější chyba začátečníků v Pythonu:

```python
class Player:
    def __init__(self, items=[]):    # ŠPATNĚ
        self.items = items
```

Výchozí hodnota `[]` se vytvoří **jednou** při definici funkce. Všechny instance pak sdílí
jeden a ten samý seznam:

```python
a, b = Player(), Player()
a.items.append("klíč")
print(b.items)      # ['klíč']  ← b má cizí věc!
```

`dataclasses` to neumožní a rovnou tě donutí použít `default_factory` – funkci, která se
zavolá **pro každou instanci zvlášť**:

```python
from dataclasses import dataclass, field

@dataclass
class Player:
    inventory: list[Item] = field(default_factory=list)   # SPRÁVNĚ
```

> **Kde to uvidíš:** `Room.items`, `Player.inventory`, `World.rooms`, `Game.player`.
> **Test, který to hlídá:** `tests/test_items.py::test_inventory_is_not_shared_between_players`.

---

## 5. Typové anotace

```python
def move(game: "Game", direction: str) -> str:
    ...
```

`direction: str` říká „čekám řetězec“, `-> str` říká „vrátím řetězec“.
**Python to nekontroluje za běhu** – je to dokumentace pro lidi a pro editory (VS Code ti
podle toho napovídá a zvýrazní chybu dřív, než program spustíš).

Zápisy, které v šabloně potkáš:

| Zápis | Význam |
|---|---|
| `str`, `int`, `bool` | základní typy |
| `list[Item]` | seznam položek typu `Item` (Python 3.9+) |
| `dict[str, str]` | slovník klíč→hodnota, obojí řetězec |
| `Item \| None` | buď `Item`, nebo `None` (Python 3.10+) |
| `Callable[["Game", str], str]` | funkce, která bere hru a text, vrací text |

`from __future__ import annotations` na začátku souboru dovolí psát anotace jako text,
takže se nevyhodnocují při importu. Řeší to cyklické importy (`registry.py` ↔ `engine.py`)
a je to dobrý zvyk.

> **Kde to uvidíš:** všude. Anotace jsou povinné u nových funkcí (viz Definition of Done).

---

## 6. `@property` – metoda, která se chová jako atribut

```python
@property
def room(self) -> Room:
    return self.world.room(self.player.room_key)
```

Používá se **bez závorek**: `game.room`, ne `game.room()`.

Proč ne obyčejný atribut: hodnota se počítá z jiných dat. Kdybychom ji drželi zvlášť
(`self.room = ...`), museli bychom ji aktualizovat při každém pohybu a dřív nebo později
by se rozešla s realitou. `@property` ji vždy spočítá z aktuálního stavu.

> **Kde to uvidíš:** `Game.room` v `engine.py`.

---

## 7. Dekorátory – jak funguje `@command`

Dekorátor je funkce, která **vezme funkci a vrátí (upravenou) funkci**. Zápis

```python
@command("jdi", "přesune hráče")
def move(game, argument):
    ...
```

je zkratka za:

```python
def move(game, argument):
    ...
move = command("jdi", "přesune hráče")(move)
```

Náš `command()` funkci neupravuje – jen si ji **zapíše do slovníku** `COMMANDS`
a vrátí ji beze změny:

```python
def command(name, help=""):
    def decorator(func):
        COMMANDS[name] = Command(name, help, func)   # registrace
        return func
    return decorator
```

Proč takhle: příkaz se registruje **v okamžiku importu souboru**. Když `load_commands()`
naimportuje všechny moduly v `game/commands/`, příkazy se samy objeví v `COMMANDS`.
Nikdo nemusí udržovat ruční seznam – a proto si 23 lidí nešlape po souborech.

> **Kde to uvidíš:** `game/registry.py`, `game/commands/basic.py`.

---

## 8. `NotImplementedError` – proč to není `pass`

V kostře jsou metody, které ještě nikdo nenapsal:

```python
def is_alive(self) -> bool:
    raise NotImplementedError("Player.is_alive")
```

`pass` by vrátil `None` a chyba by se projevila až někde daleko (např. `if None:` tiše
projde jako nepravda). `raise NotImplementedError` řekne **hned a nahlas**, co chybí.

`Game.handle()` tuhle výjimku chytá a vrátí hráči větu „Příkaz zatím není hotový“ – hra
nespadne, jen upozorní. To je ukázka toho, že výjimka je nástroj, ne katastrofa.

> **Kde to uvidíš:** `engine.py` (všechny prázdné metody), `Game.handle()`.

---

## 9. Výjimky a `try/except`

```python
try:
    return cmd.handler(self, argument)
except NotImplementedError as exc:
    return f"Příkaz '{verb}' ještě není hotový ({exc})."
```

- `try` = „zkus tohle“,
- `except X as exc` = „když se objeví výjimka typu X, udělej tohle“,
- `raise X("zpráva")` = „vyhoď výjimku“ (přeruš tok, nahlas problém).

**Nikdy nepiš `except Exception: pass`** – spolkne i chyby, které potřebuješ vidět
(např. překlep v názvu proměnné). Chytej konkrétní typ výjimky.

V testech se výjimka ověřuje takhle:

```python
with self.assertRaises(FileNotFoundError):
    game.load("neexistuje.json")
```

> **Kde to uvidíš:** `Game.handle()`, `World.room()` (vyhazuje `KeyError`),
> `tests/test_save.py`.

---

## 10. JSON a načtení dat

JSON je textový formát pro data – slovník, seznam, čísla, řetězce. Náš svět je v JSONu,
aby ho mohli měnit i ti, kdo neumí Python.

```python
import json
from pathlib import Path

data = json.loads(Path(path).read_text(encoding="utf-8"))
```

- `Path(__file__).parent` = složka, kde leží **tento** soubor (ne odkud se program spouští).
  Bez toho by hra fungovala jen z jednoho adresáře.
- `encoding="utf-8"` je povinné na Windows, jinak se česká diakritika rozsype.
- `json.loads(text)` = řetězec → Python objekty (`dict`, `list`, …).
  `json.dump(obj, soubor)` = opačný směr (použiješ při ukládání hry).

> **Kde to uvidíš:** `World.from_json()`, `game/data/world.json`, zadání pro `tests/test_save.py`.

---

## 11. `unittest` – jak číst testy

```python
class TestMovement(unittest.TestCase):
    def setUp(self) -> None:          # spustí se před každým testem
        self.game = build_game()

    def test_move_to_neighbour_room(self) -> None:   # musí začínat "test_"
        self.game.handle("jdi sever")
        self.assertEqual(self.game.player.room_key, "chodba")
```

| Metoda | Kdy ji použít |
|---|---|
| `assertEqual(a, b)` | hodnoty se rovnají |
| `assertTrue/assertFalse(x)` | pravda/nepravda |
| `assertIn(prvek, kolekce)` | prvek je v seznamu/řetězci |
| `assertGreaterEqual(a, b)` | a ≥ b |
| `assertRaises(X)` | kód vyhodí výjimku X |
| `self.subTest(...)` | jeden test pro víc případů (viz `test_smoke.py`) |

Testy se hledají podle jména: soubor `test_*.py`, třída `Test*`, metoda `test_*`.
`python -m unittest discover -s tests -t . -v` je najde a spustí.

`@unittest.skip("důvod")` test **přeskočí**. V naší šabloně to znamená „ještě neimplementováno“ –
odstraněním dekorátoru vznikne červený test, který máš dovést k zelené.

> **Kde to uvidíš:** celá složka `tests/`.

---

## 12. `if __name__ == "__main__"`

```python
if __name__ == "__main__":
    sys.exit(main())
```

Když soubor spustíš přímo (`python game/cli.py`), je `__name__` roven `"__main__"` a kód
se provede. Když ho ale **naimportuješ** (`from game.cli import build_game` v testech),
`__name__` je `"game.cli"` a kód se nespustí – jinak by testy omylem spustily hru a čekaly
na vstup od klávesnice.

`sys.exit(0)` = „program skončil úspěšně“. Nenulová hodnota = chyba (CI to pozná).

> **Kde to uvidíš:** `game/cli.py`, `game/__main__.py`, `tests/*.py`.

---

## 13. Slovníček

| Pojem | Jednou větou |
|---|---|
| **modul** | soubor `.py` |
| **balíček** | složka s `__init__.py` |
| **třída** | předpis pro objekty |
| **instance** | konkrétní objekt vytvořený třídou |
| **atribut** | data uvnitř objektu (`player.hp`) |
| **metoda** | funkce uvnitř třídy |
| **dekorátor** | funkce, která obalí/ozdobí jinou funkci (`@command`) |
| **registr** | slovník, do kterého se příkazy samy zapisují |
| **dataclass** | dekorátor, který vygeneruje `__init__`, `__repr__`, `__eq__` |
| **anotace** | typová nápověda (`name: str`), nekontroluje se za běhu |
| **výjimka** | signál, že něco selhalo (`raise`/`except`) |
| **refaktor** | změna kódu bez změny chování |
| **PR** | pull request – návrh změny ke schválení |
| **CI** | automatické testy na serveru (GitHub Actions) |

---

## 14. Pět cvičení na pochopení (10 minut)

1. Napiš `Item("klíč")` a `print` ho. Co vypíše `repr` a co `str`? Proč se liší?
2. Odstraň `field(default_factory=list)` u `Player.inventory` a dej tam `= []`.
   Co se stane v `test_inventory_is_not_shared_between_players`?
3. Přidej do `game/commands/basic.py` příkaz `ahoj`, který vrátí `"Ahoj!"`.
   Objeví se v `help` sám? Proč?
4. Zavolej `game.handle("jdi sever")` v Python konzoli. Co vrátí a proč to není výjimka?
5. Napiš test, který ověří, že `World.room("neexistuje")` vyhodí `KeyError`.

Když zvládneš všech pět, rozumíš celé šabloně a můžeš začít psát vlastní příkazy.
