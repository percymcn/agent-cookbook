---
name: tradeflow-paper
description: "Build and operate a paper-mode self-improving trading agent for BTC/USDT with parametric strategy optimization and safety gates."
version: 1.0.0
author: Hermes Agent
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [trading, paper-trading, self-improving, strategy-optimization, risk-management]
    homepage: https://hermes-agent.nousresearch.com/
    related_skills: [gideon-autonomous-prospector, autonomous-business-system, ai-pdf-guide-business]
---

# TradeFlow Paper Trading Agent Skill

This skill creates and manages a paper-trading agent for BTC/USDT that continuously improves its strategy through reflection loops, with strict safety gates to prevent accidental live deployment.

## Overview

The tradeflow-paper skill sets up a self-improving trading agent that:
- Trades BTC/USDT in paper mode only (no live broker)
- Uses a parametric strategy with EMA, RSI, ATR-based stops and targets
- Improves via reflection loops every 25 closed trades (adjusting one parameter at a time)
- Includes multiple safety layers: mode gate, kill switch, Telegram heartbeat
- Persists strategy, trade journal, and reflection history
- Provides observability via status subcommand and logs

## Directory Structure

After installation, the skill creates:
- `~/.hermes/skills/tradeflow-paper/` - Skill files (this directory)
- `~/felix-revenue/tradeflow-paper/` - Worker code and runtime data

## Installation

This skill is installed via the Hermes skill system. Once installed, it provides:
- `/skill tradeflow-paper` - Load the skill in session
- `hermes cron create ...` - To schedule the worker (see Usage)

## Usage

### 1. Start the Paper Trading Worker

The skill includes a cron job template to run the worker continuously. To start:

```bash
hermes cron create "every 5m" \
  --name "tradeflow-paper-worker" \
  --prompt "Run the tradeflow-paper worker: cd ~/felix-revenue/tradeflow-paper && python3 worker.py --mode paper" \
  --skills tradeflow-paper \
  --deliver local
```

### 2. Check Status

```bash
cd ~/felix-revenue/tradeflow-paper && python3 worker.py --status
```

### 3. View Logs

Logs are stored in `~/felix-revenue/tradeflow-paper/logs/`

### 4. Manual Reflection Trigger

```bash
cd ~/felix-revenue/tradeflow-paper && python3 worker.py --reflect
```

### 5. Kill Switch

To stop trading immediately, create the halt file:
```bash
touch ~/felix-revenue/tradeflow-paper/.halt
```

Remove it to resume:
```bash
rm ~/felix-revenue/tradeflow-paper/.halt
```

## Configuration

The skill requires no initial configuration. All parameters are defined in the strategy.yaml file that gets created on first run.

## Safety Features

### Mode Gate (Paper-Only Default)
- The agent starts in paper mode and remains there unless all three live-mode conditions are met:
  1. Rolling 60-day paper Sharpe > 1.0
  2. Total return beats BTC HODL by ≥200 bps
  3. Signed approval file exists for the current strategy version
- No environment variable can override this gate.

### Kill Switch
- Presence of `~/felix-revenue/tradeflow-paper/.halt` stops the worker immediately.

### Telegram Heartbeat
- The worker sends a heartbeat via the existing hermes_comms bridge on each reflection cycle.

## Persistence

- `strategy.yaml` - Current parameter values (git-tracked in the project)
- `journal.jsonl` - Every paper trade (entry, exit, PnL, timestamps)
- `state/history/` - Archived strategy.yaml versions after each reflection
- `state/reflections.md` - Rationale for each parameter change

## Reflection Loop

- Triggered every 25 closed paper trades
- Reads last 25 trades + current strategy.yaml
- Proposes a change to ONE parameter (knob) within its bounds
- Writes rationale and commits new strategy.yaml
- Never changes multiple knobs simultaneously

## Strategy Template (Parametric)

- Entry: EMA(fast) crosses above EMA(slow) AND RSI(period) > rsi_min
- Exit: ATR-based stop at entry − atr_mult×ATR, take-profit at entry + tp_mult×ATR
- Sizing: fixed fraction of paper equity per trade
- Tunable knobs with bounds:
    ema_fast [3, 25], ema_slow [10, 100], rsi_period [5, 30],
    rsi_min [40, 70], atr_mult [0.5, 5.0], tp_mult [1.0, 10.0],
    fraction [0.005, 0.05]
- Initial values: ema_fast=12, ema_slow=26, rsi_period=14, rsi_min=50, atr_mult=1.5, tp_mult=3.0, fraction=0.02

## Worker Code

The skill includes a template for the worker code that gets copied to `~/felix-revenue/tradeflow-paper/worker.py` on first run. The worker implements:
- CCXT paper trading for BTC/USDT
- Strategy engine with the parametric template
- Trade execution and journaling
- Reflection loop logic
- Safety checks (halt file, mode gate)
- Telegram heartbeat via hermes_comms
- Status reporting

## Dependencies

The worker requires:
- Python 3.8+
- ccxt
- pandas
- numpy
- ta-lib (optional, for indicator fallback)
- pyyaml

These should be installed in the felix-revenue environment. If missing, the worker will attempt to install them via pip.

## Notes

- This skill does NOT enable live trading. Live mode requires manual approval and meeting strict performance criteria.
- The agent is designed to run indefinitely, improving its strategy over time.
- All financial amounts are synthetic in paper mode (starting equity: $10,000).

## Example Output

After running for a while, the status command might show:
```
Paper Equity: $12,450.32
Last 5 Trades:
  1. Bought at 62,100.00, Sold at 63,500.00, PnL: +$225.50
  2. Bought at 63,200.00, Sold at 62,800.00, PnL: -$80.00
  ...
Current Strategy:
  ema_fast: 12, ema_slow: 26, rsi_period: 14, rsi_min: 50, atr_mult: 1.5, tp_mult: 3.0, fraction: 0.02
Last Reflection: 2026-05-23 14:30:00 - Increased ema_slow from 24 to 26 based on recent win rate
```

## References

- [Felix Browser Task API](references/felix-browser-task-api.md) - For when you need browser automation
- [Telegram Notification Workaround](references/telegram-notification-workaround.md) - For direct Telegram messaging
- [Communication Style Validation](references/communication_style_validation.md) - User preferences for this agent
- [F-string Syntax Fix](references/fstring_syntax_fix.md) - Common Python f-string syntax error and solution
- [Exchange Restrictions Workaround](references/exchange_restrictions_workaround.md) - Handling API restrictions with mock data fallback