# ops/ — Observability (multi-operator)

- `events-<machine>.jsonl` — appended automatically by hooks on every agent
  dispatch/return. One file PER MACHINE so two operators never merge-conflict.
  Committed to git: that is how each side sees the other's activity.
- `log_event.py` — the hook target. Append-only, never breaks a session.
- `dashboard.py` — run `python ops/dashboard.py`, open http://localhost:8787.
  Merges YOUR live events with the other machine's last-pushed events
  (fetched from origin/main every 60s). Columns show which machine did what.
  - `python ops/dashboard.py --share` additionally auto-commits and pushes
    this machine's event file every 60s, so the other operator sees you
    near-live. Run --share on both machines for a mutual live view.
- Freshness rule: remote activity is only as fresh as the last push.
  --share (60s) or /handover (session end) are what push.
- True real-time view of the OTHER machine's dashboard (optional, still
  free): a private network tool like Tailscale lets you open their
  localhost:8787 directly - check current plan terms at tailscale.com.
- Terminal equivalent: `/ops` inside Claude Code.
