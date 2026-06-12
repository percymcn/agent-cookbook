---
name: software-delivery-workflow
description: "Software delivery workflow umbrella: planning, spikes/prototypes, test-driven development, systematic debugging, debugger use, and pre-commit code review/verification. Use for class-level engineering process guidance before or during code changes."
---

# Software Delivery Workflow

Use this umbrella to choose and combine the right engineering process before changing code. The normal lifecycle is: understand → plan or spike → implement with tests → debug systematically → verify with independent review.

## 1. Planning mode

Use planning-only mode when the user asks for a plan, design, implementation plan, or `/plan` behavior.

- Do not implement code or mutate project files except the plan markdown.
- Inspect read-only context as needed.
- Save the deliverable under `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`.
- Include goal, assumptions, approach, exact files likely to change, bite-sized tasks, tests, risks, and open questions.

Good plans use exact paths, concrete commands, expected outputs, and small sequential tasks.

## 2. Spikes / throwaway experiments

Use a spike when feasibility is uncertain and a small prototype can answer a risk faster than more discussion.

Loop: decompose → research → build → verdict. Create one standalone directory per spike under `spikes/` or the repo's planning convention. Each spike README should end with:

```markdown
## Verdict: VALIDATED | PARTIAL | INVALIDATED
### What worked
### What didn't
### Surprises
### Recommendation for the real build
```

For comparison spikes, run variants side by side and produce a head-to-head table. Keep spike code disposable; do not accidentally turn it into production without a follow-up plan.

## 3. Test-driven development

When building or fixing behavior, prefer RED → GREEN → REFACTOR:

1. Write a failing test for the exact desired behavior.
2. Run the targeted test and verify it fails for the right reason.
3. Implement the smallest change that makes it pass.
4. Run the targeted test, then relevant broader tests.
5. Refactor only after green tests.

If a test suite exists, new behavior should usually have tests. Do not claim success without running the relevant commands.

## 4. Systematic debugging

For bugs, failures, or surprising behavior, do not guess-patch. Follow four phases:

1. Reproduce and collect evidence.
2. Inspect surrounding code/data/config to understand the system.
3. Form and test hypotheses one at a time.
4. Apply the smallest fix and verify it addresses the root cause.

Preserve original failure output and compare after the fix. If the failure changes, treat that as new evidence rather than success.

## 5. Debugger-specific guidance

Use `python-debugpy`/`pdb` style workflows when prints and logs are insufficient. Use Node inspector workflows when debugging JavaScript/TypeScript runtime state. Prefer real breakpoints and variable inspection for race conditions, async flow, complex state, or nondeterministic tests.

## 6. Pre-commit verification and review

Before committing/pushing nontrivial code changes:

1. Inspect `git diff` / `git diff --cached`.
2. Run security scans for obvious secrets and unsafe patterns.
3. Run tests/lints/type checks that apply to the project.
4. Use independent review when changes are substantial or risky.
5. Fix reported security/logic issues, then re-run verification.

Structured review output:

```markdown
VERIFICATION FAILED or PASSED
Security issues:
Logic errors:
Regressions:
New lint/type errors:
Suggestions:
```

## 7. Handoff discipline

When delegating or using subagents, pass the plan, exact acceptance criteria, relevant file paths, and the command outputs that define success/failure. Verify subagent claims by reading files or running commands yourself before reporting success.

## Pitfalls

- Planning and implementation are different modes; do not mutate code in planning mode.
- A spike is not production code; document the verdict and throw it away or deliberately promote it.
- Do not self-review only; fresh context catches issues the implementer misses.
- Do not skip tests because a patch looks obvious.
- Do not use usage counters or previous success as proof that current code works; run the command.
