#!/usr/bin/env bash
# Risk lane classifier adapted from dwarves-kit lane-classify pattern.
# Usage:
#   lane-classify.sh classify "<task summary>"
#   lane-classify.sh explain "<task summary>"
set -euo pipefail

cmd="${1:-classify}"
shift || true
text="${*:-}"

score=0
reasons=()

emit_hard_gate() {
  local lane="$1"
  local reason="$2"
  if [[ "$cmd" == "explain" ]]; then
    printf 'lane=%s score=0 reasons=%s\n' "$lane" "$reason"
  else
    echo "$lane"
  fi
  exit 0
}

# Hard gates
if echo "$text" | grep -qiE 'security|credential|secret|prod(uction)?|delete all|rm -rf'; then
  emit_hard_gate "full" "hard-security"
fi

if echo "$text" | grep -qiE 'bug|broken|regression|fails|error 5|root cause'; then
  emit_hard_gate "bug" "hard-bug"
fi

if echo "$text" | grep -qiE 'backfill|retrofit|audit only|document existing|no behavior change'; then
  emit_hard_gate "backfill" "hard-backfill"
fi

if echo "$text" | grep -qiE 'typo|one line|single word|label only|status reply|fix typo'; then
  emit_hard_gate "tiny" "hard-tiny"
fi

# Soft signals
echo "$text" | grep -qiE 'typo|one line|single word|label only|status reply' && { score=$((score+3)); reasons+=("tiny-signal"); }
echo "$text" | grep -qiE 'brief|team-brief|slack|jira|multi-source|publish|deploy|ship' && { score=$((score+2)); reasons+=("full-signal"); }
echo "$text" | grep -qiE 'spec|acceptance|test|verify|cross-repo|milestone' && { score=$((score+1)); reasons+=("normal+"); }

word_count=$(echo "$text" | wc -w | tr -d ' ')
[[ "$word_count" -lt 8 ]] && { score=$((score+1)); reasons+=("short"); }

lane="normal"
[[ $score -ge 3 ]] && lane="full"
[[ $score -le 0 && $word_count -lt 12 ]] && lane="tiny"

if [[ "$cmd" == "explain" ]]; then
  printf 'lane=%s score=%s reasons=%s\n' "$lane" "$score" "${reasons[*]:-none}"
else
  echo "$lane"
fi
