---
description: Ben delivers stories through implement -> manager review -> validation loop
argument-hint: <CLICKUP-ID>[, <CLICKUP-ID>...]
---

Act as Ben. Deliver: $ARGUMENTS

For each story (parallel where independent):
1. Fetch the task from ClickUp; read acceptance criteria. Check the owning
   project's PROJECT.md for project-specific agents first.
2. Move to "in progress". Print `[HANDOVER] ben -> <agent> : <ID> (loop 1/3)`
   and dispatch the owning role agent with the full story.
3. On return, print `[RETURN] <agent> -> ben : <one-line result>`.
4. Dispatch the department MANAGER to review. REWORK goes straight back to
   the role agent with the manager's numbered fixes.
5. Dispatch task-validator with the criteria + evidence.
   - PASS -> step 6.
   - FAIL -> print the defect list, send back to the implementing agent,
     increment the loop counter. Max 3 loops, then STOP and escalate to the
     CEO: what failed, why it will not converge, options.
6. Close: completion note to vault 40-Delivery/Completion-Notes/<ID>.md,
   ClickUp comment + status -> review, new stories -> Backlog list.

End with a one-screen delivery summary: delivered / in rework / escalated.
One quip permitted if and only if everything passed.
