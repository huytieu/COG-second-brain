"""Padded floating-card renderer with animated cursor, ripples, highlights, zoom.
Gradient colors: edit TOP/BOT in make_bg() or set CARD_BG_TOP / CARD_BG_BOT (hex)."""
from PIL import Image, ImageDraw, ImageFilter
import math, os, subprocess

W, H = 1920, 1080
FPS = 30

def make_bg():
    # diagonal soft blue gradient, Xnapper-ish
    def hx(n, d):
        h = (os.environ.get(n) or d).lstrip("#")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    top = hx("CARD_BG_TOP", "4facfe")
    bot = hx("CARD_BG_BOT", "00d2d8")
    bg = Image.new("RGB", (W, H))
    px = bg.load()
    for y in range(H):
        for x in range(0, W, 4):
            t = (x / W * 0.45 + y / H * 0.55)
            r = int(top[0] + (bot[0] - top[0]) * t)
            g = int(top[1] + (bot[1] - top[1]) * t)
            b = int(top[2] + (bot[2] - top[2]) * t)
            for dx in range(4):
                if x + dx < W: px[x + dx, y] = (r, g, b)
    return bg

BG = make_bg()

def rounded_card(img, radius=22, border=2):
    """screenshot -> RGBA card with rounded corners and hairline border"""
    w, h = img.size
    card = img.convert("RGBA")
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, fill=255)
    card.putalpha(mask)
    d2 = ImageDraw.Draw(card)
    d2.rounded_rectangle([0, 0, w - 1, h - 1], radius=radius, outline=(255, 255, 255, 90), width=border)
    return card

def make_shadow(w, h, radius=22, blur=38, alpha=120):
    pad = blur * 2
    sh = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    d.rounded_rectangle([pad, pad, pad + w - 1, pad + h - 1], radius=radius, fill=(10, 30, 50, alpha))
    return sh.filter(ImageFilter.GaussianBlur(blur)), pad

def smoothstep(a, b, t):
    t = max(0.0, min(1.0, (t - a) / (b - a))) if b > a else 1.0
    return t * t * (3 - 2 * t)

CURSOR_PTS = [(0,0),(0,16.5),(3.9,13.2),(6.3,19.2),(8.7,18.2),(6.3,12.2),(11.4,12.2)]
def draw_cursor(draw, x, y, scale=2.0):
    pts = [(x + px * scale, y + py * scale) for px, py in CURSOR_PTS]
    draw.polygon(pts, fill=(20, 20, 25, 255), outline=(255, 255, 255, 255))

class Seg:
    """One screenshot segment: waypoints, clicks, highlight, zoom."""
    def __init__(self, shot_path, D, waypoints, clicks, highlights, zoom):
        self.shot = Image.open(shot_path).convert("RGB")
        self.D = D
        self.wps = waypoints      # [(t, x, y)] screenshot coords
        self.clicks = clicks      # [t]
        self.hls = highlights     # [(t0, t1, rect)]
        self.zoom = zoom          # (t0, t1, t2, t3, zmax, anchor)
        self.card = rounded_card(self.shot)

    def cursor_at(self, t):
        wps = self.wps
        if t <= wps[0][0]: return wps[0][1], wps[0][2]
        for i in range(len(wps) - 1):
            t0, x0, y0 = wps[i]; t1, x1, y1 = wps[i + 1]
            if t0 <= t <= t1:
                u = smoothstep(t0, t1, t)
                return x0 + (x1 - x0) * u, y0 + (y1 - y0) * u
        return wps[-1][1], wps[-1][2]

    def transform(self, t):
        sw, sh_ = self.shot.size
        k0 = (W * 0.86) / sw
        z = 1.0
        u = 0.0
        if self.zoom:
            t0, t1, t2, t3, zmax, anchor = self.zoom
            if t < t0: z = 1.0
            elif t < t1: z = 1 + (zmax - 1) * smoothstep(t0, t1, t)
            elif t < t2: z = zmax
            elif t < t3: z = zmax - (zmax - 1) * smoothstep(t2, t3, t)
            else: z = 1.0
            u = (z - 1) / (zmax - 1) if zmax > 1 else 0
        else:
            anchor = (sw / 2, sh_ / 2)
        k = k0 * z
        float_y = 5 * math.sin(2 * math.pi * t / self.D * 2)
        off0 = ((W - k0 * sw) / 2, (H - k0 * sh_) / 2 + float_y)
        offz = (W / 2 - k * anchor[0], H / 2 - k * anchor[1])
        off = (off0[0] * (1 - u) + offz[0] * u, off0[1] * (1 - u) + offz[1] * u)
        return k, off

    def frame(self, t):
        img = BG.copy()
        k, off = self.transform(t)
        sw, sh_ = self.shot.size
        cw, ch = int(sw * k), int(sh_ * k)
        card = self.card.resize((cw, ch), Image.BILINEAR)
        shadow, pad = make_shadow(cw, ch, blur=30)
        img.paste(shadow, (int(off[0]) - pad, int(off[1]) - pad + 14), shadow)
        img.paste(card, (int(off[0]), int(off[1])), card)
        ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(ov)
        # highlights
        for (h0, h1, rect) in self.hls:
            if h0 <= t <= h1:
                a = smoothstep(h0, h0 + 0.4, t) * (1 - smoothstep(h1 - 0.4, h1, t))
                pulse = 0.75 + 0.25 * math.sin(2 * math.pi * (t - h0) * 1.6)
                alpha = int(230 * a * pulse)
                r = [off[0] + rect[0] * k, off[1] + rect[1] * k, off[0] + rect[2] * k, off[1] + rect[3] * k]
                d.rounded_rectangle(r, radius=8, outline=(255, 90, 80, alpha), width=4)
        # click ripples
        cx, cy = self.cursor_at(t)
        px, py = off[0] + cx * k, off[1] + cy * k
        for ct in self.clicks:
            if ct <= t <= ct + 0.8:
                u = (t - ct) / 0.8
                rr = 10 + 42 * u
                alpha = int(220 * (1 - u))
                cxs, cys = self.cursor_at(ct)
                pxs, pys = off[0] + cxs * k, off[1] + cys * k
                d.ellipse([pxs - rr, pys - rr, pxs + rr, pys + rr], outline=(255, 255, 255, alpha), width=5)
        draw_cursor(d, px, py)
        img = Image.alpha_composite(img.convert("RGBA"), ov)
        return img.convert("RGB")

def render(seg, out):
    n = int(seg.D * FPS)
    p = subprocess.Popen(
        ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
         "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-pix_fmt", "yuv420p", out],
        stdin=subprocess.PIPE)
    for i in range(n):
        p.stdin.write(seg.frame(i / FPS).tobytes())
    p.stdin.close(); p.wait()
    assert p.returncode == 0, out
