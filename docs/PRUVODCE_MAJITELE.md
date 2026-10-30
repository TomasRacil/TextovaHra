# Průvodce majitele repozitáře

Tohle je příručka pro toho, kdo repozitář **vlastní** – ne jen učí. Pokrývá obojí:

1. **jak takový repozitář postavit od nuly** (založení, CI, ochrana `main`, šablony,
   pozvánky, štítky) – kapitoly 1–3,
2. **jak s ním odučit 180 minut** a jak práci studentů ohodnotit – kapitoly 4–6,
3. **jak ho udržet pro další ročník** a co dělat, když se něco pokazí – kapitoly 7–9.

Studentské zadání je v [`../ZADANI.md`](../ZADANI.md), architektura v
[`ARCHITEKTURA.md`](ARCHITEKTURA.md), vysvětlení pojmů (`dataclass`, dekorátory, `self`)
v [`KONCEPTY.md`](KONCEPTY.md), board a release v [`PROJEKTY_A_RELEASE.md`](PROJEKTY_A_RELEASE.md).

---

## 0. Kdo je kdo

| Role | Kdo to je | Odpovídá za |
|---|---|---|
| **Majitel repozitáře** | učitel (admin) | nastavení repa, pravidla, CI, pozvánky, poslední slovo |
| **Učitel** | stejná osoba, jiná čepice | výklad, facilitace, hodnocení |
| **Projekt lead** | student | architektura, spory, schvalování změn ve sdílených souborech |
| **Reviewer** | student (1 za tým) | recenze PR z jiného týmu |
| **Tester** | student (1 za tým) | hraje hru, zakládá issues na chyby |
| **Student** | 23 lidí | issues, branche, PR, review |

Klíčové pravidlo pro tebe: **jsi poslední instance, ne první.** Když za tebou někdo přijde
s dotazem, první odpověď je „zeptej se leada / reviewera“. Jinak se z hodiny stane fronta
na tebe a 23 lidí čeká.

---

## 1. Rozhodnutí, která musíš udělat před založením

Pět otázek, každá mění nastavení repa. Rozhodni je dřív, než vznikne první commit.

| Otázka | Volby | Dopad na nastavení |
|---|---|---|
| Veřejný, nebo privátní? | **veřejný** (doporučeno pro výuku) / privátní | Na **Free** plánu fungují rulesets a ochrana větve jen u **veřejných** repozitářů. Privátní = ochrana `main` není vynutitelná, spoléháš na domluvu. |
| Kdo má právo push? | **spolupracovníci** (doporučeno) / forky | Spolupracovníci = jedna větev, žádná synchronizace s upstreamem, méně kroků. Forky = realističtější open source, ale každý student řeší `upstream` a první PR čeká na schválení CI. |
| Kdo reviewuje? | **studenti navzájem** (doporučeno) / učitel / obojí | Určuje `required_approving_review_count` a `CODEOWNERS`. Když reviewuješ ty, hodina se utopí. |
| Jaký stack? | Python + stdlib (tady) / cokoli jiného | Určuje CI a to, co studenti musí mít nainstalované. **Čím méně závislostí, tím méně času na instalaci.** |
| Kolik času? | 180 min (tady) | Určuje velikost MVP v zadání. Na 180 min se vejde tak 8–10 mechanik, ne víc. |

**Doporučená kombinace pro 23 studentů / 180 minut:** veřejný repo, spolupracovníci,
vzájemné review mezi týmy, Python bez závislostí, MVP v `ZADANI.md`.

### Poznámka k plánu GitHubu

- **Free**: veřejné repo = neomezené CI minuty, rulesets fungují. Privátní repo = 2 000 CI
  minut/měsíc a ochrana větve není vynutitelná.
- **Pro / Team / Education**: ochrana i u privátních repozitářů. Pokud máš přístup
  k učitelskému/Education zvýhodnění, ověř si aktuální podmínky – mění se.
