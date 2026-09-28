#!/usr/bin/env python3
"""Compose a real screen recording into an explained demo (1920x1080, 30fps).

Layers: a background with a browser window, the recording (variable speed,
eased zoom, highlight ring), step captions under the window, intro/outro cards.
Text layers are rendered once with headless Chromium so they use the same fonts
as the recap video; frames are composited with Pillow and piped to ffmpeg.

The recording is a folder of numbered JPEG frames plus a manifest
({frames_dir, fps, frame_count, img_w, img_h, duration}); frames_from_video.sh
makes one from any .mp4/.mov. Theme (colors, fonts) comes from spec["theme"].

Intro/outro title, body and kicker are inserted as HTML so <em> works; escape & < > yourself.

usage: compose_demo.py <spec.json>   (see templates/demo-spec.example.json)
"""
import json, math, pathlib, subprocess, sys, html, os
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

HERE = pathlib.Path.cwd()
W, H, FPS = 1920, 1080, 30
WIN = (80, 36, 1840, 36 + 48 + 814)          # window box
CONTENT = (80, 36 + 48, 1840, 36 + 48 + 814)  # recording area (1760 x 814)

DEFAULT_THEME = {
    "bg": "#eef0f3", "ink": "#111318", "paper": "#e5e7eb", "accent": "#6366f1", "accent_soft": "#a5b4fc",
    "fonts_css": "", "sans": "Inter, system-ui, sans-serif", "serif": "Georgia, serif", "mono": "ui-monospace, Menlo, monospace",
}


def css_for(t):
    link = f'<link rel="stylesheet" href="{t["fonts_css"]}">' if t.get("fonts_css") else ""
    return f"""{link}
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{W}px; height:{H}px; background:transparent; }}
.bg {{ position:absolute; inset:0; background:{t["bg"]}; }}
.win {{ position:absolute; left:{WIN[0]}px; top:{WIN[1]}px; width:{WIN[2]-WIN[0]}px; height:{WIN[3]-WIN[1]}px; border-radius:18px; background:#fff;
  box-shadow:0 1px 0 rgba(0,0,0,.05),0 40px 80px -30px rgba(0,0,0,.45),0 0 0 1px rgba(0,0,0,.08); }}
.bar {{ height:48px; display:flex; align-items:center; gap:10px; padding:0 20px; border-bottom:1px solid #e6e8ec; }}
.bar i {{ width:13px; height:13px; border-radius:50%; background:#d0d7de; display:block; }}
.pill {{ margin-left:18px; background:#f6f8fa; border-radius:999px; padding:7px 18px; font:500 16px/1 {t["mono"]}; color:#57606a; }}
.cap {{ position:absolute; left:80px; top:922px; display:flex; align-items:center; gap:20px; max-width:1760px;
  background:{t["ink"]}; color:{t["paper"]}; border-radius:18px; padding:20px 30px; }}
.cap b {{ font:500 20px/1 {t["mono"]}; letter-spacing:.14em; color:{t["accent_soft"]}; white-space:nowrap; }}
.cap span {{ font:400 30px/1.3 {t["sans"]}; }}
.card {{ position:absolute; inset:0; background:{t["ink"]}; color:{t["paper"]}; padding:120px 140px; }}
.card .k {{ font:500 24px/1 {t["mono"]}; letter-spacing:.16em; text-transform:uppercase; opacity:.74; display:flex; gap:16px; align-items:center; }}
.card .k i {{ width:12px; height:12px; border-radius:50%; background:{t["accent"]}; display:block; }}
.card h1 {{ margin-top:70px; font:600 104px/1.02 {t["sans"]}; letter-spacing:-.035em; }}
.card h1 em {{ font:italic 400 110px/1 {t["serif"]}; color:{t["accent_soft"]}; }}
.card p {{ margin-top:44px; max-width:1500px; font:300 42px/1.38 {t["serif"]}; opacity:.82; }}
.card .f {{ position:absolute; left:140px; bottom:100px; font:500 22px/1 {t["mono"]}; letter-spacing:.14em; text-transform:uppercase; opacity:.6; }}
</style>"""


