#!/usr/bin/env python3
"""Build the SFX track from the cues declared in index.html (data-sfx).

Each cue lands at the start time of the animation it belongs to, so every sound
is tied to something moving on screen. Writes SCENES/sfx-track.wav (48 kHz stereo).

usage: mix_sfx.py [--dir SCENES] [--sfx SFX_DIR] [--size 1080x1920]
  data-sfx="name[,gain[,rate[,at[,dur]]]]|..."  name = SFX_DIR/<name>.mp3
"""
import json, pathlib, subprocess, os, argparse
import numpy as np
from playwright.sync_api import sync_playwright

HERE = pathlib.Path.cwd()
SFX = HERE / "sfx"
SR = 48000
W, H = 1080, 1920


def cues():
    with sync_playwright() as p:
        exe = os.environ.get("CHROME_PATH")
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        pg.goto((HERE / "index.html").as_uri())
        pg.wait_for_function("window.ENGINE_READY === true")
        out = pg.evaluate("({cues: window.sfxCues(), total: window.TOTAL})")
        b.close()
    return out


def load(name):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(SFX / f"{name}.mp3"), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()
    env = np.abs(a).max(1)
    thr = 10 ** (-40 / 20) * max(env.max(), 1e-6)
    idx = np.argmax(env > thr)
    a = a[max(0, idx - int(0.004 * SR)):]
    peak = np.abs(a).max()
    return a / peak if peak > 0 else a


def main():
    global HERE, SFX, W, H
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=".")
    ap.add_argument("--sfx")
    ap.add_argument("--size", default="1080x1920")
    a = ap.parse_args()
    HERE = pathlib.Path(a.dir).resolve()
    SFX = pathlib.Path(a.sfx).resolve() if a.sfx else HERE / "sfx"
    W, H = (int(v) for v in a.size.lower().split("x"))
    data = cues()
    total = data["total"]
    track = np.zeros((int(total * SR) + SR, 2), dtype=np.float32)
    cache = {}
    for c in data["cues"]:
        name = c["name"]
        if name not in cache:
            cache[name] = load(name)
        a = cache[name]
        rate = c.get("rate") or 1
        if rate != 1:
            n = int(len(a) / rate)
            x = np.linspace(0, len(a) - 1, n)
            a = np.stack([np.interp(x, np.arange(len(a)), a[:, ch]) for ch in (0, 1)], 1).astype(np.float32)
        dur = c.get("dur") or 0
        if dur:
            a = a[: int(dur * SR)].copy()
            f = min(len(a), int(0.08 * SR))
            a[-f:] *= np.linspace(1, 0, f)[:, None]
        start = int(c["t"] * SR)
        end = min(len(track), start + len(a))
        track[start:end] += a[: end - start] * float(c["gain"]) * 0.5
    track = track[: int(total * SR)]
    track = np.tanh(track * 1.2) / np.tanh(1.2)
    peak = np.abs(track).max()
    if peak > 0:
        track *= (10 ** (-1.5 / 20)) / peak
    else:
        print("warning: no data-sfx cues found, writing a silent track")
    out = HERE / "sfx-track.wav"
    pcm = (track * 32767).astype("<i2").tobytes()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", str(out)], input=pcm, check=True)
    json.dump(data, open(HERE / "sfx-cues.json", "w"), indent=1)
    print(f"{len(data['cues'])} cues, {total:.2f}s -> {out}")


if __name__ == "__main__":
    main()
