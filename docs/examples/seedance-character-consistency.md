# Keep a character consistent across a multi-stage Seedance video

This original, skill-derived scenario follows one museum conservator through a three-stage inspection. It is not an example from the official guide and is not evidence of a generated result.

## Observable problem

A prompt asks for one character across several events, but the character's jacket changes, the case changes hands, and the person reverses direction after a cut. The brief needs an explicit continuity plan, not more decorative style language.

## Illustrative weak prompt

```text
Make a cinematic video of a conservator inspecting an artifact, carrying it through a gallery, and placing it in a case. Keep the person consistent and make the performance tense but hopeful.
```

## Copy-ready corrected prompt

```text
[Generation Goal]
Generate a cinematic museum-inspection story in which exactly one conservator safely moves a sealed sample case from a conservation bench to a gallery display case.

[References]
@Image 1 defines the conservator's face, short black hair, charcoal field jacket, tan gloves, and appearance. Do not use the image background, other people, or composition.
@Image 2 defines the sealed brass sample case and its dark leather handle. Do not use the image background or any people.

[Stage 1 — 0-10 seconds]
Initial state: exactly one conservator in the charcoal field jacket stands on the left side of a conservation bench, facing right. The sealed brass sample case rests by the conservator's right hand.
Primary event: the conservator checks the seal, then closes the right hand around the leather handle. Their brows draw together, their gaze follows the seal, and they take one controlled breath.
End state: the same conservator holds the sealed sample case in the right hand, remains on the left side of the bench, and faces right.

[Stage 2 — 10-20 seconds]
Continue from the previous stage: keep the same continuous conservator, face, hair, charcoal field jacket, tan gloves, right-hand case ownership, and left-to-right travel direction.
Primary event: a medium follow shot moves beside the conservator as they carry the case through a quiet gallery corridor; the left hand steadies the case without taking ownership of it.
End state: the conservator reaches the display case at the right side of the gallery while still holding the sample case in the right hand.

[Stage 3 — 20-30 seconds]
Continue from the previous stage: the same conservator and clothing remain unchanged, with the gallery display case on the right side of the frame.
Primary event: the conservator places the sample case inside the display case, then releases the handle and watches the latch close; their shoulders relax slightly and their eyes remain on the case.
End state: the sample case is centered inside the closed display case, and the conservator stands to its left with both hands visible and empty.

[Maintain Consistency]
Keep exactly one continuous conservator throughout. Preserve the face, short black hair, charcoal field jacket, tan gloves, case ownership, left-to-right direction, and gallery orientation. Do not duplicate, split, replace, or distort the conservator. No subtitles or on-screen text.
```

## Why the correction is material

- Individual reference roles and exclusions make the identity and prop scope explicit.
- Each stage has one primary change and an observable end state, so the next stage inherits a visible starting condition.
- The continuity lines repeat identity, clothing, prop ownership, and spatial direction.
- Tense and hopeful are expressed through brows, gaze, breathing, shoulders, and release of the handle rather than abstract emotion labels alone.

## Parameters and intended materials

Set duration, aspect ratio, resolution, and audio controls outside the prompt on the generation surface or API. Supply or verify the materials in this intended order: **Image 1** conservator; **Image 2** sample case. Treating the numbers as upload order is a working inference, not a documented platform rule; verify the mapping shown in your interface.

## Evidence basis

| Recommendation | Evidence classification | Source |
|---|---|---|
| Give each reference an explicit role and exclusion. | Documented guidance | [SOURCES.md](../../SOURCES.md), [reference materials](../../skills/seedance-prompt-forge/references/reference-materials.md), [official guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| Use one primary event and a visible end state for each long-video stage. | Documented guidance | [SOURCES.md](../../SOURCES.md), [long-video guidance](../../skills/seedance-prompt-forge/references/long-videos.md), [official guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| Keep identity, clothing, prop ownership, and spatial direction continuous. | Documented guidance | [SOURCES.md](../../SOURCES.md), [checklist](../../skills/seedance-prompt-forge/references/checklist.md), [official guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| The conservator, setting, and prompt are a worked application of those rules. | Skill-derived application | [long-video guidance](../../skills/seedance-prompt-forge/references/long-videos.md) |
| Treat supplied-material order as a number-mapping aid rather than a platform guarantee. | Working inference | [SOURCES.md](../../SOURCES.md), [reference materials](../../skills/seedance-prompt-forge/references/reference-materials.md) |

## Validation

The corrected prompt was checked with `--task longvideo`: **0 errors, 0 warnings**. The linter checks mechanically detectable prompt structure only; it does not assess generation quality or guarantee model behavior.

Results vary with inputs, settings, product surface, and randomness. Install the skill with [`npx skills add silentbuilds/seedance-prompt-forge`](../../README.md#install).
