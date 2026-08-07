#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

failures=0

fail() {
  echo "FAIL: $*" >&2
  failures=$((failures + 1))
}

make_upstream() {
  local path="$1"
  git init -q -b main "$path"
  git -C "$path" config user.name "COG Test"
  git -C "$path" config user.email "cog-test@example.invalid"
  printf '9.9.9\n' > "$path/COG-VERSION"
  printf 'upstream readme\n' > "$path/README.md"
  git -C "$path" add COG-VERSION README.md
  git -C "$path" commit -q -m "fixture: upstream"
}

make_consumer() {
  local path="$1"
  local upstream="$2"
  git init -q -b main "$path"
  git -C "$path" config user.name "COG Test"
  git -C "$path" config user.email "cog-test@example.invalid"
  cp "$ROOT_DIR/cog-update.sh" "$path/cog-update.sh"
  printf '1.0.0\n' > "$path/COG-VERSION"
  printf 'local readme\n' > "$path/README.md"
  mkdir -p "$path/scripts"
  cat > "$path/scripts/validate-agent-surface.sh" <<'EOF'
#!/usr/bin/env bash
echo "fixture validator failure" >&2
exit 42
EOF
  chmod +x "$path/scripts/validate-agent-surface.sh"
  git -C "$path" add cog-update.sh COG-VERSION README.md scripts/validate-agent-surface.sh
  git -C "$path" commit -q -m "fixture: consumer"
  git -C "$path" remote add cog-upstream "$upstream"
}

force_upstream="$TMP_DIR/force-upstream"
force_consumer="$TMP_DIR/force-consumer"
make_upstream "$force_upstream"
make_consumer "$force_consumer" "$force_upstream"

set +e
force_output="$(cd "$force_consumer" && COG_UPSTREAM_URL="$force_upstream" bash cog-update.sh --force 2>&1)"
force_status=$?
set -e

if [[ $force_status -eq 0 ]]; then
  fail "--force returned success after validator failure: $force_output"
fi
if [[ "$(cat "$force_consumer/README.md")" != "upstream readme" ]]; then
  fail "--force validator regression did not reach the post-update validation phase"
fi

interactive_upstream="$TMP_DIR/interactive-upstream"
interactive_consumer="$TMP_DIR/interactive-consumer"
make_upstream "$interactive_upstream"
make_consumer "$interactive_consumer" "$interactive_upstream"

set +e
interactive_output="$(cd "$interactive_consumer" && printf '\n\n' | COG_UPSTREAM_URL="$interactive_upstream" bash cog-update.sh 2>&1)"
interactive_status=$?
set -e

if [[ $interactive_status -eq 0 ]]; then
  fail "interactive update returned success after validator failure: $interactive_output"
fi
if [[ "$(cat "$interactive_consumer/README.md")" != "upstream readme" ]]; then
  fail "interactive validator regression did not reach the post-update validation phase"
fi

if [[ $failures -gt 0 ]]; then
  echo "$failures updater validator-failure regression(s) remain" >&2
  exit 1
fi

echo "cog-update propagates post-update validator failures in force and interactive modes"
