---
name: agentic-workflow-automation
description: Generate reusable multi-step agent workflow blueprints. Use for trigger/action orchestration, deterministic workflow definitions, and automation handoff artifacts.
---

# Agentic Workflow Automation

## Overview

Build workflow blueprints that can be translated into automation platforms such as n8n or internal orchestrators. Specializes in creating autonomous agent systems with proper human oversight.

**Common Applications:**
- Autonomous business idea scraping and analysis systems
- Content repurposing workflows (YouTube to social media)
- Lead generation and qualification pipelines
- Business plan generation automation
- Multi-step agent orchestration with human oversight checkpoints

## Workflow

1. Define workflow name, trigger, and ordered steps.
2. Normalize each step into a simple execution contract with:
   - Clear step type (youtube_scraper, reddit_scraper, analyzer, scorer, plan_generator, file_saver, etc.)
   - Explicit failure handling (retry, continue, stop, alert)
   - Single-purpose action focus
3. Build a blueprint with dependencies and execution order.
4. Export JSON/markdown artifacts for implementation.
5. **For autonomous agent systems**: Design schedule-driven execution with built-in human-in-the-loop checkpoints.

## Use Bundled Resources\n\n- Run `scripts/generate_workflow_blueprint.py` for deterministic workflow output.\n- Run `scripts/extract_youtube_business_ideas.py` to extract business ideas from YouTube video titles using enhanced patterns.\n- Read `references/workflow-blueprint-guide.md` for step design guidance.\n- Read `references/autonomous-agent-patterns.md` for patterns specific to AI agent workflows.\n- Read `references/business-idea-analysis-patterns.md` for frameworks used in autonomous business idea analysis.\n- Read `references/agentic-business-system-patterns.md` for patterns specific to autonomous business idea scraping systems.\n- Read `references/youtube_business_idea_extraction.md` for patterns specific to extracting business ideas from YouTube video titles (see agent-browser skill)

## Guardrails

- Keep each step single-purpose.
- Include clear fallback behavior for failed steps.
- Design for schedule-driven execution (cron-based or trigger-based).
- Implement human-in-the-loop checkpoints for approvals, edge cases, and explicit input requests.
- Log all actions and outcomes for monitoring and auditing.
- For agent systems: Balance autonomy with appropriate human oversight - automate the repeatable, escalate the exceptional.
- **Tool Availability**: Be aware that browser_navigate, browser_snapshot, write_file, read_file are available via tool calls but NOT accessible within execute_code Python sandbox or via hermes_tools import in terminal-executed scripts. Use direct tool calls for browser/file operations, then process data in separate execute_code blocks.

## Executing Autonomous Agent Systems
## Executing Autonomous Agent Systems

When executing autonomous agent systems (not just generating blueprints):

1. **Separation of Concerns**: 
   - Use tool calls (browser_navigate, browser_snapshot, write_file, read_file) for I/O operations
   - Use execute_code for data processing, analysis, and JSON manipulation
   - Never try to import hermes_tools in execute_code - it won't work
   - **Pitfall**: Remember that execute_code blocks have isolated scopes - define all functions needed in the same block where they're used, or structure code to avoid forward references

2. **YouTube Scraping Pattern**:
   - **Primary**: Navigate to channel videos page
   - Take snapshot and extract video headings (look for level=3 headings with video titles)
   - Extract duration from heading text or nearby elements
   - Save structured data as JSON
   - **Fallback**: When browser automation fails (Chrome launch issues), use `yt-dlp --flat-playlist --dump-json --playlist-end N "https://www.youtube.com/@channel/videos"`
   - **Pitfall**: If snapshot data is truncated or difficult to parse, manually extract key information and create structured JSON files as a fallback approach
   - **Alternative**: Use browser_console to extract heading elements directly when snapshot parsing fails
   - **Enhancement**: Extract business ideas from titles by removing duration patterns and cleaning prefixes (e.g., "I Make $X/Month From" -> core business idea)
   - **Enhancement**: After extracting titles, deduplicate them to avoid processing the same idea multiple times
   - **Enhancement**: When cleaning titles, use regex patterns to remove duration suffixes:
     * Simple minutes: `\\s+\\d+\\s*minutes?.*$`
     * Hours and minutes: `\\s+\\d+\\s*hours?,\\s+\\d+\\s*minutes?.*$`
     * Hours only: `\\s+\\d+\\s*hours?.*$`
     * Minutes and seconds: `\\s+\\d+\\s*:?\\s*\\d+\\s*(?:minutes?|seconds?)?.*$`
   - **Enhancement for Automated Contexts**: When running YouTube scraping in automated environments (cron jobs, execute_code blocks), verify the agent-browser path using `which agent-browser` or store the full path in a variable, as PATH may differ from interactive shells. This practice ensures reliable execution across different execution contexts.
   - **Enhancement**: Use the provided `scripts/extract_youtube_business_ideas.py` script for consistent, robust business idea extraction from YouTube snapshots

