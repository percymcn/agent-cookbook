#!/usr/bin/env python3
"""Dry-run of the tradeflow-research-pipeline workflow.

Reads a fixture premarket snapshot, applies the same filter rules the prod
pipeline uses (>4% gap, float <50M, sector filter), computes ATR-based
brackets, and writes a one-page markdown gameplan. No Polygon / Unusual
Whales / news API / Resend / Telegram traffic.
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def gap_pct(row: dict) -> float:
    return (row["premarket"] - row["prev_close"]) / row["prev_close"] * 100.0


def pass_filter(row: dict) -> tuple[bool, str]:
    g = gap_pct(row)
    if g < 4.0:
        return False, f"gap {g:.1f}% < 4%"
    if row["float_m"] >= 50.0:
        return False, f"float {row['float_m']}M >= 50M"
    if row["sector"] == "biotech" and "FDA" not in row["catalyst"] and "earnings" not in row["catalyst"].lower():
        return False, "biotech without binary catalyst"
    return True, "ok"


def risk_plate(row: dict) -> dict:
    entry = round(row["premarket"], 2)
    stop  = round(entry - row["atr14"], 2)
    t1    = round(entry + row["atr14"], 2)
    t2    = round(entry + 2 * row["atr14"], 2)
    return {"entry": entry, "stop": stop, "t1": t1, "t2": t2}


def render(survivors: list[dict]) -> str:
    today = date.today().isoformat()
    lines = [f"# Pre-market gameplan — {today}", ""]
    if not survivors:
        lines.append("_No tickers cleared the filter today._")
        return "\n".join(lines) + "\n"
    for s in survivors:
        rp = s["risk"]
        lines += [
            f"## {s['ticker']}  ({gap_pct(s):+.1f}% gap)",
            f"- **Catalyst**: {s['catalyst']}",
            f"- **Float**: {s['float_m']}M  |  **ATR(14)**: {s['atr14']}",
            f"- **Entry** {rp['entry']}  **Stop** {rp['stop']}  **T1** {rp['t1']}  **T2** {rp['t2']}",
            f"- **Invalidation**: close below {rp['stop']} on 5m candle.",
            "",
        ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True)
    ap.add_argument("--fixture", default=str(HERE / "fixtures" / "premarket.json"))
    ap.add_argument("--out", default=str(HERE / "out" / "gameplan.md"))
    args = ap.parse_args()

    rows = json.loads(Path(args.fixture).read_text(encoding="utf-8"))
    survivors, dropped = [], []
    for r in rows:
        ok, reason = pass_filter(r)
        if ok:
            r["risk"] = risk_plate(r)
            survivors.append(r)
        else:
            dropped.append({"ticker": r["ticker"], "reason": reason})

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render(survivors), encoding="utf-8")

    print(f"[dry-run] scanned {len(rows)} tickers")
    print(f"[dry-run] survivors: {[s['ticker'] for s in survivors]}")
    print(f"[dry-run] dropped:   {dropped}")
    print(f"[dry-run] artifact:  {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