- Rozhodující je: **chceš vynutitelnou ochranu `main`? Pak veřejný repo** (nebo placený plán).

---

## 2. Stavba repozitáře od nuly (30–40 minut)

Tohle je recept, kterým vzniklo i tohle repo. Pořadí kroků není náhodné – každý další
potřebuje předchozí.

### 2.1 Lokální projekt a první commit

```bash
mkdir TextovaHra && cd TextovaHra
git init -b main
# ... soubory: game/, tests/, .github/, README.md, ZADANI.md ...
git add -A
git commit -m "chore: základní šablona textové hry, zadání a pravidla pro spolupráci"
```

`git init -b main` hned na začátku – ať nemusíš později přejmenovávat `master`.
Do prvního commitu dej **i `.gitattributes`** (`* text=auto eol=lf`), jinak se ti za týden
vrátí celý diff jen kvůli CRLF z Windows.

### 2.2 Založení repozitáře na GitHubu

```bash
gh repo create TextovaHra --public --source=. --remote=origin --push \
  --description "Šablona a zadání týmového projektu: textová hra v Pythonu"
```

Bez `--push` bys musel pushnout ručně. Zkontroluj, že `main` existuje a je tam první commit.

### 2.3 Struktura, která snese 23 autorů

Nejdůležitější architektonické rozhodnutí celého projektu: **jak zabránit konfliktům**.
Osvědčilo se:

- **registr příkazů** (`game/registry.py` + `game/commands/*.py`) – nový příkaz = nový soubor,
  žádná úprava společného seznamu,
- **oddělené testy po oblastech** (`tests/test_parser.py`, `test_movement.py`, …) – každý tým
  vlastní svůj soubor,
- **data v JSON** (`game/data/world.json`) – obsah mění i ti, kdo neumí Python,
- **uzamčené jádro** (`engine.py`, `registry.py`, `cli.py`) – mění se jen po domluvě s leadem.

Když tohle neuděláš, strávíš poslední hodinu řešením konfliktů místo učení. Podrobnosti
v [`ARCHITEKTURA.md`](ARCHITEKTURA.md).

### 2.4 CI (GitHub Actions)

Soubor `.github/workflows/tests.yml`. Tři věci, které se v praxi osvědčily:

1. **Jeden job, jedno jméno.** Job se jmenuje `tests` a přesně tenhle název pak použiješ
   v ochraně větve jako *required status check*. Když jméno nesedí, PR nejde sloučit a ty
   budeš 20 minut hledat proč.
2. **Bez matrix.** Matice `3.11/3.12/3.13` znamená tři checky a tři názvy. Pro výuku zbytečné.
3. **Rychlost.** `python -m compileall` + `python -m unittest` = 10 sekund. Studenti nemají
   čas čekat 4 minuty na CI.

```yaml
jobs:
  tests:
    name: tests          # tohle jméno = required check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: "3.12" }
      - run: python -m compileall -q game tests
      - run: python -m unittest discover -s tests -t . -v
```

**Pushni workflow dřív, než zapneš ochranu větve.** Required check, který ještě nikdy neproběhl,
blokuje všechny PR – a to i tvůj vlastní.

### 2.5 Ochrana `main` (ruleset)

```bash
bash scripts/setup_repo.sh
```

Skript vytvoří (nebo aktualizuje) ruleset `main-protection` ze souboru
[`../scripts/ruleset.json`](../scripts/ruleset.json). Co které pravidlo dělá:

| Pravidlo | Význam pro výuku |
|---|---|
| `deletion` | `main` nejde smazat omylem ani naschvál |
| `non_fast_forward` | žádný `push --force`, historie se nedá přepsat |
| `required_linear_history` | jen squash/rebase – čitelná historie pro review |
| `pull_request` (1 schválení) | každá změna projde review někoho jiného |
| `required_review_thread_resolution` | „vyřešeno“ musí být opravdu vyřešené |
| `allowed_merge_methods: squash` | jedno PR = jeden commit na `main` |
| `required_status_checks: tests` | červené CI = žádný merge |

