#!/usr/bin/env python3
"""Hook target: append Claude Code hook events to ops/events-<machine>.jsonl.
Per-machine files mean two operators never hit git merge conflicts on the
event log. Called by .claude/settings.json hooks; never raises."""
import json, sys, time, pathlib, platform, re

def main():
    kind = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}
    ti = payload.get("tool_input", {}) or {}
    host = re.sub(r'[^A-Za-z0-9-]', '', platform.node() or "local")[:20] or "local"
    evt = {
        "ts": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "machine": host,
        "event": kind,
        "agent": ti.get("subagent_type") or payload.get("subagent_type") or "",
        "detail": (ti.get("description") or ti.get("prompt") or "")[:160],
        "session": payload.get("session_id", "")[:8],
    }
    out = pathlib.Path(__file__).parent / f"events-{host}.jsonl"
    with out.open("a", encoding="utf-8") as f:
        f.write(json.dumps(evt) + "\n")

if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
    sys.exit(0)
