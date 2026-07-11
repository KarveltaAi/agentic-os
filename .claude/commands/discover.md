---
description: Petra's team produces the discovery package (PRD, wireframes, screens, API/infra, docs suite) with an assumptions register
argument-hint: <project name> <idea file or one-line brief>
---

Act as Ben. Run discovery for: $ARGUMENTS

1. Create <project>/discovery/ (and vault 10-Projects/<project>/discovery/).
2. Dispatch Petra (product-manager) to coordinate the package - you dispatch
   each specialist (managers review, Ben dispatches):
   - Sophie (spec-writer): PRD - problem, outcomes, scope, success metrics
   - Uche (ux-designer): user flows, wireframe descriptions, screen inventory
   - Ada (architect): API design, data model, infrastructure outline, ADRs
   - Sophie + Petra: product documentation suite index (what docs exist,
     what must be written during build)
   - Mara/Kofi where market/competitor evidence is thin
3. ASSUMPTIONS REGISTER (the point of this phase): every artefact's
   assumptions are extracted into discovery/assumptions.md - each with
   impact-if-wrong (H/M/L) and how to validate.
4. Petra reviews the package; Vera checks completeness against this
   command's checklist (every artefact exists, no criteria-free specs).
5. Hand back to me (Ben): I convene /boardroom ROUND 2 on the assumptions
   register only. Board verdicts + conditions go into the register.
6. CEO GATE: present the package summary + assumptions + board round 2 to
   the CEO. On explicit CEO approval: update idea status to approved, then
   run /shadow-review (mandatory) before Paige plans anything.
