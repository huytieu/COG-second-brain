#!/usr/bin/env python3
"""Compare models across your own Claude Code transcripts (~/.claude/projects/**/*.jsonl).

Workload (tool calls and active minutes per human prompt, tool error rate, delegation),
writing style per 10k words, and with --rules the share of replies and Markdown writes
that scan.py would have refused, per rule.

usage: model_compare.py [--models m1,m2,...] [--exclude <session-id-prefix> ...]
                        [--since <ISO>] [--until <ISO>] [--rules]
Default models: every model with at least 200 responses in the transcripts.
Run the same window for every model: a rules file or hook that changed mid-window is a confound.

Rules:
- Lines are deduped by `uuid`; assistant usage is counted once per message.id.
- A session belongs to a model when that model wrote >= 80% of its assistant messages.
- Subagent transcripts (path contains /subagents/) are reported separately.
- Human prompt: user text that is not hook feedback, a system/teammate message, a skill preamble or an interrupt marker.
- Active time: sum of gaps between consecutive events, dropping gaps over 10 minutes.
"""
import json, glob, os, re, sys, collections
from datetime import datetime

MODELS = None
EXCLUDE = [a for i, a in enumerate(sys.argv) if i > 0 and sys.argv[i - 1] == "--exclude"]
SINCE = next((datetime.fromisoformat(a) for i, a in enumerate(sys.argv) if i > 0 and sys.argv[i - 1] == "--since"), None)
UNTIL = next((datetime.fromisoformat(a) for i, a in enumerate(sys.argv) if i > 0 and sys.argv[i - 1] == "--until"), None)
CORR = re.compile(r"^\s*(no[,. !]|nope|wrong|that'?s not|not what|why did you|you didn'?t|stop |don'?t|undo|revert|i said|still (wrong|broken|not)|it'?s (still )?(wrong|broken)|doesn'?t work|not working)", re.I)
NOT_HUMAN = ("Stop hook feedback", "<", "Base directory", "[Request interrupted", "Another Claude session", "[SYSTEM")
STYLE = {
    "em dash": r"—",
    "X, not Y": r"\b[a-z][a-z-]+, not (a |an |the |just |only )?[a-z][a-z -]{1,30}[.;:]",
    "semicolon": r";\s",
    "parenthetical": r"\([^)\n]{3,80}\)",
    "bullet line": r"(?m)^\s*[-*] ",
}


def ts(o):
    try:
        return datetime.fromisoformat(o["timestamp"].replace("Z", "+00:00"))
    except Exception:
        return None


def prose(t):
    t = re.sub(r"```.*?```", " ", t, flags=re.S)
    t = re.sub(r"`[^`\n]*`", " ", t)
    return t


def user_text(o):
    c = o.get("message", {}).get("content")
    if isinstance(c, str):
        return c
    return " ".join(x.get("text", "") for x in (c or []) if isinstance(x, dict) and x.get("type") == "text")


def _models():
    arg = next((a for i, a in enumerate(sys.argv) if i > 0 and sys.argv[i - 1] == "--models"), None)
    if arg:
        return arg.split(",")
    seen = collections.Counter()
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        for line in open(f, errors="ignore"):
            if '"model"' in line and '"assistant"' in line:
                m = re.search(r'"model":"(claude-[^"]+)"', line)
                if m:
                    seen[m.group(1)] += 1
    return sorted(m for m, n in seen.items() if n >= 200)


MODELS = _models()
agg = collections.defaultdict(collections.Counter)
style = collections.defaultdict(collections.Counter)

