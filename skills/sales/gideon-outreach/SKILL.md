---
name: gideon-outreach
description: Automated outreach system for Gideon's AI content repurposing business
version: 1.2.0
author: Hermes Agent
categories: sales, outreach, automation
---

# Gideon Outreach Skill

Automated outreach system for Gideon's AI content repurposing business. Handles personalized initial outreach, follow-up messages, and response tracking for prospects.

## When to Use

Use this skill to run Gideon's automated outreach cycle, which sends personalized emails to prospects who need initial contact or follow-up based on their last contact date.

## Preflight Check

Before running the cycle, audit prospect state and daily limit. Use the built-in preflight script:

```bash
cd ~/gideon_ai_business && python3 scripts/cron_preflight.py
```

Expected output format:
```
Total:801 Init:91 SentNR:705 FullCycle:481 Resp:0
Daily:50/100 Reset:2026-06-09
Actually logged today: 50
  2026-06-09T17:02:30.481134 | Fresh Realty Expert 101706 | follow_up_2
Last research: 2026-06-09T17:04:48.813544
Total researched: 801
```

If daily count is already at 100, the cycle will produce zero sends (runs harmlessly).

## Steps

1. **Initialize**: Load prospects data, outreach log, and templates from the Gideon AI business directory.
2. **Reset Daily Counter**: If it's a new day, reset the daily message counter.
3. **Identify Prospects Needing Contact**:
   - Prospects that have not received initial outreach (`outreach_sent: false`).
   - Prospects that need follow-up based on time since last contact (2 days for first follow-up, 4 days for second follow-up).
4. **Personalize Message**: Use the appropriate template (initial_outreach, follow_up_1, follow_up_2) and fill in prospect details (name, business, niche, etc.).
5. **Send Email**: Send the personalized email (currently simulated; in production configure SMTP credentials in `.env`).
6. **Update Records**:
   - Mark prospect as contacted, update `last_contact`.
   - Increment follow-up count for follow-up messages.
   - Log the sent outreach in outreach log.
   - Respect daily limit (default 100 messages per day).
7. **Save Data**: Persist updated prospects and outreach log to JSON files.
8. **Report**: Output summary of messages sent, daily total, and next reset date.

## Templates

The system uses three email templates stored in `prospects/outreach_templates.json`:
- `initial_outreach`: First contact offering a free content audit.
- `follow_up_1`: Sent 2 days after initial if no response.
- `follow_up_2`: Sent 4 days after initial if no response, offering a free week of service.

## Pitfalls

### Stale-Due SentNR Prospects (Overdue Follow-ups)
The daily limit (100) prioritizes by `last_contact` date sorted oldest-first. When FullCycle (follow_up_2) sends dominate the daily budget, SentNR prospects queued for follow_up_1 can pile up and go **4-5 days overdue**. This is visible in the preflight as `SentNR:88 FullCycle:605` with the SentNR count staying flat while FullCycle grows. If the count is large and daily limit stays 100, it may take 2-3 days to clear the backlog. Track SentNR week-over-week to spot the drift.

### Pipeline Deep-Dive Diagnostics
When preflight shows 0 responses across 700+ prospects, run these diagnostics from `~/gideon_ai_business` to inspect pipeline health:

```python
# 1) Count prospects at each pipeline stage
prospects = json.load(open('prospects/prospects.json')).get('prospects', [])
init = [p for p in prospects if not p.get('outreach_sent')]
sent_fu0 = [p for p in prospects if p.get('outreach_sent') and p.get('follow_up_count', 0) == 0]
fu1 = [p for p in prospects if p.get('follow_up_count', 0) == 1]
fu2 = [p for p in prospects if p.get('follow_up_count', 0) >= 2]
print(f'Init:{len(init)} SentFU0:{len(sent_fu0)} FU1:{len(fu1)} FU2+:{len(fu2)}')

# 2) Verify actual vs reported daily sends
log = json.load(open('prospects/outreach_log.json'))
today = date.today().isoformat()
actual = [m for m in log.get('outreach_sent', []) if m.get('sent_date','').startswith(today)]
print(f'Logged today: {len(actual)} (by type: {dict(Counter(m.get("outreach_type") for m in actual))})')

# 3) Check field name consistency across prospect database
print(f'nich:{sum(1 for p in prospects if p.get("nich"))} niche:{sum(1 for p in prospects if p.get("niche"))}')
print(f'company:{sum(1 for p in prospects if p.get("company"))} business:{sum(1 for p in prospects if p.get("business"))}')
print(f'No email:{sum(1 for p in prospects if not p.get("email"))}')

# 4) Verify follow-up due dates using Python 3.9-compatible comparison
from datetime import datetime, timezone, timedelta
now = datetime.now(timezone.utc)
for p in sent_fu0[:3]:
    lc = p.get('last_contact','')
    lc_dt = datetime.fromisoformat(lc)
    if lc_dt.tzinfo is None:
        lc_dt = lc_dt.replace(tzinfo=timezone.utc)
    print(f'{p["name"]}: {lc[:19]}, age={(now-lc_dt).total_seconds()/3600:.1f}h, due={(now-lc_dt).total_seconds()>172800}')

# 5) Check total outreach ever sent, broken down by type
Counter(m.get('outreach_type') for m in log.get('outreach_sent', []))
```

