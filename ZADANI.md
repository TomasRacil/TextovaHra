# Zadání: Textová hra (týmový projekt, 180 minut)

> Tento dokument je zadání pro studenty. Učitelská verze (nastavení repa, facilitace,
> rubrika) je v [`docs/PRUVODCE_MAJITELE.md`](docs/PRUVODCE_MAJITELE.md).
> Nerozumíš `dataclass`, dekorátorům nebo `self`? Přečti [`docs/KONCEPTY.md`](docs/KONCEPTY.md).
> Board a release: [`docs/PROJEKTY_A_RELEASE.md`](docs/PROJEKTY_A_RELEASE.md).

---

## 1. Co stavíte

Konzolovou **textovou hru v Pythonu**, na které pracuje celá třída (23 lidí) najednou
v jednom GitHub repozitáři. Za 180 minut musí vzniknout **hratelná verze 0.1**: hráč přijde
do světa, může se pohybovat, něco sebrat a použít, potkat postavu a hru dokončit (vyhrát
nebo prohrát).

**Téma hry je na vás.** Vyberte ho v prvních 20 minutách, zapište do issue a držte se ho.
Dobré téma má: místa k prozkoumání, důvod se hýbat, překážku a konec.

Příklady, které fungují: opuštěná škola po karanténě, vesmírná stanice bez posádky,
cesta ze sklepa, detektivka v jednom domě, sídlo firmy po pádu serveru.

---

## 2. Co si z hodiny odnesete

Po hodině umíte:

1. vysvětlit rozdíl mezi `clone`, `branch`, `commit`, `push`, `pull` a `pull request`,
2. založit větev, udělat v ní změnu, otevřít PR a reagovat na review,
3. vyřešit konflikt ve sdíleném souboru (a vědět, jak se mu příště vyhnout),
4. napsat třídu s metodami, stavem a testy, které její chování ověřují,
5. rozdělit práci tak, aby si 23 lidí nesedlo na jeden soubor.

---

## 3. Povinné jádro (MVP) – tohle musí hra umět na konci hodiny

Odškrtněte v issue, až to bude fungovat:

- [ ] **Parser** – příkaz + argument, nerozlišuje velikost písmen, funguje i bez diakritiky.
- [ ] **Pohyb** – `jdi <směr>` mezi místnostmi, neplatný směr hru neshodí.
- [ ] **Rozhlédnutí** – `rozhledni` popíše místnost, východy a předměty.
- [ ] **Předměty** – `vezmi`, `polož`, `použij`, `batoh`.
- [ ] **Stav hráče** – zdraví/energie, ubírání a doplňování, smrt = konec hry.
- [ ] **Postava (NPC)** – alespoň jedna, s dialogem a reakcí na předmět nebo odpověď.
- [ ] **Konec hry** – podmínka výhry a prohry, hra to hráči sdělí.
- [ ] **Uložení a načtení** – `uloz`, `nacti` do JSON souboru.
- [ ] **Nápověda** – `help` vypíše, co hra umí (nesmí být ručně psaný seznam).
- [ ] **Hratelné od začátku do konce** – tester to projde bez ručního zásahu do kódu.

### Volitelné (když zbude čas)

Soubojový systém, mapa (`mapa`), obchodování, deník úkolů, náhodné události, barvy v terminálu,
načtení světa z více JSON souborů, Easter egg.

### Technická omezení

- Python **3.10+**, jen **standardní knihovna** (žádné `pip install`, žádné externí balíčky).
- Vstup a výstup pouze text (terminál). Žádné grafické okno.
- Kód, docstringy a texty ve hře **česky**; identifikátory anglicky.
- Každá nová funkce musí mít test. Bez testu PR neschválíme.

---

## 4. Týmy a vlastnictví souborů

23 lidí = **6 týmů** (4+4+4+4+4+3). Rozdělení určí projekt lead, ideálně podle toho,
kdo co umí. Každý tým má **vlastníka souborů** – to je jediné pravidlo, které vás ušetří
konfliktů.