### Reddit Scraping Pattern:
   - **Primary**: Use .json endpoints (e.g., https://www.reddit.com/r/subreddit/.json) to avoid blocking and get structured data directly
   - **Important Note on Tool Selection**: When fetching Reddit .json endpoints, **do not use agent-browser** as it renders the JSON as HTML UI elements (showing only generic page elements) rather than providing access to the raw JSON data. Instead, use curl with proper headers for reliable JSON retrieval.
   - **Recommended Approach**: Use curl with proper User-Agent header: `curl -s -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" https://www.reddit.com/r/subreddit/.json`
   - **Fallback**: If curl fails, agent-browser can be used as a last resort, but be prepared to extract JSON from <pre> tags in the rendered HTML.
   - **Enhancement for Large Responses**: 
     * Always use limit parameters (e.g., `?limit=10`) to reduce response size
     * Increase timeouts with `--timeout 30000` for navigation and `--timeout 15000` for waits when using agent-browser
     * Validate JSON before processing - use try/catch and salvage techniques for malformed responses
     * Consider processing in chunks: extract IDs first, then fetch details individually
     * **Pitfall**: When saving raw JSON responses to files, validate the JSON structure before writing to avoid decode errors - use proper JSON serialization methods
   - Extract posts data from JSON response
   - Filter for self posts (is_self: true) when looking for discussions/ideas
   - Save structured data as JSON
   - **Pitfall**: Reddit may block automated requests; always use realistic User-Agent headers and consider rate limiting
   - **Additional Pitfall**: Large JSON responses may cause parse errors - implement validation and fallback parsing strategies
   - **Enhancement**: When extracting pain points, look for self posts with meaningful selftext and use pain indicators (problem, struggle, issue, need help, etc.) via regex patterns
   - **Enhancement**: For short titles, extract meaningful pain points from the first sentence(s) of selftext
   - **Enhancement**: Sort pain points by engagement (score) to prioritize high-impact issues

4. **Data Processing**:
   - Load all scraped JSON files in execute_code blocks
   - Perform analysis, scoring, and idea generation
   - Generate summary reports and actionable plans
   - **Scoring Framework Guidance**: When scoring ideas, consider factors like revenue potential, simplicity, and automation feasibility. Use keyword-based scoring for efficiency, and boost scores for high-engagement pain points (indicates market demand).
   - **Scoring Enhancement**: Implement a weighted scoring system with specific point values for different indicators (e.g., explicit monthly revenue: +30, "easiest" mentioned: +25, AI mentioned: +25)
   - **Scoring Enhancement**: Normalize scores to a 0-100 range for easier interpretation and comparison
   - **Scoring Enhancement**: Provide reason codes with each score to explain scoring decisions
   - **Action Plan Generation**: Based on scored ideas, generate tailored action plans by analyzing idea characteristics (e.g., app-based vs service-based vs content-based) and mapping to appropriate implementation steps.
   - **Enhancement**: Implement robust business idea extraction from raw titles using regex patterns to remove duration markers, prefixes, and suffixes while preserving core concept

5. **Error Handling**:
   - Always check tool call responses for success status
   - Handle rate limiting and blocking (consider alternative endpoints or delays)
   - Validate JSON structure before processing
   - **Pitfall**: JSON responses from social media sites may contain control characters or be truncated - implement sanitization before parsing
   - **Enhancement**: Set reasonable maximum input sizes when loading JSON files to prevent memory issues
   - **Enhancement**: Use try/catch blocks when parsing JSON and implement salvage techniques for malformed responses

6. **Workflow Orchestration**:\n   - Design modular steps that can be swapped based on tool availability\n   - Include validation checks after each step to ensure data quality\n   - Use temporary files for intermediate results, cleaning up only after successful completion\n   - Log both successes and failures with sufficient context for debugging\n   - **Pitfall**: When designing fallback chains, test each fallback path independently to ensure they work when needed\n   - **Pitfall**: When saving scraped JSON data to files, ensure proper formatting to avoid JSON decode errors - validate JSON before writing\n   - **Enhancement**: Create intermediate validation checkpoints to ensure data quality before proceeding to analysis phase\n   - **Enhancement**: After completing major processing phases, save intermediate results to allow for inspection and recovery\n   - **Enhancement**: Organize scraped data in a standardized directory structure (e.g., raw/youtube/, raw/reddit/, processed/) to simplify data loading in execute_code blocks
