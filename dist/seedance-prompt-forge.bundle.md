<!-- GENERATED FILE - do not edit. Run scripts/build_bundle.py. -->
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

## Seedance Prompt Forge

Turn an idea, draft prompt, reference set, or failed generation into a copy-ready Seedance 2.5
prompt. Prompts are flexible natural language built from optional components; every reference
material gets an explicit role.

Sources: the [Dreamina Seedance 2.5 Prompt Writing Guide](https://bytedance.larkoffice.com/docx/A88jd0B47oAd8zxWp5ycZFMfnxh)
and its [official BytePlus release](https://docs.byteplus.com/en/docs/ModelArk/2607689). Do not
apply these templates to other Seedance versions without checking that version's own guidance.
Platform behaviours described here are documented for Dreamina or for the surfaces the guide
explicitly names; verify the controls available on the user's product or API.

### Pick a route

| The user gives you | Route |
|---|---|
| An idea, brief, or reference set | **A — Author** |
| A generation that came out wrong (with or without the prompt) | **B — Diagnose** |
| An existing prompt, no output yet | **C — Audit** |

Routes B and C both end by re-entering Route A step 3.

### Core structure

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

### Running without code execution

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

### Route A — Author

#### A1. Identify the task type and load guidance

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

#### A2. Collect the brief — ask only about blockers

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

#### A3. Draft

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

#### A4. Check

Where code execution is available, run the linter for the mechanical checks:

```bash
python3 scripts/lint_prompt.py draft.txt --task edit
```

Where it is not, work the nine manual checks above instead.

Then run the judgement checks in `references/checklist.md`, applying only the blocks that
match the task type. Fix what the linter flags before delivering; if a flag is a false
positive, say why in one line rather than silently ignoring it.

#### A5. Deliver

Return the copy-ready prompt in a single code block, then:

- **Parameters to set yourself:** duration, ratio, resolution, audio toggle — and which of
  them are locked by this task type and cannot be set.
- **Material order:** list the intended order of materials so `@Image 1` resolves to the
  material the prompt calls `@Image 1`. Present this as the order to supply them in, not as a
  documented platform rule — the source guide does not specify how numbering is assigned.
- **Assumptions:** every non-blocking default you chose, one line each.

Do not add unrequested variants. When iterating, change one major variable at a time and keep
unrelated confirmed requirements intact.

### Route B — Diagnose a failed generation

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

### Route C — Audit an existing prompt

Run `scripts/lint_prompt.py`, then the applicable `references/checklist.md` blocks. Report
findings as a short list ordered by severity, each with the specific rewrite. Do not rewrite
the whole prompt unless asked — the user may have deliberate choices you would erase.

---

## Inlined: `references/core-and-examples.md`

### Core Formula and Worked Examples

#### Contents

- [Components](#components)
- [Rules](#rules)
- [Example 1: bare idea to text-to-video prompt](#example-1-bare-idea-to-text-to-video-prompt)
- [Example 2: loose brief with references](#example-2-loose-brief-with-references)
- [Example 3: repairing a failed generation](#example-3-repairing-a-failed-generation)

#### Components

- **Subject + Action or Event** — who or what is doing what. The foundation of the video; state it first.
- **Scene and Environment** — location, time, weather, spatial relationships, background state.
- **Visual Style** — lighting, color, materials, image texture, or overall mood.
- **Camera Movement/Cut** — shot size, camera angle, camera movement, the focus subject, shot transitions.
- **Audio** — dialogue, voice characteristics, ambience, sound effects, music.

#### Rules

- Omit any component you do not need.
- Do not include generation parameters in the prompt; set them on the generation page or through the API.
- State the subject and primary action or event first.

#### Example 1: bare idea to text-to-video prompt

**Brief:** "a potter finishing a cup, kind of peaceful"

Blocking gaps: none. Subject and action are present. Everything else is a non-blocking default.

**Output:**

```text
A ceramic artist finishes a pale blue cup in a studio at dawn, lifts it from the wheel, and places it in the center of a wooden shelf.
Soft morning light enters through the window. The wet clay has a delicate sheen, and the workbench remains tidy.
Begin with a medium shot of the wheel-throwing process, slowly push in toward the cup's surface texture, then cut to a frontal view of the shelf.
Retain the low hum of the pottery wheel, the friction of clay, and subtle indoor ambience.
```

**Assumptions:** dawn studio interior; pale blue glaze; documentary realism; medium shot into a push-in, one cut; diegetic ambience only, no music.

#### Example 2: loose brief with references

**Brief:** "I've got a photo of my presenter, a photo of the lab, and a clip of someone opening a case. Make a 15-second thing where she inspects a sample."

Blocking gap: which image is which. Ask once, batched:

> Confirm the mapping — is Image 1 the presenter, Image 2 the lab, Video 1 the case-opening motion? And should the presenter's own face and clothing come from Image 1, or only her face?

**Output after the answer:**

```text
@Image 1 defines <Conservator>'s facial features, hairstyle, and navy work shirt. Do not use the image background.
@Image 2 defines the <Conservation Lab>'s spatial layout, workbench position, and overhead lighting. Do not use the people in the image.
@Video 1 defines the pacing and hand path of opening a hinged case with both hands. Do not use the person's identity, clothing, or scene from the video.

<Conservator> opens a hinged sample case at the workbench in the <Conservation Lab>, lifts the sample with tweezers, and holds it up to the light to inspect it.
The visuals are clean and clinical, with cool overhead light and shallow depth of field.
Begin with a medium shot of the workbench, push in slowly toward the conservator's hands, then cut to a close-up of the sample.
Retain quiet room tone, the case latch, and soft handling sounds.

Keep <Conservator> as the same continuous instance throughout: one person, one case, unchanged clothing and workbench orientation.
```

**Upload order:** Image 1 presenter, Image 2 lab, Video 1 case-opening clip.
**Assumptions:** clinical cool-light style; three-beat shot progression; no dialogue or music.

#### Example 3: repairing a failed generation

**Report:** "It made two lamps and the desk turned into a different desk."

Two symptoms, two smallest fixes. Change one variable at a time; deliver the count lock first
because a duplicated subject usually also destabilises everything around it.

**Original edit scope line:**

```text
Replace the yellow desk lamp with the white one from @Image 1.
```

**Revised, change marked:**

```text
[Edit Scope]
Keep exactly one white folding desk lamp throughout the video. Replace only the original yellow folding desk lamp. Do not modify the desk, books, hands, or background.   <-- changed

[Timeline Inheritance]
The white folding desk lamp inherits every appearance, lamp-arm rotation, hand occlusion, and exit of the original yellow folding desk lamp, including timing, path, and speed changes.   <-- added
Except for the object explicitly modified above, keep all other people, props, scene content, camera movements, cuts, and event order from @Video 1 unchanged.   <-- added
```

The desk drift was not a separate bug — it was the missing "do not modify" list. Re-run before
changing anything else.

---

## Inlined: `references/reference-materials.md`

### Reference Materials

#### Contents

- [Limits and recommended ranges](#limits-and-recommended-ranges)
- [Define each material's role](#define-each-materials-role)
- [Multiple views of the same subject](#multiple-views-of-the-same-subject)
- [Motion references](#motion-references)
- [Multi-reference creation](#multi-reference-creation)

#### Limits and recommended ranges

Seedance 2.5 combines up to 50 reference materials total. Recommended ranges improve stability; they are not hard capability limits.

| Type | Limit | Recommended |
|---|---|---|
| Images | Up to 30, each no larger than 4K | 1–8 distinct subjects across subject-reference images |
| Videos | Up to 10, combined ≤ 30 s | 1–5 distinct subjects, 5–10 s per subject video |
| Audio | Up to 10, combined ≤ 30 s | Only dialogue, voice, ambience, or music relevant to the task |
| Video editing | Source video + reference images | Source under 20 s; 1–5 reference images |

- Above these ranges stability may drop (e.g., 9–12 subjects, 6–10 audio/video subjects, 6–8 edit references).
- If more than five subjects need multiple views, place different views in separate images; independent view images are more stable than one collage.

#### Define each material's role

- State exactly what each material contributes, and add exclusions when its background, people, or composition could leak into the output.
- Write the mappings in the prompt. Do not rely on text labels inside the images, and do not make the model infer which person, prop, or scene a material represents.
- Number references consistently (@Image 1, @Video 1, @Audio 1). The prompt's numbering must resolve to the
  same materials the user actually supplies, so always state the intended order alongside the prompt.
  (The official guide does not document how the platform assigns these numbers; treating them as upload
  order is a working assumption. Tell the user it is an assumption rather than a documented rule.)

Role template:

```text
@Image 1 defines <subject>'s <appearance, clothing, structure, or material>.
@Video 1 defines <motion, camera movement, or pacing>.
@Audio 1 defines <character or sound type>'s <voice, dialogue, ambience, or music>.

<Subject> completes <primary action or event> in <scene>.
The visuals feature <visual style>, with <camera treatment>.
```

Example:

```text
@Image 1 defines the ceramic artist's facial features, hairstyle, and dark green apron. Do not use the image background.
@Image 2 defines the wooden workbench, window placement, and morning light of the pottery studio. Do not use the people in the image.
@Video 1 defines the pacing of throwing clay with both hands, lifting the cup, and placing it down. Do not use the person's identity, clothing, or scene from the video.
```

#### Multiple views of the same subject

State each view separately and lock the count:

```text
@Image 1 defines the front view of the same folding desk lamp.
@Image 2 defines the left-side structure of the same folding desk lamp.
@Image 3 defines the right-side structure of the same folding desk lamp.
@Image 4 defines the rear structure of the same folding desk lamp.
All four images define one folding desk lamp. The output must contain only one lamp throughout.
```

#### Motion references

When a reference video already defines motion, camera movement, and sequence accurately, state only which attributes to inherit. Restating every action can conflict with the reference. A blockout video mainly provides motion and spatial structure, so the prompt must still define the intended subjects, scene, action, and visual style.

#### Multi-reference creation

Use this order when many materials are provided: **define each material's role → map subjects → group by type → create subject profiles → select references by scene**. The goal is to help the model select the correct materials for the current scene, not to make every material appear at once.

##### Step 1: Name and map each subject individually

```text
<Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Character B> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
<Prop A> corresponds to @Image 3. Use only the structure, material, and color.
<Scene A> references @Image 4. Use only the spatial layout, architecture, and lighting. Do not use the people in the image.
```

##### Step 2: Group materials by type

```text
[Characters]
<Conservator> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Registrar> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
Do not interchange the characters' appearances, clothing, actions, positions, or dialogue.

[Props]
<Sample Case> corresponds to @Image 5 and belongs only to <Conservator>.
<Record Board> corresponds to @Image 6 and belongs only to <Registrar>.

[Scenes]
<Conservation Lab> references @Image 7. Use only the space, materials, and lighting.
<Gallery> references @Image 8. Use only the space, materials, and lighting.

[Motion and Audio]
@Video 1 defines the motion of <Conservator> opening <Sample Case>. Do not use the person or scene from the video.
@Audio 1 defines <Guide>'s voice and specified dialogue.
```

##### Step 3: Create a subject profile for important characters

```text
[Subject Profile: Conservator]
Appearance and clothing: @Image 1.
Fixed prop: <Sample Case> from @Image 5.
Locations: <Conservation Lab> and <Gallery>.
Motion references: the case-opening motion from @Video 1.
Do not use: other characters' clothing. Do not give this character <Record Board> or guide equipment.
```

##### Step 4: Select references by scene

```text
Scene 1 | Inspection in the Conservation Lab
Use: <Conservator>, <Sample Case>, <Conservation Lab>, and the case-opening motion from @Video 1.
Event: <Conservator> opens <Sample Case> at the workbench and inspects the sample inside.
End state: <Conservator> remains on the inner side of the workbench. <Sample Case> stays beside the conservator's right hand, which is on the left side of the frame.

Scene 2 | Registration in the Gallery
Use: <Registrar>, <Record Board>, and <Gallery>.
Event: <Registrar> checks the number on <Record Board> beside the display case.
End state: <Registrar> still holds <Record Board> with both hands. No other character enters the display-case area.
```

---

## Inlined: `references/long-videos.md`

### Long Videos: Stages and Timing

#### Stages

For a 30-second video with several events, divide the story into consecutive stages. Give each stage only one primary state change, and state what is directly visible at its end.

```text
[Generation Goal]
Generate a <video type>. The central subject is <subject>, and the primary event is <story summary>.

[Stage 1]
Initial state: <initial state of characters, props, and scene>.
Primary event: <one primary action or event>.
End state: <character positions, prop ownership, or visible scene state>.

[Stage 2]
Continue from the previous stage: <state that must remain unchanged>.
Primary event: <one primary action or event>.
End state: <observable state>.

[Stage 3]
Primary event: <closing event>.
End state: <final visible state>.

[Maintain Consistency]
Keep <character identity, number of characters, clothing, prop ownership, spatial direction, and audio relationships> consistent.
```

Example:

```text
[Generation Goal]
Generate an instructional video showing a flower shop's order-packing process. <Florist> and <Store Assistant> arrange, wrap, and hand off a bouquet together.

[Stage 1]
Initial state: <Florist> stands behind the workbench. Loose flower stems, scissors, and wrapping paper lie on the tabletop.
Primary event: <Florist> arranges the stems and trims them to length.
End state: <Florist> holds the bouquet in the left hand, and the scissors are back on the right side of the workbench.

[Stage 2]
Continue from the previous stage: both characters retain the same identities and clothing, and <Florist> still holds the bouquet.
Primary event: <Store Assistant> unfolds the wrapping paper. <Florist> places the bouquet inside and ties it with a green ribbon.
End state: the wrapped bouquet lies flat in the center of the workbench, with the ribbon bow facing the camera.

[Stage 3]
Primary event: <Store Assistant> picks up the bouquet and places it on the pickup shelf.
End state: the bouquet is centered on the pickup shelf, and both characters stand behind the workbench inspecting the finished order.

[Maintain Consistency]
Keep <Florist> and <Store Assistant>'s identities, clothing, workbench orientation, scissors position, and bouquet ownership consistent.
```

#### Timestamps

- Use stages by default for ordinary narratives.
- Use one-second precision only for critical handoffs, entrances or exits, transitions, or explicit beats.
- Use time ranges to allocate pacing, exact time points for a single key event, and relative timing for delays between events.

```text
0-5 seconds: Show an empty wooden display table. A hand places a white ceramic plate on it. End state: the hand has left the frame, and only the white plate remains in the center of the table.
5-10 seconds: Remove the white plate, then place a clear glass on the table. End state: only the clear glass remains in the center of the table.
10-15 seconds: Remove the clear glass, then place a green ceramic vase on the table. End state: only the green vase remains in the center of the table.
```

| Pattern | Example |
|---|---|
| Time range | `0-3 seconds... 3-7 seconds... 7-12 seconds...` |
| Exact time point | `At 5 seconds, the camera whip-pans rapidly to the left and completes the transition.` |
| Relative timing | `Three seconds after the character presses the button, the room lights gradually turn off.` |

#### Timing rules

- Time ranges must be consecutive and non-overlapping.
- Ranges are an event's time budget, not a precise edit point; actions may occur slightly before or after a boundary.
- Too little content in a range gives the model freedom; too much can cause excessive cutting or omitted events.
- Do not use timestamps to demand frequencies, such as "complete three actions in one second".

---

## Inlined: `references/video-editing.md`

### Video Editing and Extension

#### Locked parameters

| Task | Aspect ratio | Duration |
|---|---|---|
| Video editing | Preserved from input; cannot be set separately | Approximately preserved; cannot be set separately (± ~0.3 s from input-frame processing) |
| First/last-frame generation | First image's ratio; first and last images should match to avoid stretching the last frame | Can be set |
| Video extension | Preserved from input; cannot be set separately | Can be set |

Locked parameters cannot be specified on the generation page or via the API, so do not ask for them in the prompt either.

#### Editing: general pattern

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

#### Subject replacement

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

#### Background replacement

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

#### Audio editing

State the speaker or sound category, the intended change, and which other sounds must remain unchanged:

```text
Edit @Video 1. Remove only the original background music. Keep the character dialogue, lip sync, ambience, and action sound effects; preserve the visuals, camera treatment, and editing rhythm from @Video 1.

Edit @Video 1. Change <Presenter>'s spoken language to natural American English while preserving the dialogue content and speaking times. Keep all other character voices, background music, ambience, and visuals from @Video 1.
```

#### Forward extension

The extension's first frame continues from the source's last frame. Describe the continuous state of the last frame first, then what happens afterward.

```text
@Video 1 is the source video to extend forward.

Extend @Video 1 forward. The first frame of the extended segment directly continues from the last frame of @Video 1. Maintain continuity in <subject pose and orientation>, <prop position>, <background and spatial relationships>, <camera position and composition>, <lighting>, and <motion direction>.

Then, <describe the new action, event, camera treatment, or audio to add>.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>, <background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout: do not duplicate or split it, and keep the person's appearance or the object's number of parts stable.
```

With additional references: define their roles first, then state that the source video controls the extension boundary. New materials may supplement characters, props, or audio but must not override the source's last-frame control of the extension's opening image.

#### Backward extension

Describe what happens before the source video begins, then define the source's first frame as the explicit end state of the extension. Writing only "then connect to the source video" can introduce later characters or effects too early.

```text
@Video 1 is the source video to extend backward.

Extend @Video 1 backward. Before the source video begins, <describe the preceding action, event, camera treatment, or audio>.

The last frame of the extended segment naturally connects to the first frame of @Video 1: <subject pose and orientation>, <prop position>, and <background and spatial relationships>. Match the <camera position and composition>, <lighting>, and <motion direction> of @Video 1's first frame.

Throughout the extension, maintain continuity in <character identity and clothing>, <key props>, <background layout>, and <axis of action>.
Keep each subject as the same continuous instance throughout: do not duplicate or split it.
```

With additional references, also state which materials appear only after the source video begins and must not appear early in the backward extension.

#### Boundary notes

Boundary frames connect naturally at a visual level, not pixel-identically. During review, inspect both sides of the boundary and the complete extended segment.

---

## Inlined: `references/advanced-modes.md`

### Keyframes, Storyboards, Blockouts, One-Click Video, Transitions

#### Contents

- [First and last frames](#first-and-last-frames)
- [Multi-keyframe sequences](#multi-keyframe-sequences)
- [Storyboard grids](#storyboard-grids)
- [Blockouts](#blockouts)
- [One-click video](#one-click-video)
- [Seamless transitions](#seamless-transitions)

#### First and last frames

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

#### Multi-keyframe sequences

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

#### Storyboard grids

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

#### Blockouts

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

#### One-click video

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

#### Seamless transitions

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

---

## Inlined: `references/audio-and-performance.md`

### Audio, Emotion, and Cinematography

#### Audio and text syntax

Prompts can be plain natural language. Use these markers only when you need to distinguish categories explicitly.

| Content | Syntax | Example |
|---|---|---|
| Music | `()` | `(Soft, rhythmic piano music plays in the background)` |
| Sound effects | `<>` | `<A bell rings in the distance>` |
| Dialogue | `{}` | `{Hello, welcome back.}` |
| Subtitles | `【】` | `【Chapter One: Departure】` |

#### Dialogue language reinforcement

- When dialogue is not in Chinese, state the language before the line. The short form is often enough: `The girl says softly in Japanese: {もう大丈夫です}`.
- If English dialogue is spoken in Chinese, or a specific regional variety matters, use the full formula: **dialogue language + regional variety or accent + delivery style + speaker + {dialogue}**.

```text
Dialogue language: American English. The girl says in natural, conversational American English: {I thought you weren't coming.}

Dialogue language: authentic Los Angeles English. The young man says in natural Los Angeles vernacular: {No way, you actually made it.}
```

#### Emotional direction and observable performance

Emotion words ("tense", "warm", "oppressive") give overall direction but leave the performance open. For stable control, add directly visible or audible cues: eye movement, brow tension, mouth movement, breathing, gaze direction, hand movement. Two to four cues are enough for a single emotional transition; use event-triggered stages when the emotion changes several times.

Single transition structure:

```text
The overall emotion shifts from <starting emotion> to <ending emotion>.
After <triggering event>, <subject> first shows <immediate observable reaction>.
Then, <eyes, brows, mouth, breathing, gaze, or hand movement> gradually <changes>.
Finally, <subject> expresses <target emotion> through <restrained or explicit outward behavior>.
```

Multi-stage structure:

```text
When <subject> hears or sees <first triggering event>, <first observable reaction>.
When <second triggering event> occurs, <change in expression, gaze, or breathing>.
After confirming <critical information>, the emotion that <subject> tries to restrain or conceal gradually becomes visible through <observable behavior>.
Finally, <subject's final action, expression, or manner of speaking>.
```

Example:

```text
Applause marking the end of the performance comes from behind the stage. The young actor's fingers suddenly stop on the program, the gaze turns slowly toward the curtain, and the shoulders remain tense.
After confirming that the curtain call is over, the actor exhales softly. The shoulders gradually relax, a restrained smile appears, and the eyes slowly well with tears, but the actor never turns to leave.
```

#### Cinematography terms

Basic camera language can be written directly:

- Shot size: extreme wide shot, wide shot, medium shot, close-up, extreme close-up.
- Camera movement: push in, pull out, pan, lateral move, follow shot, orbit, dive, dolly out, tilt up, handheld shake.
- Position and viewpoint: low angle, overhead view, first-person view.

Popular techniques can be used directly, but when several subjects are in frame, still state which subject the camera follows or revolves around, where the movement begins, and where it ends. Each technique has one detail that matters most:

| Technique | What to specify |
|---|---|
| One-take shot | The subjects, spaces, and events the continuous camera passes through, in order |
| Dolly zoom | The subject size to preserve, and whether the background appears to move closer or farther |
| Aerial view | Viewing height, movement direction, and the environmental area to reveal |
| FPV | First-person flight or traversal path, speed, and turns |
| Bullet time | The action to freeze or slow, and the camera's orbit direction |
| Handheld camera | The subject being followed and the amount of shake |
| Bounce speed ramp | Where the action accelerates, decelerates, or rebounds, and its final resting state |

For a niche term, a term with inconsistent industry usage, or a term that needs precise control, keep the term and translate it into a directly observable visual change:

**Cinematography term + target subject + visual change + foreground/background relationship + direction or speed**

```text
Rack focus: shift focus smoothly from the leaves in the foreground to the person in the background. The leaves gradually blur while the person's face changes from soft to sharp.
```

For a precise transition, also state the trigger time, occluding object, camera direction, transition method, and the composition or motion trend that continues afterward.

Worked examples:

```text
Example 1. Shallow-depth-of-field portrait: keep <Pastry Chef>'s eyes and face sharp while the glass jars and lights in the background become soft, circular bokeh.

Example 2. Tracking shot: move horizontally at the same speed as <Skateboarder>, keeping the subject sharp while the roadside wall forms horizontal motion blur from right to left.

Example 3. Golden hour: warm, low-angle sunlight enters from behind and to the left of <Hiker>, casting long shadows across the mountain ridge.

Example 4. Natural vignette: darken the four corners gradually while keeping the brightness and skin tone of <Pianist> in the center natural, without a black border.

Example 5. Whip-pan transition: at 5 seconds, move the camera rapidly to the left. Cut when the foreground bookshelf fully covers the frame, then continue moving left at a similar speed in the next scene.
```

Aperture, focal length, and shutter values can be included, but the intended visible result is usually clearer than a numeric value alone.

---

## Inlined: `references/checklist.md`

### Checklist and Limitations

Apply the **Core** block always. Apply a task block only when that task type is in play. Running
all blocks on every prompt trains rubber-stamping; skipped blocks should be skipped visibly.

Items marked ⚙ are checked mechanically by `scripts/lint_prompt.py` — run it first, then spend
judgement on the rest.

#### Core — every prompt

- [ ] Subject and primary action or event clearly stated, and stated first.
- [ ] ⚙ No unfilled `<angle-bracket placeholders>` remain.
- [ ] ⚙ Generation parameters (duration, ratio, resolution) are not written into the prompt.
- [ ] Abstract emotions and cinematography terms are paired with visible or audible cues.
- [ ] Every non-blocking default is listed as an assumption under the prompt.

#### When reference materials are used

- [ ] ⚙ Every `@Image`/`@Video`/`@Audio` cited in the body has a role-defining line.
- [ ] ⚙ Reference numbering is contiguous from 1 with no gaps.
- [ ] ⚙ No collective binding ("@Images 1 through 4 define four characters respectively").
- [ ] Every role line states what to use and what not to use.
- [ ] Every distinct character, product, and prop is named and bound individually.
- [ ] The intended material order is stated to the user alongside the prompt.
- [ ] References are selected per scene rather than required to appear all at once.
- [ ] Where a reference video defines motion, the prompt inherits attributes instead of restating the action.

#### When the video has multiple events or stages

- [ ] Each stage has one primary change and an explicit end state.
- [ ] ⚙ Time ranges are consecutive and non-overlapping.
- [ ] No frequency demands ("three actions in one second").
- [ ] Character count, clothing, prop ownership, and spatial relationships stay consistent across stages.

#### When editing an existing video

- [ ] Source video declared the sole editing master.
- [ ] Edit scope names the object, region, time range, or audio category — and nothing wider.
- [ ] Target quantity stated explicitly ("exactly one ...").
- [ ] `[Timeline Inheritance]` present for subject or background replacement.
- [ ] Content to preserve listed.
- [ ] ⚙ No aspect-ratio or duration request (both locked on this task type).

#### When extending a video

- [ ] Extension direction stated.
- [ ] Boundary frame described before the new content (forward) or as the explicit end state (backward).
- [ ] Continuous-instance lock present ("do not duplicate or split").
- [ ] For backward extension, materials that must not appear early are named.
- [ ] ⚙ No aspect-ratio request (locked).

#### When using first/last frames or keyframes

- [ ] Each anchor image described separately, never combined into one sentence.
- [ ] First and last images use the same aspect ratio.
- [ ] Supplementary references told not to override the anchor compositions.
- [ ] ⚙ No aspect-ratio request (locked to the first image).

#### When using storyboards or blockouts

- [ ] Storyboard states the reading order and which structure to inherit.
- [ ] Blockout identified as coarse or fine before drafting.
- [ ] Coarse: every blockout object mapped to its final subject or prop.
- [ ] Fine: attributes to re-render defined, and what to preserve from the blockout stated.

#### When using one-click video or seamless transitions

- [ ] One-click: material roles, image order, motion amount, editing style, and audio all defined.
- [ ] Transitions: both videos' roles, trigger action, transition process, and arrival state defined.

#### Limitations — say these out loud when they apply

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

---
