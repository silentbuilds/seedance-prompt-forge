---
name: seedance-prompt-forge
description: >
  Write, audit, and repair prompts for Seedance 2.5 video generation. Use whenever the user
  mentions Seedance, Dreamina, or a Seedance/Dreamina video prompt — and also when they want to
  fix a video generation that came out wrong, even if they never name the model. Covers
  text-to-video; reference-driven generation with images, videos, or audio; 30-second
  multi-stage videos; video editing; forward or backward extension; first/last-frame and
  multi-keyframe generation; storyboard grids; coarse or fine blockout re-rendering; one-click
  video; and seamless transitions. Symptoms it fixes: swapped subjects, identity or clothing
  drift, backgrounds or people leaking from references, all references appearing at once,
  missing or rushed events, broken continuity across a cut, dialogue in the wrong language.
  Trigger phrases: "Seedance prompt", "Dreamina prompt", "optimize my video prompt",
  "why did my video come out wrong", "fix this generation".
license: MIT
compatibility: >
  Pure Markdown; runs in any agent that reads the Agent Skills format. The optional linter in
  scripts/ needs Python 3.8+ and code execution. Without code execution, follow the manual
  checklist instead - see "Running without code execution".
metadata:
  version: "2.0.0"
  author: seedance-prompt-forge
  source-guide: Dreamina Seedance 2.5 official prompt guide
---

# Seedance Prompt Forge

Turn an idea, draft prompt, reference set, or failed generation into a copy-ready Seedance 2.5
prompt. Prompts are flexible natural language built from optional components; every reference
material gets an explicit role.

