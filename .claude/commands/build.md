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
   ClickUp comment + status -> review, new stories -> Backlog list.

End with a one-screen delivery summary: delivered / in rework / escalated.
One quip permitted if and only if everything passed.
