#!/usr/bin/env bash
# Udělí lidem z contributors.txt právo WRITER na GitHub Project (board).
#
# Proč to je potřeba: přístup do repozitáře a přístup k projektu jsou DVĚ oddělené věci.
# Kdo je spolupracovník v repu, ještě nevidí privátní projekt. Buď ho přidáš ručně
# v UI (Project → ⋯ → Settings → Manage access), nebo tímhle skriptem.
#
# Použití:
#   bash scripts/grant_project_access.sh              # owner TomasRacil, projekt 3
#   bash scripts/grant_project_access.sh OWNER CISLO
#   bash scripts/grant_project_access.sh --dry-run

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIST="$HERE/../contributors.txt"
DRY_RUN=0
OWNER="TomasRacil"
PROJECT="3"

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) if [ -z "${OWNER_SET:-}" ]; then OWNER="$arg"; OWNER_SET=1; else PROJECT="$arg"; fi ;;
  esac
done

if [ ! -f "$LIST" ]; then
  echo "Chybí $LIST" >&2
  exit 1
fi

PROJECT_ID="$(gh project view "$PROJECT" --owner "$OWNER" --format json --jq '.id')"
echo "== Projekt $PROJECT ($PROJECT_ID) vlastníka $OWNER =="
[ "$DRY_RUN" -eq 1 ] && echo "== REŽIM NÁHLEDU =="
echo

granted=0
failed=0
total=0

while IFS= read -r raw || [ -n "$raw" ]; do
  line="${raw%%#*}"
  login="$(printf '%s' "$line" | tr -d '[:space:]')"
  [ -z "$login" ] && continue

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "  [náhled] WRITER: $login"
    granted=$((granted + 1))
    continue
  fi

  node="$(gh api "users/$login" --jq .node_id 2>/dev/null || true)"
  if [ -z "$node" ]; then
    echo "  CHYBA   $login (účet nenalezen)"
    failed=$((failed + 1))
    continue
  fi

  total="$(gh api graphql \
    -f query='mutation($p: ID!, $u: ID!) { updateProjectV2Collaborators(input: {projectId: $p, collaborators: [{userId: $u, role: WRITER}]}) { collaborators { totalCount } } }' \
    -f p="$PROJECT_ID" -f u="$node" \
    --jq '.data.updateProjectV2Collaborators.collaborators.totalCount' 2>/dev/null || true)"

  if [ -n "$total" ]; then
    echo "  ok      $login (celkem v projektu: $total)"
    granted=$((granted + 1))
  else
    echo "  CHYBA   $login"
    failed=$((failed + 1))
  fi
done < "$LIST"

echo
echo "Přidáno: $granted, chyb: $failed"
echo "Kontrola: otevři board v anonymním okně – bez přihlášení nesmí být vidět."
