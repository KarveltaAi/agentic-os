---
description: Ben delivers stories through implement -> manager review -> validation loop
argument-hint: <CLICKUP-ID>[, <CLICKUP-ID>...]
---

Act as Ben. Deliver: $ARGUMENTS

**Parallel-dispatch contract rule:** when two or more stories share an
API/data contract (a request shape, field names, a shared constants file)
and are dispatched in parallel, pin the exact literal names in BOTH
dispatch prompts — copy-pasted, identical wording, not each agent
independently paraphrasing the same prose spec. Two agents reading the
same architecture doc will otherwise invent different names for the same
concept (evidenced twice: DEM-007's index name, DEM-009/012's honeypot/
consent field names — see library/improvement-log.md, 2026-09-25 retro).

**Development-department stories:** the role agents (architect,
backend-dev, fullstack-dev, uiux-dev) have no shell access and cannot
install, build, lint, test, or touch git themselves. Follow
skills/dev-build-verification/SKILL.md between steps 3 and 4 below — every
time, not just when something looks off.

For each story (parallel where independent):
1. Fetch the task from ClickUp; read acceptance criteria. Check the owning
   project's PROJECT.md for project-specific agents first.
2. Move to "in progress". Print `[HANDOVER] ben -> <agent> : <ID> (loop 1/3)`
   and dispatch the owning role agent with the full story.
   **Cite-don't-redispatch rule (2026-09-26 retro, evidenced twice —
   DEM-012 and DEM-015's Ada allocation):** if a story's allocation names
   an agent whose role is already fully answered by an existing decision
   document (an ADR, a prior story's architecture output), don't dispatch
   them for a rubber stamp — cite the existing decision directly in the
   completion note instead. Dispatch them for real when the story needs a
   genuinely new judgment call, not to re-confirm a settled one.
3. On return, print `[RETURN] <agent> -> ben : <one-line result>`. For
   Development-department stories, run skills/dev-build-verification/SKILL.md
   now — install, build, reconcile any parallel-contract mismatch, smoke-test
   — before step 4.
4. Dispatch the department MANAGER to review. REWORK goes straight back to
   the role agent with the manager's numbered fixes.
5. Dispatch task-validator with the criteria + evidence.
   - PASS -> step 6.
   - FAIL -> print the defect list, send back to the implementing agent,
     increment the loop counter. Max 3 loops, then STOP and escalate to the
     CEO: what failed, why it will not converge, options.
6. Close: for Development-department stories, this is also when the
   `story/<ID>-slug` branch gets created/committed (per
   skills/dev-build-verification/SKILL.md) — not earlier, since a branch
   cut before validator PASS just gets amended/re-cut anyway. Completion
   note to vault 40-Delivery/Completion-Notes/<ID>.md (written once, now,
   by Ben — not assembled from a role agent's own premature attempt),
   ClickUp comment + status -> review.
   **Backlog items → ClickUp call budget (2026-09-26 retro):** log EVERY
   new backlog candidate in the vault's Backlog-Candidates.md, always —
   that file has no call-volume cost. Only create a live ClickUp task for
   the top 2-3 highest-impact items per story; note the rest in the vault
   as "ClickUp: not yet created" without calling the API for them. Creating
   one ClickUp task per backlog item burned the workspace's shared
   100-call daily limit twice in one session (stalling status updates for
   3 other stories) — the vault file is the durable record either way, so
   there is no data loss, only a deferred sync. Sweep the deferred items
   into ClickUp in a batch (via clickup_get_operators/execute_operator's
   bulk-create path if available, not one clickup_create_task call per
   item) during a later /groom or /retro pass, not inline per-story.

End with a one-screen delivery summary: delivered / in rework / escalated.
One quip permitted if and only if everything passed.
