#!/usr/bin/env python3
"""
Hybrid Arcade recorder for web app flows.

Why hybrid: the Arcade Chrome extension only starts/stops recording on a *trusted*
user gesture (toolbar click or Cmd+E) that automation can't supply. But Arcade
captures the page via a content script, so it DOES capture CDP-driven clicks. This
script drives the whole flow; you supply just two keypresses (Cmd+E to start, Cmd+E
to stop). Run it in your own terminal so its input() pauses catch your timing.

Usage:
    export BU_CDP_URL=http://localhost:9222        # your daily Chrome w/ debugging
    python3 arcade-record.py <flow>                # e.g. connect-demo
    python3 arcade-record.py --list

Requires: `browser-harness` on PATH, the target Chrome logged into your app,
and the Arcade extension installed + logged into your Arcade workspace.

Add a new flow: append an entry to FLOWS below. Steps run top-to-bottom with pacing
that reads naturally in the recording. Use `click_text`/`click_testid` (resolved to
coordinates → trusted CDP click) so the flow survives minor layout shifts.
"""
import os, sys, json, subprocess, time

APP_URL = os.environ.get("APP_URL", "https://app.example.com/start")  # page the flow starts on
CDP = os.environ.get("BU_CDP_URL", "http://localhost:9222")
ENV = {**os.environ, "BU_CDP_URL": CDP}

# ---- flow library -----------------------------------------------------------
# Each flow: target URL to prep on, and a list of steps.
# step actions: goto | new_chat | click_text | click_testid | click_xy | type |
#               key | sleep | shot | note
FLOWS = {
    "connect-demo": {
        "url": APP_URL,
        "title": "Connect apps to the assistant",
        "steps": [
            {"do": "note", "msg": "Chat view: the composer has a Connect apps control"},
            {"do": "click_testid", "testid": "connect-integrations-button", "label": "open Connect apps"},
            {"do": "sleep", "s": 2.0},
            {"do": "note", "msg": "Connectors popover lists the providers"},
            {"do": "click_text", "text": "Google Drive", "label": "focus Google Drive row"},
            {"do": "sleep", "s": 2.0},
            {"do": "note", "msg": "Google Drive connected: toggle on + per-chat control"},
            {"do": "sleep", "s": 1.5},
            {"do": "key", "key": "Escape"},
            {"do": "sleep", "s": 1.0},
        ],
    },
    # template to copy for other features (fill url + steps, then re-run)
    "template": {
        "url": APP_URL,
        "title": "<feature> demo",
        "steps": [
            {"do": "note", "msg": "describe the starting state"},
            {"do": "click_text", "text": "<button label>", "label": "step 1"},
            {"do": "sleep", "s": 2.0},
        ],
    },
}

# ---- browser-harness bridge -------------------------------------------------
def bh(code: str) -> str:
    """Run a python snippet inside browser-harness (persistent daemon) and return stdout."""
    r = subprocess.run(["browser-harness"], input=code, capture_output=True, text=True, env=ENV)
    if r.returncode != 0:
        sys.stderr.write(r.stderr[-800:])
    return r.stdout.strip()

def resolve_tab(url_prefix: str) -> str:
    out = bh(f"""
tabs=list_tabs()
m=[t for t in tabs if (t.get('url') or '').startswith({url_prefix!r})]
print(m[0]['targetId'] if m else 'NONE')
""")
    tid = out.splitlines()[-1].strip() if out else "NONE"
    return tid

def prep(url: str) -> str:
    """Open/activate the flow tab, fresh chat, foreground it for recording."""
    tid = resolve_tab(url)
    if tid == "NONE":
        bh(f"new_window({url!r}); import time; time.sleep(5)")
        tid = resolve_tab(url)
    bh(f"""
import time
switch_tab({tid!r}); time.sleep(1)
cdp("Target.activateTarget", targetId={tid!r})
# start a clean chat if the New chat control exists
js('''(function(){{const b=[...document.querySelectorAll("*")].find(e=>e.children.length===0&&/^New chat$/.test((e.textContent||"").trim()));if(b)b.click();}})()''')
time.sleep(2)
""")
    return tid

def step(tid: str, s: dict):
    """Execute one step. Re-switches to the tab first (daemon can drift)."""
    pre = f'import time, json\nswitch_tab({tid!r})\n'
    do = s["do"]
    if do == "note":
        print(f"    • {s['msg']}")
        return
    if do == "sleep":
        bh(pre + f"time.sleep({s['s']})")
        return
    if do == "key":
        bh(pre + f"press_key({s['key']!r}); time.sleep(0.6)")
    elif do == "type":
        bh(pre + f"type_text({s['text']!r}); time.sleep(0.5)")
    elif do == "goto":
        bh(pre + f"goto_url({s['url']!r}); wait_for_load(); time.sleep(2)")
    elif do == "click_xy":
        bh(pre + f"click_at_xy({s['x']},{s['y']}); time.sleep(1)")
    elif do in ("click_text", "click_testid"):
        # resolve center coords via JS, then a TRUSTED coordinate click (Arcade captures it)
        if do == "click_text":
            finder = (f"[...document.querySelectorAll('button,[role=button],a,div,span')]"
                      f".filter(e=>e.children.length<=2 && (e.textContent||'').trim()==={s['text']!r})")
        else:
            finder = f"[document.querySelector('[data-testid={s['testid']}]')].filter(Boolean)"
        out = bh(pre + f"""
el=js('''(function(){{const c={finder};if(!c.length)return "NONE";const r=c[0].getBoundingClientRect();return JSON.stringify({{x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2)}});}})()''')
print(el)
""")
        line = out.splitlines()[-1].strip() if out else "NONE"
        if line == "NONE" or not line.startswith("{"):
            print(f"    ! could not find target for step: {s.get('label', do)}")
            return
        c = json.loads(line)
        bh(pre + f"click_at_xy({c['x']},{c['y']}); time.sleep(1)")
    if s.get("label"):
        print(f"    ✓ {s['label']}")

# ---- main -------------------------------------------------------------------
def main():
    if "--list" in sys.argv:
        print("Flows:", ", ".join(FLOWS)); return
    name = next((a for a in sys.argv[1:] if not a.startswith("-")), None)
    if not name or name not in FLOWS:
        print("Usage: python3 arcade-record.py <flow>   (--list to see flows)"); return
    flow = FLOWS[name]

    print(f"\n=== Arcade hybrid recording: {name} ===")
    print(f"Title: {flow['title']}")
    print("Prepping the tab...")
    tid = prep(flow["url"])
    if tid == "NONE":
        print("Could not open the flow tab. Is Chrome running with --remote-debugging-port=9222?"); return

    print("\n>>> In Chrome, on the flow tab, press **Cmd+E** now to START Arcade recording.")
    input(">>> Then press Enter here to begin driving the flow...")

    print("\nDriving the flow (watch the recording):")
    time.sleep(1.0)
    for s in flow["steps"]:
        step(tid, s)

    print("\n>>> Flow done. Press **Cmd+E** in Chrome to STOP recording.")
    input(">>> Then press Enter here...")

    print("\nArcade will open the editor for the new recording.")
    print("Next: title it '%s', tidy steps, Share -> Embed to get the demo.arcade.software URL," % flow["title"])
    print("then paste that URL into the feature package's release-note iframe.")

if __name__ == "__main__":
    main()
