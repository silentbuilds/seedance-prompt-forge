# Checklist and Limitations

Apply the **Core** block always. Apply a task block only when that task type is in play. Running
all blocks on every prompt trains rubber-stamping; skipped blocks should be skipped visibly.

Items marked ⚙ are checked mechanically by `scripts/lint_prompt.py` — run it first, then spend
judgement on the rest.

## Core — every prompt

- [ ] Subject and primary action or event clearly stated, and stated first.
- [ ] ⚙ No unfilled `<angle-bracket placeholders>` remain.
- [ ] ⚙ Generation parameters (duration, ratio, resolution) are not written into the prompt.
- [ ] Abstract emotions and cinematography terms are paired with visible or audible cues.
- [ ] Every non-blocking default is listed as an assumption under the prompt.

## When reference materials are used

- [ ] ⚙ Every `@Image`/`@Video`/`@Audio` cited in the body has a role-defining line.
- [ ] ⚙ Reference numbering is contiguous from 1 with no gaps.
- [ ] ⚙ No collective binding ("@Images 1 through 4 define four characters respectively").
- [ ] Every role line states what to use and what not to use.
- [ ] Every distinct character, product, and prop is named and bound individually.
- [ ] The intended material order is stated to the user alongside the prompt.
- [ ] References are selected per scene rather than required to appear all at once.
- [ ] Where a reference video defines motion, the prompt inherits attributes instead of restating the action.

## When the video has multiple events or stages

- [ ] Each stage has one primary change and an explicit end state.
- [ ] ⚙ Time ranges are consecutive and non-overlapping.
- [ ] No frequency demands ("three actions in one second").
- [ ] Character count, clothing, prop ownership, and spatial relationships stay consistent across stages.

## When editing an existing video

- [ ] Source video declared the sole editing master.
- [ ] Edit scope names the object, region, time range, or audio category — and nothing wider.
- [ ] Target quantity stated explicitly ("exactly one ...").
- [ ] `[Timeline Inheritance]` present for subject or background replacement.
- [ ] Content to preserve listed.
- [ ] ⚙ No aspect-ratio or duration request (both locked on this task type).

## When extending a video

- [ ] Extension direction stated.
- [ ] Boundary frame described before the new content (forward) or as the explicit end state (backward).
- [ ] Continuous-instance lock present ("do not duplicate or split").
- [ ] For backward extension, materials that must not appear early are named.
- [ ] ⚙ No aspect-ratio request (locked).

## When using first/last frames or keyframes

- [ ] Each anchor image described separately, never combined into one sentence.
- [ ] First and last images use the same aspect ratio.
- [ ] Supplementary references told not to override the anchor compositions.
- [ ] ⚙ No aspect-ratio request (locked to the first image).

## When using storyboards or blockouts

- [ ] Storyboard states the reading order and which structure to inherit.
- [ ] Blockout identified as coarse or fine before drafting.
- [ ] Coarse: every blockout object mapped to its final subject or prop.
- [ ] Fine: attributes to re-render defined, and what to preserve from the blockout stated.

## When using one-click video or seamless transitions

- [ ] One-click: material roles, image order, motion amount, editing style, and audio all defined.
- [ ] Transitions: both videos' roles, trigger action, transition process, and arrival state defined.

## Limitations — say these out loud when they apply

- Timestamps allocate time to events; they are not frame-accurate edit points.
- Editing prompts improve alignment probability but cannot guarantee frame-by-frame overlap.
- Multi-reference creation selects the right materials per scene; it does not put every material on screen.
- For subtitles, formulas, signs, product specifications, or frame-level timing that must be exact, combine prepared references, generation, and post-production.
- Video editing locks the input aspect ratio and approximate duration; output may differ from input by ~0.3 seconds.
- First/last-frame generation locks the ratio to the first image; mismatched ratios may stretch the last frame.
- Video extension locks the input ratio; the extended segment's volume may differ slightly from the source.
- One-click video: state image order or character mapping explicitly when it matters.
- Seamless transitions aim for visual and audio continuity, not pixel-identical preservation.
- Storyboard grids convey order and approximate composition, not panel-exact reproduction.
