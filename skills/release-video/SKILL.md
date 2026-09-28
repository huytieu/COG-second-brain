---
name: release-video
description: Turn a product release (the list of shipped items plus real screen recordings) into a motion recap video and one explained demo per feature, with sound effects tied to on-screen motion and a composed music bed. Deterministic HTML scenes rendered frame by frame, ElevenLabs for sound effects and music, ffmpeg for the mix. Use when asked for a release video, a changelog video, a feature recap reel, or demo clips for release notes and docs.
---

# release-video

Two outputs per release:

- **Recap**: a 45-75 s motion video, one scene per shipped feature, vertical (1080x1920) by default.
- **Explained demos**: one 30-60 s clip per feature, a real recording of the product with step captions, eased zoom on the payoff, and intro/outro cards (1920x1080).

Every frame of the recap is a pure function of time (`window.renderAt(t)` in `scripts/engine.js`), so a re-render is identical, renders split across workers, and any single frame can be pulled as a still for review before the full render.

This skill makes motion scenes and composes demos from recordings. It does not cut raw footage of people talking. For narrated takes, founder voice-overs or interviews, use [browser-use/video-use](https://github.com/browser-use/video-use), which cuts on word boundaries from a transcript, and drop the recap and demo clips into its folder as B-roll.

## Requirements

`ffmpeg`, Python 3 with `playwright`, `numpy`, `Pillow`, and `ELEVENLABS_API_KEY` for audio. If Playwright's bundled Chromium doesn't launch, point `CHROME_PATH` at any Chromium or headless-shell binary.

## Rules from review

These came from a real review of the first cut. Each one cost a full re-render when it was missed.

1. **Sound comes from the motion.** Every sound effect is declared on the element that moves (`data-sfx="pop,0.5"`) and lands on that element's animation start. A looping background track as the only audio reads as filler.
2. **Music is composed to the timeline.** Write a sectioned plan whose section lengths match the scenes: a quieter intro under the title, the full groove from the first feature, a lift on the summary, a final hit on the outro. Pick a tempo where scene boundaries land on beats (120 BPM puts a beat on every half second). Generate two or three candidates and keep the one `music_check.py` scores least repetitive.
3. **Do not reuse the reference video's ideas.** If you were shown a video to match, take its pacing and polish. Its visual metaphors belong to its subject. A radar chart made sense for a tech-radar release and means nothing for yours.
4. **Each illustration shows its feature.** A filter feature shows the filter conditions. A speed feature shows the before and after number. Generic shapes that could sit in any scene get replaced.
5. **Complete shapes only.** Draw-on strokes must finish closed and whole. Half-drawn arcs and dangling lines at rest read as low quality.
6. **Pace for reading.** Feature scenes run 6-8 s, long enough to read every line twice. In demos, sped-up stretches say so in the caption ("sped up 2.5x"), and the payoff plays at 1x with a zoom and a highlight ring.
7. **Real product, real data.** Demos come from recordings of the live product on a demo project. Numbers on screen match what the recording shows.

## Workflow

1. **Inventory.** List the shipped items from the release milestone or changelog. Pick the ones a user would notice and leave internal fixes to the written notes. For each, write one sentence of what changed and one of why it matters.
2. **Record.** Capture each feature end to end in the real product. Any recorder works. `scripts/frames_from_video.sh rec.mp4 <name>` turns a recording into the frames folder and manifest the composer reads.
3. **Storyboard.** Copy `templates/` into a working folder with `scripts/engine.js`. One `<section class="scene">` per beat, with `data-start` and `data-dur` in seconds. Element timings are relative to their scene. The comment at the top of `templates/index.html` lists every animation attribute.
4. **Review stills before rendering.** `render.py stills <t1> <t2> ... --dir <folder>` writes PNGs at chosen times. Take one per scene midpoint, tile them into a contact sheet with ffmpeg `hstack`, and look at it against the rules above. Fix, then re-take the stills.
5. **Sound effects.** `gen_audio.sh sfx <name> "<prompt>" <seconds> <folder>/sfx` once per sound (whoosh, pop, tick, chime, thump, a soft riser). Keep them short and quiet in character. `mix_sfx.py --dir <folder>` reads every `data-sfx` cue from the page and builds `sfx-track.wav`.
6. **Music.** Adapt `templates/music-plan.example.json` so section durations sum to the video length, then `gen_audio.sh music plan.json bed-a.mp3`. Run `music_check.py bed-*.mp3`, which prints scores and rejects nothing itself, and keep the candidate with the lowest far-similarity and an intro quieter than the body.
7. **Render and mix.** `render.py video --dir <folder> --out recap.mp4`, then `mix_final.sh recap.mp4 sfx-track.wav bed-a.mp3 recap-final.mp4`. The mix ducks music under each effect, normalizes toward -18 LUFS (one loudnorm pass lands within about 1 LU) with true peak under -1.5 dBTP, writes a smaller `-web.mp4`, and lists any silence over 1 s.
8. **Demos.** Write a spec per feature from `templates/demo-spec.example.json`: the recording's manifest, segments with source time ranges, speed, a caption per step, and zoom plus ring boxes on the payoff. `compose_demo.py spec.json` renders it. Pull a frame from each segment and check the captions are readable and the ring sits on the right element.
9. **Self-review.** Watch the final at 1x before handing it over. Check each rule, then check that every number on screen matches the release notes.

## Files

| Path | What it does |
|---|---|
| `scripts/engine.js` | Scene engine: timing attributes, easing, draw-on, typewriter, counters, canvas burst, SFX cue export |
| `scripts/render.py` | Stills for review, or a parallel frame render encoded with ffmpeg |
| `scripts/mix_sfx.py` | Builds the effects track from `data-sfx` cues |
| `scripts/gen_audio.sh` | ElevenLabs sound effects and composed music |
| `scripts/music_check.py` | Tempo, beat phase, loudness curve and repetition score per candidate |
| `scripts/mix_final.sh` | Sidechain mix, loudness check, web copy, silence check |
| `scripts/compose_demo.py` | Recording, window frame, captions, zoom, ring, intro and outro cards |
| `scripts/frames_from_video.sh` | Recording to frames plus manifest |
| `templates/` | Starter scenes, theme tokens, demo spec, music plan |

Theme lives in CSS variables in `templates/base.css` and in `spec["theme"]` for demos. Swap in your product's colors and fonts there; the rest of the pipeline carries no brand.
