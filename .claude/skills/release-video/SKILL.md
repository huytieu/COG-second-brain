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

8. **Upbeat music.** Beds are bright and uplifting (major key, about 115-125 BPM). A calm or sad bed reads as boring.
9. **Say acronyms right.** On `eleven_v4`, write "AI" plain and use no alias dictionary: the hyphenated alias "ay-eye" sounds unnatural, and v4 says "AI" correctly by itself (Scribe hears "AI", about 0.35 s). Keep aliases only for acronyms that v4 gets wrong in a test clip, and never use dotted spellings like A.I. Check a test clip and Scribe word timestamps before rendering the full set.

10. **Zoom slowly, keep context.** Show the target in the full frame first with a ring or spotlight for about 1 s, zoom over at least 1.2 s with easing, never past about 1.6x, keep surrounding UI visible, and zoom back out before the next step. Prefer a spotlight dim to a hard crop. A zoom box must match the window aspect: expand it before cropping, never resize a narrower box into the window, because that stretches the UI sideways (see `fit()` in `scripts/compose_demo.py`). Zoom back out with an eased move, never a cut.
11. **Explain before demoing.** Each feature clip opens with what it does and how it helps, then shows how to turn it on or set it up, then the demo.

12. **Energetic narration.** Target about 185-195 words per minute with an excited, upbeat delivery, like a social-media creator. The API's max speed of 1.2 on `eleven_v4` gives only about 160 wpm, so add `atempo=1.15` after generation. Energy comes from pace and delivery, not hype words. Write plain product language: "Select Run", "Choose Separate", "four times faster". No social-media slang such as "hit", "boom", "magic switch", "crank it". Narration runs continuously: fit the visuals to the voice-over, never leave long silent gaps between lines.

13. **Human input on camera.** Drive recordings with `scripts/human_input.py`. It reproduces timings measured on real human recordings. The cursor is visible, and its shape follows the hovered element: arrow, pointing hand, or I-beam. Moves take 150-450 ms, run nearly straight with a slight bow, and peak in speed mid-move. A long move ends with 1-3 small corrections and a 200-400 ms dwell, then a click held 80-120 ms. Real `mouseMoved` events show hover states before each click. Keys come 60-120 ms apart, with longer pauses between words; never paste a whole string. Keep the cursor still about two thirds of the time, with 1.5-2.5 s reading pauses after new content. While an AI answer streams, keep the cursor still and speed-ramp the wait. A headless capture has no OS cursor, so draw one from the event path. Record at 2x scale and at least 60 fps, on a production build: pre-release builds can show license watermarks.

## Workflow

1. **Inventory.** List the shipped items from the release milestone or changelog. Pick the ones a user would notice and leave internal fixes to the written notes. For each, write one sentence of what changed and one of why it matters.
2. **Record.** Capture each feature end to end in the real product. Any recorder works. `scripts/frames_from_video.sh rec.mp4 <name>` turns a recording into the frames folder and manifest the composer reads.
3. **Storyboard.** Copy `templates/` into a working folder with `scripts/engine.js`. One `<section class="scene">` per beat, with `data-start` and `data-dur` in seconds. Element timings are relative to their scene. The comment at the top of `templates/index.html` lists every animation attribute.
   Real UI inside a scene: crop stills and recorded frames into windows rather than redrawing the product, and map ring boxes from source pixels into each crop. A frame sequence plays with `<div data-seq="start,fps">` holding one `<img>` per frame; keep it to a few seconds at 30 fps. Crops of 1x captures read on a phone only at about 1.4x or more, so crop narrow and fade the right edge when lines run long; 2x captures stay sharp.
   Spotlight and zoom: dim the frame with a hole over the target plus a ring, glide the hole between boxes over about 640 ms so beats never jump-cut between crops, and ease any zoom toward a point, capped at 1.6x and back to 1x before the beat ends. Check that no ring crosses text, no shot renders under 1x, and no two caption lines show at once. Captions are one bar per scene whose text swaps out then in, so bars of different widths never cross-fade.
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
| `scripts/plain_demo.py` | Plain demo cut: the same spec on a browser card over a gradient, no captions or cards; honors per-segment `blur` and `speed` |
| `scripts/human_input.py` | Human-looking mouse paths, corrections, clicks and typing over CDP (`python3 human_input.py` self-checks the timings) |
| `scripts/frames_from_video.sh` | Recording to frames plus manifest |
| `templates/` | Starter scenes, theme tokens, demo spec, music plan |

Theme lives in CSS variables in `templates/base.css` and in `spec["theme"]` for demos. Swap in your product's colors and fonts there; the rest of the pipeline carries no brand.
