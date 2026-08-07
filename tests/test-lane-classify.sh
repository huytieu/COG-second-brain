#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLASSIFIER="$ROOT_DIR/.claude/lib/lane-classify.sh"

assert_eq() {
  local expected="$1"
  local actual="$2"
  local label="$3"
  if [[ "$actual" != "$expected" ]]; then
    echo "$label: expected '$expected', got '$actual'" >&2
    exit 1
  fi
}

assert_eq "full" "$(bash "$CLASSIFIER" classify "security credential rotation")" "security classify"
assert_eq "lane=full score=0 reasons=hard-security" "$(bash "$CLASSIFIER" explain "security credential rotation")" "security explain"

assert_eq "bug" "$(bash "$CLASSIFIER" classify "root cause for broken export")" "bug classify"
assert_eq "lane=bug score=0 reasons=hard-bug" "$(bash "$CLASSIFIER" explain "root cause for broken export")" "bug explain"

assert_eq "backfill" "$(bash "$CLASSIFIER" classify "audit only no behavior change")" "backfill classify"
assert_eq "lane=backfill score=0 reasons=hard-backfill" "$(bash "$CLASSIFIER" explain "audit only no behavior change")" "backfill explain"

assert_eq "tiny" "$(bash "$CLASSIFIER" classify "fix typo")" "tiny classify"
assert_eq "lane=tiny score=0 reasons=hard-tiny" "$(bash "$CLASSIFIER" explain "fix typo")" "tiny explain"

echo "lane classifier explain mode is consistent across hard gates"