**Nezapínej `require_code_owner_review`.** Jinak musíš osobně schválit všech 23 PR a hodina
se utopí v review. `CODEOWNERS` nech jako informaci („sem nešahej bez domluvy“).

**Bypass pro majitele.** V `ruleset.json` je `bypass_actors` s tvým uživatelským ID
(`gh api /user --jq .id`). Díky tomu můžeš v nouzi pushnout přímo do `main` nebo sloučit PR
bez schválení – studenti ne. Bez toho bys **nemohl sloučit ani svůj vlastní PR** (GitHub
nedovolí schválit vlastní PR) a při rozbitém `main` v 160. minutě bys byl bez východiska.

Ověření, že pravidla opravdu platí na větev:

```bash
gh api repos/TomasRacil/TextovaHra/rules/branches/main --jq '.[].type'
# deletion, non_fast_forward, required_linear_history, pull_request, required_status_checks
```

Ověření, že check má správné jméno:

```bash
gh api repos/TomasRacil/TextovaHra/commits/main/check-runs --jq '.check_runs[] | {name, conclusion}'
# {"name":"tests","conclusion":"success"}
```

### 2.6 Šablony, které dělají review použitelným

- `.github/PULL_REQUEST_TEMPLATE.md` – vynutí popis, kroky k vyzkoušení a checklist
  (testy, malý rozsah, žádné `print()`, diakritika). Bez něj dostaneš PR „oprava“ s 600 řádky.
- `.github/ISSUE_TEMPLATE/feature.md` – user story + akceptační kritéria. Studenti se učí
  formulovat zadání, ne jen kódit.
- `.github/ISSUE_TEMPLATE/bug.md` – kroky k reprodukci a traceback.
- `.github/CODEOWNERS` – seznam souborů, které mění jen majitel/lead.
- `.github/ISSUE_TEMPLATE/config.yml` – vypne prázdné issues a pošle dotazy do Discussions.

### 2.7 Štítky

Vytváří je `setup_repo.sh`: `typ: feat|fix|docs|test|chore`, `stav: blokováno|ke kontrole`,
`tým 1`–`tým 6`, `dobrý první úkol`, `potřebuje testy`.

Proč: studenti vidí stav práce bez ptaní a ty vidíš frontu (`stav: ke kontrole`).

### 2.8 Přístup studentů: spolupracovníci vs. forky

| | Spolupracovníci (doporučeno) | Forky |
|---|---|---|
| Nastavení | `bash scripts/invite_contributors.sh` + přijetí pozvánky | nic, student si forkne sám |
| Push | do vlastní větve v jednom repu | do svého forku |
| Synchronizace | `git pull` | `git fetch upstream && git merge upstream/main` |
| CI na PR | běží hned | u prvního PR čeká na schválení maintainera |
| Ochrana `main` | platí pro všechny | platí jen v tvém repu |
| Riziko | 23 lidí může zakládat větve (nevadí) | studenti zapomenou sync a žijí ve staré verzi |
| Kdy zvolit | výuka, uzavřená skupina | veřejný projekt, cizí přispěvatelé |

Pozvánky: `contributors.txt` (jeden login na řádek, `#` komentář) → `bash scripts/invite_contributors.sh`.
**Pozvat nestačí – student musí pozvánku přijmout**, jinak nemůže pushovat. Zkontroluj to
před hodinou:

```bash
gh api repos/TomasRacil/TextovaHra/invitations --jq '.[].invitee.login'   # nepotvrzené
gh api repos/TomasRacil/TextovaHra/collaborators --jq '.[].login'         # aktivní
```

### 2.9 Ověření před hodinou (5 minut, ušetří 30)

Projdi tenhle testovací scénář **jako student** (ideálně z druhého účtu, když ho máš):

