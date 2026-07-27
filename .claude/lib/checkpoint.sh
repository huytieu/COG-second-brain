#!/usr/bin/env bash
# Checkpoint recorder for V-model evidence trail.
# Usage:
#   checkpoint.sh init <run-dir>
#   checkpoint.sh record <run-dir> <CP-id> PASS|FAIL|SKIP "<note>"
#   checkpoint.sh status <run-dir>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LOG="$ROOT/.claude/logs/checkpoint-ledger.tsv"
mkdir -p "$ROOT/.claude/logs"

cmd="${1:-}"
shift || true

init_run() {
  local dir="$1"
  mkdir -p "$dir/evidence"
  [[ -f "$dir/evidence/ledger.md" ]] || cp "$ROOT/04-projects/harness/templates/evidence-ledger.md" "$dir/evidence/ledger.md"
  echo "initialized: $dir/evidence/"
}

record_cp() {
  local dir="$1" cp_id="$2" result="$3" note="${4:-}"
  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  mkdir -p "$dir/evidence"
  echo -e "${ts}\t${cp_id}\t${result}\t${note}" >> "$dir/evidence/checkpoints.tsv"
  [[ -f "$LOG" ]] || echo -e "timestamp\tcp\tresult\tnote\trun_dir" >> "$LOG"
  echo -e "${ts}\t${cp_id}\t${result}\t${note}\t${dir}" >> "$LOG"
  echo "recorded: ${cp_id} ${result} → ${dir}/evidence/checkpoints.tsv"
}

status_run() {
  local dir="$1"
  if [[ -f "$dir/evidence/checkpoints.tsv" ]]; then
    column -t -s $'\t' "$dir/evidence/checkpoints.tsv" 2>/dev/null || cat "$dir/evidence/checkpoints.tsv"
  else
    echo "no checkpoints yet: $dir"
  fi
}

case "$cmd" in
  init) init_run "${1:?run-dir}" ;;
  record) record_cp "${1:?run-dir}" "${2:?CP-id}" "${3:?PASS|FAIL|SKIP}" "${4:-}" ;;
  status) status_run "${1:?run-dir}" ;;
  *)
    echo "usage: checkpoint.sh init|record|status <run-dir> [CP-id] [PASS|FAIL|SKIP] [note]" >&2
    exit 1
    ;;
esac
