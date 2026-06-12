# Example: newsletter-pipeline (dry-run)

Mirrors [`workflows/newsletter-pipeline.md`](../../workflows/newsletter-pipeline.md).
Ranks a fixture week of trend signals, drafts a ~600-word edition with one big
idea + three supports + one CTA, and emits 5 headline variants. No Beehiiv
API call. No subscribers.

## Run

```bash
python3 run.py
```

## Expected output

```
[dry-run] top signal: 'Smol agents > giant frameworks: a thread'
[dry-run] headline variants: 5 (chosen: 'Small agents are quietly winning')
[dry-run] edition: .../examples/newsletter-pipeline/out/edition.md
```

`out/edition.md` is the Beehiiv-ready markdown; `out/headlines.json` holds the
5 candidate titles + the chosen one.

## What a real deployment replaces

| Dry-run                              | Production                                                |
| ------------------------------------ | --------------------------------------------------------- |
| `fixtures/signals.json`              | `research/blogwatcher` skill against Reddit / HN / niche subs / X |
| Hand-rolled `outline()` / `draft()`  | Claude outline + draft + 5-variant headline test          |
| File write to `out/edition.md`       | Beehiiv API POST, scheduled Tue 09:00 in subscriber TZ    |
| —                                    | Open + click rate logged to analytics; iterate every 4 editions |
