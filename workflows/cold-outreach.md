# Cold Outreach Workflow

Find → enrich → personalize → send → follow-up. Designed for low-volume,
high-quality B2B outreach (AI consulting, automation services).

## Stages

1. **Source** — pull a target list from one of: LinkedIn Sales Nav export,
   Apollo, GitHub stargazers of a relevant repo. Cap each batch at 50.
2. **Enrich** — append firmographics (size, funding, tech stack) via Clearbit
   or a free fallback (Apollo's free tier + company-name → Crunchbase).
3. **Score** — Claude rates each lead 1-5 against an ICP rubric. Keep 4-5s.
4. **Personalize** — pull a recent public signal (blog post, hiring, raised
   round) and write a one-liner referencing it.
5. **Draft** — short 3-line email; never longer than 70 words.
6. **Send** — through your warm inbox (Mailwarm, Instantly). Throttle to
   <40 sends/day per inbox.
7. **Follow up** — 2 touches max, 4 + 7 days, then bench for 90 days.

## Skills used

- `research/research-source-tools` — discover prospects from public signals.
- `sales/*` — copywriting + reply classification.
- `email/*` — send + threading helpers.

## Compliance

- CAN-SPAM / GDPR: include unsubscribe + physical address footer.
- Always verify email deliverability (Hunter, NeverBounce) before sending.
- Never scrape contact info from sources that disallow it in their ToS.

## What does NOT work

- Mass spray sequences > 4 touches.
- Generic "I noticed your company is doing well…" openings.
- Selling a service without naming a specific pain.
