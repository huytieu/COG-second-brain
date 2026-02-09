#!/usr/bin/env bash
# COG Upstream Update Script
# Safely updates framework files (skills, docs, scripts) without touching your personal content.
#
# Usage:
#   ./cog-update.sh            Interactive update
#   ./cog-update.sh --check    Check for available updates (no changes)
#   ./cog-update.sh --dry-run  Show what would change (no changes)
#   ./cog-update.sh --force    Update all framework files without prompting
#   ./cog-update.sh --help     Show this help message

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────
REMOTE_NAME="cog-upstream"
REMOTE_URL="https://github.com/huytieu/COG-second-brain.git"
BRANCH="main"
VERSION_FILE="COG-VERSION"

# Framework files — these are safe to overwrite (your content is never in this list)
FRAMEWORK_FILES=(
  # Core docs
  "README.md"
  "SETUP.md"
  "AGENTS.md"
  "GEMINI.md"
  "CHANGELOG.md"
  "CONTRIBUTING.md"
  "LICENSE"
  "COG-VERSION"
  "cog-update.sh"

  # Claude Code skills
  ".claude/skills/onboarding/SKILL.md"
  ".claude/skills/braindump/SKILL.md"
  ".claude/skills/daily-brief/SKILL.md"
  ".claude/skills/weekly-checkin/SKILL.md"
  ".claude/skills/knowledge-consolidation/SKILL.md"
  ".claude/skills/url-dump/SKILL.md"
  ".claude/skills/update-cog/SKILL.md"

  # Kiro powers
  ".kiro/powers/cog-onboarding/POWER.md"
  ".kiro/powers/cog-braindump/POWER.md"
  ".kiro/powers/cog-daily-brief/POWER.md"
  ".kiro/powers/cog-weekly-checkin/POWER.md"
  ".kiro/powers/cog-knowledge-consolidation/POWER.md"
  ".kiro/powers/cog-url-dump/POWER.md"
  ".kiro/powers/cog-update/POWER.md"

  # Gemini CLI
  ".gemini/commands/onboarding.toml"
  ".gemini/commands/braindump.toml"
  ".gemini/commands/daily-brief.toml"
  ".gemini/commands/weekly-checkin.toml"
  ".gemini/commands/knowledge-consolidation.toml"
  ".gemini/commands/url-dump.toml"
  ".gemini/commands/update-cog.toml"
  ".gemini/skills/onboarding.md"
  ".gemini/skills/braindump.md"
  ".gemini/skills/daily-brief.md"
  ".gemini/skills/weekly-checkin.md"
  ".gemini/skills/knowledge-consolidation.md"
  ".gemini/skills/url-dump.md"
  ".gemini/skills/update-cog.md"

  # Plugin metadata
  ".claude-plugin/plugin.json"
  "marketplace-entry.json"

  # Git infrastructure
  ".gitignore"
)

# ── Helpers ──────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

info()  { echo -e "${CYAN}ℹ${RESET}  $*"; }
ok()    { echo -e "${GREEN}✓${RESET}  $*"; }
warn()  { echo -e "${YELLOW}⚠${RESET}  $*"; }
err()   { echo -e "${RED}✗${RESET}  $*" >&2; }

usage() {
  cat <<'EOF'
COG Upstream Update Script

Updates framework files (skills, docs, scripts) from the official COG repo
without touching your personal content (braindumps, profiles, notes).

Usage:
  ./cog-update.sh            Interactive update (prompts per file)
  ./cog-update.sh --check    Check for available updates (no changes)
  ./cog-update.sh --dry-run  Show what would change (no changes)
  ./cog-update.sh --force    Update all framework files without prompting
  ./cog-update.sh --help     Show this help message

How it works:
  1. Adds/fetches the upstream remote (cog-upstream)
  2. Compares each framework file against the upstream version
  3. Offers to update changed files (interactive mode) or updates all (--force)
  4. Your content folders (00-inbox, 01-daily, etc.) are NEVER modified

Safe to run anytime — your notes, profiles, and braindumps are never touched.
EOF
}

