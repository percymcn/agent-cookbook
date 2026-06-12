---
name: agent-os
description: "Agent Operating System — Hermes is the command hub on Telegram. You talk to Hermes, Hermes orchestrates subagents (Felix/Claude Code), and results auto-save to memory. Built-in voice intent detection and cron job memory feedback."
version: 1.0.0
author: Hermes Agent
tags: [agent-os, hermes, felix, claude-code, voice, delegate, memory, cron]
---

# Agent OS — The Command Hub

## Architecture

```
You (Telegram voice/text)
    ↓
[1] Hermes receives — voice transcribed via faster-whisper / text direct
    ↓
[2] Intent detection — research | deploy | code | browse | cron | memory | question
    ↓
[3] Delegate or execute — delegate_task to subagents, or run cron jobs, or answer directly
    ↓
[4] Auto feedback — every result logs to ~/.hermes/agent-os/memory_log.jsonl
    ↓
[5] Dashboard updates — ~/.hermes/agent-os/dashboard.json always reflects latest state
```

## Core Scripts

### Feedback Loop
```
~/.hermes/scripts/agent-os-feedback.py
```
Usage:
```bash
python3 ~/.hermes/scripts/agent-os-feedback.py \
  --type delegate \
  --task "task description" \
  --result "what happened" \
  [--save-skill "lesson-name"]
```

### Voice Intent Detection
```
~/.hermes/scripts/voice-intent-pipeline.py
```
Usage:
```bash
echo "research the best AI voice agents" | python3 ~/.hermes/scripts/voice-intent-pipeline.py
```

Detects intents: research | deploy | code | browse | cron | question | memory | other

## Dashboard

- **`~/.hermes/agent-os/dashboard.json`** — JSON summary: total_recorded, by_type, last_10
- **`~/.hermes/agent-os/memory_log.jsonl`** — Full append-only log (auto-trimmed to last 200)
- **`~/.hermes/skills/agent-os-learned/*.md`** — Reusable lessons saved automatically

## User Interaction Signals

Purse issues commands with minimal words. The following signals mean **execute immediately** without confirmation or re-explanation:

| Signal | Meaning |
|--------|---------|
| "yes" | Go ahead with the plan you just described |
| "1 2" / "1 2 3" / numbered list | Execute those numbered steps in order |
| "?" | What's the current state? Report concisely |
| voice message | Transcribe → classify intent → execute (see Voice Intent Pipeline) |

When you receive one of these, do not ask for confirmation. Execute and report results.

### Status / Handoff Prompts Are Not Approval

Short questions like **"what is left"**, **"where are we"**, **"what now"**, **"what's pending"**, or **"what's left"** are status/handoff prompts. They mean: inspect current state first, then report pending items, blockers, and the next highest-leverage action.

Do **not** treat these as approval to create, run, or modify cron jobs/agents. Only execute a new side-effecting action when the user gives an explicit approval signal ("yes", "do it", numbered choice) or directly asks for that action.

See `references/status-handoff-questions.md` for the session note and recommended inspection sequence.

## When to Use This Skill

- User sends a voice message — transcribe → detect intent → delegate
- User says "remember this" — save to memory via the feedback script
- User replies "yes" or a number list to your plan — execute immediately
- Any task completes — call `agent-os-feedback.py --type cron --task "..." --result "..."`
- Checking system state — read `dashboard.json` for a quick overview

## Cron Job Integration

Every cron job script should call the feedback script on completion:
```python
subprocess.run([sys.executable, FEEDBACK_SCRIPT, "--type", "cron", "--task", "...", "--result", "..."])
```

## Intent Classifier Rules

| Intent | Triggers | Action |
|--------|----------|--------|
| research | "find out", "search", "research", "what is" | Web search + summarize |
| deploy | "deploy", "push live", "publish" | Deploy to Vercel/Gumroad/etc |
| code | "build", "fix", "debug", "create" | delegate_task to Claude Code |
| browse | "check site", "open url" | Browser automation via Felix |
| cron | "every day", "daily", "remind me" | Create cronjob |
| memory | "remember", "store" | Save to memory |
| question | "advice", "should I" | Direct answer from Hermes |