# Board a release: k čemu to je a jak na to

Dvě věci, které v repozitáři nejsou vidět jako soubory, ale rozhodují o tom, jestli se 23 lidí
dohodne: **GitHub Project (board)** a **release (vydaná verze)**.

---

# Část A: GitHub Projects (board)

## Co to je

**Project je nástěnka nad issues a pull requesty.** Není to soubor v repozitáři ani součást
kódu – je to vrstva nad repozitářem, která drží stav práce: kdo na čem dělá, co je volné,
co čeká na review.

Vztah tří věcí, které se pletou:

| Věc | Co to je | Kde žije |
|---|---|---|
| **Issue** | úkol nebo nápad („přidat příkaz mluv“) | v repozitáři, má číslo `#12` |
| **Pull request** | návrh konkrétní změny kódu | v repozitáři, má číslo `#34` |
| **Project** | nástěnka, která issues a PR **organizuje** | mimo repo, odkazuje na ně |

Issue bez boardu je seznam, který si nikdo neprojde. Board bez issues je prázdná tabule.
Dohromady to je jediné místo, kde je vidět celý stav projektu.

## Proč to mít na hodině

- **23 lidí se neptá „co mám dělat?“** – podívají se na sloupec *Připraveno* a vezmou si, co je volné.
- **Nevzniká dvojitá práce.** Kdo si položku nevzal (nepřiřadil), na ní nepracuje.
- **Ty vidíš frontu** na review a na blokery, aniž bys obcházel počítače.
- **Studenti vidí pokrok** – sloupec *Hotovo* roste. U 180minutové akce je to silná motivace.

## Co je nastavené v tomto repu

- Projekt: **TextovaHra – vývoj hry** → https://github.com/users/TomasRacil/projects/3
- Je **propojený s repozitářem** (`gh project link`), takže issues z repa do něj jdou přidat
  jedním kliknutím a v issue je vidět jeho stav.
- Sloupce (stav): **Backlog → Připraveno → Dělám → Ke kontrole → Hotovo**
- Vlastní pole: **Tým** (1–6), **Odhad** (body)
- Předplněný backlog: 12 položek (draft items) – nejsou to issues, dokud si je někdo nevezme

Ověření z terminálu:

```bash
gh project view 3 --owner TomasRacil
gh project item-list 3 --owner TomasRacil --format json --jq '.items[] | {title, status}'
```

## Jak board používají studenti

1. Podívají se do **Backlogu** a vyberou si položku (nebo si založí vlastní issue).
2. **Převedou ji na issue** (v UI: `...` → *Convert to issue*) a **přiřadí si ji** (Assignees).
   Tím je zamčená – nikdo jiný na ní nepracuje.
3. Přesunou ji do **Připraveno** (má zadání a kritéria) a pak do **Dělám** ve chvíli,
   kdy zakládají větev.
4. Otevřou PR → přesunou do **Ke kontrole**.
5. Po sloučení do `main` → **Hotovo**. (Většinou to udělá automatizace, viz níž.)

**Pravidlo:** stav na boardu se mění ve chvíli, kdy se změní realita – ne „až bude čas“.
Board, který lže, je horší než žádný board.

## Automatizace boardu (2 minuty v UI)

V projektu: **⋯ → Workflows**. Zapni aspoň:

- **Auto-add to project** – nové issues z repa se přidají do Backlogu samy,
- **Item closed** – zavřené issue/PR → *Hotovo*,
- **Pull request merged** – sloučený PR → *Hotovo*.

Pak studenti nemusí nic přepínat ručně a board zůstane pravdivý i bez tebe.

## Draft items vs. issues

Předplněné položky jsou **draft items** – text na boardu, který ještě není issue. Je to
schválně: studenti si téma a formulaci převezmou sami (učí se psát zadání). Převodem na issue
získají číslo, štítky a možnost diskuse v komentářích.

---

# Část B: Release a balíček

## Co je release

**Release = pojmenovaná, zmrazená verze hry, ke které se dá vrátit.** Skládá se ze dvou věcí:

1. **git tag** (`v0.1.0`) – ukazatel na konkrétní commit. Historie je neměnná, takže tag
   označuje přesně ten stav kódu, který se hrál.
