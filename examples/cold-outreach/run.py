#!/usr/bin/env python3
"""Dry-run of the cold-outreach workflow.

Reads a fixture lead list, scores against an ICP rubric, writes a draft
3-line email per qualified lead to out/drafts/. NEVER SENDS. All domains
in the fixture are *.test, which RFC 6761 reserves and which no real MX
record will accept.

In prod the orchestrator would replace:
  - fixture leads → Apollo / Sales Nav / GitHub stargazer scrape
  - rubric scoring → Claude rubric run with citations to lead.signal
  - draft writer → Claude personalized opener referencing lead.signal
  - file writer → Mailwarm / Instantly send via warm inbox (throttled)
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def icp_score(lead: dict) -> int:
    """1-5 against ICP: 25-500 ppl, post-seed, has a public signal we can hook."""
    score = 0
    if 25 <= lead["size"] <= 500:
        score += 2
    elif lead["size"] < 25:
        score += 1
    if lead["funding_stage"] in ("seed", "series_a", "series_b"):
        score += 2
    if lead.get("signal") and lead["signal"] != "none":
        score += 1
    return min(score, 5)


def draft_email(lead: dict) -> str:
    signal = lead["signal"] if lead.get("signal") and lead["signal"] != "none" else "your recent work"
    return (
        f"Subject: quick note on {lead['company']}\n"
        f"\n"
        f"Hi {lead['name'].split()[0]},\n"
        f"\n"
        f"Saw {signal} — nice. We help teams your size automate the boring "
        f"second-touch on outbound so reps focus on replies.\n"
        f"\n"
        f"Worth a 10-min look this week?\n"
        f"\n"
        f"— pharma6\n"
        f"\n"
        f"--\n"
        f"To unsubscribe, reply STOP. Mailing address: 1 Example Way, Test City.\n"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True,
                    help="Always on — this example NEVER sends.")
    ap.add_argument("--fixture", default=str(HERE / "fixtures" / "leads.json"))
    ap.add_argument("--out", default=str(HERE / "out"))
    ap.add_argument("--min-score", type=int, default=4)
    args = ap.parse_args()

    leads = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    out_dir = Path(args.out)
    draft_dir = out_dir / "drafts"
    draft_dir.mkdir(parents=True, exist_ok=True)

    report = {"scored": [], "drafts": []}
    for lead in leads:
        s = icp_score(lead)
        report["scored"].append({"company": lead["company"], "score": s})
        if s >= args.min_score:
            fname = lead["company"].lower().replace(" ", "-") + ".eml"
            (draft_dir / fname).write_text(draft_email(lead), encoding="utf-8")
            report["drafts"].append(fname)

    (out_dir / "report.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"[dry-run] scored {len(leads)} leads")
    print(f"[dry-run] scores: {report['scored']}")
    print(f"[dry-run] drafts written (NOT SENT): {report['drafts']}")
    print(f"[dry-run] artifacts: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
