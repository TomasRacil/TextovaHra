# Architektura hry

Proč je kód rozdělený takhle: **23 lidí v jednom repozitáři**. Každé rozhodnutí níž existuje
proto, aby se dva lidé nepotkali ve stejném souboru.

## Tok jednoho příkazu

```
hráč napíše "jdi sever"
        │
        ▼
game/cli.py          input() ve smyčce, tiskne odpovědi
        │
        ▼
game/engine.py       Game.handle("jdi sever")
        │              rozdělí na příkaz "jdi" + argument "sever"
        ▼
game/registry.py     COMMANDS["jdi"] → handler
        │
        ▼
game/commands/pohyb.py   @command("jdi")
        │                 pracuje se stavem: game.player, game.world
        ▼
vrací str  ──────────────►  cli.py ho vytiskne
```

Pravidlo: **handler vrací text, nikdy netiskne.** Díky tomu jde hra testovat bez terminálu
(`game.handle("jdi sever")` vrátí řetězec, test ho porovná).

## Třídy

| Třída | Soubor | Odpovídá za |
|---|---|---|
| `Item` | `engine.py` | předmět – jméno, popis, (účinek) |
| `Room` | `engine.py` | místnost – popis, východy, předměty |
| `Player` | `engine.py` | hráč – poloha, batoh, zdraví |
| `World` | `engine.py` | mapa – slovník místností, start |
| `Game` | `engine.py` | stav rozehrané hry + dispatch příkazů |
| `Command` | `registry.py` | jeden příkaz: jméno, nápověda, funkce |

`engine.py` je **kostra**: atributy a prázdné metody s `NotImplementedError`. Doplňuje se
po domluvě s projekt leadem, protože ho používají všichni.

## Jak přidat příkaz (nejčastější úkol)

```python
# game/commands/mluv.py
from ..registry import command

@command("mluv", "promluví s postavou v místnosti")
def mluv(game, argument: str) -> str:
    if not argument:
        return "S kým chceš mluvit?"
    return f"Zkusíš promluvit s: {argument}"
```

Soubor se naimportuje sám (`registry.load_commands()` projde `game/commands/`), takže
**nikam se nic nepřidává** a nikdo jiný nemusí nic měnit. To je celý trik proti konfliktům.

Aliasy (dvě jména pro totéž):

```python
@command("jdi", "přesune hráče do sousední místnosti")
@command("j", "zkratka pro jdi")
def move(game, argument: str) -> str:
    ...
```

## Jak přidat systém (složitější logika)

Logika, která není jen „přečti a vrať text“, patří do `game/systems/`:

```python
# game/systems/combat.py
class Combat:
    def __init__(self, player, enemy): ...
    def attack(self) -> str: ...
```

Příkaz v `game/commands/` je pak jen tenká slupka: přečte argument, zavolá systém, vrátí text.
Díky tomu jde souboj otestovat bez hry a příkaz bez souboje.

## Data

`game/data/world.json` – mapa, místnosti, východy, předměty. Klíče místností jsou bez diakritiky
(`nadvori`, `chodba`), zobrazované názvy s diakritikou (`Nádvoří`).

Ostatní týmy si přidávají vlastní soubory (`items.json`, `dialogs.json`), aby si nešlapaly
po `world.json`. Načítání je vždy v `World.from_json()` nebo v daném systému – ne v `engine.py`.

## Testy

- `tests/test_smoke.py` – kostra. Musí procházet vždy; když spadne, někdo rozbil jádro.
- `tests/test_<oblast>.py` – kontrakty přeskočené přes `@unittest.skip`. Odstraněním skipu
  vznikne červený test (RED), implementací zelený (GREEN). To je celý TDD cyklus hodiny.
- Nová funkce bez testu = PR se neschválí.

## Co nedělat

| Nedělat | Proč | Místo toho |
|---|---|---|
| měnit `engine.py` kvůli jedné funkci | konflikt s celou třídou | nový modul v `commands/` nebo `systems/` |
| `print()` v handleru | nedá se testovat | vrátit `str` |
| globální proměnné (`hra = Game()`) | nejde testovat dvě hry vedle sebe | předávat `game` jako parametr |
| mutable default (`items=[]`) | všichni hráči sdílí jeden seznam | `field(default_factory=list)` |
| `except Exception: pass` | chyba zmizí i s důkazem | chytat konkrétní výjimku |
| ručně psaný seznam v `help` | zapomene se aktualizovat | číst `COMMANDS` (viz `basic.py`) |
