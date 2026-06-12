---
name: prospect-response-monitoring
description: Monitors outreach logs for new prospect responses and sends urgent notifications via Telegram when responses are detected.
tags: [prospects, outreach, telegram, notifications, automation]
version: 1.0.0
---

# Prospect Response Monitoring

Monitors outreach logs for new prospect responses and sends urgent notifications via Telegram when responses are detected.

## Trigger Conditions
- Scheduled check for prospect responses (e.g., via cron job)
- Need to monitor outreach campaigns for timely follow-up
- When immediate attention is required for new prospect engagement

## Context
This skill implements the pattern used by Gideon's response notifier for checking prospect outreach logs and sending Telegram notifications for new responses. It's designed for sales/outreach workflows where timely response to prospects is critical.

## Steps
1. Locate the outreach/logs directory for your prospecting system
   - Common locations to check:
     - `~/gideon_ai_business/prospects/` (Gideon's system)
     - `~/prospects/` (Alternative prospecting system)
   - Look for outreach log files (often JSON format) and monitoring scripts

2. Find and examine the response notifier script
   - Common locations:
     - `~/gideon_ai_business/notifier_with_telegram.py` (Gideon's system)
     - `~/prospects/monitor_outreach.py` (Alternative system)
   - Review the script to understand:
     - How it loads last check state
     - How it reads the outreach log
     - How it determines new responses
     - How it formats Telegram notifications
     - **Important**: How it sends messages - may use direct Telegram Bot API via urllib (NOT hermes_tools) or Hermes CLI
     - Note: Script outputs last known and current response counts for monitoring

3. Execute the appropriate notifier script
   - Run: `python3 /path/to/notifier_script.py`
   - Ensure required dependencies are available (usually just standard library)
   - Verify Telegram credentials are configured in the associated .env file

4. Handle the output
   - If no new responses: Exit silently (appropriate for cron jobs)
   - If new responses found: Notification should be sent via Telegram
   - **Note**: Script always updates last check timestamp after execution to prevent spamming
   - Check logs for any errors in execution

2. Find and examine the response notifier script
   - Common location: `~/gideon_ai_business/notifier_with_telegram.py`
   - Review the script to understand:
     - How it loads last check state
     - How it reads the outreach log
     - How it determines new responses
     - How it formats Telegram notifications
     - **Important**: How it sends messages - uses direct Telegram Bot API via urllib (NOT hermes_tools)
     - Note: Script outputs last known and current response counts for monitoring

3. Execute the notifier script
   - Run: `python3 /path/to/notifier_script.py`
   - Ensure required dependencies are available (usually just standard library)
   - Verify Telegram credentials are configured in the associated .env file

4. Handle the output
   - If no new responses: Exit silently (appropriate for cron jobs)
   - If new responses found: Notification should be sent via Telegram
   - **Note**: Script always updates last check timestamp after execution to prevent spamming
   - Check logs for any errors in execution

## Gideon-Specific Implementation Notes\\nBased on implementation in this session with user Gideon:\\n\\n- The notifier script (`notifier_with_telegram.py`) is designed to run every 30 minutes via cron job\\n- It checks for new responses in the outreach log (`prospects/outreach_log.json`)\\n- When new responses are detected, it sends urgent notifications via Telegram\\n- **Important**: Uses direct Telegram Bot API via urllib (not hermes_tools)\\n- For Gideon's specific use case (often driving), notifications include both audio (text-to-speech) and complete text transcripts\\n- The system defaults to silent operation - only alerts for action-required situations (prospect responses, payments, complex decisions)\\n- Human-in-the-loop is sought ONLY for: financial transactions, prospect responses requiring negotiation, major strategic pivots, legal/compliance issues, or explicit user requests for input\\n- **Cron job execution**: When run as a cron job, the script should exit silently when no new responses are found (appropriate for automated monitoring)\\n- **Last check file**: Stores state in `data/last_response_check.json` with format: {\\\"last_response_count\\\": <int>, \\\"last_check_time\\\": \\\"<ISO timestamp>\\\"}\\n- **Timestamp updates**: The script updates the last check timestamp after every run (whether new responses found or not) to prevent spamming on errors or repeated notifications\\n\\n## Environment-Specific Notes from Current Session\\n- In some Hermes environments (like this cron job), the `hermes_tools` module may not be available in the Python path\\n- Scripts attempting to import `hermes_tools` will fail with `ModuleNotFoundError`\\n- **Correct approach**: Use the Hermes CLI directly: `hermes send --to telegram \"message\"`\\n- When running as a cron job, the agent's final response is auto-delivered to the configured target\\n- Additional Telegram notifications may be redundant/not needed in cron contexts\\n- Always check the actual output/result of notification attempts
## Pitfalls\\\\n- Assuming the outreach log format without verifying (check for 'responses_received' field)\\\\n- Forgetting to update the last check timestamp, causing repeated notifications\\\\n- Not handling missing Telegram configuration gracefully\\\\n- Running too frequently and hitting Telegram API rate limits\\\\n- Not setting proper file permissions for log/state files\\\\n- **Gideon-specific**: Sending notifications when user cannot read (driving) without providing audio alternative\\\\n- Assuming hermes_tools is available for Telegram notifications; in isolated environments, direct Telegram API via urllib may be required\\\\n- **Environment mismatch**: Some environments (like Gideon's) may lack `hermes_tools` module; scripts using direct Telegram API via urllib are more portable\\\\n- **Cron job redundancy**: When run as a cron job, the agent's final response is auto-delivered; additional Telegram notifications may be redundant\\\\n- **Import path errors**: Attempting to import `hermes_tools` or `tools.send_message_tool` will fail in environments where Hermes tools aren't in Python path\\\\n- **Fallback importance**: Always have a fallback to console output or CLI-based notification when direct tool imports fail\\\\n- **Cron job timeouts**: Scripts that fail silently or with import errors can cause cron jobs to timeout; always test scripts in isolation before scheduling\\\\n- **Silent output requirement**: When running as a Hermes cron job with no actionable output, return exactly \"[SILENT]\" to prevent unnecessary notifications\\\\n- **Cron job timeouts**: Scripts that fail silently or with import errors can cause cron jobs to timeout; always test scripts in isolation before scheduling\\\\n- **Silent output requirement**: When running as a Hermes cron job with no actionable output, return exactly \"[SILENT]\" to prevent unnecessary notifications

## References\n- See `references/gideon_notifier_anatomy.md` for breakdown of the specific implementation\n- See `references/paths.md` for file locations used by this skill\n- See `references/gideon_notifier_cron_job_issue_2026-05-25.md` for troubleshooting cron job execution issues and solutions\n- See `references/gideon_notifier_run_2026-05-25.md` for the execution log from May 25, 2026\n- See `references/gideon_notifier_run_2026-05-26.md` for the execution log from May 26, 2026 (shows successful cron job execution with no new responses)\n- See `references/gideon_notifier_fix_june_1_2026.md` for the fix applied on June 1, 2026 to resolve cron job timeout issues\n- See `references/gideon_notifier_fix_june_1_2026.md` for the fix applied on June 1, 2026 to resolve cron job timeout issues\n- See `references/gideon_notifier_fix_june_1_2026.md` for the fix applied on June 1, 2026 to resolve cron job timeout issues