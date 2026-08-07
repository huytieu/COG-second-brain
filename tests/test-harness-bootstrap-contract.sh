#!/usr/bin/env bash
set -euo pipefail

# Protect fresh-checkout bootstrap behavior without treating mutable user state as framework data.
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

failures=0

fail() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

registry="04-projects/harness/ultragoals.md"

for skill in .claude/skills/ultragoal/SKILL.md skills/ultragoal/SKILL.md; do
  if ! grep -Fq 'No registered ultragoals.' "$skill"; then
    fail "$skill does not define the missing-registry status behavior"
  fi
  if ! grep -Fq 'created on the first `/ultragoal new`' "$skill"; then
    fail "$skill does not define first-use registry creation"
  fi
  if ! grep -Fq 'never overwrite an existing registry' "$skill"; then
    fail "$skill does not protect existing registry state"
  fi
done

if grep -Fq "  \"$registry\"" cog-update.sh; then
  fail "cog-update.sh treats mutable ultragoal registry state as an overwrite-safe framework file"
fi

installer=".claude/lib/install-harness.sh"
if grep -Fq "$installer" WORKFLOW.md && [[ ! -f "$installer" ]]; then
  fail "WORKFLOW.md documents missing installer: $installer"
fi

backlog="04-projects/harness/BACKLOG.md"
if grep -Fq "$backlog" WORKFLOW.md && [[ ! -f "$backlog" ]]; then
  fail "WORKFLOW.md documents missing harness backlog: $backlog"
fi

if [[ $failures -gt 0 ]]; then
  echo "$failures harness bootstrap contract regression(s) remain" >&2
  exit 1
fi

echo "harness bootstrap handles missing user state without dead static references"
