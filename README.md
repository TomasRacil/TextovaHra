# Textová hra – týmový projekt

[![tests](https://github.com/TomasRacil/TextovaHra/actions/workflows/tests.yml/badge.svg)](https://github.com/TomasRacil/TextovaHra/actions/workflows/tests.yml)

Šablona a zadání pro výuku **týmové práce na GitHubu** a **objektového programování v Pythonu**.
Cíl je jednoduchý: 23 lidí napíše jednu funkční konzolovou textovou hru tak, aby si vzájemně
nerozbili práci a aby se každý naučil celý cyklus *issue → branch → PR → review → merge*.

Hra je záměrně jen kostra. Téma, příběh, mechaniky i podobu hry si určíte sami.

---

## Rychlý start

```bash
git clone https://github.com/TomasRacil/TextovaHra.git
cd TextovaHra
python -m game
```

Testy (nic se neinstaluje, stačí Python 3.10+):

```bash
python -m unittest discover -s tests -t . -v
```

Momentálně: **15 testů prochází, 20 je přeskočených**. Přeskočené testy nejsou chyba –
jsou to zadání v podobě testu (viz [Testy](#testy)).

---

## Co v repozitáři je

```
game/
  __main__.py        vstupní bod: python -m game
  cli.py             konzolová smyčka (hotové, needituj bez domluvy)
  engine.py          třídy Item, Room, Player, World, Game (kostra)
  registry.py        registr příkazů + dekorátor @command (hotové)
  commands/
    basic.py         help, rozhledni, konec – vzor, jak psát příkaz
  systems/           složitější logika oddělená od příkazů (prázdné, na vás)
  data/
    world.json       mapa světa (místnosti, východy, předměty)
tests/               testy; test_smoke.py musí procházet vždy
.github/             CI, šablony issue a PR, CODEOWNERS
scripts/             nastavení repozitáře a pozvánky studentů
docs/                architektura a průvodce pro učitele
ZADANI.md            co máte odevzdat a jak jste hodnoceni
CONTRIBUTING.md      podrobný návod na pull requesty a review
```

---

## Jak hra funguje (30 sekund)

1. `python -m game` načte `game/data/world.json` do objektů `World` a `Room`.
2. Smyčka v `cli.py` čte řádky od hráče a předává je do `Game.handle()`.
3. `Game.handle()` rozdělí řádek na **příkaz** a **argument** a najde příkaz v registru.
4. Příkaz je funkce zaregistrovaná dekorátorem `@command`, která vrátí text pro hráče.
5. Nový příkaz = **nový soubor** v `game/commands/`. Do cizích souborů se nesahá.

Podrobněji v [`docs/ARCHITEKTURA.md`](docs/ARCHITEKTURA.md).

---

## Jak přispívat (pull requesty)

**Nikdy nepushuj přímo do `main`.** Větev `main` je chráněná a push do ní GitHub odmítne.
Všechno jde přes pull request. Tohle je celý cyklus:

```bash
# 1. Aktuální main
git switch main
git pull

# 2. Vlastní větev (jméno = typ/co-dělám)
git switch -c feat/prikaz-mluv

# 3. Práce + testy
#    ... upravíš soubory ...
python -m unittest discover -s tests -t . -v

# 4. Commit ( Conventional Commits, česky je to v pořádku)
git add game/commands/mluv.py tests/test_mluv.py
git commit -m "feat(commands): příkaz mluv pro dialogy s NPC"

# 5. Push větve
git push -u origin feat/prikaz-mluv

# 6. Pull request
gh pr create --fill      # nebo tlačítko na GitHubu

# 7. Po schválení a zeleném CI se sloučí (squash merge), pak úklid
git switch main && git pull
git branch -d feat/prikaz-mluv
```

### Co musí PR splnit, aby se sloučil

| Podmínka | Kdo to kontroluje |
|---|---|
| CI `tests` je zelené | automaticky (GitHub Actions) |
| Alespoň 1 schválení od někoho jiného než autor | automaticky (pravidlo větve) |
| Vyřešené všechny komentáře v review | automaticky |
| Testy pro novou funkcionalitu | reviewer (člověk) |
| Malý rozsah, jedna věc | reviewer (člověk) |
| Vyplněná šablona PR | reviewer (člověk) |

### Konvence

- **Větev:** `feat/…`, `fix/…`, `docs/…`, `test/…`, `refactor/…`, malá písmena, pomlčky.
- **Commit:** `typ(oblast): co se změnilo` – např. `fix(engine): hp neklesne pod nulu`.
- **Jazyk:** kód, docstringy a komentáře česky (identifikátory anglicky).
- **Styl:** 4 mezery, `snake_case`, typové anotace, docstring u každé třídy a funkce.
- **Rozsah:** ideálně do ~200 změněných řádků. Větší věc = víc menších PR.
- **Závislosti:** jen standardní knihovna Pythonu. Žádné `pip install`.

### Review

Review dělá někdo z jiného týmu (rozdělení je v `ZADANI.md`). Reviewer má 10 minut a smí
říct jen tři věci: *schvaluji*, *žádám změnu (s konkrétním důvodem)*, *nevím, zeptej se učitele*.
Komentář „je to fajn“ není review. Užitečné věty: „Tohle spadne, když je batoh prázdný –
zkus `vezmi` bez argumentu.“ / „Chybí test na tuhle větev `if`.“

---

## Pravidla tohoto repozitáře

- **`main` je chráněný:** žádný přímý push, žádný force push, lineární historie,
  povinný PR + 1 schválení + zelené CI, squash merge.
- **CI** (`.github/workflows/tests.yml`) pouští testy na každý PR. Když je červené,
  PR se nesloučí – a to je správně.
- **CODEOWNERS** označuje soubory, které mění jen učitel nebo projekt lead
  (`game/engine.py`, `game/registry.py`, `game/cli.py`, `.github/`).
- **Kdo má přístup:** všichni studenti jsou *spolupracovníci* (`push` právo, ne `admin`).
  Alternativa přes forky je popsaná v `CONTRIBUTING.md` – funguje stejně, jen s víc kroky.
- **Pravidla chování:** kritizuj kód, ne člověka. Když něco nevíš, napiš to do issue.
  Když něco rozbiješ, napiš to do PR popisu. To je celé.

---

## Testy

```bash
python -m unittest discover -s tests -t . -v     # vše
python -m unittest tests.test_smoke -v           # jen kostra
python -m unittest tests.test_movement.TestMovement.test_move_to_neighbour_room -v
```

- `tests/test_smoke.py` – **musí procházet pořád.** Když spadne, rozbili jste kostru.
- `tests/test_parser.py`, `test_movement.py`, `test_items.py`, `test_save.py` – **přeskočené
  kontrakty**. Odstraň `@unittest.skip(...)` a test musí projít. To je tvůj „hotovo“.
- Každá nová funkce potřebuje vlastní test. PR bez testu vrátíme.

---

## Pro učitele

Nastavení repozitáře (pravidla větve, štítky, pozvánky), časový plán 180 minut
a hodnoticí rubrika jsou v [`docs/PRUVODCE_UCITELE.md`](docs/PRUVODCE_UCITELE.md).
Skripty: `scripts/setup_repo.sh`, `scripts/invite_students.sh`.

---

## Časté dotazy

**Musím umět git z příkazové řádky?**
Ne, GitHub Desktop nebo VS Code stačí. Příkazy tu jsou proto, že jsou nejrychlejší a u zkoušky
se hodí je vidět.

**Push mi hlásí `protected branch hook declined`.**
Přesně tak to má být – nepushuj do `main`, ale do své větve a otevři PR.

**Konflikt při `git pull`.**
Vyřeš ho u sebe: `git switch main && git pull`, pak `git switch moje-vetev && git merge main`,
oprav soubory, `git add`, `git commit`, `git push`. Nikdy nepoužívej `git push --force`
na cizí větev.

**Můj test je přeskočený, i když kód funguje.**
Odstraň dekorátor `@unittest.skip(...)` nad třídou nebo metodou.

**Můžu měnit `engine.py`?**
Jen po domluvě s projekt leadem. Skoro vždy jde přidat nový modul nebo příkaz místo toho.
