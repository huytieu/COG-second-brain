#!/usr/bin/env python3
"""
recompose.py: turn a raw screenrec capture into a clean, house-style walkthrough
video, matching the blog house style: the viewport in a simple browser window
(traffic lights + address pill) on a teal->blue gradient, NO text/captions/cards/
synthetic-cursor. Supports variable speed so long waits are sped up (not cut).

Usage (plain python3; needs ffmpeg at /opt/homebrew/bin/ffmpeg):
  RC_MANIFEST=<base>.manifest.json RC_OUT=out.mp4 \
  RC_SEGMENTS='[[0,8,1],[8,58,8],[58,70,1]]'  # [from_s,to_s,speed]; gaps=speed 1 \
  RC_ADDR="app.example.com" python3 recompose.py

Segments tile source time; anything not covered plays at 1x. Output is 30fps h264.

Opt-in options for sources that are not desktop-shaped (all off by default, so older runs
render the same):
  RC_FIT=1          fit the card inside the frame with RC_MARGIN px (default 40) on each side,
                    instead of a fixed 1680 px width. Needed for phone (portrait) and tall captures.
  RC_CROP=x0,y0,x1,y1  crop every source frame first (source pixels), e.g. a terminal replay's window.
  RC_NOBAR=1        no browser bar: for a capture that already carries its own window chrome.
  RC_SPEED_BADGE=1  show a small "Sped up Nx" pill at the right end of the browser bar while a
                    segment plays faster than 1x, so viewers know the wait was shortened.
  RC_REDACT='[[x0,y0,x1,y1],...]'  pixelate these boxes (source pixels, before RC_CROP) on every
                    frame, e.g. a person's name in a terminal replay.
"""
import os, json, glob, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

MAN = json.load(open(os.environ["RC_MANIFEST"]))
OUT = os.environ["RC_OUT"]
ADDR = os.environ.get("RC_ADDR", "app.example.com")
OUTFPS = int(os.environ.get("RC_OUTFPS", "30"))
SEGS = json.loads(os.environ.get("RC_SEGMENTS", "[]"))  # [[from,to,speed],...]
CLICKS = os.environ.get("RC_CLICKS", "") not in ("", "0", "false")  # opt-in click-pulse highlights
PULSE = float(os.environ.get("RC_PULSE", "0.55"))  # seconds a click ring stays visible
W, H = 1920, 1080
TEAL, BLUE = (34, 193, 214), (43, 119, 206)   # sampled from blog gradient

def find_ffmpeg():
    for p in (shutil.which("ffmpeg"), "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if p and os.path.exists(p): return p
FFMPEG = find_ffmpeg()

def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/HelveticaNeue.ttc"):
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()
F_ADDR = font(22)

def gradient_bg():
    bg = Image.new("RGB", (W, H))
    px = bg.load()
    for y in range(H):
        for x in range(0, W):
            t = (x / W + y / H) / 2
            px[x, y] = tuple(int(TEAL[i] + (BLUE[i] - TEAL[i]) * t) for i in range(3))
    return bg
BG = gradient_bg()

frames = sorted(glob.glob(os.path.join(MAN["frames_dir"], "*.jpg")))
CROP = tuple(int(v) for v in os.environ["RC_CROP"].split(",")) if os.environ.get("RC_CROP") else None
NOBAR = os.environ.get("RC_NOBAR", "") not in ("", "0", "false")
FIT = os.environ.get("RC_FIT", "") not in ("", "0", "false")
SPEED_BADGE = os.environ.get("RC_SPEED_BADGE", "") not in ("", "0", "false")
REDACT = [tuple(int(v) for v in b) for b in json.loads(os.environ.get("RC_REDACT", "[]"))]
c0 = Image.open(frames[0]); iw, ih = c0.size
if CROP: iw, ih = CROP[2] - CROP[0], CROP[3] - CROP[1]
CHROME = 0 if NOBAR else 44
CARD_W = 1680
if FIT:
    margin = int(os.environ.get("RC_MARGIN", "40"))
    CARD_W = int(min(W - 2 * margin, (H - 2 * margin - CHROME) * iw / ih))
scale = CARD_W / iw
CARD_H = int(ih * scale)
CX = (W - CARD_W) // 2
CY = (H - (CARD_H + CHROME)) // 2

def rounded(im, rad):
    m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, im.size[0], im.size[1]], rad, fill=255)
    out = im.convert("RGBA"); out.putalpha(m); return out

