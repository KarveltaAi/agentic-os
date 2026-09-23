---
description: >-
  /gitflow — Solo git flow. Report branch state, or release dev to main.
  No PRs, no approvals, no staging branch.
---

## Solo Git Flow

**Usage:**
```
/gitflow            # status report
/gitflow release    # ship dev to main
```

### The flow (one operator)

- Work happens on `dev` (or a short-lived `story/PREFIX-NNN-slug` branch
  merged into `dev` locally when done).
- Release = fast-forward `main` to `dev` and push. No PR, no review.
- Hotfix = commit on `main`, push, then merge `main` back into `dev`.
- GitHub guards `main` only against force-push and deletion.

### Status report

1. `git fetch`, then show: current branch, uncommitted changes, commits on
   `dev` not yet on `main`, and the last CI run (informational, never a gate).
2. Flag stories in the pending release still in `Rework` in ClickUp.

### Release (`/gitflow release`)

1. Confirm with the operator in one line: "Ship N commits from dev to main?"
2. `git checkout dev && git pull` → `git checkout main && git pull`
   → `git merge --ff-only dev` → `git push` → `git checkout dev`.
3. If fast-forward fails (main has commits dev lacks), merge `main` into
   `dev` first, then retry.
4. Note the release in the vault `40-Delivery/` and move shipped ClickUp
   stories to `done`.

If a second operator joins later, reintroduce PR review deliberately via
/retro rather than by default.
