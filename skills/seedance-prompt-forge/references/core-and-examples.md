# Core Formula and Worked Examples

## Contents

- [Components](#components)
- [Rules](#rules)
- [Example 1: bare idea to text-to-video prompt](#example-1-bare-idea-to-text-to-video-prompt)
- [Example 2: loose brief with references](#example-2-loose-brief-with-references)
- [Example 3: repairing a failed generation](#example-3-repairing-a-failed-generation)

## Components

- **Subject + Action or Event** — who or what is doing what. The foundation of the video; state it first.
- **Scene and Environment** — location, time, weather, spatial relationships, background state.
- **Visual Style** — lighting, color, materials, image texture, or overall mood.
- **Camera Movement/Cut** — shot size, camera angle, camera movement, the focus subject, shot transitions.
- **Audio** — dialogue, voice characteristics, ambience, sound effects, music.

## Rules

- Omit any component you do not need.
- Do not include generation parameters in the prompt; set them on the generation page or through the API.
- State the subject and primary action or event first.

## Example 1: bare idea to text-to-video prompt

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

## Example 2: loose brief with references

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

## Example 3: repairing a failed generation

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
