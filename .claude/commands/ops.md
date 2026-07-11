---
description: Observability report - active/sleeping agents, recent handovers, infra health
---

Act as Ben. Produce the ops picture:

1. Read ops/events.jsonl (last ~50 events). Table: time, event, agent, detail.
2. Derive agent states: ACTIVE (dispatched, not returned), recently DONE,
   everyone else in library/registry.md = SLEEPING. Show counts + names.
3. Infra checks via Bash: Ollama up? (curl http://localhost:11434/api/tags),
   disk free, git status of OS repo and vault, ClickUp MCP connected (/mcp state).
4. Application checks: any story in ClickUp "blocked"? any validation loop at 2/3?
5. Remind the CEO the live view is: python ops/dashboard.py -> http://localhost:8787
Keep it to one screen. Worst news first.