### Python 3.9 `fromisoformat` Nuance
This system runs Python 3.9. `datetime.fromisoformat()` handles microsecond timestamps (`2026-06-06T22:22:40.263227`) correctly, but the result is **tz-naive**. The code at `src/automated_outreach.py` line 170 adds `tzinfo=timezone.utc` via `.replace()` to enable comparison with `datetime.now(timezone.utc)` (which is tz-aware). When writing ad-hoc analysis scripts, use the same pattern:
```python
lc_dt = datetime.fromisoformat(lc)
if lc_dt.tzinfo is None:
    lc_dt = lc_dt.replace(tzinfo=timezone.utc)
```
On Python 3.11+ the `.replace` is optional since `fromisoformat` returns tz-aware by default.

### Response Checking (No Dedicated Script)
There is no dedicated `scripts/check-responses.py` on disk. For response checking, read `prospects/outreach_log.json` directly and inspect `log['responses_received']` (list). Compare its length against `data/last_response_check.json` if that file exists.
- The live shortcut: `python3 -c "import json; l=json.load(open('prospects/outreach_log.json')); print(f'Responses: {len(l[\"responses_received\"])}')"` from the gideon directory.
- Work around the missing script with the inline Python approach — do NOT create one from scratch without being told.

### Daily Limit (100/100) Requires Multiple Runs to Exhaust
The 10-per-batch cap (`prospects_to_contact[:10]`) plus the 100 daily limit means exhausting the day's quota takes **5–10 separate invocations** of `python3 src/automated_outreach.py`. The system processes 10 prospects per call. Run the script repeatedly in a terminal loop until the preflight shows `Daily: 100/100`:
```bash
cd ~/gideon_ai_business
python3 scripts/cron_preflight.py  # check current count
python3 src/automated_outreach.py   # send 10
# repeat until Daily: 100/100
```
The earlier cron run may have consumed 30–50 of the daily budget already, so check preflight first before assuming you can send all 100.

### Daily Limit Reached — Verify Real Sends vs Stuck Counter
When the preflight shows `Daily: 100/100` but your `messages_sent_today` inspection shows 0, the counter is legitimate but the real log entries exist. You can verify by writing a quick helper script:

```python
import json
from datetime import date
with open('prospects/outreach_log.json') as f: l = json.load(f)
today = date.today().isoformat()
actual = [m for m in l.get('outreach_sent', []) if m.get('sent_date','').startswith(today)]
print(f'Actually logged today: {len(actual)}')
for m in actual[-3:]:
    print(f'  {m.get("sent_date","?")} | {m.get("prospect_name","?")} | {m.get("outreach_type","?")}')
```

The system processes 10 prospects per `run_outreach_cycle` call (hardcoded at line 193: `prospects_to_contact[:10]`), so it may take multiple days to work through a large backlog. The 100 daily limit is hit across multiple cron runs on the same day.

### Zero Responses Signal
If the preflight shows **0 responses** across 700+ prospects, the system has a pipeline issue:
- Templates may need A/B testing (open rate tracking requires real SMTP)
- The simulation mode (`send_email` at line 234 just prints) cannot capture inbound replies
- Consider retiring `FullCycle` prospects (2+ follow-ups with no response) to a quarterly re-engagement list
- The 10-per-cycle cap in `get_prospects_needing_outreach` means many prospects who *should* get follow-up 2 may never receive it if the initial batch is large

