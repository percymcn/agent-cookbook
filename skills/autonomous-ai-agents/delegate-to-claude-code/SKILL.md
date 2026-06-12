---
name: delegate-to-claude-code
description: Delegate complex coding/reasoning tasks to Claude Code CLI via the call_claude_code Python wrapper.
trigger: When a task requires multi-file changes, debugging, refactoring, complex reasoning, or autonomous agentic work that I (Hermes) can't handle efficiently alone.
---

# Delegate to Claude Code

Claude Code (`claude -p` via `call_claude_code.py`) is a powerful agent on this machine. It has **browser automation (Playwright), MCP servers, credential access, and ~600 skills** — treat it as a superset of what I can do alone. When I hit limits (browser, credentials, MCP tools, complex multi-file work), I call Claude Code. **No need to ask Felix** — Claude Code on this machine has everything Felix had.

## When to delegate (✅)

- **Multi-file feature implementation** — reads, plans, edits, verifies across files
- **Debugging** — hypothesizes, instruments, fixes, re-verifies from stack trace
- **Architecture / codebase exploration** — maps subsystems with file:line citations
- **TDD** — failing test → green → coverage
- **Refactoring** — cross-cutting changes with verification
- **Code review / PR analysis** — reads diffs, checks for issues
- **Project scaffolding / boilerplate** — configs, migrations, CI
- **Research** — web search + synthesis
- **Long-running autonomous tasks** — sub-delegates, parallelizes, self-corrects, MCP
- **Security audits** — 600+ specialized skills
- **Browser automation** — Playwright, login, scrape logged-in pages
- **Logged-in extraction/inventory jobs** — map course/community pages, collect links/resources/transcripts, and produce machine-readable JSON plus reports when Hermes needs browser/CDP help
- **MCP tools** — Stripe, Shopify, Figma, Gmail, Cloudflare, Chrome DevTools
- **Media-generation MCP recovery** — if Hermes-native Kie/Nano Banana/Higgsfield paths are blocked by credits/auth/tooling, delegate a self-contained provider task to Claude Code and require exact returned file paths, provider used, and verification metadata; do not fall back to programmatic placeholders when the user requested real AI visuals
- **GitHub PR workflow** — `gh`, create PRs, review, merge
- **Image reading** — PNG/JPG screenshots, PDFs inline

## When NOT to delegate (❌)

- Simple tasks I can do in 1-2 tool calls
- Production deploys / DNS / OAuth (needs operator OK)
- Sending messages to external platforms
- Money / financial operations (hard-blocked without direct OK)
- Visual design / brand voice without samples
- Cross-session memory (use Hermes memory tool)
- Massive 100+ file refactors in one shot (break into milestones)

## Call pattern

```python
from call_claude_code import call_claude_code, ClaudeCodeError
output = call_claude_code(TASK_PROMPT, timeout=300, cwd="/path/to/repo")
```

## Prompt format

```
GOAL: <one sentence — what "done" looks like>
CONTEXT: <repo path, branch, why, what's been tried>
CONSTRAINTS: <don't touch X, must keep Y backward compat>
INPUTS: <specific files, line numbers, error messages>
ACCEPTANCE: <tests pass, endpoint returns Z>
OUT-OF-SCOPE: <things NOT to do>
OUTPUT: <"summary" or "open a PR" or "JSON with fields X,Y">
```

Sweet spot: **150–400 words** — medium detail beats terse or verbose.

## For structured output

```
Return JSON with keys: {status, files_changed[], next_steps[], blockers[]}
Respond with ONLY valid JSON inside a fenced code block.
```

## Pitfalls

- Python 3.9 — don't use `str | None` type hints in code for this machine
- Claude Code does NOT see the current conversation — every prompt must be self-contained
- Default timeout 300s; lower for quick queries, higher for agentic tasks
- If invoking `/Users/pharma6/ai-team/call_claude_code.py` directly as a script, its `__main__` test path does **not** pass your desired task timeout. For long browser/inventory jobs, import the helper and call `call_claude_code(prompt, timeout=550, cwd='/Users/pharma6/ai-team')` from a short Python snippet instead of relying on the script wrapper.
- Claude Code sub-delegates by default — fine, it manages context well
- For extraction/inventory jobs, require durable artifacts instead of prose only: JSON inventories, downloaded/transcribed files when possible, a final markdown report, and exact paths. After Claude Code returns, Hermes must verify the files/counts locally before reporting success to Purse.