#!/usr/bin/env bash
# Naplní GitHub Project výchozím backlogem (draft items = nejsou to issues).
# Studenti si položky převezmou a převedou na issue ("Convert to issue").
#
# Použití:
#   bash scripts/seed_backlog.sh                 # owner TomasRacil, projekt 3
#   bash scripts/seed_backlog.sh OWNER CISLO
#
# Pozor: opakované spuštění vytvoří duplicity. Pouštěj jednou na začátku kurzu.

set -euo pipefail

OWNER="${1:-TomasRacil}"
PROJECT="${2:-3}"

echo "== Projekt $PROJECT vlastníka $OWNER =="
created=0

# ID projektu, pole Status a volby "Backlog" – aby nové položky neseděly bez stavu.
PROJECT_ID="$(gh project view "$PROJECT" --owner "$OWNER" --format json --jq '.id' 2>/dev/null || true)"
STATUS_FIELD_ID=""
BACKLOG_ID=""
if [ -n "$PROJECT_ID" ]; then
  STATUS_FIELD_ID="$(gh api graphql -f query='query($p:ID!){node(id:$p){... on ProjectV2{field(name:"Status"){... on ProjectV2SingleSelectField{id}}}}}' \
    -F p="$PROJECT_ID" --jq '.data.node.field.id' 2>/dev/null || true)"
  BACKLOG_ID="$(gh api graphql -f query='query($p:ID!){node(id:$p){... on ProjectV2{field(name:"Status"){... on ProjectV2SingleSelectField{options{id name}}}}}}' \
    -F p="$PROJECT_ID" --jq '.data.node.field.options[] | select(.name=="Backlog") | .id' 2>/dev/null || true)"
fi

add_item() {
  local title="$1" body="$2" item_id
  item_id="$(gh project item-create "$PROJECT" --owner "$OWNER" --title "$title" \
    --body "$(printf '%b' "$body")" --format json --jq '.id')"
  if [ -n "$STATUS_FIELD_ID" ] && [ -n "$BACKLOG_ID" ]; then
    gh project item-edit --project-id "$PROJECT_ID" --id "$item_id" \
      --field-id "$STATUS_FIELD_ID" --single-select-option-id "$BACKLOG_ID" >/dev/null 2>&1 || true
  fi
  echo "  + $title"
  created=$((created + 1))
}

# --- Povinné jádro (MVP) ------------------------------------------------------
add_item "Parser: příkaz + argument" "Rozdělí řádek na sloveso a zbytek. Nerozlišuje velikost písmen, funguje i bez diakritiky.\n\nKritéria:\n- 'JDI sever' a 'jdi sever' dělají totéž\n- neznámý příkaz nespadne, ale poradí 'help'\n- tým 1"

add_item "Pohyb: jdi <směr>" "Přesun mezi místnostmi podle východů v world.json.\n\nKritéria:\n- platný směr změní room_key\n- neplatný směr vrátí vysvětlení a hráče nechá na místě\n- test v tests/test_movement.py prochází\n- tým 2"

add_item "Rozhlédnutí: rozhledni" "Popíše aktuální místnost, východy a předměty. Už hotové v game/commands/basic.py – rozšiřte podle tématu.\n\nKritéria:\n- vypíše název, popis, východy, předměty\n- prázdné seznamy se nevypisují jako 'None'\n- tým 2"

add_item "Předměty: vezmi / polož / použij / batoh" "Manipulace s předměty mezi místností a batohem.\n\nKritéria:\n- vezmi přesune předmět do batohu, v místnosti zmizí\n- polož ho vrátí zpět\n- vezmi neexistující předmět vrátí hlášku, ne výjimku\n- batoh vypíše obsah\n- tým 3"

add_item "Stav hráče: zdraví a smrt" "Player.damage/heal/is_alive, smrt ukončí hru.\n\nKritéria:\n- hp neklesne pod 0 a nepřeteče přes max_hp\n- is_alive vrací False při hp == 0\n- hra při smrti oznámí konec\n- tým 5"

add_item "NPC a dialogy" "Alespoň jedna postava, se kterou lze mluvit; reakce na klíčové slovo nebo předmět.\n\nKritéria:\n- 'mluv <jméno>' vrátí dialog z datového souboru\n- neznámá postava vrátí hlášku\n- texty jsou v JSON, ne v kódu\n- tým 4"

add_item "Konec hry: výhra a prohra" "Jasná podmínka, kdy hra skončí dobře a kdy špatně.\n\nKritéria:\n- hráč se dozví, že vyhrál/prohrál, a proč\n- po konci hry nejde pokračovat\n- tým 5"

add_item "Uložení a načtení hry" "uloz / nacti do JSON souboru.\n\nKritéria:\n- uloží polohu, batoh, hp\n- nacti obnoví stav\n- chybějící soubor = srozumitelná hláška\n- tým 6"

add_item "Nápověda z registru" "help vypíše příkazy z COMMANDS, ne ručně psaný seznam.\n\nKritéria:\n- nový příkaz se v help objeví automaticky\n- seznam je seřazený\n- tým 1"

add_item "Hratelnost od začátku do konce" "Tester projde hru bez zásahu do kódu.\n\nKritéria:\n- start → cíl je dosažitelný\n- nikde není slepá ulička bez vysvětlení\n- tým 6 + všichni testeři"

# --- Volitelné -----------------------------------------------------------------
add_item "Mapa (ASCII)" "Příkaz 'mapa' vykreslí prozkoumané místnosti a polohu hráče.\n\nVolitelné, až po MVP. Tým 2."

add_item "Soubojový systém" "Souboj s NPC: kolo, útok, obrana, smrt.\n\nVolitelné, až po MVP. Tým 5."

echo
echo "Vytvořeno položek: $created"
echo "Board: gh project view $PROJECT --owner $OWNER --web"
