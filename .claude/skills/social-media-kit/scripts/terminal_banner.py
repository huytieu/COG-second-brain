#!/usr/bin/env python3
"""Terminal/GitHub-README-style banner generator (dark panel + one accent color).

Produces a 5:2 (1500x600) PNG that looks like a terminal window: titlebar with
traffic-light dots, a prompt line, a big mono wordmark with a coral block
cursor, status lines on the left, feature list on the right, url + cursor
bottom-right. Good as an X Article cover when a raw app screenshot looks bad.
Adapt the CONFIG block per product; keep the layout.

Usage: python3 terminal_banner.py <out.png>
Env: BANNER_ACCENT (hex, default e13f5e), BANNER_URL, MONO_FONT (path)
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont

# CONFIG, edit per product
TITLE = "myapp - the deck your agents work on"
PROMPT = "myapp start"
WORD_A, WORD_B = "My", "App"          # white part, accent part
STATUS = [
    ("green", "●", "agent 1  coding      src/search.ts:42"),
    ("amber", "●", 'agent 2  needs you   "ship the fix?"'),
    ("green", "●", "agent 3  docs        report.md"),
    ("muted", "○", "agent 4  idle        done · 2m ago"),
]
FEATURES = ["click any path -> rendered", "tweak UI -> send to agent",
            "wiki · grid · canvas", "self-hosted · MIT"]
URL = os.environ.get("BANNER_URL", "myapp.example.com")

W, H = 1500, 600
C = {"bg": "#161616", "panel": "#1e1e1e", "border": "#3d3d3d", "fg": "#dadada",
     "muted": "#9b9b9b", "coral": "#" + os.environ.get("BANNER_ACCENT", "e13f5e").lstrip("#"), "green": "#4ec9a0", "amber": "#e5b567"}

def font(size, bold=False):
    p = os.environ.get("MONO_FONT")
    if p and os.path.exists(p):
        return ImageFont.truetype(p, size)
    if os.path.exists("/System/Library/Fonts/Menlo.ttc"):
        return ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", size, index=1 if bold else 0)
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono%s.ttf" % ("-Bold" if bold else ""), size)

def main(out):
    img = Image.new("RGB", (W, H), C["bg"])
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = 70, 60, W - 70, H - 60
    d.rounded_rectangle([x0, y0, x1, y1], radius=16, fill=C["panel"], outline=C["border"], width=2)
    d.rounded_rectangle([x0, y0, x1, y0 + 52], radius=16, fill="#282828")
    d.rectangle([x0, y0 + 30, x1, y0 + 52], fill="#282828")
    d.line([x0, y0 + 52, x1, y0 + 52], fill=C["border"], width=2)
    for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]):
        d.ellipse([x0 + 24 + i * 30, y0 + 18, x0 + 40 + i * 30, y0 + 34], fill=c)
    d.text(((x0 + x1) // 2, y0 + 26), TITLE, font=font(17), fill=C["muted"], anchor="mm")

    big, mono, sm = font(92, True), font(24), font(20)
    d.text((x0 + 48, y0 + 100), "$", font=mono, fill=C["green"])
    d.text((x0 + 78, y0 + 100), PROMPT, font=mono, fill=C["fg"])
    d.text((x0 + 44, y0 + 150), WORD_A, font=big, fill="#ffffff")
    wa = d.textlength(WORD_A, font=big)
    d.text((x0 + 44 + wa, y0 + 150), WORD_B, font=big, fill=C["coral"])
    cx = x0 + 44 + wa + d.textlength(WORD_B, font=big) + 18
    d.rectangle([cx, y0 + 168, cx + 40, y0 + 248], fill=C["coral"])

    ys = y0 + 300
    for col, dot, txt in STATUS:
        d.text((x0 + 48, ys), dot, font=mono, fill=C[col])
        d.text((x0 + 84, ys), txt, font=mono, fill=C["fg"] if col != "muted" else C["muted"])
        ys += 38
    fy = y0 + 300
    for f in FEATURES:
        d.text((x1 - 48, fy), f, font=sm, fill=C["muted"], anchor="ra")
        fy += 34
    d.text((x1 - 48, y1 - 36), URL, font=sm, fill=C["coral"], anchor="rm")
    d.rectangle([x1 - 44, y1 - 46, x1 - 36, y1 - 26], fill=C["coral"])
    img.save(out, optimize=True)
    print("saved", out)

if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "banner.png")
