# Example: self-improving-agent (dry-run)

Mirrors [`workflows/self-improving-agent.md`](../../workflows/self-improving-agent.md).
Runs the same skill-health scoring rubric used in production, but against
this repo's own `skills/` tree. Emits a per-skill JSON snapshot and a
ranked markdown backlog.

No model call, no network — the loop is structural metadata scoring.

## Run

```bash
python3 run.py
```

## Expected output

```
[dry-run] skills scanned: 95
[dry-run] avg score: 92.3
[dry-run] worst 3: [('skills/.../SKILL.md', 50), ('skills/.../SKILL.md', 60), ('skills/.../SKILL.md', 75)]
[dry-run] artifacts: .../examples/self-improving-agent/out
```

(Exact numbers depend on the current skill library.)

## What a real deployment replaces

| Dry-run                                | Production                                                     |
| -------------------------------------- | -------------------------------------------------------------- |
| `--skills-dir` defaults to `../skills` | `~/.hermes/skills` on the live operator machine                |
| Single one-shot run                    | `~/.hermes/scripts/self-improve.sh` on cron / launchd          |
| Backlog written to `out/backlog.md`    | Backlog merged with session summaries → Hermes work queue      |
| —                                      | Claude rewrites the worst-scoring skill descriptions in place  |
