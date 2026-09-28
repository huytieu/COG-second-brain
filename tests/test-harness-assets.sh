#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

required=(
  "04-projects/harness/templates/evidence-ledger.md"
  "04-projects/harness/templates/SPEC-template.md"
  "04-projects/harness/templates/report.html"
  "scripts/render-harness-report.py"
)

for path in "${required[@]}"; do
  if [[ ! -f "$path" ]]; then
    echo "missing harness asset: $path" >&2
    exit 1
  fi
done

if ! grep -Fq '04-projects/harness/templates/SPEC-template.md' .claude/skills/closed-loop/SKILL.md; then
  echo "closed-loop no longer points to the shipped spec template" >&2
  exit 1
fi

if ! grep -Fq 'scripts/render-harness-report.py' .claude/skills/closed-loop/SKILL.md; then
  echo "closed-loop no longer requires the safe report renderer" >&2
  exit 1
fi

if ! grep -Fq '04-projects/harness/templates/SPEC-template.md' .claude/skills/ultragoal/SKILL.md; then
  echo "ultragoal no longer points to the shipped spec template" >&2
  exit 1
fi

if ! grep -Fq 'scripts/render-harness-report.py' .claude/skills/ultragoal/SKILL.md; then
  echo "ultragoal no longer requires the safe report renderer" >&2
  exit 1
fi

if grep -Fq 'fill every `{{token}}`' .claude/skills/ultragoal/SKILL.md; then
  echo "ultragoal still instructs agents to substitute raw HTML tokens" >&2
  exit 1
fi

for path in scripts/render-harness-report.py tests/test-harness-report-renderer.py; do
  if ! grep -Fq "  \"$path\"" cog-update.sh; then
    echo "cog-update.sh does not track $path" >&2
    exit 1
  fi
done

echo "closed-loop harness assets, safe report renderer, and updater coverage are aligned"
