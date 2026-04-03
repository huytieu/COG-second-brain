#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# cog-sync.sh — Generate tool-specific files from the single source of truth
# ═══════════════════════════════════════════════════════════════════════
#
# Source of truth:
#   AGENTS.md                    — Framework docs, skill descriptions, vault structure
#   .agents/skills/*/SKILL.md   — Full skill playbooks (agentskills.io standard)
#
# Generated (committed to git, never hand-edited):
#   CLAUDE.md                    — Claude-specific header + AGENTS.md appended
#   GEMINI.md                    — Gemini-specific header + AGENTS.md appended
#   .claude/skills/*/SKILL.md   — Copy from .agents/skills/ (Claude Code native)
#   .gemini/skills/*.md          — Skill body only, no frontmatter (Gemini CLI native)
#   .gemini/commands/*.toml      — Gemini CLI command entry points
#   .kiro/powers/cog-*/POWER.md — Kiro format with keywords (Kiro native)
#
# Run this before releasing a new COG version.
#
# Usage:
#   ./cog-sync.sh               Sync all generated files
#   ./cog-sync.sh --dry-run     Show what would change (no writes)
#   ./cog-sync.sh --check       Parity check only (no writes)
#   ./cog-sync.sh --help        Show help
# ═══════════════════════════════════════════════════════════════════════

set -euo pipefail

# ── Colors ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()  { echo -e "${CYAN}i${RESET}  $*"; }
ok()    { echo -e "${GREEN}+${RESET}  $*"; }
warn()  { echo -e "${YELLOW}!${RESET}  $*"; }
err()   { echo -e "${RED}x${RESET}  $*" >&2; }

# ── Paths ───────────────────────────────────────────────────────────
SOURCE_DIR=".agents/skills"
CLAUDE_DIR=".claude/skills"
GEMINI_DIR=".gemini/skills"
GEMINI_CMD_DIR=".gemini/commands"
KIRO_DIR=".kiro/powers"

# ── Marker for hybrid context files ────────────────────────────────
AUTOGEN_MARKER="<!-- AUTO-GENERATED: Everything below is synced from AGENTS.md by cog-sync.sh — do not edit manually -->"

# ── YAML frontmatter helpers ────────────────────────────────────────

# Extract a top-level frontmatter field value
# Usage: get_field "name" "path/to/SKILL.md"
get_field() {
  local field="$1" file="$2"
  sed -n '1,/^---$/!b; /^---$/,/^---$/{ /^'"$field"':/{ s/^'"$field"':[[:space:]]*//; s/^"//; s/"$//; p; } }' "$file" 2>/dev/null | head -1
}

# Extract a metadata sub-field value
# Usage: get_meta "keywords" "path/to/SKILL.md"
get_meta() {
  local field="$1" file="$2"
  # Find the metadata block, then the field within it
  awk '
    /^---$/ { fm++; next }
    fm == 1 && /^metadata:/ { in_meta=1; next }
    fm == 1 && in_meta && /^[a-z]/ { in_meta=0 }
    fm == 1 && in_meta && $0 ~ "^  '"$field"':" {
      sub(/^  '"$field"':[[:space:]]*/, "")
      gsub(/^"/, ""); gsub(/"$/, "")
      print
    }
  ' "$file" 2>/dev/null | head -1
}

# Extract the markdown body (everything after the closing --- of frontmatter)
get_body() {
  local file="$1"
  awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2{print}' "$file"
}

# Convert "my-skill-name" to "My Skill Name"
title_case() {
  echo "$1" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1'
}

# ── Usage ───────────────────────────────────────────────────────────
usage() {
  cat <<'EOF'
COG Skill Sync — Generate tool-specific files from source of truth

Source of truth:
  AGENTS.md                   Framework docs and skill descriptions
  .agents/skills/*/SKILL.md   Full skill playbooks (agentskills.io standard)

Generated files (committed to git):
  CLAUDE.md                   Claude-specific header + AGENTS.md content
  GEMINI.md                   Gemini-specific header + AGENTS.md content
  .claude/skills/*/SKILL.md   Copies for Claude Code native discovery
  .gemini/skills/*.md          Body-only for Gemini CLI
  .gemini/commands/*.toml      Gemini CLI command entry points
  .kiro/powers/cog-*/POWER.md Kiro format with keywords

Usage:
  ./cog-sync.sh               Sync all generated files
  ./cog-sync.sh --dry-run     Preview changes without writing
  ./cog-sync.sh --check       Parity check only
  ./cog-sync.sh --help        This message

Run before releasing a new COG version.
EOF
}