Sources: the [Dreamina Seedance 2.5 Prompt Writing Guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh)
and its [official BytePlus release](https://docs.byteplus.com/en/docs/ModelArk/2607689). Do not
apply these templates to other Seedance versions without checking that version's own guidance.
Platform behaviours described here are documented for Dreamina or for the surfaces the guide
explicitly names; verify the controls available on the user's product or API.

## Pick a route

| The user gives you | Route |
|---|---|
| An idea, brief, or reference set | **A — Author** |
| A generation that came out wrong (with or without the prompt) | **B — Diagnose** |
| An existing prompt, no output yet | **C — Audit** |

Routes B and C both end by re-entering Route A step 3.

## Core structure

Components, in priority order:

**Subject + Action/Event + Scene/Environment + Visual Style + Camera Movement/Cut + Audio**

- Lead with what you want generated: the subject and its primary action or event.
- Add only the components that matter; omit the rest.
- Keep generation parameters (duration, aspect ratio, resolution, audio toggle) out of the
  prompt. They are set on the generation page or through the API.

```text
<Subject> performs <primary action or event> in <scene and environment>.
The visuals feature <visual style>.
Use <shot size, camera angle, camera movement, or cuts>.
Audio includes <dialogue, ambience, sound effects, or music>.
```

Worked examples of complete briefs turned into finished prompts:
`references/core-and-examples.md`.

## Running without code execution

`scripts/lint_prompt.py` is optional. Where it cannot run — a chat-only assistant, a Custom
GPT without Code Interpreter, a project with no shell — do not skip the checks; perform them by
reading. In order, on the drafted prompt:

1. List every `@Image`/`@Video`/`@Audio` number in the body. Each one must appear in a role
   line. Any that does not is an error.
2. Numbers of each kind must run 1, 2, 3… with no gaps.
3. No collective binding ("@Images 1 through 4 define four characters respectively").
4. No `<angle-bracket placeholder>` left unfilled.
5. Time ranges consecutive, non-overlapping, each moving forward. No frequency demands.
6. On editing / extension / first-last-frame tasks: no aspect ratio, duration, or resolution
   request anywhere in the prompt.
7. Scene and environment references carry an exclusion or an "only …" scope.
8. Replacement edits state an exact target count and a `[Timeline Inheritance]` block.
9. `{}` and `【】` balanced; non-Chinese dialogue preceded by a stated language.

State which checks were run by reading rather than by running, so the user knows.

## Route A — Author

### A1. Identify the task type and load guidance

| Task | Reference file |
|---|---|
| Text-to-video; worked end-to-end examples | `references/core-and-examples.md` |
| Image/video/audio references; multiple subjects, props, or scenes; per-scene selection | `references/reference-materials.md` |
| 30-second multi-event videos; timing control | `references/long-videos.md` |
| Editing an existing video; forward/backward extension | `references/video-editing.md` |
| First/last frame, keyframes, storyboards, blockouts, one-click video, seamless transitions | `references/advanced-modes.md` |
| Dialogue, voice, music/SFX, emotion, camera terminology | `references/audio-and-performance.md` |
| Final check before delivery | `references/checklist.md` |

Read the matching reference file(s) before drafting. More than one may apply.

### A2. Collect the brief — ask only about blockers

Two classes of missing information. Treat them differently.

**Blocking — you cannot write a correct prompt without it. Ask.**

- Which reference material corresponds to which character, prop, or scene.
- Edit target and edit scope, for an editing task.
- Extension direction (forward or backward), for an extension task.
- Keyframe order and which image is first/last, for keyframe tasks.
- Which video is before-transition and which is after, for a transition task.
- The primary action or event, if no action is stated at all.

**Non-blocking — choose a sensible default, label it, and move on. Do not ask.**

- Visual style, lighting, colour, mood.
- Shot sizes and camera movement.
- Ambience, sound effects, music.
- Stage count and pacing for a long video.

Ask at most one round of questions, batched. Then draft. Every default you chose appears in an
`Assumptions` list under the prompt so the user can overturn it in one line. A prompt with
labelled assumptions is more useful than a question.

### A3. Draft

Follow the template for the task type. Universal rules:

- Name and bind every distinct character, product, and prop to its reference material
  individually. Never write "@Images 1 through 4 define four characters respectively" — that
  states no mapping.
- State what each reference provides and what to exclude ("Do not use the image background",
  "Do not use the person's identity, clothing, or scene from the video").
- When a reference video already defines motion, camera, or sequence, state only which
  attributes to inherit; do not restate the full action.
- Put non-Chinese dialogue in `{}` and state the language (plus accent and delivery) before
  the line.
- Pair abstract emotions and uncommon camera terms with directly visible or audible results.
- Use stages with end states for multi-event videos; treat timestamps as time budgets, not
  frame-accurate edit points.
- Keep subject count, clothing, prop ownership, spatial relationships, and audio relationships
  consistent across stages and scenes.
- Leave no `<angle-bracket placeholder>` unfilled in the delivered prompt.

### A4. Check

Where code execution is available, run the linter for the mechanical checks:

```bash
python3 scripts/lint_prompt.py draft.txt --task edit
```

Where it is not, work the nine manual checks above instead.

Then run the judgement checks in `references/checklist.md`, applying only the blocks that
match the task type. Fix what the linter flags before delivering; if a flag is a false
positive, say why in one line rather than silently ignoring it.

### A5. Deliver

Return the copy-ready prompt in a single code block, then:

- **Parameters to set yourself:** duration, ratio, resolution, audio toggle — and which of
  them are locked by this task type and cannot be set.
- **Material order:** list the intended order of materials so `@Image 1` resolves to the
  material the prompt calls `@Image 1`. Present this as the order to supply them in, not as a
  documented platform rule — the source guide does not specify how numbering is assigned.
- **Assumptions:** every non-blocking default you chose, one line each.

Do not add unrequested variants. When iterating, change one major variable at a time and keep
unrelated confirmed requirements intact.

## Route B — Diagnose a failed generation

Ask for the prompt if it was not supplied, and for what the output did wrong in observable
terms ("two lamps appeared", not "it looked off"). Map the symptom to the smallest prompt
change, apply that one change, and return the revised prompt with the change marked. Changing
several things at once destroys the signal about which fix worked.

| Symptom | Likely cause | Smallest fix |
|---|---|---|
| Wrong or swapped subjects; identity drift | References not bound individually | Bind each character/prop to its `@Image`/`@Video`; add subject profiles |
| Backgrounds or people leak from reference images | Missing exclusions | Add "Do not use the image background/people/composition" |
| All references appear at once | Prompt asks for every material in every scene | Select references by scene; keep only scene-relevant materials in each scene |
| Events skipped, rushed, or extra cuts appear | Too many beats per stage; timestamps too dense | One primary change per stage plus an end state; widen time ranges |
| Motion wrong despite a motion reference | Restating motion conflicts with the video | State only which attributes to inherit from `@Video` |
| Clothing, props, or count change across scenes | No consistency lock | Restate identity, clothing, prop ownership, and spatial direction per stage/scene |
| Duplicate or split subject appears mid-shot | No continuous-instance lock | Add "keep each subject as the same continuous instance; do not duplicate or split it" |
| Dialogue in wrong language or voice | No language marker or speaker binding | "Dialogue language: <language>. The <speaker> says <delivery>: {line}"; bind `@Audio` to the speaker |
| Last frame stretched | First/last image ratios differ | Use matching aspect ratios for first and last frames |
| Camera term ignored | Term vague or uncommon | Keep the term, then state target subject + visible change + direction |
| Wrong or missing on-screen text | No subtitle marker or exact-text reference | Use `【】` for subtitles; for exact signs, formulas, or specs, combine prepared references with post-production |
| Extension introduces later characters too early | Backward extension ends only with "then connect to the source" | State the source's first frame as the explicit end state; name materials that must not appear early |
| Edited video drifts outside the intended region | No timeline inheritance clause | Add `[Timeline Inheritance]`: target inherits the original's appearances, motion, occlusion, exits, and timing |

Some failures are not prompt failures. If the request needs exact subtitle text, legible
formulas, product specifications, or frame-accurate timing, say so and point to prepared
references plus post-production rather than iterating the prompt further.

## Route C — Audit an existing prompt

Run `scripts/lint_prompt.py`, then the applicable `references/checklist.md` blocks. Report
findings as a short list ordered by severity, each with the specific rewrite. Do not rewrite
the whole prompt unless asked — the user may have deliberate choices you would erase.