- **Daily Limit**: The system enforces a daily limit (100 messages). Once reached, no more are sent that day. Check above subsections for troubleshooting.
- **Template Personalization**: Ensure prospect data includes required fields (`name`, `company`, `niche`). Missing fields default to generic placeholders.
  - ⚠️ **Field name inconsistency**: Old prospects use `"nich"` and `"company"` fields; new fresh prospects use `"niche"` and `"business"` fields. The code at `src/automated_outreach.py` lines ~215-224 now handles both via fallback: `prospect.get("niche", prospect.get("nich", "your industry"))` and `prospect.get("business", prospect.get("company", "your business"))`. If prospects still show generic placeholders, check the JSON field names.
- **Timezone Handling**: The follow-up timing uses UTC timestamps; ensure system clock is correct.
- **Simulation Mode**: By default, emails are simulated. To send real emails, configure SMTP settings in `.env` and modify the `send_email` method.
- **Missing recipient emails in day-3 follow-up cron**: Before sending follow-ups, verify a real recipient address exists for every eligible prospect. If `outreach_log.json` has `email_used: null` and the prospect record has no `email` field, do not send, do not mark the touchpoint as sent, and do not increment counters. Prepare Template C drafts in `workspace/artifacts/`, validate there are no placeholders like `[Your Name]` or `[similar business]`, save a blocker report, and ask Felix only to find verified recipient emails if browser/research capability is needed. See `references/day3-followup-missing-recipient-emails.md`.
- **Duplicate IDs**: Prospect IDs must be unique; duplicates can cause incorrect updates.
- **Overlapping Runs**: A cron job may already have run the cycle earlier in the same day. The daily counter in `outreach_log.json` tracks this — check `messages_sent_today` before concluding no work was done.
- **Zero responses monitoring**: The system tracks `responses_received` as an **array** of response objects in the outreach log, NOT as an integer in `settings`. To check for new responses, compare `len(log['responses_received'])` against a saved count. The inline shortcut: `python3 -c "import json; l=json.load(open('prospects/outreach_log.json')); print(f'Responses: {len(l[\"responses_received\"])}')"` from the gideon directory. See `references/outreach-log-schema.md` for the full schema.

## Reference Implementation

See `src/automated_outreach.py` for the full implementation.

## Session-Specific References

- `references/session-2026-06-11-cron-cycle.md` — Daily limit hit, full pipeline breakdown, 88 SentNR overdue for FU1, field consistency verified.
- `references/session-2026-06-10-cron-cycle.md` — Full pipeline run: preflight → 5 outreach cycles exhausting 100 daily limit, mixed follow_up_1/follow_up_2 sends, 126 Init prospects still pending.
- `references/daily-limit-debug-2026-06-06.md` — Debugging a hit daily limit and verifying actual sends vs. stuck counter.

## Files

- `prospects/prospects.json`: Prospect database.
- `prospects/outreach_log.json`: Log of sent outreach and responses. See `references/outreach-log-schema.md` for the JSON schema.
- `prospects/outreach_templates.json`: Email templates.
- `src/automated_outreach.py`: Main outreach logic.
- `scripts/cron_preflight.py`: Reusable preflight audit script (canonical — always use this).
- `scripts/send_day3_followups.py`: Scoped day-3 follow-up runner. It sends/logs only `follow_up_1` prospects whose initial outreach was 2+ days ago, have no response, and do not already have a day-3 touchpoint logged. It writes Template C value-add drafts to `/Users/pharma6/workspace/artifacts/`, resets the daily counter by date, backs up JSON files before mutation, and skips external delivery for reserved `example.com` placeholder domains while logging those touches as `simulated_reserved_example_domain`.
- `references/outreach-log-schema.md`: Full documentation of the outreach log JSON structure.
- `references/session-2026-06-03.md` through `references/session-2026-06-11-cron-cycle.md`: Session-specific run summaries.

## Configuration

Adjust the following in `src/automated_outreach.py` if needed:
- Daily message limit (line ~281).
- Follow-up timing intervals (lines ~177, 183).
- Template personalization fields.

## Success Criteria

- Messages are sent to prospects needing contact.
- Prospect records are updated with timestamps and follow-up counts.
- Daily limit is respected.
- Outreach log is properly maintained.

## Example Usage

Run from the Gideon AI business directory:

```bash
python3 src/automated_outreach.py
```