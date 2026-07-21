---
description: >-
  /gitflow — Report on branch state, CI status, and ready-to-merge PRs.
  Shows current dev branch pending PRs, staging candidates with no blockers,
  and any main PRs awaiting your approval. Also handles hotfix merges.
---

## Gitflow Status Report

**Usage:**
```
/gitflow [--staging-ready] [--hotfix-merge]
```

### What it does

1. Fetches branch state from GitHub API.
2. Lists:
   - **dev pending:** PRs targeting dev (feature branches awaiting merge).
   - **staging ready:** PRs from dev → staging with all CI passing and no failing stories in ClickUp.
   - **main awaiting approval:** PRs to main waiting for your review.
   - **recent hotfixes:** any branches tagged `#hotfix` in the last 7 days.
3. Flags blockers: stories still in `Rework`, stories without completion notes, etc.

### Options

`--staging-ready`: Only show staging PRs that are unblocked (all stories Done + completion notes present).  
`--hotfix-merge`: After you review a hotfix PR, this cascades the merge down to staging and dev.

### Integration

Run this before deciding on a release. Ben runs it proactively before opening the staging PR.
