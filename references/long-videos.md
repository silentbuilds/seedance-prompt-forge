# Long Videos: Stages and Timing

## Stages

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

## Timestamps

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

## Timing rules

- Time ranges must be consecutive and non-overlapping.
- Ranges are an event's time budget, not a precise edit point; actions may occur slightly before or after a boundary.
- Too little content in a range gives the model freedom; too much can cause excessive cutting or omitted events.
- Do not use timestamps to demand frequencies, such as "complete three actions in one second".
