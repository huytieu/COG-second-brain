#!/usr/bin/env bash
set -euo pipefail

python3 - <<'PY'
from pathlib import Path
import json
import sys

claude_agents = {path.stem for path in Path('.claude/agents').glob('*.md')}
with open('.cursor-plugin/plugin.json', encoding='utf-8') as handle:
    cursor_agents = set(json.load(handle).get('agents', []))

missing = sorted(claude_agents - cursor_agents)
extra = sorted(cursor_agents - claude_agents)

if missing or extra:
    if missing:
        print('Cursor plugin is missing agents: ' + ', '.join(missing), file=sys.stderr)
    if extra:
        print('Cursor plugin has unknown agents: ' + ', '.join(extra), file=sys.stderr)
    sys.exit(1)

print(f'Cursor agent list matches Claude agent surface ({len(claude_agents)} agents)')
PY
