# Průvodce pro učitele

Učitelská část: nastavení repozitáře, facilitace 180 minut, hodnocení, záložní plány.
Studentská verze zadání je v [`../ZADANI.md`](../ZADANI.md).

---

## 1. Checklist před hodinou

- [ ] Repozitář `TomasRacil/TextovaHra` existuje a je **veřejný** (na Free plánu jde chránit
      jen veřejné repozitáře; privátní by ochranu `main` neměl).
- [ ] Větev `main` má pravidlo `main-protection` (PR + 1 schválení + CI + lineární historie).
- [ ] CI proběhlo aspoň jednou zeleně (jinak pravidlo blokuje i první PR).
- [ ] Štítky vytvořené (`scripts/setup_repo.sh`).
- [ ] Studenti pozvaní jako spolupracovníci a **pozvánku přijali** (pozvat nestačí).
- [ ] Každý student umí `git clone` + spustit `python -m unittest` – ověřeno před hodinou
      nebo v prvních 10 minutách.
- [ ] Na projektoru máš připravený jeden „ukázkový PR“ (ideálně svůj, malý, už sloučený),
      abys na začátku ukázal celý cyklus naživo.
- [ ] Máš otevřený `gh` nebo web GitHubu na tabuli s pull requesty.
- [ ] Víš, kdo bude projekt lead (nebo necháš volbu na třídě – pak ji ohranič 5 minutami).

## 2. Nastavení repozitáře

Repozitář je založený a nakonfigurovaný. Když ho potřebuješ postavit znovu (nový ročník,
jiný účet), stačí:

```bash
# založení a první push
gh repo create TextovaHra --public --source=. --remote=origin --push

# ochrana main + štítky
bash scripts/setup_repo.sh

# pozvánky studentů (seznam loginů v students.txt)
bash scripts/invite_students.sh
```

Kontrola, že pravidlo existuje:

```bash
gh api repos/TomasRacil/TextovaHra/rulesets --jq '.[] | {name, enforcement}'
gh api repos/TomasRacil/TextovaHra/rulesets/$(gh api repos/TomasRacil/TextovaHra/rulesets --jq '.[0].id')
```

### Co pravidlo `main-protection` dělá

| Pravidlo | Význam pro výuku |
|---|---|
| `deletion` | `main` nejde smazat omylem ani naschvál |
| `non_fast_forward` | žádný `push --force`, historie se nedá přepsat |
| `required_linear_history` | jen squash/rebase – čitelná historie pro review |
| `pull_request` (1 schválení) | každá změna projde review někoho jiného |
| `required_review_thread_resolution` | „vyřešeno“ musí být opravdu vyřešené |
| `allowed_merge_methods: squash` | jedno PR = jeden commit na `main` |
| `required_status_checks: tests` | červené CI = žádný merge |

**Nezapínej** `require_code_owner_review` – jinak budeš muset schválit všech 23 PR osobně
a hodina se utopí v review. `CODEOWNERS` nech jako informaci („sem nešahej bez domluvy“).

### Volitelné, ale užitečné

- **Discussions** zapnuté – otázky k postupu nepatří do issues.
- **Projects** (board) – studenti si sami přetahují issues, učí se plánovat.
- **Tag `v0.1`** na konci hodiny: `git tag -a v0.1 -m "Hratelná verze" && git push --tags`.

## 3. Facilitace 180 minut

| Čas | Co děláš ty | Na co si dát pozor |
|---|---|---|
| 0–15 | Ukázka PR cyklu na projektoru. Mluv o *proč* (historie, review, návratnost), ne o *jak*. | Neukazuj 12 git příkazů. Ukaž 5 a řekni, že zbytek je v `CONTRIBUTING.md`. |
| 15–35 | Ohranič volbu tématu (5 min), nech třídu zvolit leada, rozděl týmy podle tabulky v zadání. | Téma nesmí být „velkolepé“ – musí jít za 2 hodiny dohrát. Nabídni 3 hotové varianty. |
| 35–60 | Projdi prvních 5 PR osobně, ostatní nech na reviewerech. | Tady se láme hodina: kdo neudělá první PR do 60. minuty, nedělá ani druhý. |
| 60–100 | Sleduj frontu PR, ne kód. Blokery řeš hned. | Neopravuj studentům kód sám – pošli je za reviewrem nebo do issue. |
| 100 | Checkpoint: každý tým jedna věta „hotovo / blokuje“. | Zapiš blokery na tabuli, ať jsou vidět. |
| 100–140 | Triage PR (viz níže). Hlídej, aby nikdo nepracoval 40 minut bez commitu. | Dlouhé větve = konflikty. Připomeň `git pull` každých 20 minut. |
| 140–165 | Tester z každého týmu hraje hru. Chyby = issues, opravy = PR. | Nekritizuj design hry, jen funkčnost a proces. |
| 165–180 | Tag `v0.1`, retro (3 věty od každého týmu), domácí úkol. | Retro ve formátu: co fungovalo / co ne / jedna změna. |

### Triage 23 PR (5–10 minut tvého času)

1. **Červené CI** → komentář autorovi, ať se podívá na log; neopravuj.
2. **Konflikt s `main`** → autor si musí pullnout `main` do své větve. To je učivo, ne otrava.
3. **PR bez testu** → „žádám změnu“ s odkazem na Definition of Done.
4. **PR s 500+ řádky** → požádej o rozdělení, jinak ho reviewer vzdá.
5. **Zbytek** → schvaluj rychle. Rychlé „schvaluji“ u čistých PR je pro třídu signál,
   že proces funguje.

Rozděl roli: **6 reviewerů** (jeden za tým) smí schvalovat PR z jiných týmů. Ty schvaluješ
jen změny ve sdílených souborech a sporné případy.

## 4. Hodnocení

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

Rychlá evidence do tabulky:

| Student | PR (počet / kvalita) | Review | Funkčnost | Testy | Docs | Σ |
|---|---|---|---|---|---|---|
| | | | | | | |

## 5. Když se něco pokazí

| Situace | Řešení |
|---|---|
| GitHub je nedostupný | Pracujte lokálně v `main` s ručním review u tabule; PR dodělejte příště. Cíle učení se tím neztratí. |
| Student nemá účet / nemůže přijmout pozvánku | Pracuje ve dvojici jako driver; jeho commity jdou přes spolužáka (do popisu PR patří, kdo co napsal). |
| Někdo pushne `main` a rozbije testy | `git revert` přes PR. Je to ideální okamžik vysvětlit, proč je revert lepší než „oprava potichu“. |
| Třída se zasekne na jednom konfliktu | Vyřeš ho na projektoru, ale nech studenty diktovat postup. |
| Někdo nestíhá | Přesuň ho na dokumentaci nebo testy – práce, která jde udělat rychle a je vidět. |
| Někdo naopak válcuje ostatní | Dej mu roli reviewera nebo mentora; výkon potřebuje jiný kanál než další featury. |

## 6. Po hodině

- Zkontroluj, že `main` je zelený a hra se dá dohrát (`printf 'rozhledni\nkonec\n' | python -m game`).
- Založ issues pro věci, které se nestihly – studenti je dostanou jako domácí práci.
- Zapiš si, co zopakovat příště (nejčastější konflikt, nejčastější chyba v PR).
- Pošli studentům odkaz na `v0.1` a na seznam jejich PR – zpětná vazba má být vidět.
