#!/usr/bin/env python3
"""Animated opening title, 4.2s @30fps 1920x1080, channel template.
Lanes draw in -> headline fades word by word -> chip + avatar + signature -> fade out.
Pipes RGB24 frames to ffmpeg.

Usage: python3 ytopen.py [out.mp4]
Env (all optional): AVATAR_PATH, BRAND_URL, ACCENT (hex), HEADLINE_FONT, MONO_FONT,
OPEN_EYEBROW, OPEN_CHIP. Edit HEAD below for the headline."""
from PIL import Image, ImageDraw, ImageFont
import subprocess, math, os, sys

def _first(*paths):
    for p in paths:
        if p and os.path.exists(p):
            return p
    raise SystemExit("No font found: set HEADLINE_FONT / MONO_FONT to a .ttf or .ttc path")


HN = _first(os.environ.get("HEADLINE_FONT"), "/System/Library/Fonts/HelveticaNeue.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
MEN = _first(os.environ.get("MONO_FONT"), "/System/Library/Fonts/Menlo.ttc",
             "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")


def _f(path, size, idx=0):
    return ImageFont.truetype(path, size, index=idx) if path.endswith(".ttc") else ImageFont.truetype(path, size)


def _hex(name, default):
    h = (os.environ.get(name) or default).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


BRAND_URL = os.environ.get("BRAND_URL", "yourblog.example")
AVATAR = os.environ.get("AVATAR_PATH", "")   # optional: PNG with white background

W, H = 1920, 1080
FPS = 30
DUR = 4.2
N = int(DUR * FPS)
BG = (10, 11, 13)
LINE = (67, 70, 76)
NODE = (154, 157, 162)
TXT = (245, 246, 247)
MUT = (150, 155, 163)
GREEN = (61, 214, 140)
RED = (242, 85, 90)
CORAL = _hex("ACCENT", "D97757")

f_eyebrow = _f(MEN, 26)
f_big = _f(HN, 96, 1)
f_chip = _f(MEN, 32)
f_sig = _f(MEN, 30, 1)

# avatar keyed (optional)
av = None
if AVATAR and os.path.exists(AVATAR):
    av = Image.open(AVATAR).convert("RGBA")
    px = av.load()
    for yy in range(av.height):
        for xx in range(av.width):
            r, g, b, a = px[xx, yy]
            if r > 235 and g > 235 and b > 235:
                px[xx, yy] = (r, g, b, 0)
    av = av.resize((640, 640), Image.NEAREST)

LANES = [(170 + i * 130) for i in range(7)]
STS = ["pass", "pass", "fail", "pass", "fail", "pass", "pass"]
X0, X1 = 1150, 1850

HEAD = [("How I test", None), ("my product", None), ("with an AI agent", "AI")]


def ease(t):
    return 0 if t <= 0 else 1 if t >= 1 else (1 - math.cos(math.pi * t)) / 2


def frame(i):
    t = i / FPS
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # 1) lanes draw 0.0-1.2
    lp = ease(t / 1.2)
    for li, y in enumerate(LANES):
        stagger = ease((t - li * 0.06) / 1.0)
        xe = X0 + (X1 - X0) * stagger
        if xe <= X0:
            continue
        if STS[li] == "fail":
            x = X0
            while x < xe:
                d.line([(x, y), (min(x + 10, xe), y)], fill=LINE, width=3)
                x += 24
        else:
            d.line([(X0, y), (xe, y)], fill=LINE, width=3)
        d.ellipse([X0 - 7, y - 7, X0 + 7, y + 7], fill=NODE)
        if stagger >= 0.999:
            c = GREEN if STS[li] == "pass" else RED
            d.ellipse([X1 - 9, y - 9, X1 + 9, y + 9], fill=c)
    # avatar fades/rises 1.6-2.6
    ap = ease((t - 1.6) / 1.0)
    if ap > 0 and av is not None:
        yoff = int(40 * (1 - ap))
        a2 = av.copy()
        if ap < 1:
            alpha = a2.getchannel("A").point(lambda v: int(v * ap))
            a2.putalpha(alpha)
        img.paste(a2, (1180, H - 660 + yoff), a2)
        d = ImageDraw.Draw(img)
    # eyebrow 0.6
    ep = ease((t - 0.6) / 0.5)
    if ep > 0:
        d.text((110, 200), os.environ.get("OPEN_EYEBROW", "AGENTIC DOGFOODING"),
               font=f_eyebrow, fill=(int(MUT[0]*ep), int(MUT[1]*ep), int(MUT[2]*ep)))
    # headline lines fade 0.9 / 1.2 / 1.5
    for k, (ln, accent) in enumerate(HEAD):
        p = ease((t - (0.9 + k * 0.3)) / 0.5)
        if p <= 0:
            continue
        x = 106
        y = 280 + k * 118
        for word in ln.split(" "):
            base = CORAL if word == accent else TXT
            col = tuple(int(c * p) for c in base)
            d.text((x, y), word, font=f_big, fill=col)
            x += d.textlength(word + " ", font=f_big)
    # chip 2.2
    cp = ease((t - 2.2) / 0.5)
    if cp > 0:
        cy = 680
        d.ellipse([116, cy + 10, 132, cy + 26], fill=tuple(int(c * cp) for c in GREEN))
        d.text((150, cy), os.environ.get("OPEN_CHIP", "134 cases designed · run · graded · filed back"),
               font=f_chip, fill=tuple(int(c * cp) for c in MUT))
    # signature 2.6
    sp = ease((t - 2.6) / 0.5)
    if sp > 0:
        sx, sy = 110, H - 120
        d.text((sx, sy), BRAND_URL, font=f_sig, fill=tuple(int(c * sp) for c in (210, 213, 218)))
        w = d.textlength(BRAND_URL, font=f_sig)
        # blinking cursor
        if int(t * 2) % 2 == 0:
            d.rectangle([sx + w + 10, sy + 2, sx + w + 26, sy + 34], fill=tuple(int(c * sp) for c in GREEN))
    # fade out last 0.5s
    if t > DUR - 0.5:
        f = (t - (DUR - 0.5)) / 0.5
        img = Image.eval(img, lambda v: int(v * (1 - f)))
    return img


OUT = sys.argv[1] if len(sys.argv) > 1 else "opening.mp4"
proc = subprocess.Popen([
    "ffmpeg", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
    "-r", str(FPS), "-i", "-",
    "-c:v", "libx264", "-crf", "19", "-pix_fmt", "yuv420p",
    OUT
], stdin=subprocess.PIPE)
for i in range(N):
    proc.stdin.write(frame(i).tobytes())
proc.stdin.close()
proc.wait()
print("done", OUT)
