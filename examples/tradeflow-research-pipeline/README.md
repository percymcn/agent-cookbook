# Example: tradeflow-research-pipeline (dry-run)

Mirrors [`workflows/tradeflow-research-pipeline.md`](../../workflows/tradeflow-research-pipeline.md).
Reads a fixture premarket snapshot, runs the same filter rules + ATR risk
plate the production pipeline uses, and writes a one-page markdown gameplan.

No Polygon / Unusual Whales / news API / Resend / Telegram traffic.

## Run

```bash
python3 run.py
```

## Expected output

```
[dry-run] scanned 5 tickers
[dry-run] survivors: ['ABCD', 'EFGH', 'MNOP']
[dry-run] dropped:   [{'ticker': 'IJKL', 'reason': 'gap 1.8% < 4%'}, {'ticker': 'QRST', 'reason': 'float 240.0M >= 50M'}]
[dry-run] artifact:  .../examples/tradeflow-research-pipeline/out/gameplan.md
```

The gameplan lands at `out/gameplan.md` with one section per surviving ticker:
catalyst, float, ATR, entry/stop/T1/T2, and an explicit invalidation level.

## What a real deployment replaces

| Dry-run                              | Production                                         |
| ------------------------------------ | -------------------------------------------------- |
| `fixtures/premarket.json`            | Polygon.io premarket OHLC + ATR(14) + avg volume   |
| Hard-coded catalyst strings          | Unusual Whales option flow + news API + Claude summary |
| Markdown to `out/`                   | Resend email + Telegram push at 08:30 ET           |
