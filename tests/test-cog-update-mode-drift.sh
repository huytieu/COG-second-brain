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
mkdir -p "$upstream/scripts"
printf '#!/usr/bin/env bash\necho executable fixture\n' > "$upstream/scripts/executable-helper.sh"
printf '#!/usr/bin/env bash\necho regular fixture\n' > "$upstream/scripts/regular-helper.sh"
chmod +x "$upstream/scripts/executable-helper.sh"
chmod -x "$upstream/scripts/regular-helper.sh"
git -C "$upstream" add scripts/executable-helper.sh scripts/regular-helper.sh
git -C "$upstream" commit -q -m "fixture: mixed file modes"

git init -q -b main "$consumer"
git -C "$consumer" remote add fixture "$upstream"
git -C "$consumer" fetch -q fixture main
mkdir -p "$consumer/scripts"
cp "$upstream/scripts/executable-helper.sh" "$consumer/scripts/executable-helper.sh"
cp "$upstream/scripts/regular-helper.sh" "$consumer/scripts/regular-helper.sh"
chmod -x "$consumer/scripts/executable-helper.sh"
chmod +x "$consumer/scripts/regular-helper.sh"

(
  cd "$consumer"
  # shellcheck disable=SC1090
  source <(sed '/^main "\$@"$/d' "$ROOT_DIR/cog-update.sh")
  REMOTE_NAME="fixture"
  BRANCH="main"

  if ! file_has_changes "scripts/executable-helper.sh"; then
    echo "expected file_has_changes to detect missing executable bit" >&2
    exit 1
  fi

  if ! file_has_changes "scripts/regular-helper.sh"; then
    echo "expected file_has_changes to detect unexpected executable bit" >&2
    exit 1
  fi
)

echo "cog-update detects mode-only drift in both directions"
