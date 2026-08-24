# Bind image, video, and audio references in a Seedance prompt

This is an original skill-derived application, not an official-guide example and not evidence of a generated result.

## Observable problem

A creator uploads portrait, motion, and sound references but asks for “use all references.” The result can leave identity, motion, voice, ambience, music, and sound effects ambiguous; image background or video performers may also leak into the scene.

## Illustrative weak prompt

```text
Use my image, dance clip, and audio to make a stylish video of a singer entering a rooftop venue. Use all references and make it emotional.
```

## Copy-ready corrected prompt

```text
[References]
@Image 1 defines the singer's face, braided hair, cobalt jacket, and silver earrings. Do not use the image background, other people, or composition.
@Video 1 defines only the singer's measured entrance pace and the lateral camera move. Do not use the video's performer identity, clothing, venue, or lighting.
@Audio 1 defines the singer's speaking voice for the line below. Do not use it as music, crowd ambience, or sound effects.

[Scene]
Exactly one singer in the cobalt jacket enters a rooftop venue at dusk and walks toward a microphone stand. Use the entrance pace and lateral camera movement from @Video 1 while preserving the singer identity from @Image 1. The camera begins beside the singer and tracks laterally toward the microphone stand.

[Performance]
The singer glances at the empty skyline, exhales, then turns toward the microphone with a small, steady smile. Dialogue language: English. In a quiet, grounded delivery using @Audio 1, the singer says: {I am ready to begin.}

[Audio]
Voice: use @Audio 1 only for the singer's spoken line.
Ambience: low rooftop wind and distant city traffic.
Music: none.
Sound effects: soft footsteps on concrete and one light microphone-stand adjustment.

[Maintain Consistency]
Keep exactly one singer with the face, braided hair, cobalt jacket, and silver earrings from @Image 1. Do not duplicate, replace, or distort the singer. Do not introduce people, clothing, or a setting from @Video 1. No subtitles or on-screen text.
```

## Why the correction is material

- Each modality has one stated job: the image controls appearance, the video supplies only pace and camera movement, and the audio supplies only the speaking voice.
- Exclusions prevent unrelated background, performer, clothing, venue, and audio categories from being requested from the references.
- Voice, ambience, music, and sound effects are separated so the spoken reference is not also treated as a music or environment source.
- The prompt names which reference controls each relevant attribute instead of asking for every uploaded material to appear.

## Parameters and intended materials

Set duration, aspect ratio, resolution, and audio controls outside the prompt on the generation surface or API. Intended order to supply or verify in the interface: **Image 1** singer portrait; **Video 1** entrance-motion clip; **Audio 1** speaking-voice clip. The guide does not document how reference numbers are assigned, so this order is a working inference rather than a guarantee.

## Evidence basis

| Recommendation | Evidence classification | Source |
|---|---|---|
| Name each material's role, select relevant attributes, and state exclusions. | Documented guidance | [SOURCES.md](../../SOURCES.md), [reference materials](../../skills/seedance-prompt-forge/references/reference-materials.md), [official guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| Inherit stated motion or camera attributes from a motion reference rather than restating its action. | Documented guidance | [SOURCES.md](../../SOURCES.md), [reference materials](../../skills/seedance-prompt-forge/references/reference-materials.md), [official guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| State dialogue language and distinguish voice, ambience, music, and sound effects. | Documented guidance | [SOURCES.md](../../SOURCES.md), [audio and performance](../../skills/seedance-prompt-forge/references/audio-and-performance.md), [checklist](../../skills/seedance-prompt-forge/references/checklist.md), [official guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh) |
| The rooftop scenario and precise bindings are a worked application. | Skill-derived application | [reference materials](../../skills/seedance-prompt-forge/references/reference-materials.md) |
| The intended material order is a mapping aid, not documented numbering behavior. | Working inference | [SOURCES.md](../../SOURCES.md), [reference materials](../../skills/seedance-prompt-forge/references/reference-materials.md) |

## Validation

The corrected prompt was checked with `--task generic`: **0 errors, 0 warnings**. The linter validates mechanically checkable prompt structure only; it does not verify generation quality or guarantee model behavior.

Results vary with inputs, settings, product surface, and randomness. Install the skill with [`npx skills add silentbuilds/seedance-prompt-forge`](../../README.md#install).
