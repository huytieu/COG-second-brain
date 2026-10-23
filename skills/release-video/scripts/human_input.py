#!/usr/bin/env python3
"""Human-looking mouse and keyboard input for demo recordings.

Timings come from 120 fps recordings of a real person using the UI:
long moves take 150-250 ms (up to ~450 ms for very long ones), run nearly
straight with a slight curve and a bell-shaped speed peak near the middle,
then 1-3 small corrections of 15-100 px and a 200-400 ms dwell before the
click. The cursor is still about two thirds of the time.

The planners are pure functions. `drive` sends the events through any
`send(method, params)` callable, so it works with a CDP session from
browser-harness, Playwright (`cdp.send`), or a raw websocket.

    from human_input import Human
    h = Human(send, start=(400, 300))
    h.click(820, 512)          # move, correct, dwell, press, release
    h.type("Empty Weekend")    # per-key timing with word-boundary pauses
    h.pause("read")            # 1.5-2.5 s still cursor after new content
"""
import math, random, time

def min_jerk(s):
    return 10 * s**3 - 15 * s**4 + 6 * s**5

def move_duration(dist, rng):
    # 200 px -> ~0.16 s, 1400 px -> ~0.25 s, capped near 0.45 s
    base = 0.11 + 0.05 * math.log2(1 + dist / 100)
    return min(0.45, max(0.08, base * rng.uniform(0.9, 1.15)))

def plan_move(p0, p1, rng, hz=120):
    """Points (x, y, dt) along a slightly curved minimum-jerk path."""
    (x0, y0), (x1, y1) = p0, p1
    dist = math.dist(p0, p1)
    if dist < 1:
        return []
    dur = move_duration(dist, rng)
    n = max(3, int(dur * hz))
    # perpendicular bow: 2-6 % of the distance, random side
    bow = dist * rng.uniform(0.02, 0.06) * rng.choice((-1, 1))
    nx, ny = -(y1 - y0) / dist, (x1 - x0) / dist
    pts = []
    for i in range(1, n + 1):
        s = min_jerk(i / n)
        b = bow * math.sin(math.pi * s)
        pts.append((x0 + (x1 - x0) * s + nx * b, y0 + (y1 - y0) * s + ny * b, dur / n))
    return pts

def plan_approach(p0, target, rng, hz=120):
    """Long move that lands slightly off, then 1-3 corrections onto the target."""
    dist = math.dist(p0, target)
    if dist < 120:
        return plan_move(p0, target, rng, hz)
    err = min(60, dist * rng.uniform(0.02, 0.06))
    a = rng.uniform(0, 2 * math.pi)
    land = (target[0] + err * math.cos(a), target[1] + err * math.sin(a))
    pts = plan_move(p0, land, rng, hz)
    cur = land
    k = rng.choice((1, 1, 2, 3))
    for j in range(k):
        f = 1.0 if j == k - 1 else rng.uniform(0.5, 0.8)
        nxt = (cur[0] + (target[0] - cur[0]) * f, cur[1] + (target[1] - cur[1]) * f)
        gap = rng.uniform(0.04, 0.12)
        if pts:
            x, y, dt = pts[-1]
            pts[-1] = (x, y, dt + gap)
        step = plan_move(cur, nxt, rng, hz)
        # corrections are slower per pixel: 70-300 ms
        scale = rng.uniform(0.07, 0.3) / max(1e-6, sum(p[2] for p in step) or 1)
        pts += [(x, y, dt * scale) for x, y, dt in step]
        cur = nxt
    return pts

def plan_typing(text, rng):
    """(char, delay_before) pairs: 60-120 ms per key, longer at boundaries."""
    out = []
    for i, ch in enumerate(text):
        d = rng.uniform(0.06, 0.12)
        if i and text[i - 1] in " .,;:-/@":
            d += rng.uniform(0.08, 0.25)
        if rng.random() < 0.04:
            d += rng.uniform(0.2, 0.45)  # occasional hesitation
        out.append((ch, d))
    return out

class Human:
    PAUSES = {"beat": (0.2, 0.45), "read": (1.5, 2.5), "think": (0.6, 1.1)}

    def __init__(self, send, start=(0, 0), seed=None, sleep=time.sleep):
        self.send, self.pos, self.sleep = send, start, sleep
        self.rng = random.Random(seed)

    def _mouse(self, type_, x, y, **kw):
        self.send("Input.dispatchMouseEvent", {"type": type_, "x": round(x, 1), "y": round(y, 1), **kw})

    def move(self, x, y):
        for px, py, dt in plan_approach(self.pos, (x, y), self.rng):
            self._mouse("mouseMoved", px, py)
            self.sleep(dt)
        self.pos = (x, y)

    def click(self, x, y, dwell=None):
        self.move(x, y)
        self.sleep(dwell if dwell is not None else self.rng.uniform(0.2, 0.4))
        self._mouse("mousePressed", x, y, button="left", clickCount=1)
        self.sleep(self.rng.uniform(0.08, 0.12))
        self._mouse("mouseReleased", x, y, button="left", clickCount=1)

    def type(self, text):
        for ch, d in plan_typing(text, self.rng):
            self.sleep(d)
            if ch == "\n":
                for t in ("rawKeyDown", "keyUp"):
                    self.send("Input.dispatchKeyEvent", {"type": t, "key": "Enter", "code": "Enter", "windowsVirtualKeyCode": 13})
                self.send("Input.dispatchKeyEvent", {"type": "char", "text": "\r"})
            else:
                self.send("Input.dispatchKeyEvent", {"type": "keyDown", "text": ch, "key": ch})
                self.send("Input.dispatchKeyEvent", {"type": "keyUp", "key": ch})

    def pause(self, kind="beat"):
        lo, hi = self.PAUSES[kind]
        self.sleep(self.rng.uniform(lo, hi))

if __name__ == "__main__":
    # Self-check against the measured ranges.
    rng = random.Random(7)
    for d in (200, 600, 1400):
        pts = plan_move((0, 0), (d, 0), rng)
        dur = sum(p[2] for p in pts)
        steps = [abs(pts[i + 1][0] - pts[i][0]) for i in range(len(pts) - 1)]
        peak = steps.index(max(steps)) / (len(steps) - 1)
        assert 0.08 <= dur <= 0.45 and 0.3 <= peak <= 0.7, (d, dur, peak)
        print(f"{d:>5}px  {dur*1000:4.0f} ms  speed peak at {peak:.2f}")
    a = plan_approach((0, 0), (900, 400), rng)
    print("approach events", len(a), "ends at", tuple(round(v) for v in a[-1][:2]))
    assert math.dist(a[-1][:2], (900, 400)) < 1
    t = plan_typing("Empty Weekend", rng)
    print("typing ms", [round(d * 1000) for _, d in t])
