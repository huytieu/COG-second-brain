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

validate_json() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    record_failure "$file is missing"
  elif python3 -m json.tool "$file" >/dev/null 2>&1; then
    ok "$file is valid JSON"
  else
    record_failure "$file is not valid JSON"
  fi
}

validate_json ".claude-plugin/plugin.json"
validate_json ".cursor-plugin/plugin.json"
validate_json "marketplace-entry.json"
validate_json "plugin.json"

# Agent Plugins standard surface (agent-plugins.org, spec 1.0.0):
# root plugin.json manifest + root skills/ mirror of .claude/skills/.
if [[ -f plugin.json ]] && python3 - <<'PY' >/dev/null 2>&1
import json
with open('plugin.json') as f:
    data = json.load(f)
assert data['$schema'] == 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
assert data['name'] == 'cog-second-brain'
PY
then
  ok "plugin.json declares the Agent Plugins 1.0.0 schema"
else
  record_failure "plugin.json is missing or does not declare the expected Agent Plugins schema/name"
fi

if [[ -d .claude/skills && -d skills ]] && diff -r .claude/skills skills >/dev/null 2>&1; then
  ok "skills/ mirror matches .claude/skills (Agent Plugins surface in sync)"
else
  record_failure "skills/ mirror is missing or drifted from .claude/skills; run ./scripts/build-agent-plugin.sh"
fi

surface_report=""
if surface_report="$(python3 - <<'PY'
from collections import Counter
from pathlib import Path
import json
import re
import sys

errors = []


def add(message):
    errors.append(message)


def skill_names(root):
    base = Path(root)
    if not base.is_dir():
        add(f"{root} is missing")
        return set()
    return {
        entry.name
        for entry in base.iterdir()
        if entry.is_dir() and (entry / "SKILL.md").is_file()
    }


def agent_names(root):
    base = Path(root)
    if not base.is_dir():
        add(f"{root} is missing")
        return set()
    return {path.stem for path in base.glob("*.md") if path.is_file()}


def format_names(names):
    return ", ".join(sorted(names))


claude_skills = skill_names(".claude/skills")
antigravity_skills = skill_names(".agents/skills")
missing_skills = claude_skills - antigravity_skills
extra_skills = antigravity_skills - claude_skills
if missing_skills:
    add(f"Antigravity is missing skill stubs: {format_names(missing_skills)}")
if extra_skills:
    add(f"Antigravity has orphan skill stubs: {format_names(extra_skills)}")

for name in sorted(claude_skills & antigravity_skills):
    stub_path = Path(".agents/skills") / name / "SKILL.md"
    text = stub_path.read_text(encoding="utf-8")
    if not re.search(rf"^name:\s*{re.escape(name)}\s*$", text, re.MULTILINE):
        add(f"{stub_path} does not declare frontmatter name: {name}")
    source = f".claude/skills/{name}/SKILL.md"
    if source not in text:
        add(f"{stub_path} does not point to {source}")
    if ".agents/rules/cog.md" not in text:
        add(f"{stub_path} does not apply .agents/rules/cog.md")
    if "invoke_subagent" not in text:
        add(f"{stub_path} is missing the invoke_subagent substitution")

claude_agents = agent_names(".claude/agents")
antigravity_agents = agent_names(".agents/agents")
missing_agents = claude_agents - antigravity_agents
extra_agents = antigravity_agents - claude_agents
if missing_agents:
    add(f"Antigravity is missing agent stubs: {format_names(missing_agents)}")
if extra_agents:
    add(f"Antigravity has orphan agent stubs: {format_names(extra_agents)}")

for name in sorted(claude_agents & antigravity_agents):
    stub_path = Path(".agents/agents") / f"{name}.md"
    text = stub_path.read_text(encoding="utf-8")
    if not re.search(rf"^name:\s*{re.escape(name)}\s*$", text, re.MULTILINE):
        add(f"{stub_path} does not declare frontmatter name: {name}")
    source = f".claude/agents/{name}.md"
    if source not in text:
        add(f"{stub_path} does not point to {source}")
    if not re.search(r"^subagent:\s*true\s*$", text, re.MULTILINE):
        add(f"{stub_path} does not declare subagent: true")

rules_path = Path(".agents/rules/cog.md")
if not rules_path.is_file():
    add(".agents/rules/cog.md is missing")
else:
    rules = rules_path.read_text(encoding="utf-8")
    if "CLAUDE.md" not in rules:
        add(".agents/rules/cog.md does not point to CLAUDE.md")
    if "invoke_subagent" not in rules:
        add(".agents/rules/cog.md is missing the invoke_subagent substitution")

agents_doc_path = Path("AGENTS.md")
if not agents_doc_path.is_file():
    add("AGENTS.md is missing")
