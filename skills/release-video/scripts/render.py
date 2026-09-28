#!/usr/bin/env python3
"""Render a scene folder's index.html frame by frame with headless Chromium, then encode.

Every frame is window.renderAt(t) from engine.js, so renders are deterministic and split
across workers. Frame size comes from --size (default 1080x1920, vertical).

usage:
  render.py stills 0.5 3.2 ... [--dir SCENES]     # PNG stills into SCENES/stills/ for visual QA
  render.py video [--dir SCENES] [--fps 30] [--workers 6] [--audio track.wav] [--out recap.mp4]
"""
import argparse, subprocess, sys, pathlib, math, shutil, os
from concurrent.futures import ProcessPoolExecutor
from playwright.sync_api import sync_playwright

HERE = pathlib.Path.cwd()
URL = None
W, H = 1080, 1920


def _launch(p):
    """Playwright's bundled Chromium, or CHROME_PATH if set."""
    exe = os.environ.get("CHROME_PATH")
    args = ["--font-render-hinting=none", "--disable-lcd-text"]
    return p.chromium.launch(executable_path=exe, args=args) if exe else p.chromium.launch(args=args)


def _open(p):
    b = _launch(p)
    pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
    pg.goto(URL)
    pg.wait_for_function("window.ENGINE_READY === true")
    pg.evaluate("document.fonts.ready")
    return b, pg


def render_slice(args):
    frames, fps, outdir, url, size = args
    global URL, W, H
    URL, (W, H) = url, size
    with sync_playwright() as p:
        b, pg = _open(p)
        for f in frames:
            pg.evaluate(f"window.renderAt({f / fps})")
            pg.screenshot(path=str(outdir / f"f{f:05d}.png"), type="png")
        b.close()
    return len(frames)


def total_seconds():
    with sync_playwright() as p:
        b, pg = _open(p)
        t = pg.evaluate("window.TOTAL")
        b.close()
    return t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["stills", "video"])
    ap.add_argument("times", nargs="*", type=float)
    ap.add_argument("--fps", type=int, default=30)
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--audio")
    ap.add_argument("--out", default="recap.mp4")
    ap.add_argument("--dir", default=".")
    ap.add_argument("--size", default="1080x1920")
    a = ap.parse_args()
    global HERE, URL, W, H
    HERE = pathlib.Path(a.dir).resolve()
    URL = (HERE / "index.html").as_uri()
    W, H = (int(v) for v in a.size.lower().split("x"))

    if a.mode == "stills":
        out = HERE / "stills"; out.mkdir(exist_ok=True)
        with sync_playwright() as p:
            b, pg = _open(p)
            for t in a.times:
                pg.evaluate(f"window.renderAt({t})")
                pg.screenshot(path=str(out / f"t{t:06.2f}.png"))
                print(out / f"t{t:06.2f}.png")
            b.close()
        return

    total = total_seconds()
    n = int(math.ceil(total * a.fps))
    fdir = HERE / "frames"
    shutil.rmtree(fdir, ignore_errors=True); fdir.mkdir()
    slices = [list(range(i, n, a.workers)) for i in range(a.workers)]
    with ProcessPoolExecutor(a.workers) as ex:
        done = sum(ex.map(render_slice, [(s, a.fps, fdir, URL, (W, H)) for s in slices]))
    print(f"rendered {done} frames ({total:.2f}s)")
    cmd = ["ffmpeg", "-v", "error", "-y", "-framerate", str(a.fps), "-i", str(fdir / "f%05d.png")]
    if a.audio:
        fade_st = max(0, total - 2.2)
        cmd += ["-i", a.audio, "-filter_complex",
                f"[1:a]atrim=0:{total},afade=t=in:d=0.4,afade=t=out:st={fade_st}:d=2.2,volume=0.9[a]",
                "-map", "0:v", "-map", "[a]", "-c:a", "aac", "-b:a", "192k"]
    cmd += ["-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-preset", "slow",
            "-movflags", "+faststart", "-t", f"{total}", str(HERE / a.out)]
    subprocess.run(cmd, check=True)
    print(HERE / a.out)


if __name__ == "__main__":
    main()
