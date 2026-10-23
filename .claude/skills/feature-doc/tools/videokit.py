#!/usr/bin/env python3
"""
videokit.py: edit a screenrec capture into a polished, public-ready video.

Reads a screenrec manifest (frames + per-action events with cursor coords/captions)
and composites, at OUTFPS, onto a branded 1920x1080 stage:
  - branded gradient background
  - the captured content in a rounded "browser card" with a fake chrome bar
  - a synthetic animated cursor that glides (ease-in-out) to each click, with a
    click-pulse ring at the action moment
  - caption lower-thirds per action (fade in/out)
  - intro + outro title cards, with short crossfades and fade in/out
Encodes to mp4 (h264, yuv420p) via ffmpeg.

Usage (plain python3, no browser needed):
  VK_MANIFEST=/path/out.manifest.json VK_OUT=/path/demo.mp4 \
  VK_TITLE="Connect your apps" VK_SUBTITLE="Bring your tools into the assistant" \
  VK_OUTRO_TITLE="Try it today" VK_LOGO="YourProduct" \
  python3 videokit.py
"""
import os, json, glob, math, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def find_ffmpeg():
    for p in (shutil.which("ffmpeg"), "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if p and os.path.exists(p): return p
    return None
FFMPEG = find_ffmpeg()

MAN   = json.load(open(os.environ["VK_MANIFEST"]))
OUT   = os.environ["VK_OUT"]
TITLE = os.environ.get("VK_TITLE", "Feature demo")
SUB   = os.environ.get("VK_SUBTITLE", "")
OTITLE= os.environ.get("VK_OUTRO_TITLE", TITLE)
OSUB  = os.environ.get("VK_OUTRO_SUB", "")
LOGO  = os.environ.get("VK_LOGO", "YourProduct")
BRAND = os.environ.get("VK_BRAND", "#3b6fd4")
OUTFPS= int(os.environ.get("VK_OUTFPS", "24"))
W, H  = 1920, 1080

def hex2rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
BR = hex2rgb(BRAND)
def mix(a, b, t): return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
INK = (17, 22, 28); BG0 = (11, 15, 19); BG1 = mix(BG0, BR, 0.28)

def font(sz, bold=True):
    cands = (["/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/HelveticaNeue.ttc",
              "/Library/Fonts/Arial Bold.ttf"] if bold else
             ["/System/Library/Fonts/Supplemental/Arial.ttf",
              "/System/Library/Fonts/HelveticaNeue.ttc"])
    for p in cands:
        try: return ImageFont.truetype(p, sz)
        except Exception: continue
    return ImageFont.load_default()

F_TITLE, F_SUB, F_CAP, F_LOGO = font(78), font(36, False), font(34), font(28)

def gradient_bg():
    bg = Image.new("RGB", (W, H), BG0)
    top = Image.new("RGB", (W, H))
    px = top.load()
    for y in range(H):
        c = mix(BG1, BG0, y / H)
        for x in range(0, W, 1): px[x, y] = c
    # radial brand glow top-left
    glow = Image.new("L", (W, H), 0); gd = ImageDraw.Draw(glow)
    gd.ellipse([-400, -500, 900, 700], fill=90)
    glow = glow.filter(ImageFilter.GaussianBlur(180))
    brand_layer = Image.new("RGB", (W, H), BR)
    return Image.composite(brand_layer, top, glow)

BG = gradient_bg()

def rounded(im, rad):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0], im.size[1]], rad, fill=255)
    out = im.convert("RGBA"); out.putalpha(m); return out

def center_text(d, cx, y, text, f, fill, anchor="mm"):
    d.text((cx, y), text, font=f, fill=fill, anchor=anchor)

# ---- content card geometry --------------------------------------------------
frames = sorted(glob.glob(os.path.join(MAN["frames_dir"], "*.jpg")))
c0 = Image.open(frames[0]); iw, ih = c0.size
CARD_W = 1580
CHROME = 46
scale = CARD_W / iw
CARD_H = int(ih * scale)
CX = (W - CARD_W) // 2
CY = 150
dpr = MAN["img_w"] / max(MAN["css_w"], 1)  # device px per css px

