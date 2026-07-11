#!/usr/bin/env python3
"""Agentic OS live dashboard - multi-operator.

Run:   python ops/dashboard.py            (view local + last-pushed remote events)
       python ops/dashboard.py --share    (also auto-commit/push THIS machine's
                                           event file every 60s so the other
                                           operator sees you near-live)
Open:  http://localhost:8787   (auto-refreshes every 3s)

Events are per-machine files (ops/events-<machine>.jsonl) synced through the
git remote you already share. Stdlib only."""
import json, pathlib, shutil, subprocess, sys, threading, time, urllib.request
from http.server import HTTPServer, BaseHTTPRequestHandler

ROOT = pathlib.Path(__file__).resolve().parent.parent
OPS = ROOT / "ops"
REGISTRY = ROOT / "library" / "registry.md"
SHARE = "--share" in sys.argv
ACTIVE_WINDOW_S = 15 * 60
_remote_cache = {"t": 0.0, "lines": []}

def git(*args, timeout=20):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True,
                          text=True, timeout=timeout)

def local_event_lines():
    lines = []
    for p in sorted(OPS.glob("events*.jsonl")):
        try:
            lines += p.read_text(encoding="utf-8").splitlines()
        except Exception:
            pass
    return lines

def remote_event_lines():
    """Read event files as they exist on origin/main (last push from anyone)."""
    now = time.time()
    if now - _remote_cache["t"] < 30:
        return _remote_cache["lines"]
    lines = []
    try:
        r = git("ls-tree", "-r", "--name-only", "origin/main", "ops/")
        for name in r.stdout.splitlines():
            if name.startswith("ops/events") and name.endswith(".jsonl"):
                s = git("show", f"origin/main:{name}")
                if s.returncode == 0:
                    lines += s.stdout.splitlines()
    except Exception:
        pass
    _remote_cache.update(t=now, lines=lines)
    return lines

def events(limit=500):
    seen, out = set(), []
    for ln in local_event_lines() + remote_event_lines():
        if ln in seen:
            continue
        seen.add(ln)
        try:
            out.append(json.loads(ln))
        except Exception:
            pass
    out.sort(key=lambda e: e.get("ts", ""))
    return out[-limit:]

def roster():
    agents = []
    if REGISTRY.exists():
        for line in REGISTRY.read_text(encoding="utf-8").splitlines():
            if line.startswith("|") and not line.startswith("|--"):
                cells = [c.strip() for c in line.strip("|").split("|")]
                if len(cells) >= 2 and cells[0] and cells[0] not in ("Agent", "---"):
                    agents.append((cells[0], cells[1]))
    return agents

def agent_states(evts):
    state = {}
    now = time.time()
    for e in evts:
        a = e.get("agent") or ""
        if not a:
            continue
        try:
            ts = time.mktime(time.strptime(e["ts"], "%Y-%m-%dT%H:%M:%S"))
        except Exception:
            ts = now
        if e["event"] == "dispatch":
            state[a] = ("ACTIVE", ts, e.get("machine", ""))
        elif e["event"] in ("return", "idle"):
            state[a] = ("DONE", ts, e.get("machine", ""))
    for a, (s, ts, m) in list(state.items()):
        if s == "ACTIVE" and now - ts > ACTIVE_WINDOW_S:
            state[a] = ("STALE", ts, m)
    return state

def infra():
    checks = {}
    try:
        urllib.request.urlopen("http://localhost:11434/api/tags", timeout=2)
        checks["Ollama (Hermes)"] = "UP"
    except Exception:
        checks["Ollama (Hermes)"] = "DOWN (run: ollama serve)"
    du = shutil.disk_usage(ROOT)
    checks["Disk free"] = f"{du.free // (1024**3)} GB"
    try:
        r = git("status", "--porcelain")
        checks["OS repo"] = "clean" if not r.stdout.strip() else f"{len(r.stdout.splitlines())} uncommitted change(s)"
    except Exception:
        checks["OS repo"] = "git not available"
    try:
        urllib.request.urlopen("https://mcp.clickup.com", timeout=3)
        checks["ClickUp reachability"] = "UP"
    except Exception:
        checks["ClickUp reachability"] = "unreachable (network?)"
    checks["Event sharing"] = "ON (--share: pushing this machine's events)" if SHARE else "read-only (start with --share to publish live)"
    return checks

