#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

failures=0
future_file="FUTURE-FRAMEWORK.md"
skip_message="Updater changed while some framework files were skipped. Run cog-update.sh again to load the new framework file list without replaying skipped choices."

fail() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

make_upstream() {
  local path="$1"
  git init -q -b main "$path"
  git -C "$path" config user.name "COG Test"
  git -C "$path" config user.email "cog-test@example.invalid"
  cp "$ROOT_DIR/cog-update.sh" "$path/cog-update.sh"
  python3 - "$path/cog-update.sh" "$future_file" <<'PY'
from pathlib import Path
import sys

path = Path(sys.argv[1])
future = sys.argv[2]
text = path.read_text(encoding="utf-8")
marker = '  "COG-VERSION"\n'
addition = f'  "{future}"\n'
if text.count(marker) != 1:
    raise SystemExit("fixture could not find unique FRAMEWORK_FILES marker")
path.write_text(text.replace(marker, marker + addition, 1), encoding="utf-8")
PY
  chmod +x "$path/cog-update.sh"
  printf '9.9.9\n' > "$path/COG-VERSION"
  printf 'future framework asset\n' > "$path/$future_file"
  git -C "$path" add cog-update.sh COG-VERSION "$future_file"
  git -C "$path" commit -q -m "fixture: upstream adds a newly tracked framework file"
}

make_consumer() {
  local path="$1"
  local upstream="$2"
  git init -q -b main "$path"
  git -C "$path" config user.name "COG Test"
  git -C "$path" config user.email "cog-test@example.invalid"
  cp "$ROOT_DIR/cog-update.sh" "$path/cog-update.sh"
  printf '1.0.0\n' > "$path/COG-VERSION"
  git -C "$path" add cog-update.sh COG-VERSION
  git -C "$path" commit -q -m "fixture: consumer before updater self-refresh"
  git -C "$path" remote add cog-upstream "$upstream"
}

# Regression 1: force mode must restart once after updating cog-update.sh so the new list is honored.
force_upstream="$TMP_DIR/force-upstream"
force_consumer="$TMP_DIR/force-consumer"
make_upstream "$force_upstream"
make_consumer "$force_consumer" "$force_upstream"

set +e
force_output="$(cd "$force_consumer" && COG_UPSTREAM_URL="$force_upstream" bash cog-update.sh --force 2>&1)"
force_status=$?
set -e

if [[ $force_status -ne 0 ]]; then
  fail "--force self-refresh failed (status=$force_status): $force_output"
elif [[ ! -f "$force_consumer/$future_file" ]]; then
  fail "--force reported success after updating itself but did not install the newly tracked framework file: $force_output"
fi

# Regression 2: interactive mode with no skips must also continue under the updated file list.
interactive_upstream="$TMP_DIR/interactive-upstream"
interactive_consumer="$TMP_DIR/interactive-consumer"
make_upstream "$interactive_upstream"
make_consumer "$interactive_consumer" "$interactive_upstream"

set +e
interactive_output="$(cd "$interactive_consumer" && printf '\n\n\n\n' | COG_UPSTREAM_URL="$interactive_upstream" bash cog-update.sh 2>&1)"
interactive_status=$?
set -e

if [[ $interactive_status -ne 0 ]]; then
  fail "interactive self-refresh failed (status=$interactive_status): $interactive_output"
elif [[ ! -f "$interactive_consumer/$future_file" ]]; then
  fail "interactive update reported success after updating itself but did not install the newly tracked framework file: $interactive_output"
fi

# Regression 3: if the user skipped anything before updating the updater, do not replay those choices automatically.
skip_upstream="$TMP_DIR/skip-upstream"
skip_consumer="$TMP_DIR/skip-consumer"
make_upstream "$skip_upstream"
make_consumer "$skip_consumer" "$skip_upstream"

set +e
skip_output="$(cd "$skip_consumer" && printf 'n\n\n' | COG_UPSTREAM_URL="$skip_upstream" bash cog-update.sh 2>&1)"
skip_status=$?
set -e

if [[ $skip_status -eq 0 ]]; then
  fail "interactive self-refresh returned success after a skipped choice: $skip_output"
fi
if [[ "$skip_output" != *"$skip_message"* ]]; then
  fail "interactive self-refresh did not explain why an explicit rerun is required after skipped choices: $skip_output"
fi
if [[ -f "$skip_consumer/$future_file" ]]; then
  fail "interactive self-refresh replayed choices and installed a newly tracked file despite a prior skip"
fi
if [[ "$(tr -d '[:space:]' < "$skip_consumer/COG-VERSION")" != "1.0.0" ]]; then
  fail "interactive self-refresh did not preserve the user's skipped COG-VERSION choice"
fi

if [[ $failures -gt 0 ]]; then
  echo "$failures updater self-refresh regression(s) remain" >&2
  exit 1
fi

echo "cog-update refreshes its file list after self-update without replaying skipped interactive choices"