2. **GitHub Release** – stránka s poznámkami k verzi a **přiloženými soubory** (u nás wheel
   a zdrojový balíček). Dá se stáhnout bez znalosti gitu.

Proč to učit: „hotovo“ musí mít důkaz. Student, který řekne „mám to hotové“, ale neumí říct
*co* je hotové a *odkud* si to stáhnu, nemá hotovo nic.

## Sémantické verzování (jednoduchá verze)

`MAJOR.MINOR.PATCH` – u školního projektu stačí chápat takhle:

| Změna | Příklad | Verze |
|---|---|---|
| hra je poprvé hratelná | první release | `0.1.0` |
| přibyla mechanika | souboj, mapa | `0.2.0` |
| oprava chyby | „vezmi“ už nespadne | `0.2.1` |

Verze je **na jednom místě**: `game/__init__.py` → `__version__ = "0.1.0"`.
`pyproject.toml` si ji odtud bere (`dynamic = ["version"]`), takže se nemůže rozejít.

## Co dělá `.github/workflows/release.yml`

Workflow se spustí **jen při pushi tagu** `v*`:

1. pustí testy – bez zelených testů se nic nevydá,
2. zkontroluje, že `v0.1.0` odpovídá `__version__` v kódu (jinak červené a konec),
3. sestaví balíček: `python -m build` → `dist/textovka-0.1.0-py3-none-any.whl` + `.tar.gz`,
4. **nainstaluje wheel a spustí hru** – tím dokáže, že balíček funguje (ne jen že se sestavil),
5. vytvoří GitHub Release s poznámkami z historie a přiloží oba soubory.

Bod 4 je nejcennější: většina „release“ workflowů balíček jen zabalí a nikdy ho nespustí.
Chyba v balíčku (chybějící `world.json`) se pak pozná až u studenta.

## Jak vydat verzi (3 příkazy)

```bash
# 1. zvedni verzi v game/__init__.py (a commitni přes PR!)
# 2. tag na aktuální main
git switch main && git pull
git tag -a v0.1.0 -m "Hratelná verze 0.1"
git push origin v0.1.0
```

Pak **Actions → release** a za minutu je release hotový. Kontrola:

```bash
gh release list
gh release view v0.1.0
gh run list --workflow=release.yml
```

Tag **nemaž a nepřesouvej** – na vydanou verzi se lidé odkazují. Chybu oprav novou verzí
(`0.1.1`), ne přepsáním staré.

## Jak si balíček nainstalovat

```bash
pip install textovka-0.1.0-py3-none-any.whl
textovka
```

`textovka` je **console script** – příkaz, který balíček přidá do systému. Definuje ho
`pyproject.toml`:

```toml
[project.scripts]
textovka = "game.cli:main"
```

## Co je v `pyproject.toml` (a proč)

| Pole | Význam |
|---|---|
| `name`, `description`, `authors` | metadata balíčku (co se vypíše na PyPI / v `pip show`) |
| `requires-python = ">=3.10"` | starší Python hru nespustí – explicitně |
| `dependencies = []` | záměrně prázdné: hra nesmí potřebovat instalaci ničeho |
| `dynamic = ["version"]` | verze se bere z `game.__version__`, neopisuje se |
| `[project.scripts]` | příkaz `textovka` po instalaci |
| `[tool.setuptools] packages` | které balíčky se zabalí (`game`, `game.commands`, `game.systems`) |
| `[tool.setuptools.package-data]` | `data/*.json` – bez toho by hra po instalaci neměla svět |

## Časté chyby

| Chyba | Projev | Řešení |
|---|---|---|
| tag neodpovídá `__version__` | workflow spadne na kontrole verze | zvedni verzi v kódu, nový tag |
| chybí `package-data` | po instalaci `FileNotFoundError: world.json` | doplň `data/*.json` do `pyproject.toml` |
| nový balíček v `game/` není v `packages` | po instalaci `ModuleNotFoundError` | přidej ho do `[tool.setuptools] packages` |
| tag na špatném commitu | release neobsahuje poslední změny | `git tag -d`, pushni nový tag (jen pokud ještě nikdo nestáhl) |
| release z rozbitého main | uživatel dostane nefunkční verzi | testy jsou gate – proto je workflow pouští první |