else:
    agents_doc = agents_doc_path.read_text(encoding="utf-8")
    for name in sorted(claude_skills):
        if f"### /{name}" not in agents_doc:
            add(f"AGENTS.md is missing /{name}")

manifest_path = Path(".claude-plugin/plugin.json")
if manifest_path.is_file():
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        entries = manifest.get("skills", [])
        names = [entry.get("name") for entry in entries]
        paths = [entry.get("path") for entry in entries]
        duplicate_names = {name for name, count in Counter(names).items() if name and count > 1}
        duplicate_paths = {path for path, count in Counter(paths).items() if path and count > 1}
        if duplicate_names:
            add(f"Plugin manifest has duplicate skill names: {format_names(duplicate_names)}")
        if duplicate_paths:
            add(f"Plugin manifest has duplicate skill paths: {format_names(duplicate_paths)}")

        manifest_names = {name for name in names if name}
        missing_manifest = claude_skills - manifest_names
        extra_manifest = manifest_names - claude_skills
        if missing_manifest:
            add(f"Plugin manifest is missing Claude skills: {format_names(missing_manifest)}")
        if extra_manifest:
            add(f"Plugin manifest declares unknown skills: {format_names(extra_manifest)}")

        for entry in entries:
            name = entry.get("name")
            path = entry.get("path")
            if not name:
                add("Plugin manifest contains a skill entry without a name")
                continue
            expected_path = f".claude/skills/{name}/SKILL.md"
            if path != expected_path:
                add(f"Plugin manifest path for {name} is {path!r}; expected {expected_path!r}")
            elif not Path(path).is_file():
                add(f"Plugin manifest path missing for {name}: {path}")
    except (OSError, json.JSONDecodeError) as exc:
        add(f"Could not inspect .claude-plugin/plugin.json: {exc}")

cursor_manifest_path = Path(".cursor-plugin/plugin.json")
if cursor_manifest_path.is_file():
    try:
        cursor_manifest = json.loads(cursor_manifest_path.read_text(encoding="utf-8"))
        cursor_entries = cursor_manifest.get("skills", [])
        cursor_names = [entry.get("name") for entry in cursor_entries]
        cursor_paths = [entry.get("path") for entry in cursor_entries]
        duplicate_cursor_names = {
            name for name, count in Counter(cursor_names).items() if name and count > 1
        }
        duplicate_cursor_paths = {
            path for path, count in Counter(cursor_paths).items() if path and count > 1
        }
        if duplicate_cursor_names:
            add(f"Cursor plugin has duplicate skill names: {format_names(duplicate_cursor_names)}")
        if duplicate_cursor_paths:
            add(f"Cursor plugin has duplicate skill paths: {format_names(duplicate_cursor_paths)}")

        cursor_skill_names = {name for name in cursor_names if name}
        missing_cursor_skills = claude_skills - cursor_skill_names
        extra_cursor_skills = cursor_skill_names - claude_skills
        if missing_cursor_skills:
            add(f"Cursor plugin is missing Claude skills: {format_names(missing_cursor_skills)}")
        if extra_cursor_skills:
            add(f"Cursor plugin declares unknown skills: {format_names(extra_cursor_skills)}")

        for entry in cursor_entries:
            name = entry.get("name")
            path = entry.get("path")
            if not name:
                add("Cursor plugin contains a skill entry without a name")
                continue
            expected_path = f".claude/skills/{name}/SKILL.md"
            if path != expected_path:
                add(f"Cursor plugin path for {name} is {path!r}; expected {expected_path!r}")
            elif not Path(path).is_file():
                add(f"Cursor plugin path missing for {name}: {path}")

        cursor_agent_entries = cursor_manifest.get("agents", [])
        duplicate_cursor_agents = {
            name for name, count in Counter(cursor_agent_entries).items() if name and count > 1
        }
        if duplicate_cursor_agents:
            add(f"Cursor plugin has duplicate agents: {format_names(duplicate_cursor_agents)}")

        cursor_agents = {name for name in cursor_agent_entries if name}
        missing_cursor_agents = claude_agents - cursor_agents
        extra_cursor_agents = cursor_agents - claude_agents
        if missing_cursor_agents:
            add(f"Cursor plugin is missing agents: {format_names(missing_cursor_agents)}")
        if extra_cursor_agents:
            add(f"Cursor plugin has unknown agents: {format_names(extra_cursor_agents)}")
    except (OSError, json.JSONDecodeError) as exc:
        add(f"Could not inspect .cursor-plugin/plugin.json: {exc}")

update_script = Path("cog-update.sh")
if not update_script.is_file():
    add("cog-update.sh is missing")
