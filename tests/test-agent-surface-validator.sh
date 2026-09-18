#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

make_fixture() {
  local name="$1"
  local fixture="$TMP_DIR/$name"
  mkdir -p "$fixture"
  git -C "$ROOT_DIR" archive HEAD | tar -xf - -C "$fixture"
  echo "$fixture"
}

run_expect_failure() {
  local fixture="$1"
  local expected="$2"
  local label="$3"
  local output status

  set +e
  output="$(cd "$fixture" && ./scripts/validate-agent-surface.sh 2>&1)"
  status=$?
  set -e

  if [[ $status -eq 0 ]]; then
    echo "expected validator to reject $label" >&2
    echo "$output" >&2
    exit 1
  fi

  if ! grep -Fq "$expected" <<< "$output"; then
    echo "validator failed, but not with the expected diagnostic for $label" >&2
    echo "$output" >&2
    exit 1
  fi
}

antigravity_fixture="$(make_fixture antigravity-drift)"
rm "$antigravity_fixture/.agents/skills/onboarding/SKILL.md"
run_expect_failure \
  "$antigravity_fixture" \
  "Antigravity is missing skill stubs: onboarding" \
  "a missing Antigravity skill stub"

echo "validator rejects a missing Antigravity skill stub"

cursor_fixture="$(make_fixture cursor-drift)"
python3 - "$cursor_fixture/.cursor-plugin/plugin.json" <<'PY'
from pathlib import Path
import json
import sys

path = Path(sys.argv[1])
data = json.loads(path.read_text(encoding='utf-8'))
data['agents'].remove('fix-agent')
path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
PY
run_expect_failure \
  "$cursor_fixture" \
  "Cursor plugin is missing agents: fix-agent" \
  "a missing Cursor agent"

echo "validator rejects a missing Cursor agent"

marketplace_fixture="$(make_fixture marketplace-version-drift)"
python3 - "$marketplace_fixture/.github/MARKETPLACE.md" <<'PY'
from pathlib import Path
import re
import sys

path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8')
text, count = re.subn(
    r'Current packaged version: \*\*[^*]+\*\*',
    'Current packaged version: **0.0.0**',
    text,
    count=1,
)
if count != 1:
    raise SystemExit('marketplace version marker not found')
path.write_text(text, encoding='utf-8')
PY
run_expect_failure \
  "$marketplace_fixture" \
  "Marketplace docs version mismatch: .github/MARKETPLACE.md=0.0.0" \
  "marketplace documentation version drift"

echo "validator rejects marketplace documentation version drift"