for f in glob.glob(os.path.expanduser("~/.claude/projects/**/*.jsonl"), recursive=True):
    if any(e in f for e in EXCLUDE):
        continue
    lane = "sub" if "/subagents/" in f else "main"
    seen, rows = set(), []
    for line in open(f, errors="ignore"):
        try:
            o = json.loads(line)
        except Exception:
            continue
        if UNTIL and o.get("timestamp") and ts(o) and ts(o) > UNTIL:
            continue
        if SINCE and o.get("timestamp") and ts(o) and ts(o) < SINCE:
            continue
        u = o.get("uuid")
        if u and u in seen:
            continue
        seen.add(u)
        rows.append(o)
    mc = collections.Counter(o["message"].get("model") for o in rows if o.get("type") == "assistant")
    mc = collections.Counter({m: n for m, n in mc.items() if m in MODELS})
    if not mc:
        continue
    model, n = mc.most_common(1)[0]
    if n / sum(mc.values()) < 0.8:
        continue
    k = (model, lane)
    c = agg[k]
    c["sessions"] += 1
    msgs, tool_ids, last_t, bash_ids = {}, {}, None, set()
    for o in rows:
        t = ts(o)
        if t and last_t and (t - last_t).total_seconds() < 600:
            c["active_s"] += (t - last_t).total_seconds()
        if t:
            last_t = t
        if o.get("type") == "assistant":
            msg = o["message"]
            if msg.get("model") != model:
                continue
            mid = msg.get("id") or o.get("uuid")
            e = msgs.setdefault(mid, {"usage": msg.get("usage") or {}, "tools": 0, "think": False})
            for b in msg.get("content", []):
                bt = b.get("type")
                if bt == "tool_use":
                    e["tools"] += 1
                    name = b.get("name", "")
                    tool_ids[b.get("id")] = name
                    c["tool_calls"] += 1
                    c["tool:" + ("mcp" if name.startswith("mcp__") else name)] += 1
                    if name in ("Write", "Edit") and str((b.get("input") or {}).get("file_path", "")).endswith(".md"):
                        txt = prose((b.get("input") or {}).get("content") or (b.get("input") or {}).get("new_string") or "")
                        style[(model, "files")]["words"] += len(txt.split())
                        for lab, rx in STYLE.items():
                            style[(model, "files")][lab] += len(re.findall(rx, txt))
                elif bt == "thinking":
                    e["think"] = True
                elif bt == "text":
                    txt = b.get("text", "")
                    c["text_blocks"] += 1
                    c["text_words"] += len(txt.split())
                    if lane == "main":
                        p = prose(txt)
                        style[(model, "chat")]["words"] += len(p.split())
                        for lab, rx in STYLE.items():
                            style[(model, "chat")][lab] += len(re.findall(rx, p))
        elif o.get("type") == "user":
            cont = o.get("message", {}).get("content")
            if isinstance(cont, list):
                for x in cont:
                    if isinstance(x, dict) and x.get("type") == "tool_result" and x.get("tool_use_id") in tool_ids:
                        name = tool_ids[x["tool_use_id"]]
                        if name == "Bash":
                            c["bash"] += 1
                        if x.get("is_error"):
                            c["tool_err"] += 1
                            if name == "Bash":
                                c["bash_err"] += 1
            s = user_text(o)
            if not s or lane != "main":
                continue
            if s.startswith("Stop hook feedback") and "Slop gate" in s:
                c["slop_blocks"] += 1
            if "[Request interrupted" in s:
                c["interrupts"] += 1
            if s.startswith(NOT_HUMAN) or "teammate-message" in s:
                continue
            c["human"] += 1
            if CORR.search(s):
                c["corrections"] += 1
    for e in msgs.values():
        u = e["usage"]
        c["msgs"] += 1
        c["out_tok"] += u.get("output_tokens", 0)
        c["ctx_tok"] += u.get("input_tokens", 0) + u.get("cache_read_input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
        c["think_msgs"] += e["think"]
        if e["tools"]:
            c["tool_msgs"] += 1
            c["parallel_msgs"] += e["tools"] > 1


def ratio(k, a, b, mul=1.0):
    d = agg[k][b]
    return agg[k][a] / d * mul if d else 0.0


ROWS = [
    ("sessions", lambda k: agg[k]["sessions"]),
    ("assistant messages", lambda k: agg[k]["msgs"]),
    ("human prompts", lambda k: agg[k]["human"]),
    ("human prompts / session", lambda k: ratio(k, "human", "sessions")),
    ("tool calls / human prompt", lambda k: ratio(k, "tool_calls", "human")),
    ("active minutes / human prompt", lambda k: ratio(k, "active_s", "human", 1 / 60)),
    ("tool error %", lambda k: ratio(k, "tool_err", "tool_calls", 100)),
    ("bash error %", lambda k: ratio(k, "bash_err", "bash", 100)),
    ("parallel-tool msgs % of tool msgs", lambda k: ratio(k, "parallel_msgs", "tool_msgs", 100)),
    ("context tokens / msg (k)", lambda k: ratio(k, "ctx_tok", "msgs", 1 / 1000)),
    ("output tokens / msg", lambda k: ratio(k, "out_tok", "msgs")),
    ("msgs with thinking %", lambda k: ratio(k, "think_msgs", "msgs", 100)),
    ("Agent spawns / 100 human prompts", lambda k: ratio(k, "tool:Agent", "human", 100)),
    ("words / text block", lambda k: ratio(k, "text_words", "text_blocks")),
    ("Read share of tool calls %", lambda k: ratio(k, "tool:Read", "tool_calls", 100)),
    ("human corrections / 100 prompts", lambda k: ratio(k, "corrections", "human", 100)),
    ("interrupts / 100 prompts", lambda k: ratio(k, "interrupts", "human", 100)),
    ("slop-gate reply blocks / 100 text blocks", lambda k: ratio(k, "slop_blocks", "text_blocks", 100)),
]

for lane in ("main", "sub"):
    print(f"\n== {lane} sessions")
    print("%-42s" % "", *["%12s" % m.replace("claude-", "") for m in MODELS])
    for lab, fn in ROWS:
        vals = [fn((m, lane)) for m in MODELS]
        print("%-42s" % lab, *[("%12d" % v) if isinstance(v, int) else ("%12.1f" % v) for v in vals])

print("\n== style, per 10k words (chat = lead replies, files = Markdown written via Write/Edit, code stripped)")
print("%-42s" % "", *["%12s" % (m.replace("claude-", "")) for m in MODELS])
for kind in ("chat", "files"):
    print("%-42s" % f"[{kind}] words", *["%12d" % style[(m, kind)]["words"] for m in MODELS])
    for lab in STYLE:
        print("%-42s" % f"[{kind}] {lab}", *["%12.1f" % (style[(m, kind)][lab] * 1e4 / max(style[(m, kind)]["words"], 1)) for m in MODELS])

# ---- rule compliance against scan.py ----
# A "unit" is one lead chat reply (all text blocks of one response) or one Markdown Write/Edit.
# Reports, per model, the share of units the gate would have refused and the per-rule hit rate.
if "--rules" in sys.argv:
    import importlib.util
    spec = importlib.util.spec_from_file_location("sg", os.path.join(os.path.dirname(os.path.abspath(__file__)), "scan.py"))
    sg = importlib.util.module_from_spec(spec); spec.loader.exec_module(sg)
    sg.SOFT = [("filler word", sg.FILLER.pattern, sg.FILLER.flags)]
    VOICE = [
        ("verdict kicker closer (That is the point/lie)", r"\bThat (is|was|'s) (the (point|lie|whole (point|thing))|all [a-z ]{2,30} is for)\.", re.I),
        ("ends on a question to the reader", r"\?\s*$", 0),
        ("'ship' used", r"\bship(s|ped|ping)?\b", re.I),
    ]
    units = collections.defaultdict(list)
    for f in glob.glob(os.path.expanduser("~/.claude/projects/*/*.jsonl")):
        if any(e in f for e in EXCLUDE):
            continue
        per_msg = collections.defaultdict(str); mmodel = {}
        for line in open(f, errors="ignore"):
            try:
                o = json.loads(line)
            except Exception:
                continue
            if o.get("type") != "assistant" or (UNTIL and ts(o) and ts(o) > UNTIL) or (SINCE and ts(o) and ts(o) < SINCE):
                continue
            m = o["message"].get("model")
            if m not in MODELS:
                continue
            mid = o["message"].get("id")
            for b in o["message"].get("content", []):
                if b.get("type") == "text":
                    per_msg[mid] += b.get("text", "") + "\n"; mmodel[mid] = m
                elif b.get("type") == "tool_use" and b.get("name") in ("Write", "Edit"):
                    ti = b.get("input") or {}
                    if str(ti.get("file_path", "")).endswith(".md"):
                        t = ti.get("content") or ti.get("new_string") or ""
                        if "slop-ok:" not in t and "no-ai-slop" not in str(ti.get("file_path")):
                            units[(m, "files")].append(t)
        for mid, t in per_msg.items():
            units[(mmodel[mid], "chat")].append(t)
    labels = sorted({l for l, _, _ in sg.HARD}) + ["filler words >= 3 (SOFT limit)"] + [l for l, _, _ in VOICE]
    for kind in ("chat", "files"):
        print(f"\n== rule compliance [{kind}]: % of units with >= 1 hit")
        print("%-46s" % "units", *["%12d" % len(units[(m, kind)]) for m in MODELS])
        res = {}
        for m in MODELS:
            cnt = collections.Counter(); blocked = 0
            for t in units[(m, kind)]:
                body = sg.strip_quoted(t); hit_any = False
                for lab, rx, fl in sg.HARD:
                    if re.search(rx, body, fl):
                        cnt[lab] += 1; hit_any = True
                soft = sum(len(re.findall(rx, body, fl)) for _, rx, fl in sg.SOFT)
                if soft >= sg.SOFT_LIMIT:
                    cnt["filler words >= 3 (SOFT limit)"] += 1; hit_any = True
                for lab, rx, fl in VOICE:
                    if re.search(rx, body, fl):
                        cnt[lab] += 1
                blocked += hit_any
            res[m] = (cnt, blocked, max(len(units[(m, kind)]), 1))
        print("%-46s" % "would be refused by the gate %", *["%12.1f" % (100 * res[m][1] / res[m][2]) for m in MODELS])
        for lab in labels:
            print("%-46s" % lab[:46], *["%12.2f" % (100 * res[m][0][lab] / res[m][2]) for m in MODELS])
