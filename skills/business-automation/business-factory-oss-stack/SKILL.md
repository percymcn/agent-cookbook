---
name: business-factory-oss-stack
description: "Use Purse's installed open-source business factory stack from the 2026-05-21 hot GitHub repos PDF: CodeGraph, Bun, Supertonic, CloakBrowser, AgentMemory, and repo-derived agent/research playbooks."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  created_by: agent
  source_pdf: /Users/pharma6/.hermes/cache/documents/doc_51df3d928223_github-hot-repos-2026-05-21.pdf
---

# Business Factory OSS Stack

Use this skill when improving Purse's faceless-video factory, AI-agent systems, coding workflows, research workflows, or automation infrastructure with free/open-source tools. Pay for tools only when reliability/revenue justifies it and after explicit approval.

## Installed/verified tools

### CodeGraph

Purpose: local codebase knowledge graph for AI coding agents.

Installed/wired:

```bash
export PATH="/opt/homebrew/bin:$HOME/.local/bin:$HOME/.bun/bin:$PATH"
codegraph --version
codegraph status /Users/pharma6/ai-team
```

Verified index for `/Users/pharma6/ai-team`:

- 7,170 files
- 122,708 nodes
- 364,588 edges

Common commands:

```bash
codegraph sync /Users/pharma6/ai-team
codegraph query factory_assemble --path /Users/pharma6/ai-team
codegraph files --path /Users/pharma6/ai-team
codegraph impact SYMBOL --path /Users/pharma6/ai-team
```

Hermes MCP config was updated by `codegraph install --target hermes --location global --yes`; start a new Hermes session for MCP changes to load.

### Bun

Purpose: fast JS runtime/package manager/test runner.

```bash
export PATH="/opt/homebrew/bin:$HOME/.bun/bin:$PATH"
bun --version
bun install
bun test
bun run <script>
```

Use Bun for lightweight JS tooling. If a CLI has `#!/usr/bin/env node`, use `/opt/homebrew/bin/node` because Node exists but may not be in non-login PATH.

### Supertonic local TTS

Purpose: free local/on-device text-to-speech for faceless-video voiceovers and quick audio memos.

Installed venv:

```bash
cd /Users/pharma6/ai-team
source .venvs/supertonic/bin/activate
supertonic info
```

Verified model cache:

- `/Users/pharma6/.cache/supertonic3`
- ~385MB
- voices: F1-F5, M1-M5
- sample rate: 44.1kHz

Smoke test used:

```bash
cd /Users/pharma6/ai-team
source .venvs/supertonic/bin/activate
supertonic tts 'Local Supertonic voice is ready for the faceless video factory.' \
  -o test_outputs/supertonic_smoke.wav \
  --voice M1 --steps 5 --lang en
```

Verified output: 4.60s WAV, generated in ~2.6s.

Reusable long-form helper:

```bash
cd /Users/pharma6/ai-team
source .venvs/supertonic/bin/activate
python supertonic_voiceover.py --text-file script.txt --out vo.wav --voice M1 --steps 5 --lang en
```

Helper verified: `/Users/pharma6/ai-team/supertonic_voiceover.py` generated a 14.2s WAV test file successfully.

Recommended usage:

- Use Supertonic first for drafts, internal videos, and cost-sensitive batches.
- Use premium TTS only when voice quality materially affects monetization/public launch.
- Always compare final audio against the brand standard before publishing.

### CloakBrowser

Purpose: Playwright-compatible Chromium automation for legitimate QA/research when normal Playwright is unreliable.

Installed venv:

```bash
cd /Users/pharma6/ai-team
source .venvs/cloakbrowser/bin/activate
python - <<'PY'
from cloakbrowser import launch
print('cloakbrowser import ok')
PY
```

Guardrails:

- Use only for legitimate browsing, app QA, public research, and owned-site testing.
- Do not use to bypass CAPTCHAs, access controls, paywalls, rate limits, or platform rules.
- First launch may download a browser binary and consume additional disk.

### AgentMemory

Purpose: local multi-agent memory across coding agents.

Status: installed and CLI works after PATH fix.

```bash
export PATH="/opt/homebrew/bin:$HOME/.bun/bin:$HOME/.local/bin:$PATH"
agentmemory --help
agentmemory status
```

Current state:

- CLI verified.
- Engine not running by default.
- Hermes auto-merge is not implemented by AgentMemory.
- Manual Hermes config is staged only; do not replace Hermes built-in memory without a deliberate decision.

Manual MCP snippet if needed later:

```yaml
mcp_servers:
  agentmemory:
    command: agentmemory
    args: ["mcp"]
```

Prefer MCP/tool access over setting `memory.provider: agentmemory` so Hermes' current memory behavior is not accidentally overridden.

## Converted/reference repos

### humanlayer/12-factor-agents

Local clone:

`/Users/pharma6/ai-team/oss_tools/12-factor-agents`

Use for production agent design:

- own prompts
- own context window
- tools as structured outputs
- compact errors into context
- small focused agents
- human-in-loop as explicit tool calls
- stateless reducer mindset

### Imbad0202/academic-research-skills

Local clone:

`/Users/pharma6/ai-team/oss_tools/academic-research-skills`

Use as reference for:

- deep research
- literature/source validation
- paper/report planning
- reproducibility lockfiles
- reviewer-style critique
- content research briefs

## Staged / not installed as runtime

### OpenHuman

Local clone retained:

`/Users/pharma6/ai-team/oss_tools/openhuman`

Do not build on this Mac while disk is tight. Use as architecture reference for local-first memory, integrations, and desktop agent design.

### Zapier MCP

Sponsored/paid-capable option. Do not connect or spend without explicit approval. Consider only when reliability/time-to-market beats native API or OSS implementation.

## Pruned clones

The following cloned copies were removed to recover disk because they are low value for the current factory. Original repos remain on GitHub:

- `datawhalechina/easy-vibe`
- `ruvnet/RuView`
- duplicate `colbymchenry/codegraph` clone after global install

## Operating workflow

1. For codebase work, sync/query CodeGraph before broad file searches.
2. For JS tooling, prefer Bun; use `/opt/homebrew/bin/node` when Node shebangs are required.
3. For video VO drafts, try Supertonic local TTS first; escalate to paid/premium TTS only when quality/revenue demands it.
4. For browser QA/research, prefer normal tools first; use CloakBrowser only for legitimate automation reliability issues.
5. For complex repo analysis or deep coding, use `/Users/pharma6/ai-team/call_claude_code.py` with detailed prompts.
6. For production agent/workflow design, reference 12-factor-agents before building fragile agent loops.
7. Keep disk above 5GB free before downloading model/runtime-heavy tools.
