#!/usr/bin/env bash
set -euo pipefail

ROOT_TAG="v0.1-magna-root"
ROOT_DOC="docs/MAGNA_PROLOGUE.md"

fail=0
echo "🔎 Scanning manifests for Magna Root link…"

# Βρες όλα τα manifests κάτω από modules/
while IFS= read -r -d '' file; do
  # Αν έχει ρητή εξαίρεση, αγνόησέ το (π.χ. για internal βοηθητικά)
  if jq -e '.root_reference.exempt == true' "$file" > /dev/null 2>&1; then
    echo "⏭  Skipping (exempt): $file"
    continue
  fi

  tag=$(jq -r '.root_reference.tag // empty' "$file")
  doc=$(jq -r '.root_reference.document // empty' "$file")

  if [[ "$tag" != "$ROOT_TAG" || "$doc" != "$ROOT_DOC" ]]; then
    echo "::error file=$file::root_reference mismatch (tag:'${tag:-∅}' doc:'${doc:-∅}'). Expect tag='$ROOT_TAG' & document='$ROOT_DOC'."
    fail=1
  else
    echo "✅ OK: $file"
  fi
done < <(find modules -type f -name "*manifest.json" -print0)

if [[ $fail -ne 0 ]]; then
  echo "❌ Some manifests are not linked to the Magna Root."
  exit 1
fi

echo "🌕 All manifests correctly linked to Magna Root."
