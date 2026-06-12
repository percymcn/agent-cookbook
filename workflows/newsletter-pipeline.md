# Newsletter Pipeline

Weekly newsletter production loop on top of Beehiiv.

## Stages

1. **Ideation** — pull a week's worth of trend signals from your domain (Reddit, HN, niche subs, X).
2. **Outline** — Claude proposes 3 angles + headline candidates.
3. **Draft** — write a 600-900 word edition: one big idea, 3 supporting points, one CTA.
4. **Headline test** — generate 5 variants, pick the one with strongest curiosity gap.
5. **Send** — via Beehiiv API; schedule for Tuesday 09:00 in subscriber TZ.
6. **Measure** — log open rate + click rate to your analytics store.
7. **Iterate** — every 4 editions, review what cohort liked most.

## Skills used

- `research/blogwatcher` — surface fresh signal.
- `creative/*` — drafting and headline variants.
- `email/*` — Beehiiv API wrapper.

## House rules

- One CTA per edition. Never two.
- Headline ≤ 60 chars (preheader picks up slack).
- Subject line + preheader written together — they're one unit.

## Common failure modes

- Drafting without a recent-week trend signal → forgettable issues.
- Burying the CTA at the end after fluff.
- Forgetting to set the `from` name; deliverability tanks.
