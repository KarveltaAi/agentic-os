# Runtimes — four cockpits, one OS

The OS is files in git. Four front-ends can drive it; they differ in how
much of the machinery they run.

| Capability | PowerShell + Claude Code | VS Code + Claude Code ext. | Antigravity | Kiro |
|---|---|---|---|---|
| Reads OS conventions | CLAUDE.md | CLAUDE.md | AGENTS.md (generated) | AGENTS.md + .kiro/steering |
| Ben + subagent orchestration | YES | YES | no (role briefs only) | no (role briefs only) |
| /plan /build /boardroom etc. | YES | YES | no | no |
| Validation loop + hooks + dashboard events | YES | YES | no | no |
| ClickUp via MCP | YES (.mcp.json) | YES | YES (user-global config) | YES (.kiro/settings/mcp.json) |
| Best for | daily driving, voice | driving + code review in one window | Gemini-agent coding sessions on project repos | spec-driven coding on project repos |

## Rules that keep four cockpits sane

1. **CLAUDE.md is the master.** Never edit AGENTS.md by hand; run
   `python scripts/sync-runtimes.py` after editing CLAUDE.md (retros do it).
2. **Delivery lives in Claude Code.** Stories move todo → done via Ben.
   If you implement something in Antigravity/Kiro, update the ClickUp task
   and write the completion note yourself (templates/completion-note.md) —
   or tell Ben afterwards and he will backfill.
3. **Dashboard blind spot:** hooks only fire in Claude Code, so
   Antigravity/Kiro sessions do not appear on the dashboard. ClickUp
   status is the cross-runtime truth.
4. **One story per cockpit at a time.** Two runtimes editing one branch is
   how merge conflicts are born.

## Setup per runtime (details in RUNBOOK Phase 6A)

- **VS Code:** install the Claude Code extension, open C:\AgenticOS\agentic-os
  (or a project repo), run Claude in the panel — identical behaviour to the
  terminal, including /commands and subagents.
- **Antigravity:** open the repo as a workspace; it reads AGENTS.md
  automatically (v1.20.3+). Add ClickUp MCP once per machine in Settings →
  Customizations → MCP (stored in ~/.gemini/config/mcp_config.json).
- **Kiro:** open the repo; it reads AGENTS.md automatically and
  .kiro/settings/mcp.json is already in the repo. Optional: promote parts of
  AGENTS.md into .kiro/steering/ files if you want inclusion modes.
- **PowerShell:** `cd C:\AgenticOS\agentic-os` then `claude`. The original.
