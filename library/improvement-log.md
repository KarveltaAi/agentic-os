# Improvement Log

Every OS upgrade lands here via /retro. Newest first.

| Date | Change | Evidence that prompted it | Expected effect |
|---|---|---|---|
| 2026-09-23 | Rolled back v5 Gitflow approvals: removed dev/staging rulesets, main keeps only no-force-push + no-delete; dropped staging/main-deploy workflows; /gitflow is now a solo dev→main fast-forward | release stuck: rulesets required 1 approving review and GitHub blocks self-approval, so all PRs were permanently BLOCKED | a solo operator can ship; Vera's PASS stays the quality gate |
| 2026-07-11 | v2.1: client isolation, skills library, /retro, /backup, cost policy | design review of CEO concerns | agency-safe, portable, self-improving |