- [ ] `git clone` + `python -m unittest discover -s tests -t . -v` → zelené.
- [ ] `python -m game` → hra nastartuje a `help` vypíše příkazy.
- [ ] Push do `main` → **odmítnuto** (`protected branch hook declined`).
- [ ] Větev + PR → CI se rozjede, PR je `BLOCKED` (chybí review).
- [ ] Schválení od jiného účtu → merge jde, squash.
- [ ] PR s rozbitým testem → merge **nejde**.
- [ ] Šablona PR a issue se opravdu zobrazí.

Když tohle projde, hodina nemá jak selhat na nastavení.

### 2.10 Board a release (10 minut navíc)

**Board (GitHub Projects)** je nástěnka nad issues – bez ní se 23 lidí ptá „co mám dělat?“.
Založení a propojení s repem:

```bash
gh project create --owner TomasRacil --title "TextovaHra – vývoj hry"
gh project link 3 --owner TomasRacil --repo TomasRacil/TextovaHra
bash scripts/seed_backlog.sh 3          # 12 draft items jako výchozí backlog
```

Sloupce stavu a vlastní pole (`Tým`, `Odhad`) se nastavují v UI nebo přes GraphQL –
v tomto repu už hotové. V projektu pak zapni **⋯ → Workflows**: *Auto-add to project*
a *Item closed → Done*, aby board nelhal.

**Release** je tag + GitHub Release s přiloženým balíčkem. Workflow
`.github/workflows/release.yml` se spustí jen na tag `v*`, pustí testy, sestaví wheel,
nainstaluje ho a hru spustí (důkaz, že balíček funguje), a teprve pak vytvoří release.

Vydání verze:

```bash
# 1. zvedni __version__ v game/__init__.py a prožeň to přes PR
git switch main && git pull
git tag -a v0.1.0 -m "Hratelná verze 0.1"
git push origin v0.1.0
```

Proč to učit a jak to vysvětlit studentům: [`PROJEKTY_A_RELEASE.md`](PROJEKTY_A_RELEASE.md).

---

## 3. Škálování: 23 lidí v jednom repozitáři

Tři pravidla, která drží projekt pohromadě:

1. **Vlastnictví souborů.** Každý tým má vypsané soubory, které vlastní (tabulka v
   `ZADANI.md`, kapitola 4). Cizí soubor = domluva s vlastníkem.
2. **Malé PR.** Do ~200 řádků. Velké PR se nerecenzuje, jen schvaluje naslepo – a to je
   horší než žádné review.
3. **Review napříč týmy.** Nikdo neschvaluje vlastní práci ani práci ze svého týmu.
   Šest reviewerů (jeden za tým) zvládne frontu 23 PR za hodinu.

Rozdělení 23 lidí: **6 týmů (4+4+4+4+4+3)** podle oblastí (parser, svět, předměty, postavy,
souboj, infrastruktura). Menší týmy (2–3) jsou pro review lepší než velké – v pěti lidech
se vždy najde někdo, kdo nic nedělá.

---

## 4. Facilitace 180 minut

| Čas | Co děláš ty | Na co si dát pozor |
|---|---|---|
| 0–15 | Ukázka PR cyklu na projektoru. Mluv o *proč* (historie, review, návratnost), ne o *jak*. | Neukazuj 12 git příkazů. Ukaž 5 a řekni, že zbytek je v `CONTRIBUTING.md`. |
| 15–35 | Ohranič volbu tématu (5 min), nech třídu zvolit leada, rozděl týmy podle tabulky v zadání. | Téma nesmí být „velkolepé“ – musí jít za 2 hodiny dohrát. Nabídni 3 hotové varianty. |
| 35–60 | Projdi prvních 5 PR osobně, ostatní nech na reviewerech. | Tady se láme hodina: kdo neudělá první PR do 60. minuty, nedělá ani druhý. |
| 60–100 | Sleduj frontu PR, ne kód. Blokery řeš hned. | Neopravuj studentům kód sám – pošli je za reviewrem nebo do issue. |
| 100 | Checkpoint: každý tým jedna věta „hotovo / blokuje“. | Zapiš blokery na tabuli, ať jsou vidět. |
| 100–140 | Triage PR (kapitola 5). Hlídej, aby nikdo nepracoval 40 minut bez commitu. | Dlouhé větve = konflikty. Připomeň `git pull` každých 20 minut. |
| 140–165 | Tester z každého týmu hraje hru. Chyby = issues, opravy = PR. | Nekritizuj design hry, jen funkčnost a proces. |
| 165–180 | Tag `v0.1`, retro (3 věty od každého týmu), domácí úkol. | Retro ve formátu: co fungovalo / co ne / jedna změna. |

