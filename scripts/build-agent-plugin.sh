#!/usr/bin/env bash
# build-agent-plugin.sh — regenerate the Agent Plugins standard surface.
#
# COG conforms to the Agent Plugins specification 1.0.0 (https://agent-plugins.org):
# a root plugin.json manifest plus a root skills/ directory. The canonical skills
# live in .claude/skills/ (that is what the distill and update flows write); this
# script mirrors them to skills/ so any standard-conformant client can load COG
# as a plugin. Run it after adding or editing any skill, then commit the result.
#
# skills/ is GENERATED — never edit it by hand. The packaging validator
# (scripts/validate-agent-surface.sh) fails if the two trees drift.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [[ ! -d .claude/skills ]]; then
  echo "✗ .claude/skills not found — run from a COG checkout" >&2
  exit 1
fi

rm -rf skills
cp -R .claude/skills skills

count=$(find skills -name SKILL.md | wc -l | tr -d ' ')
echo "✓ Mirrored .claude/skills → skills/ ($count skills, Agent Plugins spec 1.0.0)"
