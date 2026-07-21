#!/usr/bin/env python3
"""Regenerate runtime adapter files from CLAUDE.md (the master).
Run after ANY edit to CLAUDE.md (retros do this automatically).

Generates:
  AGENTS.md               read automatically by Antigravity and Kiro
  .kiro/settings/mcp.json ClickUp MCP for Kiro (created only if missing)

Reminder printed for Antigravity's user-global MCP config."""
import json, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parent.parent
master = (ROOT / "CLAUDE.md").read_text(encoding="utf-8")

header = f"""<!-- GENERATED from CLAUDE.md by scripts/sync-runtimes.py on {datetime.date.today()} —
edit CLAUDE.md, not this file. -->

# Agentic OS — runtime-neutral instructions (AGENTS.md)

This workspace is an Agentic OS. Full conventions follow (mirrored from
CLAUDE.md). NOTE for non-Claude-Code runtimes (Antigravity, Kiro):
- Subagents (.claude/agents/), slash commands (.claude/commands/) and hooks
  are Claude Code features. In this runtime, treat each agent .md as a ROLE
  BRIEF: when acting as that role, open the file and follow it.
- Delivery orchestration (Ben's loop, validation loops, event logging) runs
  in Claude Code. From this runtime: do implementation work, keep ClickUp
  statuses current via MCP, and write completion notes by hand from
  templates/completion-note.md.
- Everything else below applies verbatim.

---

"""
(ROOT / "AGENTS.md").write_text(header + master, encoding="utf-8")
print("AGENTS.md regenerated")

kiro = ROOT / ".kiro" / "settings" / "mcp.json"
if not kiro.exists():
    kiro.parent.mkdir(parents=True, exist_ok=True)
    kiro.write_text(json.dumps(
        {"mcpServers": {"clickup": {"url": "https://mcp.clickup.com/mcp"}}},
        indent=2), encoding="utf-8")
    print(".kiro/settings/mcp.json created (check kiro.dev docs if the remote-MCP field name differs)")
else:
    print(".kiro/settings/mcp.json exists, untouched")

print("Antigravity MCP is user-global: add ClickUp in Settings -> Customizations -> MCP,")
print("or edit ~/.gemini/config/mcp_config.json (one-time, per machine).")
