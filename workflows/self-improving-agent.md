# Self-Improving Agent Loop

How Hermes (the orchestrator behind this cookbook) inspects its own skill
library and queues fixes. The same pattern works for any Claude-based agent
that maintains a folder of skills/playbooks.

## Files

The loop lives in `~/.hermes/`:

```
~/.hermes/
├── brain/
│   ├── manifest.json
│   ├── sessions/          ← one .json per session (decisions, next-actions)
│   ├── health/            ← skill-health JSON + markdown reports
│   └── backlog/           ← ranked improvement queue
└── scripts/
    ├── session-summarizer.py
    ├── skill-health-scanner.py
    ├── improvement-loop.py
    └── self-improve.sh
```

## Stages

1. **Session summarizer** — at session end, dump decisions, artifacts, and
   next-actions into `brain/sessions/<date>-<slug>.json`.
2. **Skill-health scanner** — walk `~/.hermes/skills`, score each `SKILL.md`
   on frontmatter, description quality, in-skill ref integrity, and recency.
   Writes `brain/health/skills-<ts>.json` + `latest.json`.
3. **Improvement loop** — fuse latest health snapshot with the last 14d of
   sessions. Output a ranked backlog in `brain/backlog/`.
4. **Runner** — `self-improve.sh` invokes (2) and (3) end-to-end; safe to
   call from cron or launchd.

## Scoring rubric (skill-health-scanner)

- Missing SKILL.md or frontmatter → -35.
- Description < 40 chars → -40 ; > 600 chars → -10.
- Description lacks "Use when ..." trigger → -15.
- Generic adjectives ("useful", "various") → -5 each.
- Broken in-skill references → up to -20.
- Stale (> 120d untouched) → -5.

## Wiring

```bash
# manual run
~/.hermes/scripts/self-improve.sh

# cron (daily 07:00 local)
crontab -e
# add:
0 7 * * * /Users/me/.hermes/scripts/self-improve.sh >/dev/null 2>&1
```

## Why it works

The bottleneck for agent quality is usually not the model — it's the metadata
the model reads to decide which skill to load. By keeping that metadata
under continuous review, the agent's routing accuracy improves on its own.
