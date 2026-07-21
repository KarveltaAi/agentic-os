---
name: ship-static-site
description: Use when deploying a static website or landing page for a client at zero hosting cost.
---
# Ship a static site (near-zero cost)

1. Build output to /dist (or /out). No server-side secrets in the bundle.
2. Host options, in order of preference (all have free tiers as of mid-2026;
   verify current limits before promising a client):
   - Cloudflare Pages (generous free tier, custom domains, fast global CDN)
   - GitHub Pages (public repos free; fine for brochure sites)
   - Netlify / Vercel free tiers (watch bandwidth caps for client traffic)
3. Connect the client repo → auto-deploy on push to main.
4. Custom domain: client buys/owns the domain in THEIR registrar account
   (never yours — avoids handover pain and lock-in).
5. Done-criteria: HTTPS live, client-owned domain, deploy-on-push proven,
   rollback tested (revert commit), handover pack updated with access notes.