**Prvních 15 minut rozhoduje.** Ukázka musí být naživo: založ větev, změň jeden řádek,
pushni, otevři PR, nech někoho schválit, sluč. Když to studenti vidí jednou celé, zvládnou
to sami. Když to jen popíšeš, strávíš pak 40 minut chozením od počítače k počítači.

---

## 5. Triage 23 PR (5–10 minut tvého času)

1. **Červené CI** → komentář autorovi, ať se podívá na log; neopravuj.
2. **Konflikt s `main`** → autor si musí pullnout `main` do své větve. To je učivo, ne otrava.
3. **PR bez testu** → „žádám změnu“ s odkazem na Definition of Done.
4. **PR s 500+ řádky** → požádej o rozdělení, jinak ho reviewer vzdá.
5. **Zbytek** → schvaluj rychle. Rychlé „schvaluji“ u čistých PR je pro třídu signál,
   že proces funguje.

Frontu si vyfiltruj:

```bash
gh pr list --label "stav: ke kontrole"
gh pr list --json number,title,author,mergeStateStatus,statusCheckRollup \
  --jq '.[] | "\(.number) \(.mergeStateStatus) \(.author.login) \(.title)"'
```

---

## 6. Hodnocení

Data ber z repozitáře, ne z dojmů:

```bash
gh pr list --state all --limit 100 --json number,title,author,state,additions,deletions
gh pr list --state merged --json number,author,reviews
gh issue list --state all --limit 100 --json number,title,assignees,state
```

| Položka | Body | Kde to najdeš |
|---|---|---|
| 4× kvalitní PR (malý rozsah, testy, popis) | 40 | `gh pr list --author <login>` |
| 2× review s konkrétními komentáři | 20 | `gh pr view <n> --json reviews,comments` |
| Funkčnost featury | 25 | zahrát hru, projít akceptační kritéria v issue |
| Kvalita testů | 10 | čtení `tests/` |
| Dokumentace | 5 | docstringy, `docs/` |

**Tvrdé podmínky:** 0 bez sloučeného PR; max 80 bez odevzdaného review. Řekni to studentům
v prvních 5 minutách – je to nejsilnější motivace k PR cyklu.

| Student | PR (počet / kvalita) | Review | Funkčnost | Testy | Docs | Σ |
|---|---|---|---|---|---|---|
| | | | | | | |

---

## 7. Údržba a další ročník

### Po hodině

- Zkontroluj, že `main` je zelený: `gh run list --limit 1` a
  `printf 'rozhledni\nkonec\n' | python -m game`.
- Založ issues pro věci, které se nestihly – studenti je dostanou jako domácí práci.
- Tag: `git tag -a v0.1 -m "Hratelná verze" && git push --tags`.
- Zapiš si nejčastější konflikt a nejčastější chybu v PR. Příští rok je z nich zadání.

### Z repa udělej šablonu (další ročník)

Nastavení → **Template repository**, nebo:

```bash
gh repo edit TomasRacil/TextovaHra --template
```

Pak studenti (nebo ty) zakládají nový repo tlačítkem **Use this template** – bez historie
a bez cizích větví. To je nejrychlejší cesta k dalšímu běhu výuky.

### Archivace běhu

Po skončení kurzu: **Settings → Archive this repository**. Repo zůstane čitelný, ale nikdo
do něj omylem nepushne. Pro výuku je lepší než mazání – studenti mají portfolio.

