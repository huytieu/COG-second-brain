---
name: youtube-video-kit
description: >
  Produce YouTube-ready video packaging: a branded thumbnail, an animated
  opening title, background music via ElevenLabs Music, and the upload metadata
  bundle. Use whenever you make or publish a video (deep dives, demos, blog
  companions) or want thumbnails, intros, video music, or channel and playlist
  consistency.
---

# YouTube video kit

Package videos like a channel, not a screen recording. The template fuses two reference styles: cinematic stills with minimal text (the Anthropic channel) and dark IDE screenshots with huge boxed text, one accent word, readable at 320px (AI-coding channels). It uses the dark lane-art language from the `social-media-kit` skill.

## Configuration

Scripts read environment variables, so nothing personal is hardcoded.

| Setting | Env var | Default |
|---|---|---|
| Signature text (bottom-left) | `BRAND_URL` | `yourblog.example` |
| Avatar PNG with a white background (optional) | `AVATAR_PATH` | unset (no avatar drawn) |
| Accent word color | `ACCENT` | `D97757` (terracotta, configurable) |
| Fonts | `HEADLINE_FONT`, `MONO_FONT` | macOS Helvetica Neue and Menlo, DejaVu on Linux |
| Opening eyebrow and chip text | `OPEN_EYEBROW`, `OPEN_CHIP` | example strings |
| ElevenLabs key | `ELEVENLABS_API_KEY` | none, required for music |

Your channel ID, handle and avatar belong in your own config.

## Requirements

- Python 3 with Pillow
- ffmpeg
- `ELEVENLABS_API_KEY` for music generation
- A CDP-driven Chrome logged in to YouTube Studio, for publishing (for example the `browser-harness` skill)

## Thumbnail

`scripts/ytthumb.py`, 1280x720 (rendered at 2560x1440, then downscaled). Keep the template identical across a playlist and vary only headline, accent word and lane pattern.

- Background `#0A0B0D` plus lane art on the right third, with green and red end dots.
- Your avatar, if you set one, is keyed (white above 235 becomes transparent), resized with NEAREST, and placed bottom-right over the lanes. Use one consistent avatar as the channel identity rather than varying photo cutouts.
- Headline: 2 lines at most, about 5 words, bold sans around 210px at 2x, white, with one accent word. It must stay legible at 320px wide (squint test).
- One mono chip with real numbers and a green dot.
- Signature and a cursor block, bottom-left.

```bash
AVATAR_PATH=./avatar.png BRAND_URL=myblog.dev python3 .claude/skills/youtube-video-kit/scripts/ytthumb.py "MY AI TESTS|MY PRODUCT." AI "7 passed · 4 failed" thumb.png
```

## Opening title

`scripts/ytopen.py [out.mp4]` renders 4.2s at 30fps, 1920x1080, with PIL frames piped to ffmpeg (rawvideo to libx264 crf 19). Sequence: lanes draw in, staggered (0-1.2s); eyebrow (0.6s); headline fades in by line (0.9, 1.2, 1.5s, accent word colored); chip (2.2s); avatar rises (1.6-2.6s); signature with a blinking cursor (2.6s); 0.5s fade to black. Edit `HEAD` in the script for the headline.

To join it to the main video, give the opening a silent AAC track (`-f lavfi -i anullsrc=r=44100:cl=mono -shortest`) matching the main video's audio params, then use the concat demuxer with `-c copy`.

## Music with ElevenLabs

```bash
curl -X POST "https://api.elevenlabs.io/v1/music" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" -H "Content-Type: application/json" \
  -d '{"prompt": "<style prompt>", "music_length_ms": 250000}' -o bgm.mp3
```

Check that your plan includes the Music API first. For a narration bed, ask for "very minimal, unobtrusive, no melody hooks, no vocals". Mix the bed about 20dB under the voice-over, and louder only during the title:

```bash
ffmpeg -i video.mp4 -i bgm.mp3 -filter_complex \
 "[1:a]atrim=0:<dur>,volume='if(lt(t,4.2),0.45,0.13)':eval=frame,afade=t=in:d=1.2,afade=t=out:st=<dur-3>:d=3[bg];\
  [0:a][bg]amix=inputs=2:duration=first:normalize=0[a]" \
 -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 160k out.mp4
```

Sanity check with `volumedetect` on a narration window: mean near -25dB, max at or above -6dB. Store generated tracks durably so a playlist reuses the same music family.

## Storyboarding: illustrate, do not slide

The principle: every frame should show the concept being narrated, not print it. A text-list frame is a slide, and viewers skim it.

- For each voice-over sentence ask "what is the picture of this idea?" A loop that eats itself gets a drawn loop. Two lanes converging get drawn converging. Fall back to typography only for the one or two anchor statements.
- Screenshots count as illustration only with a guided camera: a cursor moving to the thing discussed, click ripples, a highlight wrapping the exact row, zooms. A static screenshot is a slide.
- Voice-over pacing: on non-illustration frames (rules, recaps, quotes) narrate faster, with shorter sentences or trimmed silence. Slow down only where the visual needs watching time (footage, terminal replay). A boring frame with slow narration is the biggest drop-off combination.
- Animation speed: cursor hops 0.4s or less, element fade-ins 0.5s or less, and no static frame longer than 2.5s without something moving (cursor, spinner, highlight pulse).

## Shot-segment QA before assembling

A highlight box once shipped floating over empty page space because its coordinates were guessed. Every screenshot segment passes this before concat:

1. Highlights are in card coordinates (the screenshot scaled to card width). Cursor waypoints are in screen coordinates. Do not mix them.
2. A highlight wraps one actual UI row or element edge to edge. It never slices through a row or floats in whitespace. Snap it to the real bounding box read off the image.
3. Audit before rendering: paste the highlight rect onto the scaled screenshot with PIL and look at it. After rendering, extract a frame at each highlight's midpoint (`ffmpeg -ss <t> -frames:v 1`) and look at it.
4. Highlights must not overlap zoom windows. The highlight rect does not scale with zoom, so end it before the zoom starts.
5. Cursor waypoints and click ripples land on the element being narrated, not in dead space.

## Upload bundle and Studio publishing

Per video, keep in the kit folder: the final mp4, the thumbnail PNG, and `youtube-description.txt` (hook line, chapters, blog link first, skill links, tags). Title formula: benefit, plus the named product, plus the "AI agent" keyword, 70 characters or fewer. For playlist consistency use the same thumbnail template, the same opening and the same music family.

To publish through YouTube Studio in a logged-in Chrome (your own channel):

- The upload dialog's file input is sometimes in shadow DOM. Use `cdp("DOM.performSearch", query="input[type=file]")` plus `DOM.setFileInputFiles` by nodeId.
- Title and description boxes are `#textbox` elements: select all, then type.
- Thumbnail: `input#file-loader`.
- Audience: click the `VIDEO_MADE_FOR_KIDS_NOT_MFK` radio through JS `.click()`.
- Playlist: the dropdown checkbox in the dialog.
- Advance: `#next-button` three times through JS click. Set visibility with the PUBLIC radio through JS `.click()`, then `#done-button`.
- Deleting an old upload: video edit page, Options, Delete, consent checkbox, Delete forever.
- Replacing a video file creates a new video ID, so update every posted link. An X reply must be deleted and reposted. LinkedIn posts and Reddit comments are editable.

## Definition of done

- [ ] Thumbnail passes the 320px squint test, with signature (and avatar if you use one)
- [ ] Opening uses the channel animation, and terminal shots follow the `terminal-replica` skill
- [ ] Music bed generated, mixed and level-checked, and tracks stored durably
- [ ] Upload bundle complete for manual publish
