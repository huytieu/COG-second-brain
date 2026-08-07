#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

failures=0

fail() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

make_repo() {
  local path="$1"
  git init -q -b main "$path"
  git -C "$path" config user.name "COG Test"
  git -C "$path" config user.email "cog-test@example.invalid"
}

# Regression 1: an existing cog-upstream remote must not silently redirect updates.
untrusted="$TMP_DIR/untrusted-upstream"
consumer="$TMP_DIR/consumer"
make_repo "$untrusted"
printf '9.9.9\n' > "$untrusted/COG-VERSION"
printf 'untrusted readme\n' > "$untrusted/README.md"
git -C "$untrusted" add COG-VERSION README.md
git -C "$untrusted" commit -q -m "fixture: untrusted upstream"

make_repo "$consumer"
cp "$ROOT_DIR/cog-update.sh" "$consumer/cog-update.sh"
printf '1.0.0\n' > "$consumer/COG-VERSION"
printf 'local readme\n' > "$consumer/README.md"
git -C "$consumer" add cog-update.sh COG-VERSION README.md
git -C "$consumer" commit -q -m "fixture: consumer"
git -C "$consumer" remote add cog-upstream "$untrusted"

set +e
remote_output="$(cd "$consumer" && bash cog-update.sh --force 2>&1)"
remote_status=$?
set -e

if [[ $remote_status -eq 0 ]]; then
  fail "updater trusted a pre-existing cog-upstream remote with an unexpected URL: $remote_output"
fi
if [[ "$(cat "$consumer/README.md")" != "local readme" ]]; then
  fail "untrusted remote changed README.md before trust validation: $remote_output"
fi
if [[ "$(tr -d '[:space:]' < "$consumer/COG-VERSION")" != "1.0.0" ]]; then
  fail "untrusted remote changed COG-VERSION before trust validation: $remote_output"
fi

# Regression 2: sourced write helpers must fail closed until REPO_ROOT is initialized.
fixture="$TMP_DIR/helper-upstream"
helper_consumer="$TMP_DIR/helper-consumer"
make_repo "$fixture"
mkdir -p "$fixture/scripts"
printf '#!/usr/bin/env bash\necho fixture\n' > "$fixture/scripts/owned.sh"
chmod +x "$fixture/scripts/owned.sh"
git -C "$fixture" add scripts/owned.sh
git -C "$fixture" commit -q -m "fixture: helper"

make_repo "$helper_consumer"
git -C "$helper_consumer" remote add fixture "$fixture"
git -C "$helper_consumer" fetch -q fixture main

set +e
helper_output="$( (
  cd "$helper_consumer"
  # shellcheck disable=SC1090
  source <(sed '/^main "\$@"$/d' "$ROOT_DIR/cog-update.sh")
  REMOTE_NAME="fixture"
  BRANCH="main"
  REPO_ROOT=""
  update_file "scripts/owned.sh"
) 2>&1 )"
helper_status=$?
set -e

if [[ $helper_status -eq 0 ]]; then
  fail "sourced update_file succeeded with an uninitialized REPO_ROOT: $helper_output"
fi
if [[ -e "$helper_consumer/scripts/owned.sh" ]]; then
  fail "sourced update_file created a framework file before repository-root initialization: $helper_output"
fi

if [[ $failures -gt 0 ]]; then
  echo "$failures updater trust-boundary regression(s) remain" >&2
  exit 1
fi

echo "cog-update rejects untrusted remotes and uninitialized write-helper roots"
