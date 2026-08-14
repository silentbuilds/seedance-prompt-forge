#!/usr/bin/env python3
"""Flatten the skill into one Markdown file for agents with no filesystem.

Progressive disclosure needs a filesystem: the agent reads SKILL.md, then loads the
reference file the task calls for. ChatGPT Custom GPTs, Claude Projects, Gemini Gems and
plain chat have no such mechanism, so they need everything inlined up front.

    python3 scripts/build_bundle.py

Writes dist/seedance-prompt-forge.bundle.md. Regenerate after editing any source file;
CI checks that the bundle is not stale.
"""

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "dist" / "seedance-prompt-forge.bundle.md"

# Order matters: routing first, then the material it routes to.
ORDER = [
    "references/core-and-examples.md",
    "references/reference-materials.md",
    "references/long-videos.md",
    "references/video-editing.md",
    "references/advanced-modes.md",
    "references/audio-and-performance.md",
    "references/checklist.md",
]

HEADER = """<!-- GENERATED FILE - do not edit. Run scripts/build_bundle.py. -->
# Seedance Prompt Forge - single-file bundle

For agents that cannot read files on demand: ChatGPT Custom GPT instructions, Claude Project
instructions, Gemini Gems, or a plain chat window. Paste the whole thing.

Everything below is inlined. Where the instructions say "read
`references/<file>`", the content is already present under the matching heading in this
document - scroll to it instead of trying to open a file.

The linter at `scripts/lint_prompt.py` is not included here, because these surfaces usually
cannot execute code. Use the nine manual checks in "Running without code execution" instead.
If your environment does have code execution, fetch the script from the repository.

---

"""


def demote(md: str, levels: int = 1) -> str:
    """Push headings down so inlined files nest under their section heading."""
    out = []
    fenced = False
    for line in md.splitlines():
        if line.lstrip().startswith("```"):
            fenced = not fenced
        if not fenced and line.startswith("#"):
            line = "#" * levels + line
        out.append(line)
    return "\n".join(out)


def main() -> int:
    skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
    # drop YAML frontmatter - meaningless when pasted into a chat box
    if skill.startswith("---"):
        skill = skill.split("---", 2)[2].lstrip("\n")

    parts = [HEADER, demote(skill, 1), "\n\n---\n"]

    missing = [p for p in ORDER if not (ROOT / p).exists()]
    if missing:
        print(f"error: missing source files: {missing}", file=sys.stderr)
        return 1
    for rel in ORDER:
        body = (ROOT / rel).read_text(encoding="utf-8")
        parts.append(f"\n## Inlined: `{rel}`\n\n")
        parts.append(demote(body, 2))
        parts.append("\n\n---\n")

    # Second output: a compact version that fits ChatGPT's 8,000-char instructions field.
    # Long tables move to the knowledge file; routing and rules stay inline.
    compact = skill
    start = compact.find("| Symptom | Likely cause | Smallest fix |")
    if start != -1:
        end = compact.find("\nSome failures are not prompt failures", start)
        compact = (compact[:start]
                   + "The symptom-to-fix table is in the uploaded knowledge file under\n"
                     "\"Route B\". Consult it before revising - map the symptom to the single\n"
                     "smallest change rather than rewriting.\n"
                   + compact[end:])
    s2 = compact.find("## Running without code execution")
    if s2 != -1:
        e2 = compact.find("## Route A", s2)
        compact = (compact[:s2]
                   + "## Checking your work\n\n"
                     "You cannot run the linter here. Work the nine manual checks listed under\n"
                     "\"Running without code execution\" in the knowledge file before delivering,\n"
                     "and tell the user the checks were done by reading rather than by running.\n\n"
                   + compact[e2:])
    compact = compact.replace(
        "| Task | Reference file |", "| Task | Section of the uploaded knowledge file |")
    compact = compact.replace("`references/", "`Inlined: references/")
    compact = ("# Seedance Prompt Forge\n\n"
               "Paste into the ChatGPT Custom GPT instructions field, or Claude Project / Gemini\n"
               "Gem instructions. Upload seedance-prompt-forge.bundle.md as a knowledge file\n"
               "alongside it; the section names below refer to headings in that file.\n\n---\n\n"
               + compact.split("\n", 1)[1].lstrip("\n"))
    COMPACT = OUT.parent / "chatgpt-instructions.md"
    COMPACT.parent.mkdir(parents=True, exist_ok=True)
    COMPACT.write_text(compact, encoding="utf-8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(parts).rstrip() + "\n"
    OUT.write_text(text, encoding="utf-8")

    words = len(text.split())
    print(f"wrote {OUT.relative_to(ROOT)}")
    print(f"  {len(text):,} chars, ~{words:,} words, ~{int(words * 1.4):,} tokens (rough)")
    print(f"wrote {COMPACT.relative_to(ROOT)}")
    status = "fits" if len(compact) <= 8000 else "OVER LIMIT"
    print(f"  {len(compact):,} chars - {status} the 8,000-char instructions field")
    if len(text) > 8000:
        print("  note: exceeds the ChatGPT Custom GPT instructions field (8,000 chars).")
        print("        Upload it as a knowledge file and keep a short pointer in the")
        print("        instructions field - see README.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
