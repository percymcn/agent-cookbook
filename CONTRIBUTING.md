# Contributing

Thanks for the interest. The cookbook is curated — small repo, high signal.

## What we accept

- **New skills** — single `SKILL.md` with a clear `Use when …` description, a
  short body (~200–800 words), and a working code/CLI example.
- **Playbooks** — long-form market or operations breakdowns, no client/contact
  data, no logs.
- **Workflows** — runnable end-to-end recipes that connect 2+ skills.

## What we reject

- Anything containing API keys, tokens, real emails, phone numbers, customer
  data, contact lists, outreach logs, or production credentials.
- Skills that are just thin wrappers around a single API call with no usage
  rules.
- Generic "AI assistant" essays.

## House style

- YAML frontmatter with `name` and `description`. Description is one sentence,
  starts with a usage trigger ("Use when ...").
- Body in plain Markdown. Code blocks tagged with the language.
- Prefer CLI/Python examples over screenshots.

## Validation

Before opening a PR:

```bash
python3 scripts/validate_repo.py
```

The script exits non-zero if structure is broken or it spots a secret-looking
string anywhere in the repo.
