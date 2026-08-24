# Fix identity drift, duplication, or splitting in a Seedance prompt

This diagnosis uses an original failure report. It is repository-authored troubleshooting, not an official-guide example or a guarantee about why a specific generation failed.

## Observable problem

The original output begins with one courier in a red coat, then shows a second similar courier after a doorway cut; the first courier's coat also becomes blue. The existing prompt already has the desired action, setting, and camera move, so replacing every creative choice would hide the signal of the repair.

## Illustrative weak prompt

```text
@Image 1 defines the courier.

A courier in a red coat crosses a rainy alley, opens a blue doorway, and carries a parcel inside. Use a slow push in as the doorway opens.
```

## Smallest copy-ready repair

```text
@Image 1 defines the courier's face, short curly hair, red coat, black trousers, and parcel. Do not use the image background, other people, or composition.

Exactly one courier in the red coat crosses the rainy alley, opens the blue doorway, and carries the parcel inside. Keep the subject as the same continuous instance; do not duplicate or split it. Preserve the face, short curly hair, red coat, black trousers, parcel ownership, and travel direction before and after the doorway cut. Use a slow push in as the doorway opens. No subtitles or on-screen text.
```

## Diagnosis and material change

The documented portion is that consistent reference mappings, subject count, clothing, and continuity should be stated. Mapping identity drift or duplication to a missing continuity lock is a **diagnostic heuristic**, not an official model guarantee. The repair wording—“keep the subject as the same continuous instance; do not duplicate or split it”—is **skill-derived repair guidance**. It reduces ambiguity but does not guarantee that duplication or identity drift will never occur.

The smallest relevant change is to make the existing identity binding specific, lock the count, and add continuity across the doorway cut. The location, action sequence, rain, doorway color, and slow push-in remain intact.

## Parameters and intended materials

Set duration, aspect ratio, resolution, and audio controls outside the prompt on the generation surface or API. Intended order to supply or verify: **Image 1** courier reference. This ordering is a working inference for reference numbering, not documented platform behavior; confirm the mapping in the interface.

## Evidence basis

| Recommendation | Evidence classification | Source |
|---|---|---|
| Bind the reference individually, state the subject count and clothing, and maintain continuity. | Documented guidance | [SOURCES.md](../../SOURCES.md), [checklist](../../skills/seedance-prompt-forge/references/checklist.md), [long-video guidance](../../skills/seedance-prompt-forge/references/long-videos.md), [official guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| Missing continuity lock as a likely explanation for drift, duplication, or splitting. | Diagnostic heuristic | [diagnostic table in SKILL.md](../../skills/seedance-prompt-forge/SKILL.md) |
| “Same continuous instance; do not duplicate or split it” as the smallest repair. | Skill-derived application | [diagnostic table in SKILL.md](../../skills/seedance-prompt-forge/SKILL.md) |
| Intended material order supports the prompt mapping but is not guaranteed numbering behavior. | Working inference | [SOURCES.md](../../SOURCES.md), [reference materials](../../skills/seedance-prompt-forge/references/reference-materials.md) |

## Validation

The repaired prompt was checked with `--task generic`: **0 errors, 0 warnings**. The linter checks mechanically checkable prompt structure only; it does not verify generation quality or guarantee model behavior.

Results vary with inputs, settings, product surface, and randomness. Install the skill with [`npx skills add silentbuilds/seedance-prompt-forge`](../../README.md#install).
