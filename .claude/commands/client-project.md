---
description: Spin up a new client project with full isolation (repo, ClickUp, vault, secrets)
argument-hint: <client name> <project name> <one-line brief>
---

Act as Ben. New client project: $ARGUMENTS

1. ISOLATION FIRST. Create:
   - Git repo: projects/<client>-<project>/ (own repo, own .env, own
     .claude/agents/ + PROJECT.md; gh repo create --private)
   - ClickUp: Folder "<Client> — <Project>" with a Stories list + statuses
   - Vault: 10-Projects/<client>-<project>/ (brief, decisions, meeting notes)
2. PROJECT.md from templates/project.md: client contact, scope, deadlines,
   stack, IP/handover terms, any client-specific agents or skills.
3. Confidentiality rule (state it in PROJECT.md): agents working this
   project must not reference other clients' code, data, pricing or names
   in any output. One client per session where possible.
4. Kick off: recommend /boardroom for the approach if novel, then /plan.
5. Definition of Done for the PROJECT (not just stories): deploy + handover
   pack (templates/client-handover.md) + retro (/retro <project>).
