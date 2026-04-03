#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════
# cog-migrate-skills.sh — Migrate skills from .claude/skills/ to .agents/skills/
# ═══════════════════════════════════════════════════════════════════════
#
# Converts existing Claude Code skill frontmatter:
#   name, description, roles: [...], integrations: [...]
#
# To agentskills.io standard format:
#   name, description, metadata: { roles, integrations, keywords, display-name }
#
# Keywords are pulled from existing .kiro/powers/ when available,
# otherwise generated from the skill name and description.
#
# Usage:
#   ./cog-migrate-skills.sh               Migrate all skills
#   ./cog-migrate-skills.sh --dry-run     Preview changes without writing
#   ./cog-migrate-skills.sh --help        Show help
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
SOURCE_DIR=".claude/skills"
TARGET_DIR=".agents/skills"
KIRO_DIR=".kiro/powers"

DRY_RUN=false

# ── Usage ───────────────────────────────────────────────────────────
usage() {
  cat <<'EOF'
COG Skill Migration — Convert .claude/skills/ to .agents/skills/ (agentskills.io)

Reads:
  .claude/skills/*/SKILL.md     Current Claude Code skills
  .kiro/powers/cog-*/POWER.md   Keywords (where available)

Writes:
  .agents/skills/*/SKILL.md     New agentskills.io standard format

Usage:
  ./cog-migrate-skills.sh               Migrate all skills
  ./cog-migrate-skills.sh --dry-run     Preview without writing
  ./cog-migrate-skills.sh --help        This message
EOF
}

# ── Helpers ─────────────────────────────────────────────────────────

# Extract a YAML frontmatter field (top-level only)
get_field() {
  local field="$1" file="$2"
  awk -v f="$field" '
    /^---$/ { fm++; next }
    fm == 1 && $0 ~ "^"f":" {
      sub("^"f":[[:space:]]*", "")
      gsub(/^"/, ""); gsub(/"$/, "")
      print
      exit
    }
    fm >= 2 { exit }
  ' "$file" 2>/dev/null
}

# Extract keywords from Kiro POWER.md (JSON array → comma-separated)
# Handles name mismatches: update-cog → cog-update (not cog-update-cog)
get_kiro_keywords() {
  local name="$1"
  local kiro_file=""

  # Try standard mapping: cog-${name}
  if [[ -f "${KIRO_DIR}/cog-${name}/POWER.md" ]]; then
    kiro_file="${KIRO_DIR}/cog-${name}/POWER.md"
  # Try stripping -cog suffix: update-cog → cog-update
  elif [[ "$name" == *-cog ]] && [[ -f "${KIRO_DIR}/cog-${name%-cog}/POWER.md" ]]; then
    kiro_file="${KIRO_DIR}/cog-${name%-cog}/POWER.md"
  # Try exact name match
  elif [[ -f "${KIRO_DIR}/${name}/POWER.md" ]]; then
    kiro_file="${KIRO_DIR}/${name}/POWER.md"
  else
    return
  fi

  awk '
    /^---$/ { fm++; next }
    fm == 1 && /^keywords:/ {
      sub(/^keywords:[[:space:]]*\[/, "")
      sub(/\][[:space:]]*$/, "")
      # Remove quotes and clean up
      gsub(/"/, "")
      gsub(/,[[:space:]]+/, ",")
      print
      exit
    }
    fm >= 2 { exit }
  ' "$kiro_file" 2>/dev/null
}

# Parse roles array: [all] → all, [pm, eng] → pm,eng
parse_array() {
  local raw="$1"
  # Remove brackets, quotes, spaces after commas
  echo "$raw" | sed 's/^\[//; s/\]$//; s/"//g; s/,\s*/,/g; s/^[[:space:]]*//; s/[[:space:]]*$//'
}

# Convert "my-skill-name" to "COG My Skill Name"
make_display_name() {
  local name="$1"
  local title
  title=$(echo "$name" | tr '-' ' ' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')
  echo "COG ${title}"
}

# Curated keywords for skills without Kiro powers (extracted from "When to Invoke" sections)
get_curated_keywords() {
  local name="$1"
  case "$name" in
    auto-research)           echo "research,auto-research,investigate,strategic analysis,deep dive" ;;
    comprehensive-analysis)  echo "weekly analysis,comprehensive review,board prep,deep dive,comprehensive analysis" ;;
    create-user-story)       echo "create story,new story,add issue,write user story,create ticket,create user story" ;;
    export-open-issues)      echo "export issues,open issues,backlog audit,issue report,what's open,export open issues" ;;
    generate-prd)            echo "generate PRD,write PRD,product requirements,spec doc,feature spec,generate prd" ;;
    generate-release-notes)  echo "release notes,changelog,what shipped,write release notes,generate release notes" ;;
    meeting-transcript)      echo "process meeting,meeting notes,meeting transcript,extract action items,meeting" ;;
    publish-to-confluence)   echo "publish to Confluence,push to wiki,send to Confluence,confluence publish" ;;
    team-brief)              echo "team brief,team update,what did we ship,standup prep" ;;
    update-cog)              echo "update COG,check for updates,get latest COG version,update skills" ;;
    update-knowledge-base)   echo "update knowledge base,update KB,sync knowledge,update product docs" ;;
    scout)                   echo "scout,evaluate,should I save this,is this relevant,scout this,triage url" ;;
    *) echo "" ;;
  esac
}

