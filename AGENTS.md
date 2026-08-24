# AGENTS.md

Context for AI coding agents working **on this repository**. If you are looking for how to
*use* the skill, read `skills/seedance-prompt-forge/SKILL.md` instead — that is the product.

## What this is

`seedance-prompt-forge` is a single Agent Skill: a procedure for writing, auditing, and
repairing prompts for Seedance 2.5 video generation. The distributable skill lives under
`skills/seedance-prompt-forge/`; repository-level files support development and release.

- `skills/seedance-prompt-forge/SKILL.md` — routing and universal rules. Loaded whenever the
  skill activates. Keep under 500 lines and roughly 5,000 tokens.
- `skills/seedance-prompt-forge/references/*.md` — task-specific templates. Loaded on demand,
  one level deep only.
- `skills/seedance-prompt-forge/scripts/lint_prompt.py` — deterministic checks. No third-party
  dependencies. Python 3.8+.
- `dist/` — generated. Never edit by hand.

## Commands

```bash
python3 scripts/run_tests.py                      # fixtures only
python3 scripts/run_tests.py --guide GUIDE.md     # plus regression against the official guide
python3 scripts/build_bundle.py                   # regenerate dist/
./scripts/install.sh --list                       # show per-agent install paths
```

There is no build step for the skill itself. It is Markdown.

## Rules specific to this repo

**Fidelity to the source guide is the product.** Every template and rule traces to the
official Dreamina Seedance 2.5 prompt guide. When you add or change guidance:

- If the guide states it, state it the same way. Do not compress a structured block template
  into prose — block structure is what users copy.
- If the guide does not state it, either leave it out or mark it inline as an assumption. The
  `@Image` numbering note in `references/reference-materials.md` is the worked example of how
  to phrase an unsourced inference.
- Never present an inference as documented platform behaviour.

**The linter must never reject the guide's own examples.** `run_tests.py --guide` enforces
this. Any new check has to survive all 29 filled examples with zero errors before it ships.
Warnings are acceptable where they represent a defensible tightening; errors are not.

**Regenerate `dist/` after touching the skill's `SKILL.md` or `references/`.** The bundle is what
chat-only surfaces consume; a stale bundle ships wrong instructions to ChatGPT and Claude
Project users.

**Keep frontmatter portable.** `name`, `description`, `license`, `compatibility`, `metadata`
only. `name` must match the directory name. Agent-specific fields such as `allowed-tools` are
ignored by most agents and are not worth the incompatibility.

**Version numbers live in `metadata.version`**, not as a top-level frontmatter key — a
top-level `version` is not in the Agent Skills spec and some implementations reject it.

## Scope boundary

This repo describes prompt construction. It does not call any generation API, ship model
weights, or reproduce generated media. Keep it that way — it is what lets the skill run
unmodified inside every agent without credentials or network access.
