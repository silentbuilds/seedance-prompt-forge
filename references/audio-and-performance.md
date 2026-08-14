# Audio, Emotion, and Cinematography

## Audio and text syntax

Prompts can be plain natural language. Use these markers only when you need to distinguish categories explicitly.

| Content | Syntax | Example |
|---|---|---|
| Music | `()` | `(Soft, rhythmic piano music plays in the background)` |
| Sound effects | `<>` | `<A bell rings in the distance>` |
| Dialogue | `{}` | `{Hello, welcome back.}` |
| Subtitles | `【】` | `【Chapter One: Departure】` |

## Dialogue language reinforcement

- When dialogue is not in Chinese, state the language before the line. The short form is often enough: `The girl says softly in Japanese: {もう大丈夫です}`.
- If English dialogue is spoken in Chinese, or a specific regional variety matters, use the full formula: **dialogue language + regional variety or accent + delivery style + speaker + {dialogue}**.

```text
Dialogue language: American English. The girl says in natural, conversational American English: {I thought you weren't coming.}

Dialogue language: authentic Los Angeles English. The young man says in natural Los Angeles vernacular: {No way, you actually made it.}
```

## Emotional direction and observable performance

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

## Cinematography terms

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
