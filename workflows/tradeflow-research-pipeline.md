# TradeFlow Research Pipeline

Pre-market research routine that turns market data + news into a same-day
trade gameplan. Built on Polygon.io, Unusual Whales, and Claude.

## Inputs

- Polygon: previous close, premarket OHLC, ATR(14), avg volume.
- Unusual Whales: option flow ranked by premium, repeat tickers in the last 5 sessions.
- News: top-5 catalysts per ticker via a news API + Claude summarization.

## Stages

1. **Universe build** — scan for premarket gappers > 4% with float < 50M.
2. **Filter** — drop biotech / SPAC unless catalyst is binary (FDA, earnings).
3. **Catalyst attach** — for each survivor, find the 1-line "why" via news search.
4. **Risk plate** — for each ticker, compute entry / stop / first target using
   ATR-based brackets.
5. **Gameplan write** — Claude formats a 1-page markdown briefing.
6. **Deliver** — email via Resend + Telegram push at 08:30 ET.

## Skills used

- `trading/tradeflow-pipeline` — orchestrator.
- `trading/tradeflow-risk-manager` — bracket sizing.
- `research/*` — news search and summarization.

## Notes

- Keep the gameplan to one page. Long briefings get ignored at the open.
- Always include the invalidation level — without it the call is not actionable.
- Cache premarket data once at 08:00 ET; re-querying live in the loop adds
  latency and Polygon quota burn.
