# Jak přispívat do této hry

Tenhle dokument je návod krok za krokem. Když něco nefunguje, hledej v části
[Když se něco pokazí](#když-se-něco-pokazí).

## 0. Jednorázové nastavení

```bash
git clone https://github.com/TomasRacil/TextovaHra.git
cd TextovaHra

git config user.name  "Jméno Příjmení"
git config user.email "tvuj@email.cz"
```

Ověření, že testy procházejí (nic se neinstaluje):

```bash
python -m unittest discover -s tests -t . -v
```

Chceš-li `gh` (GitHub CLI), přihlas se jednou:

```bash
gh auth login
```

## 1. Vyber si issue

Bez issue nezačínej. Vezmi si jednu položku z backlogu a **přiřaď si ji** (Assignees),
aby ji nezačal dělat někdo jiný. Když issue neexistuje, založ ho podle šablony.

## 2. Založ větev

Vždy z aktuálního `main`:

```bash
git switch main
git pull
git switch -c feat/prikaz-mluv
```

Větev = jedna věc. `feat/`, `fix/`, `docs/`, `test/`, `refactor/` + krátký název s pomlčkami.

## 3. Napiš kód a test

Pravidla, která review kontroluje:

- nový příkaz = nový soubor v `game/commands/`, ne úprava cizího souboru,
- handler **vrací** text (`return "..."`), nikdy netiskne (`print`),
- třídy a funkce mají docstring a typové anotace,
- každá nová větev kódu má test,
- jen standardní knihovna.

Spusť testy:

```bash
python -m unittest discover -s tests -t . -v
```

Zelené? Pokračuj. Červené? Oprav, nebo se přiznej v PR popisu – ale necommituj rozbité testy
bez vysvětlení.

## 4. Commit

```bash
git add game/commands/mluv.py tests/test_mluv.py
git commit -m "feat(commands): příkaz mluv pro dialogy s NPC"
```

Formát: `typ(oblast): co se změnilo`

| typ | kdy |
|---|---|
| `feat` | nová funkce pro hráče |
| `fix` | oprava chyby |
| `test` | jen testy |
| `docs` | jen dokumentace |
| `refactor` | změna kódu bez změny chování |
| `chore` | úklid, konfigurace |

Malý commit = jedna myšlenka. Když musíš do message psát „a ještě“, patří to do jiného commitu.

## 5. Push a pull request

```bash
git push -u origin feat/prikaz-mluv
gh pr create --fill
```

Nebo na GitHubu: po pushi se objeví tlačítko **Compare & pull request**.

Do PR vyplň šablonu: co to dělá, jak to vyzkoušet, `Closes #12`, checklist.

## 6. Review

Review dělá někdo z **jiného týmu**. Ty jako autor:

- čekáš na CI (2 minuty), pak na reviewera,
- na každý komentář odpovíš: opravím / neopravím, protože…,
- opravy pushneš do **stejné** větve – PR se aktualizuje sám,
- „Resolve conversation“ mačkej jen když je opravdu vyřešeno.

Ty jako reviewer:

- přečti si popis a **zkus to podle kroků v PR**, ne jen čti diff,
- piš konkrétně: soubor, řádek, co je špatně, co čekáš,
- rozlišuj „tohle musí“ (blokuje merge) a „tohle by šlo lépe“ (návrh),
- nekomentuj styl, který řeší konvence (odsazení, názvy) – to není review.

## 7. Merge

Sloučívá **autor** po schválení, tlačítkem **Squash and merge** (jiná varianta není povolená,
aby historie zůstala čitelná). Pak:

```bash
git switch main
git pull
git branch -d feat/prikaz-mluv
```

## 8. Když se něco pokazí

**Push odmítnut: `protected branch hook declined`**
Pushuješ do `main`. Vytvoř větev (`git switch -c feat/...`), pushni ji a otevři PR.

**Konflikt při merge**

```bash
git switch main
git pull
git switch moje-vetev
git merge main          # tady vznikne konflikt
# otevři soubory se značkami <<<<<<< ======= >>>>>>>
# uprav tak, aby dával smysl výsledek, značky smaž
git add upravene_soubory
git commit
git push
```

Konflikt **nikdy** neřeš tak, že zahodíš cizí změny. Když si nejsi jistý, zeptej se autora.

**Commitnul jsem omylem do `main` a ještě nepushnul**

```bash
git switch -c feat/muj-prace     # přenese commity do nové větve
git switch main
git reset --hard origin/main     # main zpět na stav serveru
```

**Chci zrušit poslední commit, ale ne změny v souborech**

```bash
git reset --soft HEAD~1
```

**Nevím, co se děje**

```bash
git status
git log --oneline --graph --decorate -15
```

Když ani to nepomůže: `git stash`, přepni na `main`, `git pull`, nová větev, `git stash pop`.
A napiš do issue, co se stalo – ne do chatu v 175. minutě.

## 9. Varianta přes fork (když nemáš právo push)

Používá se v open source, kde přispěvatel nemá do repozitáře zápis. Funguje stejně, jen
přibude krok „fork“ a „upstream“:

```bash
gh repo fork TomasRacil/TextovaHra --clone
cd TextovaHra
git remote add upstream https://github.com/TomasRacil/TextovaHra.git

git switch -c feat/prikaz-mluv
# ... práce, testy, commit ...
git push -u origin feat/prikaz-mluv
gh pr create --fill --repo TomasRacil/TextovaHra
```

Před každou prací si stáhni změny z upstreamu:

```bash
git fetch upstream
git switch main
git merge --ff-only upstream/main
git push origin main
```

U prvního PR od nového přispěvatele GitHub **nespustí CI automaticky** – musí ho schválit
maintainer. Počkej na učitele, není to chyba.

## 10. Rychlý tahák

| Chci… | Příkaz |
|---|---|
| vědět, kde jsem | `git status` |
| vidět historii | `git log --oneline --graph -15` |
| novou větev | `git switch -c feat/nazev` |
| přepnout větev | `git switch nazev` |
| stáhnout main | `git switch main && git pull` |
| commitnout | `git add -A && git commit -m "typ(oblast): popis"` |
| pushnout | `git push` (prvně `git push -u origin vetev`) |
| zahodit necommitnuté změny | `git restore .` |
| vrátit soubor | `git restore soubor.py` |
| smazat sloučenou větev | `git branch -d nazev` |

## 11. Pravidla chování

- Kritizuj kód, ne člověka. „Tohle spadne na prázdném batohu“ je OK, „to je hloupé“ není.
- Když nerozumíš cizímu kódu, zeptej se v komentáři – je to normální a užitečné.
- Když něco rozbiješ, napiš to. Skrývání chyby je horší než chyba.
- Necommituj cizí práci ani cizí soubory „aby to prošlo“.
- Nemazej cizí komentáře v review.
