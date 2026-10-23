#!/usr/bin/env python3
"""Social cards in a dark thin-line "lane field" art language.

Configuration (environment variables, all optional):
  BRAND_URL      signature text bottom-right (default "yourblog.example")
  CARD_OUT_DIR   output folder (default ".")
  CARD_SCREENSHOT  path to a screenshot for the runner card (card skipped if unset)
  HEADLINE_FONT / MONO_FONT  paths to .ttf/.ttc files (macOS defaults used if present)
  CARD_ACCENT_PASS / CARD_ACCENT_FAIL  hex colors for the pass/fail dots

Inspired by the line-art cards on linear.app/now.

Verified against Linear's real OG art (linear-og.png):
bg #0A0B0D, thin gray strokes, dashed alt-paths, lines flow around circle
nodes with small dots at the break points, arrowheads at line ends.
Text: Helvetica Neue Bold headline, Menlo only for eyebrow/signature.
Render at 2x, downscale for AA.
"""
from PIL import Image, ImageDraw, ImageFont
import math, os


def _hex(h, default):
    h = (os.environ.get(h) or default).lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

W, H = 3200, 1800  # 2x
BG = (10, 11, 13)
LINE = (67, 70, 76)        # stroke gray
NODE = (154, 157, 162)     # dots/arrowheads
TXT = (242, 243, 244)
MUT = (138, 143, 152)
GREEN = _hex("CARD_ACCENT_PASS", "3DD68C")
RED = _hex("CARD_ACCENT_FAIL", "F2555A")
BRAND_URL = os.environ.get("BRAND_URL", "yourblog.example")
OUT_DIR = os.environ.get("CARD_OUT_DIR", ".")

def _first(*paths):
    for p in paths:
        if p and os.path.exists(p):
            return p
    raise SystemExit("No font found: set HEADLINE_FONT / MONO_FONT to a .ttf or .ttc path")


HN = _first(os.environ.get("HEADLINE_FONT"), "/System/Library/Fonts/HelveticaNeue.ttc",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf")
MEN = _first(os.environ.get("MONO_FONT"), "/System/Library/Fonts/Menlo.ttc",
             "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf")
_TTC = HN.endswith(".ttc")
_MTC = MEN.endswith(".ttc")


def _f(path, size, idx, ttc):
    return ImageFont.truetype(path, size, index=idx) if ttc else ImageFont.truetype(path, size)
f_head = _f(HN, 124, 1, _TTC)   # Bold
f_head_s = _f(HN, 104, 1, _TTC)
f_chip = _f(MEN, 42, 0, _MTC)            # mono chips (has arrows)
f_eyebrow = _f(MEN, 34, 0, _MTC)
f_sig = _f(MEN, 38, 1, _MTC)    # Menlo Bold
f_sig_dim = _f(MEN, 38, 0, _MTC)
f_quote = _f(HN, 150, 1, _TTC)
f_attr = _f(HN, 48, 10 if _TTC else 0, _TTC)


def rounded_line(d, pts, fill, width, dash=None):
    """polyline from float points; dash = (on, off) in px."""
    if dash is None:
        d.line(pts, fill=fill, width=width, joint="curve")
        return
    on, off = dash
    acc, drawing, seg_start = 0.0, True, pts[0]
    for i in range(1, len(pts)):
        x0, y0 = pts[i - 1]; x1, y1 = pts[i]
        seg = math.hypot(x1 - x0, y1 - y0)
        t = 0.0
        while t < seg:
            step = min((on if drawing else off) - acc, seg - t)
            nt = t + step
            xa, ya = x0 + (x1 - x0) * t / seg, y0 + (y1 - y0) * t / seg
            xb, yb = x0 + (x1 - x0) * nt / seg, y0 + (y1 - y0) * nt / seg
            if drawing:
                d.line([(xa, ya), (xb, yb)], fill=fill, width=width)
            acc += step
            if acc >= (on if drawing else off) - 0.01:
                acc, drawing = 0.0, not drawing
            t = nt


def lane_points(x0, x1, y, bulges):
    """horizontal lane with smooth vertical bulges.
    bulges: list of (cx, radius, amount): lane bends by `amount` at cx."""
    pts = []
    x = x0
    while x <= x1:
        dy = 0.0
        for cx, r, amt in bulges:
            u = (x - cx) / r
            if abs(u) < 2.2:
                dy += amt * math.exp(-u * u * 1.6)
        pts.append((x, y + dy))
        x += 6
    return pts


def arrowhead(d, x, y, col=NODE, s=13):
    d.polygon([(x, y), (x - s * 1.5, y - s * 0.85), (x - s * 1.5, y + s * 0.85)], fill=col)


def dot(d, x, y, col=NODE, r=7):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)


def circle_node(d, cx, cy, r, width=3):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=LINE, width=width)
    dot(d, cx - r, cy); dot(d, cx + r, cy)