# ── Parity check ────────────────────────────────────────────────────
parity_check() {
  local issues=0

  echo -e "${BOLD}Parity check${RESET}"
  echo ""

  # 1. Check generated files exist for each source skill
  for skill_dir in "${SOURCE_DIR}"/*/; do
    [[ -d "$skill_dir" ]] || continue
    local skill_file="${skill_dir}SKILL.md"
    [[ -f "$skill_file" ]] || continue

    local name
    name=$(get_field "name" "$skill_file")
    [[ -z "$name" ]] && continue

    [[ ! -f "${CLAUDE_DIR}/${name}/SKILL.md" ]] && warn "Missing: ${CLAUDE_DIR}/${name}/SKILL.md" && issues=$((issues + 1))
    [[ ! -f "${GEMINI_DIR}/${name}.md" ]] && warn "Missing: ${GEMINI_DIR}/${name}.md" && issues=$((issues + 1))
    [[ ! -f "${GEMINI_CMD_DIR}/${name}.toml" ]] && warn "Missing: ${GEMINI_CMD_DIR}/${name}.toml" && issues=$((issues + 1))
    [[ ! -f "${KIRO_DIR}/cog-${name}/POWER.md" ]] && warn "Missing: ${KIRO_DIR}/cog-${name}/POWER.md" && issues=$((issues + 1))
  done

  # 3. Check context files contain AGENTS.md content
  for ctx_file in CLAUDE.md GEMINI.md; do
    if [[ -f "$ctx_file" ]]; then
      # Verify AGENTS.md content is present (either as pure copy or after marker)
      local first_agents_line
      first_agents_line=$(head -1 AGENTS.md)
      if ! grep -qF "$first_agents_line" "$ctx_file" 2>/dev/null; then
        warn "${ctx_file} out of sync with AGENTS.md"
        issues=$((issues + 1))
      fi
    else
      warn "Missing: ${ctx_file}"
      issues=$((issues + 1))
    fi
  done

  echo ""
  if [[ $issues -eq 0 ]]; then
    ok "All files in sync"
  else
    warn "${issues} issue(s) found — run ${BOLD}./cog-sync.sh${RESET} to fix"
  fi

  return $issues
}

# ── Sync one skill ──────────────────────────────────────────────────
sync_skill() {
  local skill_file="$1" dry_run="$2"
  local name description display_name keywords body

  name=$(get_field "name" "$skill_file")
  if [[ -z "$name" ]]; then
    warn "Skipping ${skill_file} — no 'name' in frontmatter"
    return 1
  fi

  description=$(get_field "description" "$skill_file")
  display_name=$(get_meta "display-name" "$skill_file")
  keywords=$(get_meta "keywords" "$skill_file")

  # Defaults
  [[ -z "$display_name" ]] && display_name="COG $(title_case "$name")"
  [[ -z "$keywords" ]] && keywords="$name"

  info "Syncing: ${BOLD}${name}${RESET}"

  # ── Claude Code: copy as-is ────────────────────────────────────
  local claude_target="${CLAUDE_DIR}/${name}/SKILL.md"
  if $dry_run; then
    echo "    ${claude_target}"
  else
    mkdir -p "${CLAUDE_DIR}/${name}"
    cp "$skill_file" "$claude_target"

    # Also copy scripts/, references/, assets/ if they exist
    local skill_base
    skill_base=$(dirname "$skill_file")
    for subdir in scripts references assets; do
      if [[ -d "${skill_base}/${subdir}" ]]; then
        cp -r "${skill_base}/${subdir}" "${CLAUDE_DIR}/${name}/"
      fi
    done
  fi

  # ── Gemini CLI: body only (no frontmatter) ─────────────────────
  local gemini_target="${GEMINI_DIR}/${name}.md"
  if $dry_run; then
    echo "    ${gemini_target}"
  else
    mkdir -p "$GEMINI_DIR"
    get_body "$skill_file" > "$gemini_target"
  fi

  # ── Gemini CLI: .toml command entry point ──────────────────────
  local gemini_cmd_target="${GEMINI_CMD_DIR}/${name}.toml"
  if $dry_run; then
    echo "    ${gemini_cmd_target}"
  else
    mkdir -p "$GEMINI_CMD_DIR"
    cat > "$gemini_cmd_target" <<TOML
description = "${description}"
prompt = """
You are running the COG ${name} workflow. Follow this playbook exactly:

@{.gemini/skills/${name}.md}
"""
TOML
  fi

  # ── Kiro: transform frontmatter to Kiro format ────────────────
  local kiro_name="cog-${name}"
  local kiro_target="${KIRO_DIR}/${kiro_name}/POWER.md"

  if $dry_run; then
    echo "    ${kiro_target}"
  else
    mkdir -p "${KIRO_DIR}/${kiro_name}"

    # Build Kiro keywords array from comma-separated string
    local kw_json=""
    local first=true
    IFS=',' read -ra kw_array <<< "$keywords"
    for kw in "${kw_array[@]}"; do
      kw=$(echo "$kw" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
      [[ -z "$kw" ]] && continue
      $first || kw_json+=", "
      kw_json+="\"${kw}\""
      first=false
    done

    {
      echo '---'
      echo "name: \"${kiro_name}\""
      echo "displayName: \"${display_name}\""
      echo "description: \"${description}\""
      echo "keywords: [${kw_json}]"
      echo '---'
      echo ""
      get_body "$skill_file"
    } > "$kiro_target"
  fi

  return 0
}

# ── Sync context file ─────────────────────────────────────────────
# Copies AGENTS.md to the target file. If the target has content above
# the auto-gen marker, that header is preserved; otherwise the file
# becomes a pure copy of AGENTS.md.
sync_context_file() {
  local target="$1" dry_run="$2"

  if $dry_run; then
    echo "    ${target} (copy of AGENTS.md)"
    return 0
  fi

  if [[ -f "$target" ]] && grep -qF "$AUTOGEN_MARKER" "$target" 2>/dev/null; then
    # Check if there's meaningful content above the marker
    local header
    header=$(awk -v marker="$AUTOGEN_MARKER" 'index($0, marker){exit} {print}' "$target" | grep -v '^[[:space:]]*$' || true)
    if [[ -n "$header" ]]; then
      # Preserve header above marker, replace everything below
      awk -v marker="$AUTOGEN_MARKER" '
        { print }
        index($0, marker) { found=1; exit }
        END { if (!found) print marker }
      ' "$target" > "${target}.tmp"
      echo "" >> "${target}.tmp"
      cat AGENTS.md >> "${target}.tmp"
      mv "${target}.tmp" "$target"
      ok "  ${target} (header + AGENTS.md)"
    else
      # No meaningful header — pure copy
      cp AGENTS.md "$target"
      ok "  ${target} (copy)"
    fi
  else
    # No marker or file doesn't exist — pure copy
    cp AGENTS.md "$target"
    ok "  ${target} (copy)"
  fi
}

# ── Clean up orphaned generated files ──────────────────────────────
cleanup_orphans() {
  local dry_run="$1"
  local removed=0

  info "Checking for orphaned generated files..."

  # Build set of expected skill names from source
  local -a source_names=()
  for d in "${SOURCE_DIR}"/*/; do
    [[ -d "$d" ]] || continue
    local skill_file="${d}SKILL.md"
    [[ -f "$skill_file" ]] || continue
    local sname
    sname=$(get_field "name" "$skill_file")
    [[ -n "$sname" ]] && source_names+=("$sname")
  done

  # Helper: check if name is in source_names
  is_source_skill() {
    local check="$1"
    for sn in "${source_names[@]}"; do
      [[ "$sn" == "$check" ]] && return 0
    done
    return 1
  }

  # Claude skills
  for d in "${CLAUDE_DIR}"/*/; do
    [[ -d "$d" ]] || continue
    local skill_name
    skill_name=$(basename "$d")
    if ! is_source_skill "$skill_name"; then
      warn "Orphaned: ${d}"
      if ! $dry_run; then rm -rf "$d"; ok "  Removed: ${d}"; fi
      removed=$((removed + 1))
    fi
  done

  # Gemini skills (.md)
  for f in "${GEMINI_DIR}"/*.md; do
    [[ -f "$f" ]] || continue
    local skill_name
    skill_name=$(basename "$f" .md)
    if ! is_source_skill "$skill_name"; then
      warn "Orphaned: ${f}"
      if ! $dry_run; then rm "$f"; ok "  Removed: ${f}"; fi
      removed=$((removed + 1))
    fi
  done

  # Gemini commands (.toml)
  for f in "${GEMINI_CMD_DIR}"/*.toml; do
    [[ -f "$f" ]] || continue
    local skill_name
    skill_name=$(basename "$f" .toml)
    if ! is_source_skill "$skill_name"; then
      warn "Orphaned: ${f}"
      if ! $dry_run; then rm "$f"; ok "  Removed: ${f}"; fi
      removed=$((removed + 1))
    fi
  done

  # Kiro powers (cog-* prefix) — use forward-mapping from source names
  # Build set of expected Kiro dir names
  local -a expected_kiro=()
  for sn in "${source_names[@]}"; do
    expected_kiro+=("cog-${sn}")
  done

  for d in "${KIRO_DIR}"/cog-*/; do
    [[ -d "$d" ]] || continue
    local kiro_basename
    kiro_basename=$(basename "$d")
    local found=false
    for ek in "${expected_kiro[@]}"; do
      [[ "$ek" == "$kiro_basename" ]] && found=true && break
    done
    if ! $found; then
      warn "Orphaned: ${d}"
      if ! $dry_run; then rm -rf "$d"; ok "  Removed: ${d}"; fi
      removed=$((removed + 1))
    fi
  done

  if [[ $removed -eq 0 ]]; then
    ok "No orphaned files found"
  else
    if $dry_run; then
      warn "Found ${removed} orphaned item(s) — will be removed on sync"
    else
      ok "Removed ${removed} orphaned item(s)"
    fi
  fi
}

