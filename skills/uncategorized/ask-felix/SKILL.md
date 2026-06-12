---
name: ask-felix
description: Ask Felix (big brother agent) for help when you need capabilities beyond your own.
version: 1.0.0
author: Hermes Agent
---

# ask-felix

Ask Felix (big brother agent) for help when you need capabilities beyond your own.

## When to Use

- You need browser automation
- You need credentials or API keys you don't have
- You need to access external services (SSH to servers, etc.)
- You need MCP tools (Chrome, Playwright, etc.)
- You're stuck and need a more capable agent
- You encounter missing Python modules or dependency issues that prevent script execution
- You need to set up Python virtual environments or install packages

## How It Works

1. Write a request to the shared comms channel (`/Users/pharma6/.hermes/comms/requests.jsonl`)
2. Felix monitors the channel and picks up requests
3. Felix may execute the task directly or forward it to the Felix Task API for certain types of requests (you'll see this indicated in the response)
4. Felix writes back a response to `/Users/pharma6/.hermes/comms/responses.jsonl`
5. You read the response and continue

## Response Types

Felix returns different response types depending on how the request is handled:

1. **Direct Execution**: For simple tasks Felix can handle immediately
   ```json
   {
     "id": "same-id",
     "from": "felix",
     "timestamp": "ISO8601",
     "type": "response",
     "status": "done|error|pending",
     "result": "the answer or result"
   }
   ```

2. **Task Forwarding**: For certain requests (especially those involving external communication or long-running tasks), Felix forwards to the Task API
   ```json
   {
     "id": "same-id",
     "from": "felix",
     "timestamp": "ISO8601",
     "type": "response",
     "status": "forwarded",
     "result": "Request forwarded to Felix Task API as hermes_file_<timestamp>_<hash>. Use http://192.168.1.17:7777/task/<task_id> to check status."
   }
   ```

When receiving a forwarded response, extract the task ID from the result message (format: hermes_file_<timestamp>_<hash>) and poll the provided URL to check task status. The Task API endpoint is: http://192.168.1.17:7777/task/<task_id>

**Session Learning (May 27, 2026)**: When requesting Telegram message delivery, Felix forwarded the request to the Task API with result: "Request forwarded to Felix Task API as hermes_file_1779912143_af46. Use http://192.168.1.17:7777/task/hermes_file_1779912143_af46 to check status." This confirms the forwarding pattern for external communication requests.

## User Preference: Visibility into Agent Coordination

Based on user feedback, the user prefers visibility into Hermes-Felix coordination to avoid confusion about whether agents are communicating. When appropriate, consider:

- Mirroring important Felix-Hermes communications to the user's Telegram channel for transparency
- Providing brief updates in the main chat when significant coordination occurs
- Using the comms system for technical details while keeping the user informed at a higher level

This balances efficient agent-to-agent coordination with user visibility into the multi-agent system.

## Usage

Write to `/Users/pharma6/.hermes/comms/requests.jsonl`:

```bash
echo '{"id":"'\"$(date +%s)\"'\","from":"hermes","timestamp":"'\"$(date -Iseconds)\"'\","type":"request","priority":"normal","task":"DESCRIBE WHAT YOU NEED","context":"WHY YOU NEED IT"}' >> /Users/pharma6/.hermes/comms/requests.jsonl
```

Then poll for response:
```bash
grep '"id":"YOUR_ID"' /Users/pharma6/.hermes/comms/responses.jsonl
```

## Examples

### Need browser access
```bash
echo '{"id":"1234","from":"hermes","timestamp":"2026-05-11T22:00:00","type":"request","priority":"normal","task":"Check if mytradeflow.app is loading correctly","context":"User asked me to verify the site"}' >> /Users/pharma6/.hermes/comms/requests.jsonl
```

### Need credentials
```bash
echo '{"id":"1235","from":"hermes","timestamp":"2026-05-11T22:00:00","type":"request","priority":"urgent","task":"Need the Polygon.io API key for market data","context":"User wants stock data and I dont have the key"}' >> /Users/pharma6/.hermes/comms/requests.jsonl
```

### Need SSH access
```bash
echo '{"id":"1236","from":"hermes","timestamp":"2026-05-11T22:00:00","type":"request","priority":"normal","task":"SSH to OneGo server and check nginx status","context":"Debugging a deployment issue"}' >> /Users/pharma6/.hermes/comms/requests.jsonl
```