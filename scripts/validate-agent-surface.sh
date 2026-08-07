#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RESET='\033[0m'

info()  { echo -e "${CYAN}ℹ${RESET}  $*"; }
ok()    { echo -e "${GREEN}✓${RESET}  $*"; }
warn()  { echo -e "${YELLOW}⚠${RESET}  $*"; }
err()   { echo -e "${RED}✗${RESET}  $*" >&2; }

failures=0
warnings=0

record_failure() {
  err "$*"
  failures=$((failures + 1))
}

record_warning() {
  warn "$*"
  warnings=$((warnings + 1))
}

if ! command -v python3 >/dev/null 2>&1; then
  record_failure "python3 is required for validation"
  exit 1
fi

info "Validating packaged agent surfaces from $ROOT_DIR"

if python3 -m json.tool .claude-plugin/plugin.json >/dev/null 2>&1; then
  ok ".claude-plugin/plugin.json is valid JSON"
else
  record_failure ".claude-plugin/plugin.json is not valid JSON"
fi

if python3 -m json.tool marketplace-entry.json >/dev/null 2>&1; then
  ok "marketplace-entry.json is valid JSON"
else
  record_failure "marketplace-entry.json is not valid JSON"
fi

# Agent Plugins standard surface (agent-plugins.org, spec 1.0.0):
# root plugin.json manifest + root skills/ mirror of .claude/skills/.
if python3 - <<'PY' >/dev/null 2>&1
import json
with open('plugin.json') as f:
    data = json.load(f)
assert data['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
assert data['name'] == 'cog-second-brain'
PY
then
  ok "plugin.json is valid JSON and declares the Agent Plugins 1.0.0 schema"
else
  record_failure "plugin.json is missing, invalid JSON, or missing \$schema/name (Agent Plugins spec 1.0.0)"
fi

if [[ -d skills ]] && diff -r .claude/skills skills >/dev/null 2>&1; then
  ok "skills/ mirror matches .claude/skills (Agent Plugins surface in sync)"
else
  record_failure "skills/ mirror is missing or drifted from .claude/skills — run ./scripts/build-agent-plugin.sh"
fi

manifest_tmp="$(mktemp)"
python3 - <<'PY' > "$manifest_tmp"
import json
with open('.claude-plugin/plugin.json') as f:
    data = json.load(f)
for skill in data.get('skills', []):
    print(f"{skill['name']}\t{skill['path']}")
PY

manifest_count=$(wc -l < "$manifest_tmp" | tr -d ' ')
claude_skill_count=$(find .claude/skills -name SKILL.md | wc -l | tr -d ' ')

if [[ "$manifest_count" == "$claude_skill_count" ]]; then
  ok "Plugin manifest skill count matches shipped Claude skills ($manifest_count)"
else
  record_failure "Plugin manifest declares $manifest_count skills but .claude/skills contains $claude_skill_count SKILL.md files"
fi

while IFS=$'\t' read -r name path; do
  [[ -z "$name" ]] && continue

  if [[ -f "$path" ]]; then
    ok "Manifest path exists for $name → $path"
  else
    record_failure "Manifest path missing for $name → $path"
  fi

  if grep -Fq "### /$name" AGENTS.md; then
    ok "AGENTS.md documents /$name"
  else
    record_failure "AGENTS.md is missing /$name"
  fi
done < "$manifest_tmp"

rm -f "$manifest_tmp"

plugin_version=$(python3 - <<'PY'
import json
with open('.claude-plugin/plugin.json') as f:
    print(json.load(f)['version'])
PY
)
marketplace_version=$(python3 - <<'PY'
import json
with open('marketplace-entry.json') as f:
    print(json.load(f)['version'])
PY
)
cog_version=$(tr -d '[:space:]' < COG-VERSION)
agent_plugin_version=$(python3 - <<'PY'
import json
with open('plugin.json') as f:
    print(json.load(f)['version'])
PY
)

if [[ "$plugin_version" == "$marketplace_version" && "$plugin_version" == "$cog_version" && "$plugin_version" == "$agent_plugin_version" ]]; then
  ok "Version is aligned across .claude-plugin/plugin.json, plugin.json, marketplace-entry.json, and COG-VERSION ($cog_version)"
else
  record_failure "Version mismatch: .claude-plugin/plugin.json=$plugin_version plugin.json=$agent_plugin_version marketplace-entry.json=$marketplace_version COG-VERSION=$cog_version"
fi

if rg -n "agents\.md" README.md SETUP.md CONTRIBUTING.md .github/MARKETPLACE.md >/dev/null 2>&1; then
  record_failure "Found lowercase 'agents.md' references in packaging docs; use AGENTS.md consistently"
else
  ok "Packaging docs consistently use AGENTS.md casing"
fi

kiro_count=$(find .kiro/powers -name POWER.md | wc -l | tr -d ' ')
gemini_commands_count=$(find .gemini/commands -type f | wc -l | tr -d ' ')
gemini_skills_count=$(find .gemini/skills -type f | wc -l | tr -d ' ')

if [[ "$kiro_count" == "7" ]]; then
  ok "Kiro core surface count is $kiro_count"
else
  record_warning "Expected 7 Kiro powers, found $kiro_count"
fi

if [[ "$gemini_commands_count" == "7" && "$gemini_skills_count" == "7" ]]; then
  ok "Gemini core surface counts are aligned (commands=$gemini_commands_count, skills=$gemini_skills_count)"
else
  record_warning "Expected 7 Gemini commands and 7 Gemini skills, found commands=$gemini_commands_count skills=$gemini_skills_count"
fi

if [[ -f docs/AGENT-SUPPORT.md ]]; then
  ok "docs/AGENT-SUPPORT.md exists"
else
  record_failure "docs/AGENT-SUPPORT.md is missing"
fi

if [[ $failures -gt 0 ]]; then
  echo
  err "Validation failed with $failures error(s) and $warnings warning(s)"
  exit 1
fi

echo
ok "Validation passed with $warnings warning(s)"
