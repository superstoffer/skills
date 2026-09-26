#!/usr/bin/env bash
# Report which Nuxt docs pages cited by the references changed since the
# bundle was distilled. Report only: it never edits a reference.
#
#   check-freshness.sh           compare live pages against sources.lock
#   check-freshness.sh --update  rewrite sources.lock from the live pages
#
# Exit 0: nothing changed. Exit 1: changes found. Exit 2: a fetch failed.
set -euo pipefail

dir="$(cd "$(dirname "$0")/.." && pwd)"
refs="$dir/references"
lock="$refs/sources.lock"
base="https://nuxt.com/raw/docs"

hash() { if command -v sha256sum >/dev/null; then sha256sum | cut -d' ' -f1; else shasum -a 256 | cut -d' ' -f1; fi; }

# Every cited page, e.g. "4.x/api/composables/use-fetch".
sources=$(grep -hoE '<!-- src: /docs/[^ ]+' "$refs"/*.md | sed 's#<!-- src: /docs/##; s/#.*//' | sort -u || true)

if [[ "${1:-}" == "--update" ]]; then
  tmp=$(mktemp)
  for s in $sources; do
    body=$(curl -sfL "$base/$s.md") || { echo "FETCH FAILED  $s" >&2; rm -f "$tmp"; exit 2; }
    printf '%s %s\n' "$s" "$(printf '%s' "$body" | hash)" >>"$tmp"
  done
  mv "$tmp" "$lock"
  echo "sources.lock: $(wc -l <"$lock" | tr -d ' ') pages recorded"
  exit 0
fi

[[ -f "$lock" ]] || { echo "no sources.lock — run with --update first" >&2; exit 2; }

changed=0 failed=0
for s in $sources; do
  if ! body=$(curl -sfL "$base/$s.md"); then
    echo "FETCH FAILED  $s"; failed=1; continue
  fi
  now=$(printf '%s' "$body" | hash)
  was=$(awk -v s="$s" '$1 == s { print $2 }' "$lock")
  if [[ -z "$was" ]]; then
    echo "NEW CITATION  $s"; changed=1
  elif [[ "$now" != "$was" ]]; then
    echo "CHANGED       $s"; changed=1
  fi
done

stamped=$(grep -hoE '^> Distilled for Nuxt [0-9.]+' "$refs"/*.md | head -1 | awk '{print $NF}')
if latest=$(npm view nuxt version 2>/dev/null); then
  [[ "$latest" != "${stamped:-}" ]] && changed=1
else
  echo "FETCH FAILED  npm nuxt@latest"
  latest=unknown
  failed=1
fi
echo "npm nuxt@latest: $latest · bundle distilled for: ${stamped:-unknown}"

(( failed )) && exit 2
(( changed )) && exit 1
echo "No cited page changed."
