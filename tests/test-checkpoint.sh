#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

failures=0

record_failure() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

init_dir="$TMP_DIR/init-run"
if init_output="$(bash "$ROOT_DIR/.claude/lib/checkpoint.sh" init "$init_dir" 2>&1)"; then
  init_status=0
else
  init_status=$?
fi

if [[ $init_status -ne 0 ]]; then
  record_failure "checkpoint init exited with status $init_status: $init_output"
elif [[ ! -f "$init_dir/evidence/ledger.md" ]]; then
  record_failure "checkpoint init did not create evidence/ledger.md"
elif ! grep -Fq "initialized: $init_dir/evidence/" <<< "$init_output"; then
  record_failure "checkpoint init did not report the initialized evidence directory"
fi

invalid_dir="$TMP_DIR/invalid-result"
if invalid_output="$(bash "$ROOT_DIR/.claude/lib/checkpoint.sh" record "$invalid_dir" CP-1 MAYBE "invalid result" 2>&1)"; then
  invalid_status=0
else
  invalid_status=$?
fi

if [[ $invalid_status -ne 2 ]]; then
  record_failure "checkpoint record returned status $invalid_status for MAYBE; expected 2: $invalid_output"
fi

safe_dir="$TMP_DIR/safe-note"
note=$'first field\tsecond field\rthird segment\nfourth line'
bash "$ROOT_DIR/.claude/lib/checkpoint.sh" record "$safe_dir" CP-3 PASS "$note" >/dev/null

checkpoint_file="$safe_dir/evidence/checkpoints.tsv"
if [[ ! -f "$checkpoint_file" ]]; then
  record_failure "checkpoint record did not create checkpoints.tsv"
else
  line_count=$(wc -l < "$checkpoint_file" | tr -d ' ')
  if [[ "$line_count" != "1" ]]; then
    record_failure "checkpoint note created $line_count TSV rows; expected 1"
  fi

  if ! awk -F '\t' 'NF == 4 {ok=1} END {exit !ok}' "$checkpoint_file"; then
    record_failure "checkpoint TSV row does not contain exactly 4 fields"
  fi

  if LC_ALL=C grep -q $'\r' "$checkpoint_file"; then
    record_failure "checkpoint TSV row still contains a carriage return"
  fi
fi

if [[ $failures -gt 0 ]]; then
  echo "$failures checkpoint regression(s) remain" >&2
  exit 1
fi

echo "checkpoint helper initializes ledgers, validates results, and preserves TSV row integrity"
