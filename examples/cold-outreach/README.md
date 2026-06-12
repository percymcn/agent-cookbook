# Example: cold-outreach (dry-run, NEVER sends)

Mirrors [`workflows/cold-outreach.md`](../../workflows/cold-outreach.md).
Scores a fixture lead list against an ICP rubric and writes draft `.eml`
files to `out/drafts/`. No mail server is touched.

The fixture uses `*.test` domains (RFC 6761 reserved). They cannot accept
mail even if the script were modified to send.

## Run

```bash
python3 run.py
```

## Expected output

```
[dry-run] scored 4 leads
[dry-run] scores: [{'company': 'Northwind Robotics', 'score': 5}, {'company': 'Acme Geo', 'score': 4}, {'company': 'BluePine Foods', 'score': 0}, {'company': 'Mintleaf Labs', 'score': 2}]
[dry-run] drafts written (NOT SENT): ['northwind-robotics.eml', 'acme-geo.eml']
[dry-run] artifacts: .../examples/cold-outreach/out
```

Each draft is a 3-line email with a signal-referenced opener, a single ask,
and a CAN-SPAM-style footer.

## What a real deployment replaces

| Dry-run                                | Production                                          |
| -------------------------------------- | --------------------------------------------------- |
| `fixtures/leads.json`                  | Apollo / LinkedIn Sales Nav export / GitHub stargazers |
| Hand-rolled `icp_score()`              | Claude rubric run with cited evidence per lead      |
| Hand-rolled `draft_email()`            | Claude personalized opener referencing each signal  |
| Drafts written to `out/drafts/`        | Mailwarm / Instantly send via warm inbox (throttle <40/day) |
| No follow-up                           | 2-touch follow-up at 4 + 7 days, bench 90 days      |