| Tým | Oblast | Vlastní soubory |
|---|---|---|
| 1 | Parser, základní slovesa, nápověda | `game/commands/parser_*.py`, `tests/test_parser.py` |
| 2 | Svět, mapa, místnosti | `game/data/world.json`, `game/commands/pohyb.py`, `game/systems/movement.py` |
| 3 | Předměty, inventář | `game/commands/predmety.py`, `game/systems/inventory.py`, `game/data/items.json` |
| 4 | Postavy a dialogy | `game/commands/mluv.py`, `game/systems/dialogs.py`, `game/data/dialogs.json` |
| 5 | Souboj, stav hráče | `game/commands/boj.py`, `game/systems/combat.py`, `tests/test_combat.py` |
| 6 | Ukládání, UI, dokumentace | `game/systems/save.py`, `game/commands/uloz.py`, `docs/`, `tests/test_save.py` |

**Sdílené soubory – sem se nesahá bez souhlasu projekt leada:**

```
game/engine.py      game/registry.py      game/cli.py      README.md
```

Když potřebuješ změnu ve sdíleném souboru, napiš to do issue a označ projekt leada.
Většinou to jde obejít: nový soubor v `game/commands/` nebo `game/systems/`.

**Role:**

- **Projekt lead** (1 student) – drží architekturu, rozhoduje spory, schvaluje změny ve
  sdílených souborech, hlídá, aby se `main` nerozbil. Nemusí psát nejvíc kódu.
- **Reviewer** – v každém týmu jeden; recenzuje PR z *jiného* týmu (nikdy vlastní).
- **Tester** – v každém týmu jeden; na konci hraje hru jako hráč a zakládá issues na chyby.
- **Učitel** – poslední instance, ne první. Nejdřív se ptejte leada a týmu.

### Kde je vidět, kdo co dělá: board

