#!/usr/bin/env python3
"""Dry-run of the newsletter-pipeline workflow.

Reads a week of fixture trend signals, ranks them, generates an outline +
600-word draft + 5 headline variants + preheader, writes a Beehiiv-ready
edition to out/edition.md. No Beehiiv API call. No subscribers.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def rank(signals: list[dict]) -> list[dict]:
    return sorted(signals, key=lambda s: s["score"], reverse=True)


def outline(top: dict) -> dict:
    return {
        "big_idea":   "Small, single-purpose agents are quietly winning over framework stacks.",
        "supporting": [
            f"Signal: {top['title']}",
            "Caching + tighter tool surfaces > bigger orchestrators.",
            "What this means if you're building this quarter.",
        ],
        "cta": "Reply with your stack. I read every one.",
    }


def headlines() -> list[str]:
    return [
        "Small agents are quietly winning",                       # 31
        "The 60-line agent that ate a RAG stack",                 # 37
        "Why your framework feels heavier this month",            # 44
        "Frameworks are getting unbundled — here's the read",     # 51
        "One signal, three lessons, no fluff",                    # 36
    ]


def draft(top: dict, plan: dict) -> str:
    today = date.today().isoformat()
    body = f"""# {plan['big_idea']}

_{today} edition_

This week the loudest signal was: **{top['title']}** (score {top['score']}, source {top['source']}).

It rhymes with three other items on my radar:

1. {plan['supporting'][1]}
2. {plan['supporting'][2]}
3. The unbundling of monolith agent stacks into focused libraries.

**Why it matters.** The bottleneck for shipping a useful agent in 2026 is
not model quality — it's how much of the orchestration layer you can throw
away without losing reliability. Teams that strip down to a small loop +
tool-use + caching consistently ship faster and pay less.

**What to do this week.** Pick one workflow you currently run through a
heavy framework. Rewrite the same loop in <100 lines using only the
SDK + a couple of tools. Measure latency and cost before and after.

If the rewrite wins, you have your migration plan. If it loses, you
learned exactly which framework feature was earning its keep.

> CTA: {plan['cta']}
"""
    return body


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--fixture", default=str(HERE / "fixtures" / "signals.json"))
    ap.add_argument("--out", default=str(HERE / "out" / "edition.md"))
    args = ap.parse_args()

    signals = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    ranked = rank(signals)
    top = ranked[0]
    plan = outline(top)
    body = draft(top, plan)
    titles = headlines()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(body, encoding="utf-8")
    (out.parent / "headlines.json").write_text(
        json.dumps({"variants": titles, "chosen": titles[0]}, indent=2),
        encoding="utf-8",
    )

    print(f"[dry-run] top signal: {top['title']!r}")
    print(f"[dry-run] headline variants: {len(titles)} (chosen: {titles[0]!r})")
    print(f"[dry-run] edition: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