---

## 8. Když se něco pokazí

| Situace | Řešení |
|---|---|
| GitHub je nedostupný | Pracujte lokálně v `main` s ručním review u tabule; PR dodělejte příště. Cíle učení se tím neztratí. |
| Student nemá účet / nemůže přijmout pozvánku | Pracuje ve dvojici jako driver; jeho commity jdou přes spolužáka (do popisu PR patří, kdo co napsal). |
| Někdo pushne `main` a rozbije testy | `git revert` přes PR. Ideální okamžik vysvětlit, proč je revert lepší než „oprava potichu“. |
| `main` je rozbitý a nemáš čas na PR | Máš bypass: oprav, pushni, vysvětli. Nebo dočasně `enforcement: disabled` a hned zpět na `active`. |
| Nikdo nemůže sloučit PR | Zkontroluj jméno required checku (`tests`) a že CI na PR vůbec běží. |
| Třída se zasekne na jednom konfliktu | Vyřeš ho na projektoru, ale nech studenty diktovat postup. |
| Někdo nestíhá | Přesuň ho na dokumentaci nebo testy – práce, která jde udělat rychle a je vidět. |
| Někdo válcuje ostatní | Dej mu roli reviewera nebo mentora; výkon potřebuje jiný kanál než další featury. |

---

## 9. Tahák majitele

| Chci… | Příkaz |
|---|---|
| ověřit pravidla na `main` | `gh api repos/OWNER/REPO/rules/branches/main --jq '.[].type'` |
| vidět rulesety | `gh api repos/OWNER/REPO/rulesets --jq '.[] \| {name,enforcement}'` |
| vypnout/zapnout ochranu | `gh api -X PUT repos/OWNER/REPO/rulesets/ID -f enforcement=disabled` (pak `active`) |
| pozvat studenta | `gh api -X PUT repos/OWNER/REPO/collaborators/LOGIN -f permission=push` |
| nepotvrzené pozvánky | `gh api repos/OWNER/REPO/invitations --jq '.[].invitee.login'` |
| kdo co udělal | `gh pr list --state merged --json author,number --jq '.[] \| "\(.author.login) #\(.number)"'` |
| poslední běh CI | `gh run list --limit 5` |
| stav boardu | `gh project item-list 3 --owner TomasRacil --format json --jq '.items[] \| {title, status}'` |
| vydat verzi | `git tag -a v0.1.0 -m "Hratelná verze" && git push origin v0.1.0` |
| stáhnout release | `gh release download v0.1.0` |
| log neúspěšného CI | `gh run view ID --log-failed` |
| udělat z repa šablonu | `gh repo edit OWNER/REPO --template` |
| zjistit, co blokuje PR | `gh pr view N --json mergeStateStatus,statusCheckRollup` |

### Pasti, na které jsem narazil při stavbě (ušetři si je)

- **`gh api --input soubor.json` a MSYS cesty.** V git-bashi na Windows se `/c/...` cestuje
  špatně a `gh` spadne na „Systém nemůže nalézt uvedenou cestu“. Řešení: `--input - < soubor.json`
  (čte ze stdin, cesta se neřeší).
- **Required check, který nikdy neběžel,** zablokuje všechny PR. Pushni workflow první.
- **Vlastní PR nemůžeš schválit.** Bez `bypass_actors` si majitel sám zablokuje repo.
- **Jméno jobu = jméno required checku.** `tests` ≠ `Test` ≠ `pytest`.
- **CRLF.** Bez `.gitattributes` uvidíš v PR celý soubor jako změněný.
- **Pozvánka nestačí.** Dokud ji student nepřijme, nemá push právo a `git push` selže na 403.

---

## 10. Co bych příště udělal jinak

Až hodinu odučíš, doplň si sem tři věci, které tě překvapily. Tenhle dokument je pracovní –
nejcennější částí je kapitola 9, ne ta teoretická.
