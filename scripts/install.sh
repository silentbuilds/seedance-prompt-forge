#!/usr/bin/env bash
# Install seedance-prompt-forge into one or more agents' skills directories.
#
#   ./scripts/install.sh              # every agent detected on this machine
#   ./scripts/install.sh claude codex # named agents
#   ./scripts/install.sh --project    # into ./.agents/skills (neutral, commit to repo)
#   ./scripts/install.sh --list       # show paths without writing
#
# The Agent Skills format is identical across agents. Only the directory differs.

set -euo pipefail

NAME="seedance-prompt-forge"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$REPO_ROOT/skills/$NAME"

# agent : destination directory
PERSONAL=(
  "claude:$HOME/.claude/skills"
  "codex:$HOME/.codex/skills"
  "openclaw:$HOME/.openclaw/skills"
  "gemini:$HOME/.gemini/skills"
)
# Project-scoped. .agents/skills is the vendor-neutral path several agents read.
PROJECT=(
  "neutral:$PWD/.agents/skills"
  "cursor:$PWD/.cursor/skills"
  "copilot:$PWD/.github/skills"
  "claude-project:$PWD/.claude/skills"
  "codex-project:$PWD/.codex/skills"
)

usage() { sed -n '2,10p' "$0" | sed 's/^# \{0,1\}//'; exit 0; }

list_paths() {
  echo "Personal (whole machine):"
  for e in "${PERSONAL[@]}"; do printf '  %-16s %s\n' "${e%%:*}" "${e#*:}/$NAME"; done
  echo "Project (this directory):"
  for e in "${PROJECT[@]}"; do printf '  %-16s %s\n' "${e%%:*}" "${e#*:}/$NAME"; done
}

install_to() {
  local dest="$1/$NAME"
  mkdir -p "$1"
  rm -rf "$dest"
  mkdir -p "$dest"
  # Ship only what an agent needs at runtime.
  cp "$SRC/SKILL.md" "$dest/"
  cp -r "$SRC/references" "$dest/"
  mkdir -p "$dest/scripts" && cp "$SRC/scripts/lint_prompt.py" "$dest/scripts/"
  [ -d "$SRC/agents" ] && cp -r "$SRC/agents" "$dest/"
  [ -f "$SRC/LICENSE" ] && cp "$SRC/LICENSE" "$dest/"
  echo "  installed -> $dest"
}

[ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ] && usage
[ "${1:-}" = "--list" ] && { list_paths; exit 0; }

if [ "${1:-}" = "--project" ]; then
  echo "Installing project-scoped:"
  for e in "${PROJECT[@]}"; do install_to "${e#*:}"; done
  echo
  echo "Commit .agents/skills/$NAME so collaborators get it automatically."
  exit 0
fi

if [ $# -gt 0 ]; then
  for want in "$@"; do
    found=0
    for e in "${PERSONAL[@]}" "${PROJECT[@]}"; do
      [ "${e%%:*}" = "$want" ] && { echo "$want:"; install_to "${e#*:}"; found=1; }
    done
    [ $found -eq 0 ] && { echo "unknown agent: $want" >&2; list_paths; exit 1; }
  done
  exit 0
fi

# No arguments: install where a parent directory already exists.
echo "Detecting installed agents..."
any=0
for e in "${PERSONAL[@]}"; do
  agent="${e%%:*}"; dir="${e#*:}"
  if [ -d "$(dirname "$dir")" ]; then echo "$agent:"; install_to "$dir"; any=1; fi
done
if [ $any -eq 0 ]; then
  echo "No agent home directories found. Pick one explicitly, or use --project."
  list_paths
  exit 1
fi
echo
echo "Start a new agent session for the skill to be discovered."