def content_to_stage(cx_css, cy_css):
    ix, iy = cx_css * dpr, cy_css * dpr           # css -> image px
    return CX + ix * scale, CY + CHROME + iy * scale

# precompute cursor keyframes from events that have coords
kf = [(e["t"], *content_to_stage(e["x"], e["y"])) for e in MAN["events"] if e.get("x") is not None]
def ease(t): return t * t * (3 - 2 * t)
def cursor_at(tf):
    if not kf: return None
    if tf <= kf[0][0]: return kf[0][1], kf[0][2]
    for i in range(len(kf) - 1):
        t0, x0, y0 = kf[i]; t1, x1, y1 = kf[i + 1]
        if t0 <= tf <= t1:
            a = ease((tf - t0) / max(t1 - t0, 1e-3))
            return x0 + (x1 - x0) * a, y0 + (y1 - y0) * a
    return kf[-1][1], kf[-1][2]

def draw_cursor(layer, x, y):
    d = ImageDraw.Draw(layer)
    p = [(x, y), (x, y + 34), (x + 9, y + 25), (x + 15, y + 38), (x + 21, y + 35), (x + 15, y + 22), (x + 26, y + 22)]
    d.polygon(p, fill=(255, 255, 255), outline=(20, 20, 20))
def draw_pulse(layer, x, y, prog):  # prog 0..1
    d = ImageDraw.Draw(layer); r = int(12 + prog * 42); a = int(180 * (1 - prog))
    d.ellipse([x - r, y - r, x + r, y + r], outline=BR + (a,), width=5)