else:
    text = update_script.read_text(encoding="utf-8")
    match = re.search(r"FRAMEWORK_FILES=\((.*?)^\)", text, re.MULTILINE | re.DOTALL)
    if not match:
        add("Could not parse FRAMEWORK_FILES in cog-update.sh")
    else:
        framework_paths = re.findall(r'^\s*"([^"]+)"\s*$', match.group(1), re.MULTILINE)
        duplicate_framework_paths = {
            path for path, count in Counter(framework_paths).items() if count > 1
        }
        if duplicate_framework_paths:
            add(
                "cog-update.sh FRAMEWORK_FILES has duplicates: "
                + format_names(duplicate_framework_paths)
            )
        declared = set(framework_paths)
        required = {
            *(f".claude/skills/{name}/SKILL.md" for name in claude_skills),
            *(f".agents/skills/{name}/SKILL.md" for name in antigravity_skills),
            *(f".claude/agents/{name}.md" for name in claude_agents),
            *(f".agents/agents/{name}.md" for name in antigravity_agents),
            ".agents/rules/cog.md",
        }
        missing_framework = required - declared
        if missing_framework:
            add(
                "cog-update.sh FRAMEWORK_FILES is missing surface files: "
                + format_names(missing_framework)
            )

if errors:
    print("\n".join(errors))
    sys.exit(1)

print(
    "Claude/Antigravity/Cursor parity is aligned "
    f"({len(claude_skills)} skills, {len(claude_agents)} agents); "
    "manifest paths and update coverage are consistent"
)
PY
)"; then
  ok "$surface_report"
else
  while IFS= read -r line; do
    [[ -n "$line" ]] && record_failure "$line"
  done <<< "$surface_report"
fi

for doc in README.md SETUP.md CONTRIBUTING.md .github/MARKETPLACE.md; do
  if [[ ! -f "$doc" ]]; then
    record_failure "$doc is missing"
  fi
done

if [[ -f README.md && -f SETUP.md && -f CONTRIBUTING.md && -f .github/MARKETPLACE.md ]]; then
  if grep -nH "agents\.md" README.md SETUP.md CONTRIBUTING.md .github/MARKETPLACE.md >/dev/null 2>&1; then
    record_failure "Found lowercase 'agents.md' references in packaging docs; use AGENTS.md consistently"
  else
    ok "Packaging docs consistently use AGENTS.md casing"
  fi
fi

version_report=""
if version_report="$(python3 - <<'PY'
from pathlib import Path
import json
import re
import sys

try:
    marketplace_docs = Path(".github/MARKETPLACE.md").read_text(encoding="utf-8")
    marketplace_match = re.search(
        r"Current packaged version:\s+\*\*([^*]+)\*\*",
        marketplace_docs,
    )
    if not marketplace_match:
        print("Could not read marketplace documentation version")
        sys.exit(1)

    values = {
        ".claude-plugin/plugin.json": json.loads(Path(".claude-plugin/plugin.json").read_text())["version"],
        ".cursor-plugin/plugin.json": json.loads(Path(".cursor-plugin/plugin.json").read_text())["version"],
        "plugin.json": json.loads(Path("plugin.json").read_text())["version"],
        "marketplace-entry.json": json.loads(Path("marketplace-entry.json").read_text())["version"],
        ".github/MARKETPLACE.md": marketplace_match.group(1).strip(),
        "COG-VERSION": Path("COG-VERSION").read_text().strip(),
    }
except (OSError, KeyError, json.JSONDecodeError) as exc:
    print(f"Could not read package versions: {exc}")
    sys.exit(1)

cog_version = values["COG-VERSION"]
marketplace_docs_version = values[".github/MARKETPLACE.md"]
if marketplace_docs_version != cog_version:
    print(
        "Marketplace docs version mismatch: "
        f".github/MARKETPLACE.md={marketplace_docs_version} "
        f"COG-VERSION={cog_version}"
    )
    sys.exit(1)

versions = set(values.values())
if len(versions) != 1:
    detail = " ".join(f"{path}={version}" for path, version in values.items())
    print(f"Version mismatch: {detail}")
    sys.exit(1)

print(next(iter(versions)))
PY
)"; then
  ok "Version is aligned across .claude-plugin/plugin.json, .cursor-plugin/plugin.json, plugin.json, marketplace-entry.json, .github/MARKETPLACE.md, and COG-VERSION ($version_report)"
else
  record_failure "$version_report"
fi

if [[ -d .kiro/powers ]]; then
  kiro_count=$(find .kiro/powers -name POWER.md | wc -l | tr -d ' ')
else
  kiro_count=0
  record_warning ".kiro/powers is missing"
fi

if [[ -d .gemini/commands ]]; then
  gemini_commands_count=$(find .gemini/commands -type f | wc -l | tr -d ' ')
else
  gemini_commands_count=0
  record_warning ".gemini/commands is missing"
fi

if [[ -d .gemini/skills ]]; then
  gemini_skills_count=$(find .gemini/skills -type f | wc -l | tr -d ' ')
else
  gemini_skills_count=0
  record_warning ".gemini/skills is missing"
fi

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
