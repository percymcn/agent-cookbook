# agent-cookbook

Production-ready Claude / AI-agent skills, playbooks, and workflows extracted from a
working operator stack — pharma6's automation lab covering content production,
trading research, cold outreach, newsletter ops, and self-improving agents.

> Everything in this repo has been sanitized (no secrets, contact lists, or private
> client data) and is meant to be copied, adapted, and shipped.

## What's inside

| Path           | Contents                                                              |
| -------------- | --------------------------------------------------------------------- |
| `skills/`      | `SKILL.md` files grouped by category (research, devops, trading…).    |
| `playbooks/`   | Long-form market / business / monetization playbooks.                 |
| `workflows/`   | End-to-end how-to docs that wire skills + tools into a runnable flow. |
| `scripts/`     | Build + validation utilities for the repo itself.                     |

## Quickstart

```bash
# clone, then validate the repo layout
python3 scripts/validate_repo.py

# (re)build from the source skill library on your local machine
python3 scripts/build_cookbook.py
```

## Installing skills

```bash
# list all available skills and categories
python3 scripts/install_skill.py --list

# preview what an install would do (no files changed)
python3 scripts/install_skill.py --skill domain --dry-run

# install a single skill into ~/.hermes/skills (default target)
python3 scripts/install_skill.py --skill domain

# install every skill in a category
python3 scripts/install_skill.py --category trading

# install to a custom directory
python3 scripts/install_skill.py --skill domain --target ~/my-agent/skills
```

If the destination already exists, a timestamped backup is created automatically before overwriting.

## Skill format

Each skill lives at `skills/<category>/<skill-name>/SKILL.md` with YAML frontmatter:

```markdown
---
name: my-skill
description: "Use when the user wants X. Provides Y by calling Z."
---

# Skill body, examples, safety notes…
```

Claude / Claude Code (and most agent runners) load skills by name + description, so a
sharp `"Use when ..."` trigger is the single highest-leverage edit you can make.

## Workflows (start here)

Every workflow has a runnable dry-run example under [`examples/`](examples/).
Examples are stdlib-only, never call paid APIs, never send / publish, and
write artifacts to their own `out/` directory.

| Workflow                                                                                       | Runnable example                                                              |
| ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| [`workflows/faceless-video-engine.md`](workflows/faceless-video-engine.md)                     | [`examples/faceless-video-engine/`](examples/faceless-video-engine/)           |
| [`workflows/tradeflow-research-pipeline.md`](workflows/tradeflow-research-pipeline.md)         | [`examples/tradeflow-research-pipeline/`](examples/tradeflow-research-pipeline/) |
| [`workflows/cold-outreach.md`](workflows/cold-outreach.md)                                     | [`examples/cold-outreach/`](examples/cold-outreach/)                           |
| [`workflows/newsletter-pipeline.md`](workflows/newsletter-pipeline.md)                         | [`examples/newsletter-pipeline/`](examples/newsletter-pipeline/)               |
| [`workflows/self-improving-agent.md`](workflows/self-improving-agent.md)                       | [`examples/self-improving-agent/`](examples/self-improving-agent/)             |

Run any one:

```bash
python3 examples/faceless-video-engine/run.py
```

Run all (via the validator):

```bash
python3 scripts/validate_repo.py
```

## License

MIT. See [LICENSE](LICENSE).

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Short version: open a PR with a new
skill/playbook + a one-line entry in this README's workflow table if it's a
top-level flow.
