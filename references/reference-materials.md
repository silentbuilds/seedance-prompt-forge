# Reference Materials

## Contents

- [Limits and recommended ranges](#limits-and-recommended-ranges)
- [Define each material's role](#define-each-materials-role)
- [Multiple views of the same subject](#multiple-views-of-the-same-subject)
- [Motion references](#motion-references)
- [Multi-reference creation](#multi-reference-creation)

## Limits and recommended ranges

Seedance 2.5 combines up to 50 reference materials total. Recommended ranges improve stability; they are not hard capability limits.

| Type | Limit | Recommended |
|---|---|---|
| Images | Up to 30, each no larger than 4K | 1–8 distinct subjects across subject-reference images |
| Videos | Up to 10, combined ≤ 30 s | 1–5 distinct subjects, 5–10 s per subject video |
| Audio | Up to 10, combined ≤ 30 s | Only dialogue, voice, ambience, or music relevant to the task |
| Video editing | Source video + reference images | Source under 20 s; 1–5 reference images |

- Above these ranges stability may drop (e.g., 9–12 subjects, 6–10 audio/video subjects, 6–8 edit references).
- If more than five subjects need multiple views, place different views in separate images; independent view images are more stable than one collage.

## Define each material's role

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

## Multiple views of the same subject

State each view separately and lock the count:

```text
@Image 1 defines the front view of the same folding desk lamp.
@Image 2 defines the left-side structure of the same folding desk lamp.
@Image 3 defines the right-side structure of the same folding desk lamp.
@Image 4 defines the rear structure of the same folding desk lamp.
All four images define one folding desk lamp. The output must contain only one lamp throughout.
```

## Motion references

When a reference video already defines motion, camera movement, and sequence accurately, state only which attributes to inherit. Restating every action can conflict with the reference. A blockout video mainly provides motion and spatial structure, so the prompt must still define the intended subjects, scene, action, and visual style.

## Multi-reference creation

Use this order when many materials are provided: **define each material's role → map subjects → group by type → create subject profiles → select references by scene**. The goal is to help the model select the correct materials for the current scene, not to make every material appear at once.

### Step 1: Name and map each subject individually

```text
<Character A> corresponds to @Image 1. Use only the appearance, hairstyle, and clothing.
<Character B> corresponds to @Image 2. Use only the appearance, hairstyle, and clothing.
<Prop A> corresponds to @Image 3. Use only the structure, material, and color.
<Scene A> references @Image 4. Use only the spatial layout, architecture, and lighting. Do not use the people in the image.
```

### Step 2: Group materials by type

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

### Step 3: Create a subject profile for important characters

```text
[Subject Profile: Conservator]
Appearance and clothing: @Image 1.
Fixed prop: <Sample Case> from @Image 5.
Locations: <Conservation Lab> and <Gallery>.
Motion references: the case-opening motion from @Video 1.
Do not use: other characters' clothing. Do not give this character <Record Board> or guide equipment.
```

### Step 4: Select references by scene

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
