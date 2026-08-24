# Keyframes, Storyboards, Blockouts, One-Click Video, Transitions

## Contents

- [First and last frames](#first-and-last-frames)
- [Multi-keyframe sequences](#multi-keyframe-sequences)
- [Storyboard grids](#storyboard-grids)
- [Blockouts](#blockouts)
- [One-click video](#one-click-video)
- [Seamless transitions](#seamless-transitions)

## First and last frames

In multimodal reference mode, state in the first line that @Image 1 is the first frame and @Image 2 is the last frame; no separate mode switch is needed. The output ratio locks to the first image, and duration is set on the page or API. First and last images should use the same aspect ratio.

```text
@Image 1 is the first frame. It defines the opening composition, subject position, pose, prop state, scene, and camera direction.
@Image 2 is the last frame. It defines the ending composition, subject position, pose, prop state, scene, and camera direction.
@Image 3 defines <Subject A>'s <appearance, clothing, structure, or material>. Do not change the first-frame composition defined by @Image 1 or the last-frame composition defined by @Image 2.

<Describe one continuous action or event>.
The video begins naturally from the first frame defined by @Image 1 and reaches the last frame defined by @Image 2 after the continuous action.
Between the first and last frames, maintain continuity in <character identity, prop structure and ownership, scene layout, and camera direction>.
```

Describe each anchor image separately; never combine them into "@Images 1 and 2 are the first and last frames".

## Multi-keyframe sequences

```text
Use @Image 1 through @Image N as keyframes in this order.

@Image 1 is the first frame. It defines <opening composition, subject position, pose, prop state, and camera direction>.
@Image 2 defines the second keyframe: <visible end state of Stage 1>.
@Image 3 defines the third keyframe: <visible end state of Stage 2>.
@Image N is the last frame. It defines <ending composition, subject position, pose, prop state, and camera direction>.

The video passes through the states defined by @Image 1, @Image 2, @Image 3, and @Image N in order, using continuous action to transition naturally between stages.
Maintain continuity in <subject identity, prop structure and ownership, scene layout, lighting, and axis of action> throughout.
```

Independent keyframe images align more easily than frames combined into a grid. Keyframes control stage order and key states; they do not reproduce every frame exactly.

## Storyboard grids

- A grid communicates story, shot order, and approximate composition. It is not for strict reproduction of every panel detail.
- Use at most 15 panels; prefer clean line art or simple diagrams with minimal text labels.
- State the reading order, then describe each panel's subject action, shot size or camera movement, final visual style, and audio.

```text
@Image 1 provides an <N-panel storyboard grid> for shot order and approximate composition. Read it <left to right, top to bottom>. Do not use the grid's <line-art style, text labels, or placeholder characters>.
@Image 2 defines <Subject A>'s <appearance and clothing>.
@Image 3 defines <key prop or scene>'s <structure, material, or lighting>.

Shot 1: <shot size, subject action, and scene state>.
Shot 2: <shot size, subject action, camera movement, or transition>.
...
Shot N: <closing action and final visible state>.

The final video uses <visual style>. Audio includes <dialogue, ambience, action sound effects, or music>.
```

## Blockouts

Decide first whether the blockout is coarse or fine.

| Type | Best for | Material requirements | Prompt focus |
|---|---|---|---|
| Coarse | Simple geometry previewing action, paths, blocking, camera, cuts | Clear shape relationships and a complete action sequence; character/prop/scene images may be added | Map every blockout subject to its final subject or prop; state which temporal and spatial information to inherit |
| Fine | Complete modeling needing new materials, colors, characters, scenes, or style | Complete, clean model — remove path lines, coordinate axes, controllers, and camera frustums before uploading | Preserve structure, action, and camera; define the attributes to re-render |

For a coarse blockout, state each kind of information the blockout carries:

| Blockout information | What to state in the prompt |
|---|---|
| Path | Action trajectory, motion direction, subject blocking, entrance/exit order |
| Camera movement | Camera position, path, direction, speed changes |
| Lighting | Light direction, brightness changes, and when those changes occur |
| Cuts | Cut positions and the subject/composition before and after each cut |
| Audio | Whether to inherit dialogue, music, ambience, or action sound effects |

Coarse template:

```text
@Video 1 is a coarse blockout reference. It provides only <motion paths, subject blocking, camera position, camera movement, cuts, lighting changes, sound rhythm, or spatial relationships>. Do not use its blockout appearance, materials, or scene.
<Blockout Subject A> in @Video 1 corresponds to <Subject A>.
@Image 1 defines <Subject A>'s <appearance, clothing, or structure>.
@Image 2 defines <specified attributes> of <Subject B, key prop, or scene>.

<Subject> completes <primary action or event> in <scene>.
Keep <motion path, blocking, camera movement, cuts, lighting, or sound rhythm> from @Video 1.
The final video uses <characters, scene, materials, and visual style>. Audio includes <dialogue, ambience, or action sound effects>.
```

Fine template:

```text
@Video 1 is a fine blockout reference. Preserve <subject structure, action, spatial layout, camera position, camera movement, and cuts>. Do not use its original gray materials or empty background.
@Image 1 defines <subject>'s <character appearance, material, color, or surface details>.
@Image 2 defines <scene>'s <space, materials, lighting, or visual style>.

Re-render <subject> from @Video 1 as <final subject>, and re-render the scene as <final scene>.
Keep <structure, action, camera treatment, and spatial relationships> from @Video 1. Use <materials, colors, and style>. Audio includes <ambience, sound effects, or music>.
```

For coarse blockouts, prefer simple geometry; arms, wings, and other appendages only when the action sequence is complete (otherwise stiff motion or structural misinterpretation).

## One-click video

Organize multiple images (or images plus a style-reference video) into a complete video. State, in order: **material roles → image order → motion amount → editing style → visual treatment → audio**. Never write only "turn these materials into a video".

```text
[Material Roles]
@Image 1 is used for <character, product, scene, or opening image>.
@Image 2 is used for <character, product, scene, or process image>.
@Image 3 is used for <character, product, scene, or ending image>.
@Video 1 is used only for <editing rhythm, transitions, subtitle treatment, or music style>. Do not use its character identities or scene (optional).

[Arrangement]
Show the images in <upload order, a specified order, or a model-selected thematic order>.
<State the character, product, location, and event relationships that must remain consistent>.

[Image Motion]
Apply <subtle live motion, parallax, push-in/pull-out, lateral movement, or local action> to each image.
Keep <subject appearance, product structure, text, or background relationships> stable.

[Final Style]
Use <editing rhythm, transition style, subtitle or graphic treatment, and color style>.

[Audio]
Include <dialogue, ambience, sound effects, or music>.
```

If image order matters, state the exact sequence; otherwise say the model may organize them by theme.

## Seamless transitions

Generate a continuous bridge between two videos. Order: **before video → after video → trigger action → camera movement → visual transformation → arrival state → audio**.

Each transition method needs a different detail specified:

| Transition method | What to specify |
|---|---|
| Dive or reverse movement | Camera direction, speed change, and when the next scene begins |
| Character rotation | Pose, rotation direction, and how clothing or background changes continuously |
| Foreground occlusion | When the foreground object fills the frame, and the composition that follows |
| Object morph | Corresponding shapes, materials, and the transformation process |
| Push/pull or focus change | Camera movement, focus target, and continuous spatial relationship |

```text
@Video 1 is the before-transition clip. Use its <ending subject, action, composition, camera direction, and audio>.
@Video 2 is the after-transition clip. Use its <opening subject, composition, camera direction, and audio>.
Keep <character identity, product structure, scene, and primary action> stable in the original portions of @Video 1 and @Video 2.

At the end of @Video 1, <subject or foreground object> triggers the transition through <action>.
The camera <movement direction and speed change>, while <shape, material, light, or space> gradually transforms into <corresponding element> at the start of @Video 2.
The transition ends naturally at @Video 2's opening composition, preserving continuity in <subject position, camera direction, and motion trend>.
Audio transitions smoothly from <before audio> to <after audio>.
```

The generated bridge is not a pixel-identical edit splice; the goal is visual and audio continuity.