def render_layers(spec, out):
    out.mkdir(parents=True, exist_ok=True)
    CSS = css_for({**DEFAULT_THEME, **spec.get("theme", {})})
    pages = {"bg": f'<div class="bg"></div><div class="win"><div class="bar"><i></i><i></i><i></i><span class="pill">{html.escape(spec["address"])}</span></div></div>'}
    for key in ("intro", "outro"):
        c = spec[key]
        pages[key] = f'<div class="card"><div class="k"><i></i>{c["kicker"]}</div><h1>{c["title"]}</h1><p>{c["body"]}</p><div class="f">{c.get("foot","")}</div></div>'
    for i, seg in enumerate(spec["segments"]):
        if seg.get("caption"):
            pages[f"cap{i}"] = f'<div class="cap"><b>{seg.get("step","")}</b><span>{seg["caption"]}</span></div>'
    with sync_playwright() as p:
        exe = os.environ.get("CHROME_PATH")
        b = p.chromium.launch(executable_path=exe) if exe else p.chromium.launch()
        pg = b.new_page(viewport={"width": W, "height": H})
        for k, body in pages.items():
            f = out / f"{k}.html"
            f.write_text(f"<!doctype html><html><head><meta charset='utf-8'>{CSS}</head><body>{body}</body></html>")
            pg.goto(f.as_uri()); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(150)
            pg.screenshot(path=str(out / f"{k}.png"), omit_background=(k not in ("bg", "intro", "outro")))
        b.close()
    return {k: Image.open(out / f"{k}.png").convert("RGBA") for k in pages}


def ease(p):
    p = max(0.0, min(1.0, p))
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def main():
    spec = json.load(open(sys.argv[1]))
    accent = spec.get("theme", {}).get("accent", DEFAULT_THEME["accent"]).lstrip("#")
    ACCENT = tuple(int(accent[i:i + 2], 16) for i in (0, 2, 4))
    man = json.load(open(spec["manifest"]))
    fdir = pathlib.Path(man["frames_dir"]); sfps = man["fps"]; nfr = man["frame_count"]
    srcw, srch = man["img_w"], man["img_h"]
    layers = render_layers(spec, HERE / "layers" / spec["name"])
    cw, ch = CONTENT[2] - CONTENT[0], CONTENT[3] - CONTENT[1]
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, -30, cw, ch), radius=18, fill=255)

    # timeline: intro card, segments, outro card
    plan = [("card", "intro", spec["intro"]["dur"])]
    for i, seg in enumerate(spec["segments"]):
        dur = (seg["src"][1] - seg["src"][0]) / seg.get("speed", 1)
        plan.append(("seg", i, dur))
    plan.append(("card", "outro", spec["outro"]["dur"]))
    total = sum(d for _, _, d in plan)
    out = HERE / f'{spec["name"]}.mp4'
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    cache = {}

    def src_frame(t):
        i = min(nfr - 1, max(0, int(round(t * sfps))))
        if i not in cache:
            if len(cache) > 40: cache.clear()
            cache[i] = Image.open(fdir / f"{i:05d}.jpg").convert("RGB")
        return cache[i]

    full = (0, 0, srcw, srch)
    t0 = 0.0
    prev_zoom = full
    for kind, key, dur in plan:
        nloc = int(round(dur * FPS))
        for k in range(nloc):
            lt = k / FPS
            if kind == "card":
                card = layers[key]
                a = min(1.0, lt / 0.35) if key == "intro" else min(1.0, lt / 0.35)
                frame = layers["bg"].copy().convert("RGB")
                frame = Image.blend(frame, card.convert("RGB"), a) if key == "outro" else card.convert("RGB")
            else:
                seg = spec["segments"][key]
                sp = seg.get("speed", 1)
                st = seg["src"][0] + lt * sp
                img = src_frame(st)
                z = seg.get("zoom")
                box = full
                if z:
                    zin = ease((lt - z.get("at", 0)) / z.get("dur", 0.8))
                    tgt = z["box"]
                    box = tuple(full[j] + (tgt[j] - full[j]) * zin for j in range(4))
                crop = img.crop(tuple(int(v) for v in box)).resize((cw, ch), Image.LANCZOS)
                ring = seg.get("ring")
                if ring and lt >= ring["at"]:
                    d = ImageDraw.Draw(crop)
                    sx = cw / (box[2] - box[0]); sy = ch / (box[3] - box[1])
                    r = [(ring["box"][0] - box[0]) * sx, (ring["box"][1] - box[1]) * sy, (ring["box"][2] - box[0]) * sx, (ring["box"][3] - box[1]) * sy]
                    grow = ease((lt - ring["at"]) / 0.35)
                    pad = 10 + 30 * (1 - grow)
                    d.rounded_rectangle((r[0] - pad, r[1] - pad, r[2] + pad, r[3] + pad), radius=16, outline=ACCENT + (255,), width=6)
                frame = layers["bg"].copy()
                frame.paste(crop, (CONTENT[0], CONTENT[1]), mask)
                cap = layers.get(f"cap{key}")
                if cap:
                    a = min(1.0, lt / 0.3)
                    if a < 1:
                        c2 = cap.copy(); c2.putalpha(cap.getchannel("A").point(lambda v: int(v * a)))
                        frame.alpha_composite(c2)
                    else:
                        frame.alpha_composite(cap)
                frame = frame.convert("RGB")
            ff.stdin.write(frame.tobytes())
        t0 += dur
    ff.stdin.close(); ff.wait()
    print(f"{out} {total:.1f}s")


if __name__ == "__main__":
    main()
