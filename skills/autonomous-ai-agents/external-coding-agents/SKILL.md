---
name: external-coding-agents
description: "Umbrella for delegating software work to external coding-agent CLIs: Claude Code, OpenAI Codex, and OpenCode. Use for autonomous implementation, refactoring, code review, PR work, parallel worktrees, long-running agent sessions, PTY/tmux orchestration, and CLI-specific pitfalls."
---

# External Coding Agents

Use this umbrella when Hermes should orchestrate an external coding agent CLI rather than doing all implementation directly. Always verify the requested CLI is installed/authenticated before relying on it, and report concrete outputs: changed files, tests run, PRs opened, and unresolved risks.

## Selection guide

- **Claude Code**: strongest for long autonomous work, rich CLI/session controls, print mode, structured JSON, tmux interactive sessions, and Claude-specific project memory.
- **Codex CLI**: use when the user explicitly requests Codex/OpenAI or wants Codex `exec`; requires a git repository and PTY for interactive runs.
- **OpenCode**: provider-agnostic open-source agent; use when explicitly requested or when provider/model flexibility is important.

Do not run multiple agents in the same working tree concurrently. Use git worktrees or temp clones for parallelism.

## Common preflight

```bash
pwd
git status --short
git rev-parse --show-toplevel 2>/dev/null || echo "not a git repo"
```

Then CLI-specific checks:

```bash
claude --version && claude auth status 2>/dev/null || true
codex --version 2>/dev/null || true
opencode --version 2>/dev/null && opencode auth list 2>/dev/null || true
```

## Claude Code patterns

Prefer print mode for bounded tasks because it skips TUI dialogs:

```bash
claude -p 'Add retry handling to API calls and update tests' --allowedTools 'Read,Edit,Bash' --max-turns 10
```

Use JSON output for automation, `--max-turns` and `--max-budget-usd` to cap loops/cost, and `--bare` for CI-style runs when API-key auth is available.

Use tmux for multi-turn interactive sessions:

```bash
tmux new-session -d -s claude-work -x 140 -y 40
tmux send-keys -t claude-work 'cd /path/to/project && claude' Enter
tmux capture-pane -t claude-work -p -S -60
```

Dialog gotchas: workspace trust usually accepts Enter; the `--dangerously-skip-permissions` warning defaults to "No" and requires Down then Enter. Kill tmux sessions when done.

## Codex CLI patterns

Codex needs a git repository. Use a temporary repo for scratch work.

```bash
codex exec 'Refactor the auth module and run tests'
codex exec --full-auto 'Fix issue #78 and commit when done'
```

Hermes terminal calls should use `pty=true` for Codex. For long bounded tasks, start in background with `notify_on_complete` or poll with `process` tools. `--full-auto` auto-approves sandboxed workspace changes; `--yolo` removes guardrails and should be reserved for explicitly trusted contexts.

## OpenCode patterns

Use `opencode run` for bounded one-shot tasks; it normally does not need PTY:

```bash
opencode run 'Review this config for security issues' -f config.yaml -f .env.example
opencode run 'Refactor auth module' --model openrouter/anthropic/claude-sonnet-4
```

Use interactive background mode for iterative sessions:

```bash
opencode
# then process(action="submit", ...) and process(action="poll"|"log", ...)
```

OpenCode TUI exits with Ctrl+C (`\x03`) or process kill. Do not type `/exit`; it opens an agent selector. If behavior differs across shells, inspect `which -a opencode` and pin an explicit binary path.

## Parallel work pattern

1. Create one worktree per independent task.
2. Launch one agent per worktree.
3. Monitor logs without interrupting.
4. Validate outputs yourself before merging or reporting success.
5. Remove worktrees and kill background sessions after completion.

```bash
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main
```

## Review pattern

For PR/code review, prefer an isolated checkout or worktree. Have the external agent produce findings, then verify important claims yourself before posting comments or approving.

## Reporting requirements

When finished, summarize:

- Agent/CLI used and command mode.
- Files changed or reviewed.
- Tests/lints/checks actually run and their results.
- Commits/PRs created, if any.
- Known limitations or follow-up needed.