# ── Ensure remote exists & fetch ─────────────────────────────────────
ensure_remote() {
  if ! git remote get-url "$REMOTE_NAME" &>/dev/null; then
    info "Adding remote ${BOLD}${REMOTE_NAME}${RESET} → ${REMOTE_URL}"
    git remote add "$REMOTE_NAME" "$REMOTE_URL"
  fi
  info "Fetching latest from ${BOLD}${REMOTE_NAME}/${BRANCH}${RESET}..."
  git fetch "$REMOTE_NAME" "$BRANCH" --quiet
}

# ── Get local and upstream versions ──────────────────────────────────
local_version() {
  if [[ -f "$VERSION_FILE" ]]; then
    cat "$VERSION_FILE" | tr -d '[:space:]'
  else
    echo "unknown"
  fi
}

upstream_version() {
  git show "${REMOTE_NAME}/${BRANCH}:${VERSION_FILE}" 2>/dev/null | tr -d '[:space:]' || echo "unknown"
}

# ── Diff a single file ──────────────────────────────────────────────
file_has_changes() {
  local file="$1"
  # File exists upstream?
  if ! git show "${REMOTE_NAME}/${BRANCH}:${file}" &>/dev/null; then
    return 1  # no upstream version
  fi
  # File differs from upstream?
  if [[ -f "$file" ]]; then
    ! diff -q <(git show "${REMOTE_NAME}/${BRANCH}:${file}" 2>/dev/null) "$file" &>/dev/null
  else
    return 0  # file missing locally → counts as changed
  fi
}

# ── Update a single file from upstream ───────────────────────────────
update_file() {
  local file="$1"
  local dir
  dir=$(dirname "$file")
  [[ "$dir" != "." ]] && mkdir -p "$dir"
  git show "${REMOTE_NAME}/${BRANCH}:${file}" > "$file" 2>/dev/null
}

# ── Backup a file before overwriting ─────────────────────────────────
backup_file() {
  local file="$1"
  if [[ -f "$file" ]]; then
    local backup="${file}.backup-$(date +%Y%m%d-%H%M%S)"
    cp "$file" "$backup"
    echo "$backup"
  fi
}

