#!/usr/bin/env bash
# Pozve spolupracovníky ze souboru contributors.txt (právo push).
#
# Použití:
#   bash scripts/invite_contributors.sh                 # aktuální repo
#   bash scripts/invite_contributors.sh OWNER/REPO
#   bash scripts/invite_contributors.sh --dry-run       # jen vypíše, co by udělal
#
# Formát contributors.txt: jeden GitHub login na řádek, # = komentář.
# Pozvánku musí člověk přijmout (e-mailem nebo na github.com/notifications),
# jinak nemůže pushovat.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIST="$HERE/../contributors.txt"
DRY_RUN=0
REPO=""

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY_RUN=1 ;;
    *) REPO="$arg" ;;
  esac
done

REPO="${REPO:-$(gh repo view --json nameWithOwner -q .nameWithOwner)}"

if [ ! -f "$LIST" ]; then
  echo "Chybí $LIST" >&2
  exit 1
fi

echo "== Repozitář: $REPO =="
echo "== Seznam: $LIST =="
[ "$DRY_RUN" -eq 1 ] && echo "== REŽIM NÁHLEDU (nic se neodešle) =="
echo

invited=0
failed=0

while IFS= read -r raw || [ -n "$raw" ]; do
  line="${raw%%#*}"                       # odřízni komentář
  login="$(printf '%s' "$line" | tr -d '[:space:]')"
  [ -z "$login" ] && continue

  if [ "$DRY_RUN" -eq 1 ]; then
    echo "  [náhled] pozvat: $login"
    invited=$((invited + 1))
    continue
  fi

  if gh api -X PUT "repos/$REPO/collaborators/$login" -f permission=push >/dev/null 2>&1; then
    echo "  ok      $login"
    invited=$((invited + 1))
  else
    echo "  CHYBA   $login (neexistující účet, nebo nemáš právo admin?)"
    failed=$((failed + 1))
  fi
done < "$LIST"

echo
echo "Pozváno: $invited, chyb: $failed"
echo "Stav pozvánek: gh api repos/$REPO/invitations --jq '.[].invitee.login'"
echo "Přijatí spolupracovníci: gh api repos/$REPO/collaborators --jq '.[].login'"