def draw_chrome(canvas):
    d = ImageDraw.Draw(canvas)
    bar = Image.new("RGBA", (CARD_W, CHROME), (245, 246, 248, 255))
    bd = ImageDraw.Draw(bar)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        bd.ellipse([16 + i * 22, CHROME // 2 - 6, 28 + i * 22, CHROME // 2 + 6], fill=col)
    bd.rounded_rectangle([90, 10, CARD_W - 20, CHROME - 10], 9, fill=(255, 255, 255))
    bd.text((104, CHROME // 2), "app.example.com", font=F_LOGO, fill=(120, 128, 138), anchor="lm")
    canvas.paste(rounded(bar, 12), (CX, CY), rounded(bar, 12))

def caption_for(tf):
    for e in MAN["events"]:
        if e.get("caption") and e["t"] <= tf <= e["t"] + 2.6:
            k = min(1.0, (tf - e["t"]) / 0.3, (e["t"] + 2.6 - tf) / 0.3)
            return e["caption"], max(0.0, k)
    return None, 0

def draw_caption(canvas, text, alpha):
    tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(tmp)
    bb = d.textbbox((0, 0), text, font=F_CAP); tw = bb[2] - bb[0]
    pw, ph = tw + 64, 74; x0 = (W - pw) // 2; y0 = 980
    d.rounded_rectangle([x0, y0, x0 + pw, y0 + ph], 20, fill=(12, 16, 20, 235))
    d.rounded_rectangle([x0, y0, x0 + 6, y0 + ph], 20, fill=BR + (255,))
    d.text((W // 2, y0 + ph // 2), text, font=F_CAP, fill=(255, 255, 255, 255), anchor="mm")
    if alpha < 1: tmp.putalpha(tmp.getchannel("A").point(lambda a: int(a * alpha)))
    canvas.alpha_composite(tmp)

# ---- frame renderers --------------------------------------------------------
def card_frame(tf):
    canvas = BG.convert("RGBA").copy()
    idx = min(len(frames) - 1, int(tf * MAN["fps"]))
    content = Image.open(frames[idx]).convert("RGB").resize((CARD_W, CARD_H))
    # shadow
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([CX - 6, CY - 6, CX + CARD_W + 6, CY + CHROME + CARD_H + 6], 22, fill=(0, 0, 0, 150))
    canvas.alpha_composite(sh.filter(ImageFilter.GaussianBlur(24)))
    draw_chrome(canvas)
    canvas.paste(rounded(content, 12), (CX, CY + CHROME), rounded(content, 12))
    center_text(ImageDraw.Draw(canvas), W // 2, 74, TITLE, font(46), (255, 255, 255, 255))
    # cursor + pulse
    cur = cursor_at(tf)
    if cur:
        lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        for e in MAN["events"]:
            if e.get("x") is not None and 0 <= tf - e["t"] <= 0.45:
                sx, sy = content_to_stage(e["x"], e["y"]); draw_pulse(lay, sx, sy, (tf - e["t"]) / 0.45)
        draw_cursor(lay, cur[0], cur[1]); canvas.alpha_composite(lay)
    cap, al = caption_for(tf)
    if cap: draw_caption(canvas, cap, al)
    d = ImageDraw.Draw(canvas); center_text(d, W - 130, H - 40, LOGO, F_LOGO, (255, 255, 255, 180))
    return canvas.convert("RGB")

def title_card(title, sub, badge="DEMO"):
    canvas = BG.convert("RGBA").copy(); d = ImageDraw.Draw(canvas)
    d.rounded_rectangle([W // 2 - 70, 372, W // 2 + 70, 420], 24, fill=BR + (255,))
    center_text(d, W // 2, 396, badge, F_LOGO, (255, 255, 255, 255))
    center_text(d, W // 2, 500, title, F_TITLE, (255, 255, 255, 255))
    if sub: center_text(d, W // 2, 585, sub, F_SUB, (200, 210, 218, 255))
    center_text(d, W // 2, H - 70, LOGO, F_LOGO, (255, 255, 255, 190))
    return canvas.convert("RGB")

# ---- assemble output frames -------------------------------------------------
TMP = OUT + ".render"
if os.path.isdir(TMP): shutil.rmtree(TMP)
os.makedirs(TMP)
seq = []
INTRO, OUTRO = 1.7, 1.9
flow_dur = MAN["duration"]
def hold(img, secs):
    return [img] * max(1, int(secs * OUTFPS))
# intro (with text fade-in), flow, outro
intro_frames = []
ni = int(INTRO * OUTFPS)
base_intro = title_card(TITLE, SUB, "DEMO")
for i in range(ni):
    a = min(1.0, i / (0.4 * OUTFPS))
    fr = Image.blend(BG.convert("RGB"), base_intro, a) if a < 1 else base_intro
    intro_frames.append(fr)
flow_frames = [card_frame(i / OUTFPS) for i in range(int(flow_dur * OUTFPS))]
outro_frames = hold(title_card(OTITLE, OSUB, "TRY IT"), OUTRO)

def crossfade(a, b, n):
    n = min(n, len(a), len(b))
    if n <= 0: return a + b
    mid = [Image.blend(a[-n + i], b[i], (i + 1) / (n + 1)) for i in range(n)]
    return a[:-n] + mid + b[n:]

seq = crossfade(intro_frames, flow_frames, int(0.3 * OUTFPS))
seq = crossfade(seq, outro_frames, int(0.3 * OUTFPS))
# fade in/out to black
fn = int(0.3 * OUTFPS)
for i in range(fn):
    seq[i] = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), seq[i], (i + 1) / fn)
    seq[-1 - i] = Image.blend(Image.new("RGB", (W, H), (0, 0, 0)), seq[-1 - i], (i + 1) / fn)

for i, fr in enumerate(seq):
    fr.save(os.path.join(TMP, f"{i:05d}.jpg"), quality=90)
print(f"rendered {len(seq)} output frames @ {OUTFPS}fps ({len(seq)/OUTFPS:.1f}s)")

if not FFMPEG:
    print("ffmpeg missing: frames at", TMP, "(run: brew install ffmpeg)"); raise SystemExit
r = subprocess.run([FFMPEG, "-y", "-framerate", str(OUTFPS), "-i", os.path.join(TMP, "%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                    "-crf", "20", OUT], capture_output=True, text=True)
if r.returncode != 0:
    print("ffmpeg failed:", r.stderr[-500:]); raise SystemExit(1)
shutil.rmtree(TMP)
print("POLISHED_OUT:", OUT)