# ── Main logic ───────────────────────────────────────────────────────
main() {
  local mode="interactive"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --check)   mode="check";   shift ;;
      --dry-run) mode="dry-run"; shift ;;
      --force)   mode="force";   shift ;;
      --help|-h) usage; exit 0 ;;
      *) err "Unknown option: $1"; usage; exit 1 ;;
    esac
  done

  # Sanity check — are we in a git repo?
  if ! git rev-parse --is-inside-work-tree &>/dev/null; then
    err "Not inside a git repository. Run this from your COG folder."
    exit 1
  fi

  echo ""
  echo -e "${BOLD}COG Upstream Update${RESET}"
  echo -e "─────────────────────"
  echo ""

  ensure_remote

  local lv uv
  lv=$(local_version)
  uv=$(upstream_version)

  info "Local version:    ${BOLD}${lv}${RESET}"
  info "Upstream version: ${BOLD}${uv}${RESET}"
  echo ""

  if [[ "$uv" == "unknown" ]]; then
    err "Could not read upstream version. Check your internet connection."
    exit 1
  fi

  # Collect changed files
  local changed=()
  local new_files=()
  for file in "${FRAMEWORK_FILES[@]}"; do
    if file_has_changes "$file"; then
      if [[ -f "$file" ]]; then
        changed+=("$file")
      else
        new_files+=("$file")
      fi
    fi
  done

  local total=$(( ${#changed[@]} + ${#new_files[@]} ))

  if [[ $total -eq 0 ]]; then
    ok "Everything is up to date! (v${lv})"
    exit 0
  fi

  info "${BOLD}${#changed[@]}${RESET} file(s) changed, ${BOLD}${#new_files[@]}${RESET} new file(s) available"
  echo ""

  # ── Check mode ───────────────────────────────────────────────────
  if [[ "$mode" == "check" ]]; then
    if [[ ${#changed[@]} -gt 0 ]]; then
      echo -e "${BOLD}Changed:${RESET}"
      for f in "${changed[@]}"; do echo "  ~ $f"; done
    fi
    if [[ ${#new_files[@]} -gt 0 ]]; then
      echo -e "${BOLD}New:${RESET}"
      for f in "${new_files[@]}"; do echo "  + $f"; done
    fi
    echo ""
    info "Run ${BOLD}./cog-update.sh${RESET} to update, or ${BOLD}./cog-update.sh --dry-run${RESET} to preview."
    exit 0
  fi

  # ── Dry-run mode ─────────────────────────────────────────────────
  if [[ "$mode" == "dry-run" ]]; then
    echo -e "${BOLD}Dry run — no changes will be made:${RESET}"
    echo ""
    if [[ ${#changed[@]} -gt 0 ]]; then
      echo "Would update:"
      for f in "${changed[@]}"; do echo "  ~ $f"; done
    fi
    if [[ ${#new_files[@]} -gt 0 ]]; then
      echo "Would create:"
      for f in "${new_files[@]}"; do echo "  + $f"; done
    fi
    echo ""
    info "Run ${BOLD}./cog-update.sh --force${RESET} to apply all, or ${BOLD}./cog-update.sh${RESET} for interactive mode."
    exit 0
  fi

  # ── Force mode ───────────────────────────────────────────────────
  if [[ "$mode" == "force" ]]; then
    local updated=0
    for f in "${changed[@]}" "${new_files[@]}"; do
      if [[ -f "$f" ]]; then
        backup_file "$f" >/dev/null
      fi
      update_file "$f"
      ok "Updated: $f"
      ((updated++))
    done
    echo ""
    ok "Updated ${updated} file(s) to v${uv}"
    info "Backups saved as *.backup-YYYYMMDD-HHMMSS alongside originals"
    exit 0
  fi

  # ── Interactive mode ─────────────────────────────────────────────
  local updated=0 skipped=0

  # New files first
  if [[ ${#new_files[@]} -gt 0 ]]; then
    echo -e "${BOLD}New files available:${RESET}"
    for f in "${new_files[@]}"; do
      echo -ne "  ${GREEN}+${RESET} ${f} — add? [Y/n] "
      read -r answer
      if [[ -z "$answer" || "$answer" =~ ^[Yy] ]]; then
        update_file "$f"
        ok "Added: $f"
        ((updated++))
      else
        warn "Skipped: $f"
        ((skipped++))
      fi
    done
    echo ""
  fi

  # Changed files
  if [[ ${#changed[@]} -gt 0 ]]; then
    echo -e "${BOLD}Changed files:${RESET}"
    for f in "${changed[@]}"; do
      echo -ne "  ${YELLOW}~${RESET} ${f} — update? [Y/n/d(iff)/b(ackup+update)] "
      read -r answer
      case "$answer" in
        d|D|diff)
          diff --color=auto <(cat "$f") <(git show "${REMOTE_NAME}/${BRANCH}:${f}") || true
          echo -ne "  Update this file? [Y/n/b] "
          read -r answer2
          if [[ -z "$answer2" || "$answer2" =~ ^[Yy] ]]; then
            update_file "$f"
            ok "Updated: $f"
            ((updated++))
          elif [[ "$answer2" =~ ^[Bb] ]]; then
            local bk
            bk=$(backup_file "$f")
            update_file "$f"
            ok "Updated: $f (backup: $bk)"
            ((updated++))
          else
            warn "Skipped: $f"
            ((skipped++))
          fi
          ;;
        b|B)
          local bk
          bk=$(backup_file "$f")
          update_file "$f"
          ok "Updated: $f (backup: $bk)"
          ((updated++))
          ;;
        n|N)
          warn "Skipped: $f"
          ((skipped++))
          ;;
        *)
          update_file "$f"
          ok "Updated: $f"
          ((updated++))
          ;;
      esac
    done
  fi

  echo ""
  echo -e "${BOLD}Summary:${RESET}"
  ok "${updated} file(s) updated"
  [[ $skipped -gt 0 ]] && warn "${skipped} file(s) skipped"
  echo ""

  if [[ $updated -gt 0 ]]; then
    info "Review changes with ${BOLD}git diff${RESET}, then commit when ready:"
    echo "  git add -A && git commit -m \"Update COG framework to v${uv}\""
  fi
}

main "$@"
