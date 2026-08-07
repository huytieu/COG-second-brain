#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

upstream="$TMP_DIR/upstream"
consumer="$TMP_DIR/consumer"

git init -q -b main "$upstream"
git -C "$upstream" config user.name "COG Test"
git -C "$upstream" config user.email "cog-test@example.invalid"
printf '9.9.9\n' > "$upstream/COG-VERSION"
printf 'new readme\n' > "$upstream/README.md"
printf 'new setup\n' > "$upstream/SETUP.md"
git -C "$upstream" add COG-VERSION README.md SETUP.md
git -C "$upstream" commit -q -m "fixture: upstream update"

git init -q -b main "$consumer"
git -C "$consumer" config user.name "COG Test"
git -C "$consumer" config user.email "cog-test@example.invalid"
cp "$ROOT_DIR/cog-update.sh" "$consumer/cog-update.sh"
printf '1.0.0\n' > "$consumer/COG-VERSION"
printf 'old readme\n' > "$consumer/README.md"
printf 'old setup\n' > "$consumer/SETUP.md"
git -C "$consumer" add cog-update.sh COG-VERSION README.md SETUP.md
git -C "$consumer" commit -q -m "fixture: consumer state"
git -C "$consumer" remote add cog-upstream "$upstream"

set +e
output="$(cd "$consumer" && bash cog-update.sh --force 2>&1)"
status=$?
set -e

if [[ $status -ne 0 ]]; then
  echo "expected --force to update all changed files and exit successfully" >&2
  echo "$output" >&2
  exit 1
fi

if [[ "$(cat "$consumer/README.md")" != "new readme" ]]; then
  echo "README.md was not updated" >&2
  exit 1
fi

if [[ "$(cat "$consumer/SETUP.md")" != "new setup" ]]; then
  echo "SETUP.md was not updated" >&2
  exit 1
fi

if [[ "$(tr -d '[:space:]' < "$consumer/COG-VERSION")" != "9.9.9" ]]; then
  echo "COG-VERSION was not updated" >&2
  exit 1
fi

echo "cog-update --force updates multiple files under set -e"
