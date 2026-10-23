#!/usr/bin/env python3
"""YouTube thumbnail, channel template.

Template = dark lane-art bg + huge bold headline with one accent word
+ your avatar (right, optional) + data chip + signature.
Playlist consistency: same layout, vary headline/accent/lane pattern only.

Env (all optional): AVATAR_PATH, BRAND_URL, ACCENT (hex, default D97757),
HEADLINE_FONT, MONO_FONT.
Usage: python3 ytthumb.py "MY AI TESTS|MY PRODUCT." AI "7 passed · 4 failed" out.png
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os, sys

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

W, H = 2560, 1440  # 2x of 1280x720
BG = (10, 11, 13)
LINE = (67, 70, 76)
NODE = (154, 157, 162)
TXT = (245, 246, 247)
MUT = (150, 155, 163)
GREEN = (61, 214, 140)
RED = (242, 85, 90)
CORAL = _hex("ACCENT", "D97757")   # one accent word color, configurable

f_big = _f(HN, 210, 1)
f_chip = _f(MEN, 54)
f_sig = _f(MEN, 44, 1)


def lane_field(d, x0, x1, ys, statuses, circles=()):
    circ = list(circles)
    for i, y in enumerate(ys):
        dash = None if statuses[i] != "fail" else (14, 18)
        # simple straight lanes with optional circle break
        brk = next(((cx, r) for cx, li, r in circ if li == i), None)
        segs = [(x0, x1)] if not brk else [(x0, brk[0]-brk[1]-6), (brk[0]+brk[1]+6, x1)]
        for (a, b) in segs:
            if dash:
                x = a
                while x < b:
                    d.line([(x, y), (min(x+14, b), y)], fill=LINE, width=4)
                    x += 32
            else:
                d.line([(a, y), (b, y)], fill=LINE, width=4)
        d.ellipse([x0-9, y-9, x0+9, y+9], fill=NODE)
        endc = GREEN if statuses[i] == "pass" else RED if statuses[i] == "fail" else NODE
        d.ellipse([x1-12, y-12, x1+12, y+12], fill=endc)
    for cx, li, r in circ:
        y = ys[li]
        d.ellipse([cx-r, y-r, cx+r, y+r], outline=LINE, width=4)
        d.ellipse([cx-r-8, y-8, cx-r+8, y+8], fill=NODE)
        d.ellipse([cx+r-8, y-8, cx+r+8, y+8], fill=NODE)


def avatar_cut(size):
    """avatar, near-white keyed to transparent. Returns None if no AVATAR_PATH."""
    if not AVATAR or not os.path.exists(AVATAR):
        return None
    im = Image.open(AVATAR).convert("RGBA")
    px = im.load()
    w, h = im.size
    for yy in range(h):
        for xx in range(w):
            r, g, b, a = px[xx, yy]
            if r > 235 and g > 235 and b > 235:
                px[xx, yy] = (r, g, b, 0)
    return im.resize((size, size), Image.NEAREST)


def signature(d, x, y):
    t = BRAND_URL
    d.text((x, y), t, font=f_sig, fill=(210, 213, 218))
    w = d.textlength(t, font=f_sig)
    d.rectangle([x + w + 16, y + 4, x + w + 40, y + 52], fill=GREEN)


def thumb(headline_lines, accent_word, chip_txt, out):
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    # lane art behind avatar zone, right third
    ys = [200 + i * 180 for i in range(7)]
    lane_field(d, 1490, 2450, ys,
               ["pass", "pass", "fail", "pass", "fail", "pass", "pass"],
               circles=[(1900, 3, 120)])
    # avatar on right, sitting on the lanes
    av = avatar_cut(1120)
    if av:
        img.paste(av, (W - 1150, H - 1140), av)
    d = ImageDraw.Draw(img)
    # headline top-left, accent word colored
    y = 150
    for ln in headline_lines:
        x = 110
        for word in ln.split(" "):
            col = CORAL if word.strip(".") == accent_word else TXT
            d.text((x, y), word, font=f_big, fill=col)
            x += d.textlength(word + " ", font=f_big)
        y += 232
    # chip
    cy = y + 60
    d.ellipse([122, cy+18, 146, cy+42], fill=GREEN)
    d.text((170, cy), chip_txt, font=f_chip, fill=MUT)
    signature(d, 110, H - 130)
    img.resize((1280, 720), Image.LANCZOS).save(out)
    print("saved", out)


if __name__ == "__main__":
    a = sys.argv[1:]
    head = (a[0] if a else "MY AI TESTS|MY PRODUCT.").split("|")
    thumb(head, a[1] if len(a) > 1 else "AI",
          a[2] if len(a) > 2 else "7 passed · 4 failed · every failure filed",
          a[3] if len(a) > 3 else "yt-thumb.png")
