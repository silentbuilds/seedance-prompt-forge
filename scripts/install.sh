#!/usr/bin/env bash
# Install seedance-prompt-forge into one or more agents' skills directories.
#
#   ./scripts/install.sh                         # every personal agent detected
#   ./scripts/install.sh claude codex            # named personal agents
#   ./scripts/install.sh --project /path/to/repo  # explicit project-scoped install
#   ./scripts/install.sh --force claude           # back up and replace an install
#   ./scripts/install.sh --list                    # show paths without writing
#
# The Agent Skills format is identical across agents. Only the directory differs.

set -euo pipefail

NAME="seedance-prompt-forge"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/skills/$NAME"
FORCE=0

ARGS=()
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    *) ARGS+=("$arg") ;;
  esac
done
set -- "${ARGS[@]}"

# agent : destination directory
PERSONAL=(
  "claude:$HOME/.claude/skills"
  "codex:$HOME/.codex/skills"
  "openclaw:$HOME/.openclaw/skills"
  "gemini:$HOME/.gemini/skills"
)
set_project_paths() {
  local project_root="$1"
  PROJECT=(
    "neutral:$project_root/.agents/skills"
    "cursor:$project_root/.cursor/skills"
    "copilot:$project_root/.github/skills"
    "claude-project:$project_root/.claude/skills"
  )
}

set_project_paths "$PWD"

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }

list_paths() {
  echo "Personal (whole machine):"
  for e in "${PERSONAL[@]}"; do printf '  %-16s %s\n' "${e%%:*}" "${e#*:}/$NAME"; done
  echo "Project (this directory):"
  for e in "${PROJECT[@]}"; do printf '  %-16s %s\n' "${e%%:*}" "${e#*:}/$NAME"; done
}

install_to() {
  local dest="$1/$NAME"
  local backup stamp suffix
  if [ -e "$dest" ] || [ -L "$dest" ]; then
    stamp="$(date +%Y%m%d%H%M%S)"
    backup="$dest.backup-$stamp"
    suffix=1
    while [ -e "$backup" ] || [ -L "$backup" ]; do
      backup="$dest.backup-$stamp-$suffix"
      suffix=$((suffix + 1))
    done
    mv "$dest" "$backup"
    echo "  backed up -> $backup"
  fi
  mkdir -p "$1"
  mkdir -p "$dest"
  cp -R "$SRC/." "$dest/"
  echo "  installed -> $dest"
}

preflight() {
  local failed=0 dest
  [ "$FORCE" -eq 1 ] && return 0
  for base in "$@"; do
    dest="$base/$NAME"
    if [ -e "$dest" ] || [ -L "$dest" ]; then
      echo "existing install found: $dest" >&2
      failed=1
    fi
  done
  if [ "$failed" -eq 1 ]; then
    echo "Re-run with --force to back up and replace existing installs." >&2
    return 1
  fi
}

[ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ] && usage
[ "${1:-}" = "--list" ] && { list_paths; exit 0; }

if [ "${1:-}" = "--project" ]; then
  [ $# -eq 2 ] || { echo "--project requires exactly one target path" >&2; exit 2; }
  [ -d "$2" ] || { echo "project path does not exist: $2" >&2; exit 2; }
  project_root="$(cd "$2" && pwd)"
  set_project_paths "$project_root"
  bases=()
  for e in "${PROJECT[@]}"; do bases+=("${e#*:}"); done
  preflight "${bases[@]}"
  echo "Installing project-scoped:"
  for e in "${PROJECT[@]}"; do install_to "${e#*:}"; done
  echo
  echo "Commit $project_root/.agents/skills/$NAME so collaborators get it automatically."
  exit 0
fi

if [ $# -gt 0 ]; then
  bases=()
  for want in "$@"; do
    found=0
    for e in "${PERSONAL[@]}"; do
      [ "${e%%:*}" = "$want" ] && { bases+=("${e#*:}"); found=1; }
    done
    [ $found -eq 0 ] && { echo "unknown agent: $want" >&2; list_paths; exit 1; }
  done
  preflight "${bases[@]}"
  for want in "$@"; do
    for e in "${PERSONAL[@]}"; do
      [ "${e%%:*}" = "$want" ] && { echo "$want:"; install_to "${e#*:}"; }
    done
  done
  exit 0
fi

# No arguments: install where a parent directory already exists.
echo "Detecting installed agents..."
any=0
detected=()
for e in "${PERSONAL[@]}"; do
  agent="${e%%:*}"; dir="${e#*:}"
  if [ -d "$(dirname "$dir")" ]; then detected+=("$e"); any=1; fi
done
if [ $any -eq 0 ]; then
  echo "No agent home directories found. Pick one explicitly, or use --project."
  list_paths
  exit 1
fi
detected_bases=()
for e in "${detected[@]}"; do detected_bases+=("${e#*:}"); done
preflight "${detected_bases[@]}"
for e in "${detected[@]}"; do
  echo "${e%%:*}:"
  install_to "${e#*:}"
done
echo
echo "Start a new agent session for the skill to be discovered."
