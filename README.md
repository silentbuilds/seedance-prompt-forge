# Seedance Prompt Forge

Turn a rough brief or failed Seedance 2.5 generation into a validated, copy-ready prompt.

[![CI](https://github.com/silentbuilds/seedance-prompt-forge/actions/workflows/ci.yml/badge.svg)](https://github.com/silentbuilds/seedance-prompt-forge/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/silentbuilds/seedance-prompt-forge)](https://github.com/silentbuilds/seedance-prompt-forge/releases/latest)
[![License: MIT](https://img.shields.io/github/license/silentbuilds/seedance-prompt-forge)](LICENSE)

[Install](#install) · [See the transformation](#before-and-after) ·
[Download the latest skill ZIP][latest-zip]

Seedance Prompt Forge is an open [Agent Skill](https://agentskills.io) for writing, auditing,
and repairing Seedance 2.5 video prompts. It names and binds every reference, structures
multi-stage events, converts vague creative direction into visible and audible cues, and runs
deterministic checks before you spend a generation.

It supports Claude Code and Cowork, Codex CLI, Cursor, Cline, GitHub Copilot, Gemini CLI, and
other Agent Skills-compatible tools. A browser-uploadable ZIP and single-file builds cover
chat-only surfaces.

## Before and after

The same creative idea becomes substantially easier for the model to follow once references,
timing, continuity, performance, and audio are made explicit.

### Original

```text
Create a 30-second vertical video in 9:16 format using the uploaded image, image1.jpg, as the visual reference for the main character. Keep the woman’s face, hairstyle, clothing, and overall appearance consistent throughout the video. Use audio.mp3 as the reference for her voice whenever she speaks.

The video begins on a rainy night, with the woman walking alone along a neon-lit city street. She appears sad, lost, and deep in thought. Alternate between wider shots of her walking and close-up shots of her face, falling raindrops, reflections on the wet street, and the surrounding city lights. Near the end, the rain gradually stops and the sky begins to brighten. She looks up, pauses, and gives a subtle smile, suggesting a renewed sense of hope.

Use a realistic, beautiful, and cinematic visual style. Keep camera movements and scene transitions smooth, and avoid changes or distortions to the character’s appearance.
```

### Optimized with Seedance Prompt Forge

```text
[Generation Goal]
Generate a photorealistic cinematic story of a solitary woman moving from quiet sadness to restrained hope on a rainy neon-lit city street.

[References]
@Image 1 defines the woman's face, hairstyle, clothing, and overall appearance. Use only those identity and wardrobe features; do not use the image background, composition, or any other people.
@Audio 1 defines the woman's speaking voice for her final line. Do not use it as music or as the city ambience.

[Stage 1 — 0-10 seconds]
Initial state: exactly one woman walks alone along a rain-soaked city street at night; cool blue and magenta neon signs reflect in the puddles. Her shoulders are slightly drawn in, her gaze stays low, and her pace is slow and thoughtful.
Primary event: a smooth wide follow shot tracks beside and slightly behind her as she walks through the rain.
End state: she reaches a brighter pool of reflected neon light, still walking alone in the same clothing.

[Stage 2 — 10-20 seconds]
Continue from the previous stage: keep the same continuous woman, face, hairstyle, clothing, street direction, rain intensity, and night setting.
Primary event: use smooth match cuts between close-ups of her pensive face, raindrops striking the wet pavement, rippling neon reflections, and blurred city lights; her eyes briefly scan the empty street and her lips press together.
End state: she slows to a stop beneath the fading rain, her face in close-up and her eyes beginning to lift.

[Stage 3 — 20-30 seconds]
Continue from the previous stage: the same woman remains alone and unchanged in the same spot. The rain gradually stops and the dark sky begins to brighten with soft warm dawn light.
Primary event: begin in a medium-wide view, then gently push in as she raises her head, takes a small steadying breath, and gives a subtle, believable smile. Dialogue language: English. In a quiet, reflective delivery using @Audio 1, the woman says: {Maybe there's still a way forward.}
End state: finish on a close-up of her calm face turned toward the brighter sky, with only a few residual drops on her hair and clothing.

[Maintain Consistency]
Keep exactly one continuous woman throughout; do not duplicate, split, replace, or distort her. Preserve her face, hairstyle, clothing, age, and overall appearance from @Image 1 across every shot. Maintain realistic rain physics, natural walking and facial motion, smooth camera movement, smooth match-cut transitions, and a coherent progression from cool neon night to softly warming dawn. No subtitles or on-screen text.

[Audio]
Ambience: steady rain, distant traffic, and a subdued nighttime city bed through the first two stages; the rain ambience thins naturally in the final stage.
Sound effects: soft footsteps on wet pavement and raindrops striking puddles.
Music: none.
```

### What the skill changed

| Improvement | Why it matters |
|---|---|
| **Explicit reference roles** | Converts filenames into `@Image 1` and `@Audio 1`, states what each reference controls, and excludes unwanted backgrounds, people, composition, music, and ambience. |
| **Stage timing** | Turns a broad 30-second arc into three event budgets with one primary change per stage. |
| **Continuity and end states** | Carries the same woman, wardrobe, direction, weather, location, and emotional progression from one stage into the next. |
| **Observable performance** | Replaces “sad, lost, and deep in thought” with lowered gaze, drawn-in shoulders, slow pacing, scanning eyes, a steadying breath, and a restrained smile. |
| **Camera intent** | Assigns a concrete follow shot, match cuts, close-ups, medium-wide framing, and a final push-in instead of asking only for smooth movement. |
| **Identity guardrails** | Locks exactly one continuous woman and explicitly forbids duplication, splitting, replacement, and distortion. |
| **Audio plan** | Separates voice, ambience, sound effects, and music; gives the voice reference an actual line and states its language and delivery. |
| **Generation parameters** | Keeps 9:16 in the generation controls rather than the prompt, while timestamps allocate the 30-second event budget. |

This comparison demonstrates prompt structure, not a guaranteed visual result. Output still
depends on the model, input materials, generation settings, and randomness.

## What it handles

| Workflow | What the skill adds |
|---|---|
| Text-to-video | Subject, event, scene, style, camera, and audio structure |
| Image/video/audio references | Individual bindings, inclusions, exclusions, and scene selection |
| 30-second multi-stage videos | Timed stages, continuity statements, and explicit end states |
| Failed generations | Symptom-to-cause diagnosis and the smallest corrective edit |
| Video editing | Sole editing master, edit scope, count locks, and timeline inheritance |
| Forward/backward extension | Boundary-frame, motion, spatial, and audio continuity |
| First/last frame and keyframes | One role per image and ordered state transitions |
| Storyboards and blockouts | Explicit structure, motion, material, and style inheritance |
| Dialogue and performance | Language, voice, delivery, emotion, ambience, music, and SFX |

## Install

### GitHub CLI — recommended

Preview the package before installing it:

```bash
gh skill preview silentbuilds/seedance-prompt-forge seedance-prompt-forge
gh skill install silentbuilds/seedance-prompt-forge seedance-prompt-forge
```

Start a new agent session after installation; skills are discovered at startup.

### Browser upload — ChatGPT and Claude

1. [Download the latest skill ZIP][latest-zip].
2. In ChatGPT, open **Settings → Plugins → Browse plugins → Skills**, then choose
   **Upload from your computer**. You can also open <https://chatgpt.com/skills>.
3. In Claude, open **Settings → Skills** or **Customize → Skills**, then choose
   **Create skill → Upload a skill**.
4. Select the ZIP and enable the skill.

![Uploading Seedance Prompt Forge on chatgpt.com](docs/chatgpt-com-upload-skill.png)

### Manual fallback

The distributable package lives in `skills/seedance-prompt-forge/`:

```bash
git clone https://github.com/silentbuilds/seedance-prompt-forge
cp -R seedance-prompt-forge/skills/seedance-prompt-forge \
  ~/.claude/skills/
```

Swap the destination for your agent:

| Agent | Personal | Project |
|---|---|---|
| Claude Code / Cowork | `~/.claude/skills/` | `.claude/skills/` |
| Codex CLI | `~/.agents/skills/` | `.agents/skills/` |
| Cursor | — | `.cursor/skills/` |
| GitHub Copilot | — | `.github/skills/` |
| Gemini CLI | `~/.gemini/skills/` | `.gemini/skills/` |
| Cline, Amp, OpenCode, Warp, Antigravity | — | `.agents/skills/` |

To install into several detected agents or an explicit project:

```bash
./scripts/install.sh
./scripts/install.sh claude codex
./scripts/install.sh --project /path/to/your-project
./scripts/install.sh --list
```

The fallback installer refuses to overwrite an installation. Add `--force` to create a
timestamped backup and replace it:

```bash
./scripts/install.sh --force --project /path/to/your-project
```

## Use it

Ask naturally—the skill chooses whether to author, audit, or diagnose:

```text
Use Seedance Prompt Forge to turn this idea and my three references into a copy-ready prompt.

Audit this Seedance prompt before I generate it.

These two characters swapped faces and the prop duplicated. Diagnose the failure and repair
only what caused it.
```

## Deterministic prompt checks

The optional Python linter catches mechanically verifiable problems:

- cited references that were never assigned a role;
- gaps or collective mappings in reference numbering;
- unfilled `<placeholders>`;
- reversed, overlapping, or invalid time ranges;
- per-second frequency demands;
- parameters placed in the prompt or requested for tasks that lock them;
- scene references without an exclusion or an `only …` scope;
- replacement edits missing a target count or timeline inheritance;
- unbalanced dialogue/subtitle markers; and
- non-Chinese dialogue with no stated language.

```bash
python3 skills/seedance-prompt-forge/scripts/lint_prompt.py \
  my-prompt.txt --task edit
```

The linter has no third-party dependencies and supports Python 3.8+.

## Quality and provenance

```bash
python3 scripts/run_tests.py
python3 scripts/run_tests.py --guide /path/to/authorized-guide-export.md
```

The committed suite includes positive and negative coverage for every advertised lint rule.
When an authorized guide export is supplied, the regression runner checks that the linter
rejects none of the guide's filled examples.

The exact guide editions, verification date, platform boundaries, and distinction between
documented guidance, tested implementation, and working inference are recorded in
[source provenance](SOURCES.md).

This repository targets Dreamina Seedance 2.5. Verify behavior before applying its templates
to another Seedance version, provider, product surface, or API.

Generation results vary with input materials, task complexity, settings, and randomness.

## Contributing

Read `AGENTS.md` before changing skill guidance or linter rules. Generated files in `dist/`
must be regenerated whenever the runtime skill changes.

## Independent project

Seedance Prompt Forge is independent and unofficial. It is not affiliated with, authorised
by, or endorsed by ByteDance, BytePlus, or Dreamina. Seedance and Dreamina are trademarks of
their respective owners.

MIT licensed — see [LICENSE](LICENSE).

[latest-zip]: https://github.com/silentbuilds/seedance-prompt-forge/releases/latest/download/seedance-prompt-forge.zip
