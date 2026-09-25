---
name: dev-build-verification
description: Use whenever Ben dispatches any Development-department role agent (architect, backend-dev, fullstack-dev, uiux-dev, devops-release, code-reviewer) on a story that touches a real codebase. These agents have no Bash tool and cannot run git, install dependencies, build, lint, or execute tests themselves — Ben must do it, between implementation and dev-manager review, every time.
---

# Dev-department build verification (Ben's job, not the implementer's)

**Why this exists:** on DemoProject, every single Development-department
story (DEM-005, DEM-007, DEM-009, DEM-012) hit the same wall — the
implementing agent has no shell, tried to claim a branch/commit/build
happened, and couldn't. Before this skill existed, that got discovered
piecemeal each time and Ben improvised a fix ad hoc. It also caused real
integration bugs to go unnoticed until a human (Ben) actually compiled the
code — see the DEM-009/DEM-012 field-name mismatch this skill's process
step 3 exists to catch. Retro: 2026-09-25 (`library/improvement-log.md`).

## When an implementer returns

1. **Install and build immediately**, before dispatching manager review.
   `cd` into the project repo, `npm install` (approve any pending native
   install scripts — `sharp`, native bindings, etc. — don't skip them),
   `npm run build`. If the stack isn't Node, use its equivalent (pip
   install + test run, go build, etc.).
2. **Fix trivial, mechanical failures yourself** rather than round-tripping
   a whole agent dispatch: lint errors with an obvious one-line fix
   (missing `next/link` import, an unused variable), a missing native
   asset conversion the implementer specified but couldn't run. Don't fix
   anything that requires a judgment call about behavior — that goes back
   to the implementer or through review.
3. **If two agents built in parallel against a shared contract** (API
   shape, field names, a honeypot/consent-style pairing), check their
   outputs actually agree on literal names before building — they won't,
   by default, if the contract was only described in prose. Reconcile by
   picking whichever name is more deeply embedded (touches more call
   sites) and updating the other side; document the reconciliation in both
   files' comments so a reviewer can see it happened deliberately. See
   `.claude/commands/build.md`'s parallel-dispatch rule for how to prevent
   this pre-emptively next time.
4. **Smoke-test the running app** for anything the acceptance criteria
   claim (start a dev server, curl the routes/endpoints that matter,
   check a real screenshot at the viewport sizes named in the AC — don't
   trust a Tailwind class string to prove a no-scroll claim). This is what
   actually catches whether the code does what the implementer said it
   does.
5. **Only after the build is green and manager review + validator PASS**:
   create the `story/<ID>-slug` branch (stack multiple same-wave stories
   if one depends on files the other created — e.g. a form implementation
   that replaces a placeholder page built by the other story), commit with
   a message naming what was built and who (implementer + reviewer)
   caught what, push if the repo has a remote.
6. **Do not let the implementer's own completion-note-shaped text become
   the vault completion note.** Their report-back is input to yours, not a
   substitute for it — write the canonical note yourself once, after
   validator PASS, per `templates/completion-note.md`.

## Don't do this instead

- Don't dispatch a fresh agent instance just to run `npm install` — none of
  them have Bash either (except `task-validator`, which is scoped to
  validation, not build-fixing). Run it yourself.
- Don't give the agents `Bash` to solve this. Two `fullstack-dev` instances
  (Femi-1/Femi-2) dispatched in parallel share one working directory in
  this OS's setup — simultaneous `npm install`/`git` calls from both would
  race. Centralizing on Ben, who runs things sequentially between
  dispatches, avoids that class of bug entirely; this was verified working
  cleanly on DEM-009/DEM-012's parallel build.
- Don't skip the build step because "the code looks right." Every story
  that skipped this historically shipped a broken OG image, a missing
  dependency, or a field-name mismatch that would have 500'd on first use.

## Done-criteria before dev-manager review

- `npm run build` (or equivalent) is green, run by you, in the actual repo.
- Any cross-agent contract (API shapes, shared constants) verified to
  actually match, not assumed from reading two separate files.
- At least one live smoke test per hard/numeric acceptance criterion
  (viewport pixels, status codes, rate-limit thresholds) — not just a
  read-through of the code that's supposed to produce it.
