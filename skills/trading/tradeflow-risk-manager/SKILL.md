---
name: tradeflow-risk-manager
description: Manages risk parameters and live-mode eligibility checks for the TradeFlow paper trading agent.
category: trading
---
# TradeFlow Risk Manager

This skill provides tools to adjust risk parameters in the TradeFlow paper trading agent's strategy.yaml file and implements a live-mode eligibility checklist for transitioning from paper to live trading.

## Risk Parameter Adjustment

### Usage
```bash
hermes run tradeflow-risk-manager --action adjust --parameter <param_name> --value <new_value>
```

### Available Parameters
- `ema_fast`: Fast EMA period (bounds: 3-25)
- `ema_slow`: Slow EMA period (bounds: 10-100)
- `rsi_period`: RSI period (bounds: 5-30)
- `rsi_min`: Minimum RSI for entry (bounds: 40-70)
- `atr_mult`: ATR multiplier for stop loss (bounds: 0.5-5.0)
- `tp_mult`: TP multiplier for take profit (bounds: 1.0-10.0)
- `fraction`: Fraction of equity risked per trade (bounds: 0.005-0.05)

### Example
```bash
hermes run tradeflow-risk-manager --action adjust --parameter ema_fast --value 10
```

## Live-Mode Eligibility Checklist

### Usage
```bash
hermes run tradeflow-risk-manager --action check-live
```

### Conditions Checked
1. **Performance**: Rolling 60-day paper Sharpe ratio > 1.0
2. **Outperformance**: Total return beats BTC HODL by ≥200 basis points
3. **Approval**: Signed approval file exists (`.live-approved-{timestamp}.sig`)
4. **Drawdown**: Maximum drawdown < 20%
5. **Consistency**: Profit factor > 1.5 over last 50 trades

### Output
Returns a JSON object with:
- `eligible`: boolean
- `conditions`: object with each condition's status
- `recommendations`: list of actions to improve eligibility

## Files Modified
- Strategy file: `/Users/pharma6/felix-revenue/tradeflow-paper/strategy.yaml`
- Approval files: `/Users/pharma6/felix-revenue/tradeflow-paper/.live-approved-*.sig`

## Safety Features
- Parameter bounds validation prevents unsafe values
- Changes are logged to Telegram via hermes_comms
- Original strategy backed up before modification
- Live mode requires explicit approval file creation