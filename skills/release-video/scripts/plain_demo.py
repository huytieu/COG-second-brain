#!/usr/bin/env python3
"""Plain demo: the same cut as the explained spec, browser card on a gradient, no captions, no cards.
usage: plain_demo.py <spec.json> <out.mp4>   (honors per-segment "blur" and "speed")"""
import json, pathlib, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1920, 1080, 30
CW = 1568; CH = round(CW * 1080 / 1920); BAR = 48
L = (W - CW) // 2; T = (H - CH - BAR) // 2

def gradient():
    y, x = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip((x / W) * 0.35 + (y / H) * 0.65, 0, 1)[..., None]
    a = np.array([34, 193, 220], np.float32); b = np.array([37, 99, 201], np.float32)
    return Image.fromarray((a + (b - a) * t).astype(np.uint8))

def main():
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]
    man = json.load(open(spec["manifest"]))
    fdir = pathlib.Path(man["frames_dir"]); sfps = man["fps"]; nfr = man["frame_count"]
    bg = gradient().convert("RGBA")
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle((L, T + 24, L + CW, T + BAR + CH + 24), radius=16, fill=(0, 0, 0, 90))
    bg.alpha_composite(sh.filter(ImageFilter.GaussianBlur(28)))
    d = ImageDraw.Draw(bg)
    d.rounded_rectangle((L, T, L + CW, T + BAR + CH), radius=16, fill=(255, 255, 255, 255))
    d.rectangle((L, T + BAR - 1, L + CW, T + BAR), fill=(230, 232, 236, 255))
    for i, c in enumerate([(255, 95, 87), (254, 188, 46), (40, 200, 64)]):
        d.ellipse((L + 18 + i * 20, T + 18, L + 30 + i * 20, T + 30), fill=c)
    d.rounded_rectangle((L + 90, T + 9, L + CW - 18, T + 39), radius=15, fill=(244, 246, 248, 255))
    try: f = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 20)
    except Exception: f = ImageFont.load_default()
    d.text((L + 112, T + 15), spec["address"].split("/")[0], fill=(70, 78, 88, 255), font=f)
    mask = Image.new("L", (CW, CH), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, -30, CW, CH), radius=16, fill=255)
    ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
        "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", "-preset", "medium", "-movflags", "+faststart", out], stdin=subprocess.PIPE)
    total = 0.0
    for seg in spec["segments"]:
        sp = seg.get("speed", 1); dur = (seg["src"][1] - seg["src"][0]) / sp
        for k in range(int(round(dur * FPS))):
            i = min(nfr - 1, int(round((seg["src"][0] + k / FPS * sp) * sfps)))
            img = Image.open(fdir / f"{i:05d}.jpg").convert("RGB")
            for bx in seg.get("blur", []):
                bx = tuple(int(v) for v in bx)
                img.paste(img.crop(bx).filter(ImageFilter.GaussianBlur(16)), bx[:2])
            fr = bg.copy(); fr.paste(img.resize((CW, CH), Image.LANCZOS), (L, T + BAR), mask)
            ff.stdin.write(fr.convert("RGB").tobytes())
        total += dur
    ff.stdin.close(); ff.wait(); print(f"{out} {total:.1f}s")

if __name__ == "__main__": main()