def sync_loop():
    """Every 60s: fetch remote events; with --share also publish ours."""
    while True:
        try:
            git("fetch", "-q", "origin")
            if SHARE:
                changed = git("status", "--porcelain", "--", "ops/").stdout.strip()
                if changed:
                    git("add", "ops/")
                    git("commit", "-q", "-m", "ops: event sync", "--", "ops/")
                p = git("push", "-q", "origin", "HEAD")
                if p.returncode != 0:
                    git("pull", "-q", "--rebase", "--autostash", "origin", "main")
                    git("push", "-q", "origin", "HEAD")
        except Exception:
            pass
        time.sleep(60)

def page():
    evts = events()
    states = agent_states(evts)
    reg = roster()
    active = [(a, d, states[a][2]) for a, d in reg if a in states and states[a][0] == "ACTIVE"]
    sleeping = [(a, d) for a, d in reg if not (a in states and states[a][0] == "ACTIVE")]
    machines = sorted({e.get("machine", "?") for e in evts if e.get("machine")})
    rows_active = "".join(f"<tr><td>&#9679;</td><td>{a}</td><td>{d}</td><td>{m}</td></tr>" for a, d, m in active) or "<tr><td colspan=4>none - everyone is asleep</td></tr>"
    rows_sleep = "".join(f"<tr><td>&#9790;</td><td>{a}</td><td>{d}</td></tr>" for a, d in sleeping)
    hand = "".join(
        f"<tr><td>{e['ts'][11:]}</td><td>{e.get('machine','')}</td><td>{e['event']}</td><td>{e.get('agent','')}</td><td>{e.get('detail','')}</td></tr>"
        for e in reversed(evts[-25:]))
    inf = "".join(f"<tr><td>{k}</td><td>{v}</td></tr>" for k, v in infra().items())
    return f"""<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="3"><title>Agentic OS</title>
<style>body{{font-family:Segoe UI,Arial;background:#111;color:#ddd;margin:24px}}
h1{{color:#fff}}h2{{color:#8ab4f8;margin-top:28px}}table{{border-collapse:collapse;width:100%}}
td,th{{border-bottom:1px solid #333;padding:6px 10px;text-align:left;font-size:14px}}
.active td:first-child{{color:#4caf50}}.sleep td:first-child{{color:#666}}
.meta{{color:#888;font-size:13px}}</style></head>
<body><h1>Agentic OS &mdash; Mission Control</h1>
<div class="meta">machines reporting: {', '.join(machines) or 'none yet'}</div>
<h2>Active agents ({len(active)})</h2><table class="active"><tr><th></th><th>agent</th><th>scope</th><th>machine</th></tr>{rows_active}</table>
<h2>Recent handovers &amp; events</h2><table><tr><th>time</th><th>machine</th><th>event</th><th>agent</th><th>detail</th></tr>{hand}</table>
<h2>Infrastructure</h2><table>{inf}</table>
<h2>Sleeping agents ({len(sleeping)})</h2><table class="sleep">{rows_sleep}</table>
</body></html>"""

class H(BaseHTTPRequestHandler):
    def do_GET(self):
        body = page().encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a):
        pass

if __name__ == "__main__":
    threading.Thread(target=sync_loop, daemon=True).start()
    mode = "SHARING (publishing this machine's events)" if SHARE else "read-only"
    print(f"Agentic OS dashboard [{mode}] -> http://localhost:8787  (Ctrl+C to stop)")
    HTTPServer(("127.0.0.1", 8787), H).serve_forever()
