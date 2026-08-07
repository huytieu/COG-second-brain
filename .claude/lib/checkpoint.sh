#!/usr/bin/env bash
# Checkpoint recorder for V-model evidence trail.
# Usage:
#   checkpoint.sh init <run-dir>
#   checkpoint.sh record <run-dir> <CP-id> PASS|FAIL|SKIP "<note>"
#   checkpoint.sh status <run-dir>
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LOG="$ROOT/.claude/logs/checkpoint-ledger.tsv"
TEMPLATE="$ROOT/04-projects/harness/templates/evidence-ledger.md"
mkdir -p "$ROOT/.claude/logs"

cmd="${1:-}"
shift || true

sanitize_tsv_field() {
  local value="$1"
  value="${value//$'\t'/ }"
  value="${value//$'\r'/ }"
  value="${value//$'\n'/ }"
  printf '%s' "$value"
}

init_run() {
  local dir="$1"
  if [[ ! -f "$TEMPLATE" ]]; then
    echo "missing evidence ledger template: $TEMPLATE" >&2
    return 1
  fi

  mkdir -p "$dir/evidence"
  [[ -f "$dir/evidence/ledger.md" ]] || cp "$TEMPLATE" "$dir/evidence/ledger.md"
  echo "initialized: $dir/evidence/"
}

record_cp() {
  local dir="$1" cp_id="$2" result="$3" note="${4:-}"
  local ts safe_cp safe_note safe_dir

  case "$result" in
    PASS|FAIL|SKIP) ;;
    *)
      echo "invalid checkpoint result: $result (expected PASS, FAIL, or SKIP)" >&2
      return 2
      ;;
  esac

  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  safe_cp=$(sanitize_tsv_field "$cp_id")
  safe_note=$(sanitize_tsv_field "$note")
  safe_dir=$(sanitize_tsv_field "$dir")

  mkdir -p "$dir/evidence"
  printf '%s\t%s\t%s\t%s\n' "$ts" "$safe_cp" "$result" "$safe_note" >> "$dir/evidence/checkpoints.tsv"

  if [[ ! -f "$LOG" ]]; then
    printf 'timestamp\tcp\tresult\tnote\trun_dir\n' >> "$LOG"
  fi
  printf '%s\t%s\t%s\t%s\t%s\n' "$ts" "$safe_cp" "$result" "$safe_note" "$safe_dir" >> "$LOG"

  echo "recorded: ${safe_cp} ${result} -> ${dir}/evidence/checkpoints.tsv"
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
