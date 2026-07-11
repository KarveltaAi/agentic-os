---
description: Anti-lock-in export - snapshot ClickUp state into the vault as plain markdown
---

Act as Ben. Run the portability backup:

1. Pull every list in the Agentic OS space from ClickUp (tasks, statuses,
   descriptions, comments of open tasks).
2. Write to vault: 95-Backups/clickup/<YYYY-MM-DD>/<list>.md — one table
   per list: ID, title, status, assignee-dept, criteria summary.
3. Git commit + push the vault.
4. Confirm: "If ClickUp vanished tonight, we lose nothing but the UI."
Run weekly (or schedule it). Everything else (agents, knowledge, code) is
already plain markdown in git and needs no export.