# ── Main ────────────────────────────────────────────────────────────
main() {
  local mode="sync"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run) mode="dry-run"; shift ;;
      --check)   mode="check";   shift ;;
      --help|-h) usage; exit 0 ;;
      *) err "Unknown option: $1"; usage; exit 1 ;;
    esac
  done

  echo ""
  echo -e "${BOLD}COG Skill Sync${RESET}"
  echo -e "──────────────"
  echo ""

  # Validate source of truth exists
  if [[ ! -f "AGENTS.md" ]]; then
    err "AGENTS.md not found. Run from the COG root directory."
    exit 1
  fi

  if [[ ! -d "$SOURCE_DIR" ]]; then
    err "Source directory ${SOURCE_DIR}/ not found."
    err "Skills must live in .agents/skills/*/SKILL.md (agentskills.io standard)."
    exit 1
  fi

  # Count skills
  local skill_count=0
  for d in "${SOURCE_DIR}"/*/; do
    [[ -f "${d}SKILL.md" ]] && skill_count=$((skill_count + 1))
  done
  info "Found ${BOLD}${skill_count}${RESET} skills in ${SOURCE_DIR}/"
  echo ""

  # ── Check mode ─────────────────────────────────────────────────
  if [[ "$mode" == "check" ]]; then
    parity_check
    exit $?
  fi

  local dry_run=false
  [[ "$mode" == "dry-run" ]] && dry_run=true

  $dry_run && info "Dry run — no files will be written" && echo ""

  # ── Sync context files (hybrid: header + AGENTS.md) ────────────
  info "Context files:"
  sync_context_file "CLAUDE.md" "$dry_run"
  sync_context_file "GEMINI.md" "$dry_run"
  echo ""

  # ── Sync each skill ───────────────────────────────────────────
  local synced=0 errors=0
  info "Skills:"
  echo ""

  for skill_dir in "${SOURCE_DIR}"/*/; do
    [[ -d "$skill_dir" ]] || continue
    local skill_file="${skill_dir}SKILL.md"
    [[ -f "$skill_file" ]] || continue

    if sync_skill "$skill_file" "$dry_run"; then
      synced=$((synced + 1))
    else
      errors=$((errors + 1))
    fi
  done

  # ── Clean up orphans ──────────────────────────────────────────
  echo ""
  cleanup_orphans "$dry_run"

  # ── Summary ────────────────────────────────────────────────────
  echo ""
  echo -e "${BOLD}Summary${RESET}"
  ok "Synced ${synced} skills to Claude Code, Gemini CLI, and Kiro"
  ok "Synced CLAUDE.md and GEMINI.md from AGENTS.md"
  [[ $errors -gt 0 ]] && warn "${errors} skill(s) skipped due to errors"

  if ! $dry_run; then
    echo ""

    # Run parity check
    echo ""
    parity_check || true

    echo ""
    info "Review with ${BOLD}git diff${RESET}, then commit when ready."
  fi
}

main "$@"
