# Runnable examples

One safe, dry-run example per workflow in `../workflows/`. All examples are
stdlib-only Python — no paid APIs, no network calls, no credentials, no real
outreach or publishing. Each writes its output under its own `out/` directory.

| Example                                                              | Mirrors workflow                                  |
| -------------------------------------------------------------------- | ------------------------------------------------- |
| [`faceless-video-engine/`](faceless-video-engine/)                   | `workflows/faceless-video-engine.md`              |
| [`tradeflow-research-pipeline/`](tradeflow-research-pipeline/)       | `workflows/tradeflow-research-pipeline.md`        |
| [`cold-outreach/`](cold-outreach/)                                   | `workflows/cold-outreach.md`                      |
| [`newsletter-pipeline/`](newsletter-pipeline/)                       | `workflows/newsletter-pipeline.md`                |
| [`self-improving-agent/`](self-improving-agent/)                     | `workflows/self-improving-agent.md`               |

## Running all examples

```bash
python3 scripts/validate_repo.py
```

The validator executes every example in `--dry-run` mode and asserts an artifact
was produced. Each example's own `README.md` lists the single command to run it
and the section of the real workflow it stands in for.