# pre-render shadow + chrome bar (static)
SHADOW = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ImageDraw.Draw(SHADOW).rounded_rectangle([CX - 8, CY - 8, CX + CARD_W + 8, CY + CHROME + CARD_H + 8], 20, fill=(0, 0, 0, 120))
SHADOW = SHADOW.filter(ImageFilter.GaussianBlur(26))
BAR_R = None
if not NOBAR:
    BAR = Image.new("RGBA", (CARD_W, CHROME), (246, 247, 249, 255))
    _bd = ImageDraw.Draw(BAR)
    for i, col in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        _bd.ellipse([16 + i * 22, CHROME // 2 - 6, 28 + i * 22, CHROME // 2 + 6], fill=col)
    _bd.rounded_rectangle([92, 9, CARD_W - 20, CHROME - 9], 8, fill=(255, 255, 255))
    _bd.text((108, CHROME // 2), ADDR, font=F_ADDR, fill=(110, 118, 128), anchor="lm")
    BAR_R = rounded(BAR, 10)

# click events (image-pixel space) mapped onto the card, for opt-in pulse highlights
IMG_W = MAN.get("img_w", iw); IMG_H = MAN.get("img_h", ih)
CLICK_EV = [e for e in MAN.get("events", []) if e.get("do", "").startswith("click") and e.get("x") is not None]

def click_at(st):
    """Return (cx, cy, phase 0..1) for a click ring active at source-time st, else None."""
    for e in CLICK_EV:
        dt = st - e["t"]
        if 0 <= dt <= PULSE:
            cx = CX + e["x"] * (CARD_W / IMG_W)
            cy = CY + CHROME + e["y"] * (CARD_H / IMG_H)
            return cx, cy, dt / PULSE
    return None

F_BADGE = font(17)
_BADGES = {}

def badge(speed):
    """Dark pill with "Sped up Nx", cached per speed."""
    if speed not in _BADGES:
        txt = f"Sped up {speed:g}x"
        tw = int(F_BADGE.getlength(txt))
        b = Image.new("RGBA", (tw + 22, CHROME - 18), (0, 0, 0, 0))
        bd = ImageDraw.Draw(b)
        bd.rounded_rectangle([0, 0, b.width - 1, b.height - 1], b.height // 2, fill=(40, 44, 52, 235))
        bd.text((11, b.height // 2), txt, font=F_BADGE, fill=(255, 255, 255), anchor="lm")
        _BADGES[speed] = b
    return _BADGES[speed]

def pixelate(im, box, block=12):
    reg = im.crop(box)
    small = reg.resize((max(1, reg.width // block), max(1, reg.height // block)), Image.BILINEAR)
    im.paste(small.resize(reg.size, Image.NEAREST), box[:2])

def stage(src_idx, st=None, speed=1.0):
    canvas = BG.convert("RGBA").copy()
    canvas.alpha_composite(SHADOW)
    if not NOBAR:
        canvas.paste(BAR_R, (CX, CY), BAR_R)
        if SPEED_BADGE and speed > 1.05:
            b = badge(speed)
            canvas.alpha_composite(b, (CX + CARD_W - 20 - 5 - b.width, CY + (CHROME - b.height) // 2))
    content = Image.open(frames[src_idx]).convert("RGB")
    for box in REDACT: pixelate(content, box)
    if CROP: content = content.crop(CROP)
    content = content.resize((CARD_W, CARD_H), Image.LANCZOS if FIT else Image.BICUBIC)
    cr = rounded(content, 10)
    canvas.paste(cr, (CX, CY + CHROME), cr)
    if CLICKS and st is not None:
        hit = click_at(st)
        if hit:
            cx, cy, ph = hit
            ov = Image.new("RGBA", (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
            # expanding ring (fades out) + steady dot
            r = int(16 + 46 * ph); a = int(200 * (1 - ph))
            od.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(255, 189, 46, a), width=6)
            dot = int(200 * (1 - ph * 0.4))
            od.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], fill=(255, 189, 46, dot))
            canvas.alpha_composite(ov)
    return canvas.convert("RGB")

# ---- build the source-time -> output-frame plan (variable speed) ------------
src_fps = MAN["fps"]; dur = MAN["duration"]
segs = sorted([[float(a), float(b), float(s)] for a, b, s in SEGS], key=lambda x: x[0])
# fill gaps at speed 1
plan = []; cur = 0.0
for a, b, s in segs:
    if a > cur: plan.append([cur, a, 1.0])
    plan.append([a, b, s]); cur = b
if cur < dur: plan.append([cur, dur, 1.0])
if not plan: plan = [[0, dur, 1.0]]

TMP = OUT + ".rc";
if os.path.isdir(TMP): shutil.rmtree(TMP)
os.makedirs(TMP)
oi = 0
for a, b, s in plan:
    n = max(1, round((b - a) / max(s, 0.01) * OUTFPS))
    for i in range(n):
        st = a + (i / n) * (b - a)
        idx = min(len(frames) - 1, max(0, round(st * src_fps)))
        stage(idx, st, s).save(os.path.join(TMP, f"{oi:05d}.jpg"), quality=88); oi += 1
print(f"recomposed {oi} frames @ {OUTFPS}fps ({oi/OUTFPS:.1f}s); plan={[[round(a,1),round(b,1),s] for a,b,s in plan]}")

if not FFMPEG:
    print("no ffmpeg; frames at", TMP); raise SystemExit
r = subprocess.run([FFMPEG, "-y", "-framerate", str(OUTFPS), "-i", os.path.join(TMP, "%05d.jpg"),
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-crf", "20", OUT],
                   capture_output=True, text=True)
if r.returncode != 0: print("ffmpeg failed:", r.stderr[-400:]); raise SystemExit(1)
shutil.rmtree(TMP)
print("RECOMPOSED_OUT:", OUT)
