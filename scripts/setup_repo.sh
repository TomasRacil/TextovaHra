#!/usr/bin/env bash
# Nastaví repozitář pro týmovou výuku: ochranu větve main a štítky.
#
# Použití:
#   bash scripts/setup_repo.sh                  # použije aktuální repo (gh repo view)
#   bash scripts/setup_repo.sh OWNER/REPO
#
# Vyžaduje: gh (přihlášený), oprávnění admin na repozitáři.
# Opakované spuštění je bezpečné – pravidlo se aktualizuje, štítky přepíšou.

set -euo pipefail

REPO="${1:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RULESET_FILE="$HERE/ruleset.json"

echo "== Repozitář: $REPO =="

visibility="$(gh repo view "$REPO" --json visibility -q .visibility)"
echo "Viditelnost: $visibility"
if [ "$visibility" != "PUBLIC" ]; then
  echo "POZOR: na Free plánu GitHubu fungují rulesets jen u veřejných repozitářů."
  echo "       U privátního repa pravidlo vznikne, ale nebude vynucené."
fi

# --- 1. Pravidlo pro main -----------------------------------------------------
echo
echo "== Ochrana větve main =="
existing_id="$(gh api "repos/$REPO/rulesets" --jq '.[] | select(.name=="main-protection") | .id' 2>/dev/null || true)"

if [ -n "$existing_id" ]; then
  echo "Pravidlo existuje (id $existing_id), aktualizuji."
  gh api -X PUT "repos/$REPO/rulesets/$existing_id" --input - < "$RULESET_FILE" >/dev/null
else
  echo "Vytvářím pravidlo main-protection."
  gh api -X POST "repos/$REPO/rulesets" --input - < "$RULESET_FILE" >/dev/null
fi

gh api "repos/$REPO/rulesets" --jq '.[] | "  \(.name): \(.enforcement)"'

# --- 2. Štítky ----------------------------------------------------------------
echo
echo "== Štítky =="

make_label() {
  local name="$1" color="$2" desc="$3"
  gh label create "$name" --color "$color" --description "$desc" --force >/dev/null 2>&1 \
    && echo "  ok  $name" \
    || echo "  --  $name (přeskočeno)"
}

make_label "typ: feat"         "0e8a16" "Nová funkce pro hráče"
make_label "typ: fix"          "d73a4a" "Oprava chyby"
make_label "typ: docs"         "0075ca" "Dokumentace"
make_label "typ: test"         "5319e7" "Testy"
make_label "typ: chore"        "ededed" "Úklid, konfigurace"
make_label "stav: blokováno"   "b60205" "Někdo na něco čeká"
make_label "stav: ke kontrole" "fbca04" "Připraveno k review"
make_label "dobrý první úkol"  "7057ff" "Vhodné pro začátečníka"
make_label "potřebuje testy"   "d4c5f9" "Chybí test k nové logice"
make_label "tým 1"             "1d76db" "Parser a příkazy"
make_label "tým 2"             "0e8a16" "Svět a mapa"
make_label "tým 3"             "fbca04" "Předměty a inventář"
make_label "tým 4"             "d93f0b" "Postavy a dialogy"
make_label "tým 5"             "5319e7" "Souboj a stav hráče"
make_label "tým 6"             "006b75" "Ukládání, UI, dokumentace"

# --- 3. Shrnutí ---------------------------------------------------------------
echo
echo "== Hotovo =="
echo "Zkontroluj v nastavení repozitáře: Settings → Rules → Rulesets."
echo "Dále: bash scripts/invite_students.sh  (potřebuje vyplněný students.txt)"
