# Video Editing and Extension

## Locked parameters

| Task | Aspect ratio | Duration |
|---|---|---|
| Video editing | Preserved from input; cannot be set separately | Approximately preserved; cannot be set separately (± ~0.3 s from input-frame processing) |
| First/last-frame generation | First image's ratio; first and last images should match to avoid stretching the last frame | Can be set |
| Video extension | Preserved from input; cannot be set separately | Can be set |

Locked parameters cannot be specified on the generation page or via the API, so do not ask for them in the prompt either.

## Editing: general pattern

Define the source video as the sole editing master, then state the edit target, edit scope, target material, and content to preserve.

```text
[Edit Goal]
Edit @Video 1. Within <the entire video or a specific time range>, <add, remove, replace, or adjust> <visual object, region, or audio category>.

[Source Video Role]
@Video 1 is the sole editing master. It defines <characters, scene, actions, composition, camera movement, occlusion relationships, audio, and event order>.

[Target Material Role]
@Image 1 or @Audio 1 defines <specified attributes of the target object or sound>.

[Edit Scope]
Modify only <object, region, time range, or audio category>.

[Content to Preserve]
Keep <visual content, motion, audio, and timing relationships that must not change> from @Video 1.
```

Example:

```text
[Edit Goal]
Edit @Video 1. Only from 4-7 seconds, change the cool blue light on the right wall to warm orange light.

[Source Video Role]
@Video 1 is the sole editing master. It defines the character, room layout, actions, composition, camera movement, audio, and event order.

[Edit Scope]
Change only the light color on the right wall and the area it illuminates. Allow the character's skin tone to respond naturally to the environmental light.

[Content to Preserve]
Keep the character's identity, clothing, expression, position, motion, room structure, camera movement, dialogue, and ambience from @Video 1.
```

## Subject replacement

Use the full block structure. `[Timeline Inheritance]` is what makes the target object follow the original's whole behavior instead of only its appearance; without it the replacement drifts.

```text
[Edit Goal]
Edit @Video 1. Change only <original object> to <target object>.

[Source Video Role]
@Video 1 is the sole editing master. It defines the original scene, camera position, camera movement, motion path, occlusion relationships, and event order.

[Target Reference Role]
@Image 1 defines <target object>'s <appearance, structure, or material>. Do not use <irrelevant background, people, or composition>.

[Edit Scope]
Modify only <specific object and area>. The entire video contains <number> target object(s). Do not modify <content to preserve>.

[Timeline Inheritance]
<Target object> inherits every appearance, motion, occlusion, and exit of <original object>, including timing, duration, path, and speed changes.
Except for the object or area explicitly modified above, keep all other people, props, scene content, camera movements, cuts, and event order from @Video 1 unchanged.
```

Stating the target count explicitly ("the entire video contains exactly one white desk lamp") is the single most reliable guard against a duplicated subject.

## Background replacement

```text
[Edit Goal]
Edit @Video 1. Replace only <original background area> with <target environment> from @Image 1.

[Source Video Role]
@Video 1 is the sole editing master. It defines the people, foreground objects, actions, composition, camera movement, and event order.

[Target Reference Role]
@Image 1 defines only <target environment>'s spatial layout, materials, depth of field, ambient color, and lighting direction. Do not use the people or foreground objects in the image.

[Edit Scope]
Modify only <background outside the subject's silhouette>. Do not modify <subject identity, facial features, hairstyle, clothing, expression, position, size, or motion>.

[Timeline Inheritance]
Keep the character actions and occlusion relationships from @Video 1. Except for the area explicitly modified above, keep all other people, props, scene content, camera movements, cuts, and event order from @Video 1 unchanged.
```

## Audio editing

State the speaker or sound category, the intended change, and which other sounds must remain unchanged:

```text
Edit @Video 1. Remove only the original background music. Keep the character dialogue, lip sync, ambience, and action sound effects; preserve the visuals, camera treatment, and editing rhythm from @Video 1.

Edit @Video 1. Change <Presenter>'s spoken language to natural American English while preserving the dialogue content and speaking times. Keep all other character voices, background music, ambience, and visuals from @Video 1.
```

## Forward extension

The extension's first frame continues from the source's last frame. Describe the continuous state of the last frame first, then what happens afterward.

```text
@Video 1 is the source video to extend forward.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the last frame of @Video 1. Maintain continuity in <subject pose and orientation>, <prop position>, <background and spatial relationships>, <camera position and composition>, <lighting>, and <motion direction>.

Then, <describe the new action, event, camera treatment, or audio to add>.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>, <background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout: do not duplicate or split it, and keep the person's appearance or the object's number of parts stable.
```

With additional references: define their roles first, then state that the source video controls the extension boundary. New materials may supplement characters, props, or audio but must not override the source's last-frame control of the extension's opening image.

## Backward extension

Describe what happens before the source video begins, then define the source's first frame as the explicit end state of the extension. Writing only "then connect to the source video" can introduce later characters or effects too early.

```text
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source video begins, <describe the preceding action, event, camera treatment, or audio>.

The last frame of the extended segment naturally connects to the first frame of @Video 1: <subject pose and orientation>, <prop position>, and <background and spatial relationships>. Match the <camera position and composition>, <lighting>, and <motion direction> of @Video 1's first frame.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>, <background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout: do not duplicate or split it.
```

With additional references, also state which materials appear only after the source video begins and must not appear early in the backward extension.

## Boundary notes

Boundary frames connect naturally at a visual level, not pixel-identically. During review, inspect both sides of the boundary and the complete extended segment.