# Generate basic keywords from skill name (last resort)
generate_keywords() {
  local name="$1"
  local spaced
  spaced=$(echo "$name" | tr '-' ' ')
  echo "${name},${spaced}"
}

# Extract body (everything after closing --- of frontmatter)
get_body() {
  local file="$1"
  awk 'BEGIN{fm=0} /^---$/{fm++; next} fm>=2{print}' "$file"
}

# ── Migrate one skill ──────────────────────────────────────────────
migrate_skill() {
  local skill_file="$1"
  local name description roles_raw integrations_raw
  local roles integrations keywords display_name

  name=$(get_field "name" "$skill_file")
  if [[ -z "$name" ]]; then
    warn "Skipping ${skill_file} — no 'name' in frontmatter"
    return 1
  fi

  description=$(get_field "description" "$skill_file")
  roles_raw=$(get_field "roles" "$skill_file")
  integrations_raw=$(get_field "integrations" "$skill_file")

  # Parse arrays
  roles=$(parse_array "$roles_raw")
  integrations=$(parse_array "$integrations_raw")

  # Get keywords: Kiro → curated map → generated from name
  keywords=$(get_kiro_keywords "$name")
  if [[ -z "$keywords" ]]; then
    keywords=$(get_curated_keywords "$name")
    if [[ -n "$keywords" ]]; then
      info "  ${YELLOW}(curated keywords)${RESET}"
    else
      keywords=$(generate_keywords "$name")
      info "  ${YELLOW}(generated keywords)${RESET}"
    fi
  fi

  display_name=$(make_display_name "$name")

  local target="${TARGET_DIR}/${name}/SKILL.md"

  echo -e "  ${BOLD}${name}${RESET}"
  echo -e "    roles: ${roles:-all}"
  echo -e "    integrations: ${integrations:-(none)}"
  echo -e "    keywords: ${keywords}"
  echo -e "    display-name: ${display_name}"
  echo -e "    → ${target}"

  if $DRY_RUN; then
    echo ""
    return 0
  fi

  mkdir -p "${TARGET_DIR}/${name}"

  # Build new frontmatter + body
  {
    echo '---'
    echo "name: ${name}"
    echo "description: ${description}"
    echo 'metadata:'
    echo "  roles: ${roles:-all}"
    if [[ -n "$integrations" ]]; then
      echo "  integrations: ${integrations}"
    fi
    echo "  keywords: ${keywords}"
    echo "  display-name: ${display_name}"
    echo '---'
    get_body "$skill_file"
  } > "$target"

  ok "  Written: ${target}"
  echo ""
}

# ── Main ────────────────────────────────────────────────────────────
main() {
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dry-run) DRY_RUN=true; shift ;;
      --help|-h) usage; exit 0 ;;
      *) err "Unknown option: $1"; usage; exit 1 ;;
    esac
  done

  echo ""
  echo -e "${BOLD}COG Skill Migration${RESET}"
  echo -e "═══════════════════"
  echo ""

  # Validate source exists
  if [[ ! -d "$SOURCE_DIR" ]]; then
    err "Source directory ${SOURCE_DIR}/ not found. Run from the COG root directory."
    exit 1
  fi

  # Check if target already exists
  if [[ -d "$TARGET_DIR" ]]; then
    warn "Target directory ${TARGET_DIR}/ already exists."
    warn "Existing files will be overwritten."
    echo ""
  fi

  # Count skills
  local skill_count=0
  for d in "${SOURCE_DIR}"/*/; do
    [[ -f "${d}SKILL.md" ]] && skill_count=$((skill_count + 1))
  done

  info "Found ${BOLD}${skill_count}${RESET} skills in ${SOURCE_DIR}/"
  $DRY_RUN && info "${YELLOW}Dry run — no files will be written${RESET}"
  echo ""

  # ── Migrate each skill ─────────────────────────────────────────
  local migrated=0 errors=0

  for skill_dir in "${SOURCE_DIR}"/*/; do
    [[ -d "$skill_dir" ]] || continue
    local skill_file="${skill_dir}SKILL.md"
    [[ -f "$skill_file" ]] || continue

    if migrate_skill "$skill_file"; then
      migrated=$((migrated + 1))
    else
      errors=$((errors + 1))
    fi
  done

  # ── Summary ────────────────────────────────────────────────────
  echo ""
  echo -e "${BOLD}Summary${RESET}"
  echo -e "───────"
  ok "Migrated: ${migrated}/${skill_count} skills"
  [[ $errors -gt 0 ]] && warn "Skipped: ${errors} (check warnings above)"

  if ! $DRY_RUN; then
    echo ""
    info "Next steps:"
    echo "  1. Review the new files:  ls ${TARGET_DIR}/"
    echo "  2. Run the sync script:   ./cog-sync.sh"
    echo "  3. Verify parity:         ./cog-sync.sh --check"
    echo "  4. Commit when satisfied"
  fi

  echo ""
}

main "$@"