def draw_lane_field(d, x0, x1, lanes, circles, statuses):
    """lanes: list of y. circles: list of (cx, cy_lane_idx, r).
    statuses: per-lane 'pass'|'fail'|None → end accent."""
    circ = [(cx, lanes[li], r) for cx, li, r in circles]
    for i, y in enumerate(lanes):
        bulges = []
        on_circle = None
        for cx, cy, r in circ:
            dyl = y - cy
            if abs(dyl) < 2:            # lane passes THROUGH this circle
                on_circle = (cx, cy, r)
            elif abs(dyl) < r + 60:      # neighbour: bulge away
                sgn = 1 if dyl > 0 else -1
                amt = sgn * (r + 34 - abs(dyl)) * 0.62
                if (r + 34 - abs(dyl)) > 0:
                    bulges.append((cx, r * 1.35, amt))
        dash = (10, 14) if statuses[i] == "fail" else None
        if on_circle:
            cx, cy, r = on_circle
            p1 = lane_points(x0, cx - r - 4, y, bulges)
            p2 = lane_points(cx + r + 4, x1, y, bulges)
            rounded_line(d, p1, LINE, 3, dash)
            rounded_line(d, p2, LINE, 3, dash)
        else:
            rounded_line(d, lane_points(x0, x1, y, bulges), LINE, 3, dash)
        dot(d, x0, y)
        if statuses[i] == "pass":
            arrowhead(d, x1 + 16, y); dot(d, x1 - 26, y, GREEN, 9)
        elif statuses[i] == "fail":
            # dashed lane stops short with a red node, no arrow
            dot(d, x1 - 170, y, RED, 9)
        else:
            arrowhead(d, x1 + 16, y)
    for cx, cy, r in circ:
        circle_node(d, cx, cy, r)


def text_block(d, x, y, eyebrow, head_lines, chips, font_head=f_head):
    d.text((x, y), eyebrow, font=f_eyebrow, fill=MUT)
    yy = y + 90
    for ln in head_lines:
        d.text((x, yy), ln, font=font_head, fill=TXT)
        yy += font_head.size + 26
    yy += 40
    for chip_txt, col in chips:
        dot(d, x + 12, yy + 30, col, 10)
        d.text((x + 44, yy), chip_txt, font=f_chip, fill=MUT)
        yy += 86
    return yy


def signature(d, img_w, img_h):
    t = BRAND_URL
    w = d.textlength(t, font=f_sig)
    x = img_w - w - 120 - 34
    y = img_h - 130
    d.text((x, y), t, font=f_sig, fill=(200, 203, 208))
    d.rectangle([x + w + 14, y + 2, x + w + 34, y + 44], fill=GREEN)


def new_canvas():
    img = Image.new("RGB", (W, H), BG)
    return img, ImageDraw.Draw(img)


def save(img, path):
    img.resize((W // 2, H // 2), Image.LANCZOS).save(path)
    print("saved", path)


def out(name):
    os.makedirs(OUT_DIR, exist_ok=True)
    return os.path.join(OUT_DIR, name)


# The three cards below are EXAMPLES. Replace the copy with your own claim,
# real numbers and attribution, then re-run.

# ---------- hero card: 11 lanes through a central circle, 7 pass 4 fail ----
img, d = new_canvas()
lanes = [300 + i * 118 for i in range(11)]
statuses = ["pass", "pass", "fail", "pass", "pass", "fail", "pass", "fail", "pass", "fail", "pass"]
draw_lane_field(d, 1560, 3020, lanes, circles=[(2210, 5, 150), (1840, 1, 84), (2660, 8, 84)], statuses=statuses)
text_block(d, 120, 240,
           "YOUR PRODUCT  x  YOUR TOOL",
           ["One agent runs the", "whole test cycle."],
           [("43 issues -> 134 test cases", NODE),
            ("designed, executed, reported back", NODE)])
signature(d, W, H)
save(img, out("hero-card.png"))

# ---------- runner card: lanes converge into a screenshot ----
shot_path = os.environ.get("CARD_SCREENSHOT")
if shot_path:
    img, d = new_canvas()
    shot = Image.open(shot_path).convert("RGB")
    tw = 1720
    th = int(shot.height * tw / shot.width)
    shot = shot.resize((tw, th), Image.LANCZOS)
    mask = Image.new("L", shot.size, 0)
    md = ImageDraw.Draw(mask)
    md.rounded_rectangle([0, 0, tw - 1, th - 1], radius=20, fill=255)
    px, py = W - tw - 150, (H - th) // 2 + 60
    # short entry stubs leading into the shot (must not cross the text block)
    lanes = [py + 120 + i * ((th - 240) // 6) for i in range(7)]
    sts = ["pass", "pass", "fail", "pass", "fail", "pass", "pass"]
    for i, y in enumerate(lanes):
        dashed = (10, 14) if sts[i] == "fail" else None
        rounded_line(d, lane_points(px - 280, px - 40, y, []), LINE, 3, dashed)
        dot(d, px - 280, y)
        dot(d, px - 40, y, GREEN if sts[i] == "pass" else RED, 9)
    img.paste(shot, (px, py), mask)
    db = ImageDraw.Draw(img)
    db.rounded_rectangle([px, py, px + tw - 1, py + th - 1], radius=20, outline=(48, 51, 56), width=3)
    text_block(db, 120, 200,
               "REAL RUN  ·  REAL VERDICTS",
               ["The AI runner", "grades my own", "work."],
               [("7 passed  ·  4 failed", NODE),
                ("every failure filed as a ticket", NODE)], font_head=f_head_s)
    signature(db, W, H)
    save(img, out("runner-card.png"))

# ---------- quote card ----------
img, d = new_canvas()
lanes = [1330 + i * 90 for i in range(3)]
draw_lane_field(d, 2380, 3020, lanes, circles=[(2680, 1, 90)], statuses=[None, None, None])
d.text((120, 330), "\u201c", font=_f(HN, 300, 1, _TTC), fill=(60, 63, 70))
qy = 560
for ln in ["The failures are", "the product."]:
    d.text((120, qy), ln, font=f_quote, fill=TXT)
    qy += 180
d.text((126, qy + 60), os.environ.get("QUOTE_ATTRIBUTION", "Your Name  ·  your role"), font=f_attr, fill=MUT)
signature(d, W, H)
save(img, out("quote-card.png"))
