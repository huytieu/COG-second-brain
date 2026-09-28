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
output="$(cd "$consumer" && COG_UPSTREAM_URL="$upstream" bash cog-update.sh --force 2>&1)"
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

# Regression fixture: changed[] is empty and new_files[] is non-empty.
# Bash 3.2 with `set -u` rejects a bare "${changed[@]}" expansion in this state.
upstream_new="$TMP_DIR/upstream-new-only"
consumer_new="$TMP_DIR/consumer-new-only"

git init -q -b main "$upstream_new"
git -C "$upstream_new" config user.name "COG Test"
git -C "$upstream_new" config user.email "cog-test@example.invalid"
printf '1.0.0\n' > "$upstream_new/COG-VERSION"
printf 'same readme\n' > "$upstream_new/README.md"
printf 'brand new setup\n' > "$upstream_new/SETUP.md"
git -C "$upstream_new" add COG-VERSION README.md SETUP.md
git -C "$upstream_new" commit -q -m "fixture: new file only"

git init -q -b main "$consumer_new"
git -C "$consumer_new" config user.name "COG Test"
git -C "$consumer_new" config user.email "cog-test@example.invalid"
cp "$ROOT_DIR/cog-update.sh" "$consumer_new/cog-update.sh"
printf '1.0.0\n' > "$consumer_new/COG-VERSION"
printf 'same readme\n' > "$consumer_new/README.md"
git -C "$consumer_new" add cog-update.sh COG-VERSION README.md
git -C "$consumer_new" commit -q -m "fixture: consumer missing one framework file"
git -C "$consumer_new" remote add cog-upstream "$upstream_new"

set +e
new_only_output="$(cd "$consumer_new" && COG_UPSTREAM_URL="$upstream_new" bash cog-update.sh --force 2>&1)"
new_only_status=$?
set -e

if [[ $new_only_status -ne 0 ]]; then
  echo "expected --force to handle an empty changed[] array with only new framework files" >&2
  echo "$new_only_output" >&2
  exit 1
fi

if [[ "$(cat "$consumer_new/SETUP.md")" != "brand new setup" ]]; then
  echo "SETUP.md was not created in the new-file-only force-mode case" >&2
  exit 1
fi

force_loop=$(grep -F 'for f in ' "$ROOT_DIR/cog-update.sh" | grep 'changed' | grep 'new_files' | head -n 1 || true)
if [[ "$force_loop" != *'${changed:+'* || "$force_loop" != *'${new_files:+'* ]]; then
  echo "force-mode iteration must guard both arrays for Bash 3.2 nounset compatibility" >&2
  exit 1
fi

echo "cog-update --force handles changed files and the new-file-only Bash 3.2 compatibility case"
