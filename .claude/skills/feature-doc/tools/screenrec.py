# screenrec.py: autonomous flow screen recorder for browser-harness.
#
# Captures continuous JPEG frames at a target fps while injecting time-scheduled
# actions, and writes a manifest (fps, viewport + image dims, per-action events with
# resolved cursor coords + captions) so videokit.py can add a synthetic cursor,
# captions, and polish. Assembles a raw mp4/GIF too (quick preview). No Arcade, no
# user gesture.
#
# Run THROUGH browser-harness (helpers in scope):
#     SR_OUT=/path/out SR_URL=https://... SR_STEPS='[...]' browser-harness < screenrec.py
#
# Env:
#   SR_OUT   output base (no ext). Writes <OUT>.frames/*.jpg, <OUT>.manifest.json,
#            and a quick <OUT>.raw.mp4|gif preview.
#   SR_URL   target URL (reuse+activate matching tab, else open background window).
#   SR_STEPS JSON list of actions, each {"at":sec,"do":...,"caption":"..."}:
#            click_xy{x,y} | click_testid{testid} | click_text{text} | type{text}
#            | key{key} | scroll{dx,dy}
#   SR_FPS   target fps (default 8).  SR_DURATION seconds (default last at +2.5, min 4).
#   SR_MAXDIM max frame dim px (default 1600).
import os, json, time, base64, glob, subprocess, shutil

OUT   = os.environ["SR_OUT"]
URL   = os.environ.get("SR_URL", "")
STEPS = json.loads(os.environ.get("SR_STEPS", "[]"))
FPS   = float(os.environ.get("SR_FPS", "8"))
MAXD  = int(os.environ.get("SR_MAXDIM", "1600"))
DUR   = float(os.environ.get("SR_DURATION", "0")) or (max((s["at"] for s in STEPS), default=2) + 2.5)
DUR   = max(DUR, 4.0)

FRAMES = OUT + ".frames"
if os.path.isdir(FRAMES): shutil.rmtree(FRAMES)
os.makedirs(FRAMES, exist_ok=True)

def tabs(): return cdp("Target.getTargets")["targetInfos"]  # noqa: F821
tid = None
if URL:
    m = [t for t in tabs() if (t.get("url") or "").startswith(URL) and t["type"] == "page"]
    if not m:
        new_window(URL); wait_for_load(); time.sleep(3)  # noqa: F821
        m = [t for t in tabs() if (t.get("url") or "").startswith(URL) and t["type"] == "page"]
    tid = m[0]["targetId"] if m else None
if tid:
    switch_tab(tid); cdp("Target.activateTarget", targetId=tid); time.sleep(1)  # noqa: F821

css = js("JSON.stringify({w:window.innerWidth,h:window.innerHeight})")  # noqa: F821
css = json.loads(css) if css else {"w": 1512, "h": 800}

def rect_of(finder_js):
    v = js(f"""(function(){{const c={finder_js};if(!c.length)return null;const r=c[0].getBoundingClientRect();return JSON.stringify({{x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)}});}})()""")  # noqa: F821
    try: return json.loads(v) if v and v.startswith("{") else None
    except Exception: return None

EVENTS = []  # {t, x, y, caption, do}
def act(s, t):
    if tid: switch_tab(tid)  # noqa: F821
    do = s["do"]; x = y = None
    try:
        if do == "click_xy":
            x, y = s["x"], s["y"]; click_at_xy(x, y)  # noqa: F821
        elif do == "click_testid":
            r = rect_of(f"[document.querySelector('[data-testid={s['testid']}]')].filter(Boolean)")
            if r: x, y = r["x"], r["y"]; click_at_xy(x, y)  # noqa: F821
        elif do == "click_text":
            r = rect_of(f"[...document.querySelectorAll('button,[role=button],a,div,span')].filter(e=>e.children.length<=2&&(e.textContent||'').trim()==={s['text']!r})")
            if r: x, y = r["x"], r["y"]; click_at_xy(x, y)  # noqa: F821
        elif do == "type":
            type_text(s["text"])  # noqa: F821
        elif do == "key":
            press_key(s["key"])  # noqa: F821
        elif do == "scroll":
            scroll(s.get("x", 600), s.get("y", 400), s.get("dx", 0), s.get("dy", 400))  # noqa: F821
    except Exception as e:
        print(f"  action {do} @{s['at']}s failed: {e}")
    EVENTS.append({"t": round(t, 3), "x": x, "y": y, "caption": s.get("caption", ""), "do": do})

def grab(i):
    r = cdp("Page.captureScreenshot", format="jpeg", quality=70)  # noqa: F821
    p = os.path.join(FRAMES, f"{i:05d}.jpg")
    open(p, "wb").write(base64.b64decode(r["data"]))
    return p

print(f"recording ~{DUR:.0f}s @ {FPS}fps -> {OUT}")
interval = 1.0 / max(FPS, 1)
t0 = time.time(); i = 0; fired = set()
while True:
    t = time.time() - t0
    if t >= DUR: break
    for si, s in enumerate(STEPS):
        if si not in fired and t >= s["at"]:
            act(s, t); fired.add(si)
    grab(i); i += 1
    dt = interval - ((time.time() - t0) - t)
    if dt > 0: time.sleep(dt)
n = i; real_fps = n / DUR if DUR else FPS
frames = sorted(glob.glob(os.path.join(FRAMES, "*.jpg")))

img_w = img_h = 0
try:
    from PIL import Image
    im = Image.open(frames[0]); img_w, img_h = im.size
except Exception:
    pass

manifest = {"fps": round(real_fps, 3), "frame_count": n, "duration": round(DUR, 3),
            "css_w": css["w"], "css_h": css["h"], "img_w": img_w, "img_h": img_h,
            "events": EVENTS, "frames_dir": FRAMES}
open(OUT + ".manifest.json", "w").write(json.dumps(manifest, indent=2))
print(f"captured {n} frames (~{real_fps:.1f} fps), img {img_w}x{img_h}, css {css['w']}x{css['h']}")

def _ffmpeg():
    for p in (shutil.which("ffmpeg"), "/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if p and os.path.exists(p): return p
    return None
FFMPEG = _ffmpeg()
prev = None
if len(frames) >= 2 and FFMPEG:
    prev = OUT + ".raw.mp4"
    r = subprocess.run([FFMPEG, "-y", "-framerate", f"{real_fps:.2f}", "-pattern_type", "glob",
                        "-i", os.path.join(FRAMES, "*.jpg"), "-c:v", "libx264", "-pix_fmt", "yuv420p",
                        "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2", prev], capture_output=True, text=True)
    if r.returncode != 0: prev = None
if prev is None and len(frames) >= 2:
    try:
        from PIL import Image
        prev = OUT + ".raw.gif"
        imgs = [Image.open(p).convert("RGB") for p in frames]
        for im in imgs:
            if max(im.size) > MAXD: im.thumbnail((MAXD, MAXD))
        imgs[0].save(prev, save_all=True, append_images=imgs[1:], duration=int(1000/max(real_fps,1)), loop=0, optimize=True)
    except Exception: prev = FRAMES
print("MANIFEST:", OUT + ".manifest.json")
print("RAW_PREVIEW:", prev)
