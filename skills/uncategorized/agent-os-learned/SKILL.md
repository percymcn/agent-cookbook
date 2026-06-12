---
name: agent-os-learned
description: "Use when reviewing or referencing past agent-OS architecture analysis sessions. Contains notes from evaluating local JARVIS-style AI assistants (e.g. Mark-XL) covering Whisper STT, Ollama LLM integration, tool ecosystems, and persistent memory patterns."
---

# Agent OS Learned

Knowledge base of architectural analysis notes captured while evaluating local-first AI assistant frameworks.

## When to use

- Referencing how Mark-XL or similar JARVIS-style agents wire STT + LLM + tools + memory.
- Comparing local agent architectures before building or extending Hermes capabilities.
- Reviewing prior teardown notes on tool counts, memory backends, and voice pipelines.

## Key files

- `mark-xl-analysis.md` — Analysis of Mark-XL agent: Whisper STT, Ollama LLM, 18 tools, persistent memory.

## Notes

- Read-only reference skill. Does not execute commands or modify system state.
- Content is point-in-time analysis; verify against current upstream repos before acting on details.
