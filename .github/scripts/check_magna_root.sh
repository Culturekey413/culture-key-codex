#!/usr/bin/env bash
set -euo pipefail

ROOT_TAG="v0.1-magna-root"
ROOT_DOC="docs/MAGNA_PROLOGUE.md"

echo "🔎 Scanning manifests for Magna Root link…"
fail=0
# Βρες όλα τα *_manifest.json κάτω από modules/
find modules -type f -name '*_manifest.json' -print0 | while IFS= read -r -d '' file; do
  # Αν exempt, skip
  if jq -e '.root_reference.exempt == true' "$file" >/dev/null 2>&1; then
    echo "↷ Skipping (exempt): $file"
    continue
  fi

  # Πάρε tag/doc
  tag=$(jq -r '.root_reference.tag // empty' "$file")
  doc=$(jq -r '.root_reference.document // empty' "$file")

  if [[ -z "$tag" || -z "$doc" || "$tag" != "$ROOT_TAG" || "$doc" != "$ROOT_DOC" ]]; then
    echo "❌ root_reference mismatch in $file (tag:'$tag' doc:'$doc') — expected tag:'$ROOT_TAG' doc:'$ROOT_DOC'"
    fail=1
  else
    echo "✅ ok: $file"
  fi
done

exit $fail