Práce není „v hlavě“, je na [boardu projektu](https://github.com/users/TomasRacil/projects/3).
Sloupce: **Backlog → Připraveno → Dělám → Ke kontrole → Hotovo**.

1. Vyber si položku z **Backlogu** (dvanáct jich tam je předpřipravených).
2. Převeď ji na issue a **přiřaď si ji** – tím je zamčená, nikdo jiný na ní nepracuje.
3. Přesuň do **Dělám**, když zakládáš větev. Do **Ke kontrole**, když otevřeš PR.
4. **Hotovo** = sloučeno do `main` (většinou to udělá automatizace).

Pravidlo: **stav na boardu se mění ve chvíli, kdy se změní realita.** Board, který lže,
je horší než žádný. Kdo na boardu nic nemá, na ničem nepracuje – a je to vidět.

Jak board a release fungují a proč, je v [`docs/PROJEKTY_A_RELEASE.md`](docs/PROJEKTY_A_RELEASE.md).

---

## 5. Průběh hodiny (180 minut)

| Čas | Fáze | Co děláte | Výstup |
|---|---|---|---|
| 0–15 | **Úvod** | Ukázka celého cyklu na projektoru: issue → branch → PR → review → merge. Pravidla repa, ochrana `main`. | Víte, jak vypadá hotový PR |
| 15–35 | **Rozjezd** | Volba tématu, volba projekt leada, rozdělení do týmů, každý tým zapíše 3–5 issues. | Téma + 20+ issues v backlogu |
| 35–60 | **První PR každého** | Každý student udělá *jeden malý* PR: oprava překlepu v `world.json`, nový test, docstring, jedno sloveso. Cíl je naučit se cyklus, ne kódit. | 23 malých sloučených PR |
| 60–140 | **Funkce** | Týmy pracují na svých issues. Průběžně: PR → review od jiného týmu → merge. Checkpoint v 100. minutě (viz níže). | Fungující mechaniky na `main` |
| 140–165 | **Integrace a hraní** | Tester z každého týmu hraje hru od začátku do konce, zakládá issues na chyby, opravy jdou přes PR. | Hratelná verze 0.1 |
| 165–180 | **Uzávěrka** | Tag `v0.1`, krátké retro (co fungovalo, co příště jinak), zadání domácího úkolu. | Release + retro |

**Checkpoint ve 100. minutě** (5 minut, celá třída): každý tým řekne jednou větou, co má
hotové a co ho blokuje. Blokery se řeší hned – ne v 160. minutě.

**Pravidlo 20 minut:** když se na něčem zasekneš na víc než 20 minut, napiš to do issue,
označ tým a jdi dělat něco jiného. Zaseknutí není ostuda, mlčení je.

---

## 6. Backlog – z čeho vybírat

Tohle je nabídka, ne povinný seznam. Týmy si ji upraví podle tématu.

**Parser a příkazy:** zkratky (`j` = `jdi`), diakritika na vstupu, neznámý příkaz s nápovědou
„myslel jsi…?“, příkazy s více slovy (`použij klíč na dveře`), historie příkazů.

**Svět:** další místnosti v `world.json`, zamčené východy, místnosti, kde je tma (bez louče
nevidíš), tajné východy, mapa, kterou jde vykreslit jako ASCII.

**Předměty:** přenositelné/nepřenositelné, kombinování (`spoj provaz a hák`), předmět s účinkem
(léčivý čaj), peníze a obchod, truhla vyžadující klíč.

**Postavy:** NPC, které odpovídá na klíčová slova, NPC, které něco chce výměnou, nepřátelská
postava, průvodce, který komentuje váš postup.

**Stav hry:** hlad/únava, postupně ubývající světlo, otrava, smrt a respawn (nebo konec),
skóre na konci.

**Systém:** ukládání do JSON, načtení světa z více souborů, logování tahů pro testování,
generátor náhodných událostí.

---

## 7. Definition of Done

PR je hotový, když platí **všechno** tohle:

1. Kód dělá, co slibuje issue, a je za ním test, který to ověřuje.
2. `python -m unittest discover -s tests -t . -v` prochází lokálně.
3. CI na GitHubu je zelené.
4. Někdo jiný PR schválil a jeho komentáře jsou vyřešené.
5. Změna je malá (do ~200 řádků) a týká se jedné věci.
6. Nové třídy a funkce mají docstring a typové anotace.
7. V kódu nejsou `print()` na ladění, `TODO` ani zakomentované bloky.
8. Funguje to i na vstupech bez diakritiky a s velkými písmeny.

---

## 8. Hodnocení (100 bodů)

| Body | Za co | Jak se to pozná |
|---|---|---|
| 40 | **Kvalita PR** (4 PR × 10) | Malý rozsah, popis, testy, dodržené konvence, žádný spam |
| 20 | **Review** (2 × 10) | Konkrétní, věcné komentáře; odhalená chyba nebo chybějící test |
| 25 | **Funkčnost vlastní featury** | Dá se to použít ve hře, zvládá okrajové případy, neshodí hru |
| 10 | **Testy** | Testuje chování, ne implementaci; čitelné názvy; pokrývá chyby |
| 5 | **Dokumentace** | Docstringy, aktualizovaný `docs/`, srozumitelný popis v issue |

**Tvrdé podmínky:** bez alespoň jednoho sloučeného PR je hodnocení 0 (i když jsi kód psal
lokálně a nepushnul). Bez odevzdaného review je maximum 80 bodů.

**Co body nespasí:** „napsal jsem to celé doma a poslal zip“. Hodnotí se práce v repozitáři.

---

## 9. Nejčastější chyby (a jak je poznat)

| Chyba | Jak se projeví | Řešení |
|---|---|---|
| Práce přímo na `main` | push odmítnut ochranou větve | větev + PR, viz README |
| Dlouhá větev bez pull z `main` | obří konflikt v poslední hodině | `git switch main && git pull` každých ~20 minut, merge do své větve |
| Mutable default argument | `def __init__(self, items=[])` – všichni hráči sdílí batoh | `field(default_factory=list)` nebo `None` + vytvoření uvnitř |
| Příkaz tiskne místo vrací text | `print()` v handleru, testy nemají co ověřit | handler vrací `str`, tiskne jen `cli.py` |
| Úprava cizího souboru | konflikt s týmem, který soubor vlastní | nový modul v `game/commands/` nebo `game/systems/` |
| Test jen pro šťastnou cestu | chybí test na neplatný vstup | přidej test na chybu, ne jen na úspěch |
| PR s 800 řádky | reviewer to vzdá, merge se odkládá | rozděl na víc PR po menších kusech |

---

## 10. Po hodině

Do příští hodiny každý:

1. dokončí svoji rozpracovanou větev a otevře PR (i když nebude sloučený),
2. udělá jedno review na PR z jiného týmu,
3. zapíše do issue jednu věc, kterou by příště udělal jinak.

Společný cíl pro další hodinu: **v0.2** – hra má tři kapitoly, ukládání a projde ji tester
bez nápovědy autora.
