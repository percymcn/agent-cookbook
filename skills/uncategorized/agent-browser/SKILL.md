---
name: agent-browser
description: Headless browser automation CLI optimized for AI agents with accessibility tree snapshots and ref-based element selection
metadata: {"clawdbot":{"emoji":"🌐","requires":{"commands":["agent-browser"]},"homepage":"https://github.com/vercel-labs/agent-browser"}}
---

# Agent Browser Skill

Fast browser automation using accessibility tree snapshots with refs for deterministic element selection.

## Why Use This Over Built-in Browser Tool

**Use agent-browser when:**
- Automating multi-step workflows
- Need deterministic element selection
- Performance is critical
- Working with complex SPAs
- Need session isolation

**Use built-in browser tool when:**
- Need screenshots/PDFs for analysis
- Visual inspection required
- Browser extension integration needed

## Core Workflow

```bash
# 1. Navigate and snapshot
agent-browser open https://example.com
agent-browser snapshot -i --json

# 2. Parse refs from JSON, then interact
agent-browser click @e2
agent-browser fill @e3 "text"

# 3. Re-snapshot after page changes
agent-browser snapshot -i --json
```

## Key Commands

### Navigation
```bash
agent-browser open <url>
agent-browser back | forward | reload | close
```

### Snapshot (Always use -i --json)
```bash
agent-browser snapshot -i --json          # Interactive elements, JSON output
agent-browser snapshot -i -c -d 5 --json  # + compact, depth limit
agent-browser snapshot -s "#main" -i      # Scope to selector
```

### Interactions (Ref-based)
```bash
agent-browser click @e2
agent-browser fill @e3 "text"
agent-browser type @e3 "text"
agent-browser hover @e4
agent-browser check @e5 | uncheck @e5
agent-browser select @e6 "value"
agent-browser press "Enter"
agent-browser scroll down 500
agent-browser drag @e7 @e8
```

### Get Information
```bash
agent-browser get text @e1 --json
agent-browser get html @e2 --json
agent-browser get value @e3 --json
agent-browser get attr @e4 "href" --json
agent-browser get title --json
agent-browser get url --json
agent-browser get count ".item" --json
```

### Check State
```bash
agent-browser is visible @e2 --json
agent-browser is enabled @e3 --json
agent-browser is checked @e4 --json
```

### Wait
```bash
agent-browser wait @e2                    # Wait for element
agent-browser wait 1000                   # Wait ms
agent-browser wait --text "Welcome"       # Wait for text
agent-browser wait --url "**/dashboard"   # Wait for URL
agent-browser wait --load networkidle     # Wait for network
agent-browser wait --fn "window.ready === true"
```

### Sessions (Isolated Browsers)
```bash
agent-browser --session admin open site.com
agent-browser --session user open site.com
agent-browser session list
# Or via env: AGENT_BROWSER_SESSION=admin agent-browser ...
```

### State Persistence
```bash
agent-browser state save auth.json        # Save cookies/storage
agent-browser state load auth.json        # Load (skip login)
```

### Screenshots & PDFs
```bash
agent-browser screenshot page.png
agent-browser screenshot --full page.png
agent-browser pdf page.pdf
```

### Network Control
```bash
agent-browser network route "**/ads/*" --abort           # Block
agent-browser network route "**/api/*" --body '{"x":1}'  # Mock
agent-browser network requests --filter api              # View
```

### Cookies & Storage
```bash
agent-browser cookies                     # Get all
agent-browser cookies set name value
agent-browser storage local key           # Get localStorage
agent-browser storage local set key val
```

### Tabs & Frames
```bash
agent-browser tab new https://example.com
agent-browser tab 2                       # Switch to tab
agent-browser frame @e5                   # Switch to iframe
agent-browser frame main                  # Back to main
```

## Snapshot Output Format

```json
{
  "success": true,
  "data": {
    "snapshot": "...",
    "refs": {
      "e1": {"role": "heading", "name": "Example Domain"},
      "e2": {"role": "button", "name": "Submit"},
      "e3": {"role": "textbox", "name": "Email"}
    }
  }
}
```

## Best Practices\\\\\\\\n\\\\\\\\\\\\\\\\n\\\\\\\\\\\\\\\\n1. **Always use `-i` flag** - Focus on interactive elements\\\\\\\\\\\\\\\\n2. **Always use `--json`** - Easier to parse\\\\\\\\\\\\\\\\n3. **Wait for stability** - `agent-browser wait --load networkidle`\\\\\\\\\\\\\\\\n4. **Save auth state** - Skip login flows with `state save/load`\\\\\\\\\\\\\\\\n5. **Use sessions** - Isolate different browser contexts\\\\\\\\\\\\\\\\n6. **Use `--headed` for debugging** - See what's happening\\\\\\\\\\\\\\\\n7. **Handle dynamic content** - Re-snapshot after clicks/fills that may change the DOM\\\\\\\\\\\\\\\\n8. **Verify refs before use** - If an interaction fails, re-snapshot and get fresh refs\\\\\\\\\\\\\\\\n9. **Handle iframes/popups** - Check for new frames or portals after actions\\\\\\\\\\\\\\\\n10. **Confirm actions worked** - Look for success indicators after submitting forms\\\\\\\\\\\\\\\\n11. **Validate information authenticity** - Regularly check that scraped/processed data represents real information (not simulated/demo data) by examining raw outputs, timestamps, and cross-referencing with multiple sources\\\\\\\\\\\\\\\\n12. **Complete workflow steps** - After navigation, ensure you complete all required interaction steps (snapshot, interact, re-snapshot) before considering the task done.\\\\\\\\\\\\\\\\n13. **User-visible browser handoffs** - When the user asks to open a site on the Mac screen and will manually log in/select content, open the exact source platform they named first (e.g. Skool before NotebookLM), verify the active tab URL/title if possible, and only move to downstream tools after source access is established. If Chrome/macOS blocks page reading, ask for the exact address-bar URL or have the user enable `View → Developer → Allow JavaScript from Apple Events`; then retry or escalate to Felix. See `references/user_visible_browser_handoff.md`.
14. **YouTube-specific patterns** - When scraping YouTube channels for business ideas:\\\\\\\\\\\\\\\\n    • Navigate to @channel/videos page\\\\\\\\\\\\\\\\n    • Wait for networkidle\\\\\\\\\\\\\\\\n    • Take snapshot -i --json\\\\\\\\\\\\\\\\n    • Extract video titles from refs where name contains duration patterns (minutes, hours)\\\\\\\\\\\\\\\\\\n    • Clean titles by removing duration suffixes using comprehensive regex patterns:\\\\\\\\\\\\\\\\n      - Simple minutes: \\\\\\\\s+\\\\\\\\d+\\\\\\\\s*minutes?.*$\\\\\\\\\\\\\\\\n      - Hours and minutes: \\\\\\\\s+\\\\\\\\d+\\\\\\\\s*hours?,\\\\\\\s+\\\\\\\\d+\\\\\\\\s*minutes?.*$\\\\\\\\\\\\\\\\n      - Hours only: \\\\\\\\s+\\\\\\\\d+\\\\\\\\s*hours?.*$\\\\\\\\\\\\\\\\n      - Minutes and seconds: \\\\\\\\s+\\\\\\\\d+\\\\\\\\s*:\\\\\\\\s*\\\\\\\\d+\\\\\\\\s*(?:minutes?|seconds?)?.*$\\\\\\\\\\\\\\\\n    • Deduplicate extracted titles to avoid processing same idea multiple times\\\\\\\\\\\\\\\\n    • **Alternative approach**: When browser-based extraction is unreliable (blocked, slow, or complex page structure), use yt-dlp flat-playlist mode as a more reliable alternative:\\\\\\\\\\\\\\\\n      * `yt-dlp --flat-playlist --print \\\\\\\\\\\\\\\"https://www.youtube.com/watch?v=%(id)s|%(title)s\\\\\\\\\\\\\\\" --playlist-items 1-5 \\\\\\\\\\\\\\\"https://www.youtube.com/@CHANNEL/videos\\\\\\\\\\\\\\\"`\\\\\\\\\\\\\\\\n    • See references/youtube_business_idea_extraction.md for detailed patterns
    • **For automated/cron job environments**: Browser automation for YouTube is often unreliable due to blocking. Use yt-dlp flat-playlist mode as primary method for YouTube scraping in automated environments. See references/youtube_extraction_lessons_may_2026.md for detailed patterns.
    • **For YouTube metadata extraction in automated environments**: Direct yt-dlp usage with blocking bypass parameters (`--force-ipv4 --add-header Host:www.youtube.com`) is more reliable and faster than browser automation. Process in batches with 10-15s delays between requests and 30-60m cooldowns between batches.
    • **YouTube-specific blocking mitigation**: When using yt-dlp in automated environments, always include `--force-ipv4 --add-header Host:www.youtube.com` and implement exponential backoff retry logic (start 5s, double each attempt up to 60s).
    • **Session learning**: See references/session_learnings_may_26_2026_business_opportunity_scan.md for detailed learnings from AI automation business opportunity scanning including YouTube blocking realities in automated environments (May 26, 2026)
    • **Session Learning (June 3, 2026)**: In automated environments (cron job execution), the youtube-content skill was successfully used to extract metadata from YouTube videos when transcript extraction failed, enabling the generation of AI automation agency playbooks. See references/session_learnings_june_3_2026_cron_job_youtube_playbook.md in the youtube-content skill for detailed learnings.\\\\\\\\n14. **Verify agent-browser path in automated contexts** - When running agent-browser from scripts or execute_code blocks, verify the full path (e.g., using `which agent-browser`) as the PATH environment may differ from interactive shells. Consider storing the path in a variable for reuse.\\\\\\\\n15. **Using in Restricted Environments** - In execute_code blocks, cron jobs, or other restricted environments:\\\\\\\\n    • Use full paths for external tools (e.g., `/opt/homebrew/bin/agent-browser` instead of `agent-browser`) \\\\\\\\n    • Use full paths for yt-dlp (e.g., `/opt/homebrew/bin/yt-dlp` instead of `yt-dlp`)\\\\\\\\\n    • For YouTube scraping: Use yt-dlp flat-playlist as a reliable alternative to browser automation\\\\\\\\n    • For Reddit scraping: Use .json endpoints with proper User-Agent header (e.g., `curl -s -H \"User-Agent: Mozilla/5.0...\" https://www.reddit.com/r/subreddit/.json`) instead of browser automation\\\\\\\\n    • Consider using metadata fallback strategy when transcript extraction is consistently blocked\\\\\\\\n    • Implement longer timeouts (60-120s) for network operations in restricted environments\\\\\\\\n\\\\\\\\n## Troubleshooting\\\\\\\\n\\\\\\\\n### Chrome Launch Failures\\\\\\\\nIf you see \\\\\\\\\\\\\\\"Auto-launch failed: Chrome exited early\\\\\\\\\\\\\\\" or similar errors:\\\\\\\\n\\\\\\\\n1. **Try `--args \\\\\\\\\\\\\\\"--no-sandbox\\\\\\\\\\\\\\\"`** - Add this flag when Chrome crashes silently\\\\\\\\n2. **Verify Chrome installation** - Run `agent-browser install` to ensure binaries are present\\\\\\\\n3. **Specify executable path** - Use `--executable-path /path/to/chrome` if auto-detection fails\\\\\\\\n4. **Check permissions** - Ensure the Chrome binary is executable\\\\\\\\n5. **Fallback approach** - For YouTube scraping, consider using `yt-dlp` as an alternative when browser automation fails\\\\\\\\n\\\\\\\\nSee references/newsletter_dynamic_content.md for detailed patterns from processing dynamic newsletter sites.\\\\\\\\nSee references/troubleshooting_chrome_launch.md for Chrome launch failure troubleshooting.\\\\\\\\n\\\\\\\\n### Large JSON Response Issues\\\\\\\\nWhen scraping sites that return large JSON payloads (Reddit, Twitter, etc.):\\\\\\\\n- You may encounter JSON parse errors, timeouts, or memory constraints\\\\\\\\n- **Always use limit parameters** (e.g., `?limit=10`) to reduce response size\\\\\\\\n- **Increase timeouts** with `--timeout 30000` for navigation and `--timeout 15000` for waits\\\\\\\\n- **Validate JSON before processing** - use try/catch and salvage techniques\\\\\\\\n- **Consider alternative approaches** like yt-dlp for YouTube or direct API calls\\\\\\\\n- See references/handling_large_json_responses.md for detailed strategies\\\\\\\\n\\\\\\\\n### YouTube Transcript Availability\\\\\\\\nWhen trying to access YouTube transcripts:\\\\\\\\n- Look for \\\\\\\"Subtitles/closed captions unavailable\\\\\\\" indicator\\\\\\\\n- Check for \\\\\\\"...more\\\\\\\" or \\\\\\\"Description\\\\\\\" buttons that need to be clicked first\\\\\\\\n- Look for \\\\\\\"Show transcript\\\\\\\" button after expanding description\\\\\\\\n- Always re-snapshot after clicks to reveal new elements\\\\\\\\n- If transcripts unavailable, extract video metadata (title, description) as fallback\\\\\\\\n- Consider using yt-dlp for metadata extraction when browser-based transcript access fails, using parameters like `--force-ipv4 --add-header Host:www.youtube.com` to bypass blocking (see references/yt_dlp_blocking_fix.md in youtube-content skill)\\\\\\\\n\\\\\\\\nSee references/youtube_transcript_extraction.md for detailed patterns from processing dynamic YouTube content.
See references/troubleshooting_chrome_launch.md for Chrome launch failure troubleshooting.

### Large JSON Response Issues
When scraping sites that return large JSON payloads (Reddit, Twitter, etc.):
- You may encounter JSON parse errors, timeouts, or memory constraints
- **Always use limit parameters** (e.g., `?limit=10`) to reduce response size
- **Increase timeouts** with `--timeout 30000` for navigation and `--timeout 15000` for waits
- **Validate JSON before processing** - use try/catch and salvage techniques
- **Consider alternative approaches** like yt-dlp for YouTube or direct API calls
- See references/handling_large_json_responses.md for detailed strategies

#### Reddit-specific patterns
When scraping Reddit:
- **Primary**: Use `.json` endpoints (e.g., https://www.reddit.com/r/subreddit/.json) to avoid blocking and get structured data
- **Fallback**: When blocked, use curl with proper User-Agent header: `curl -s -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" https://www.reddit.com/r/subreddit/.json`
- **Enhancement for Large Responses**: 
  * Always use limit parameters (e.g., `?limit=10`) to reduce response size
  * Increase timeouts with `--timeout 30000` for navigation and `--timeout 15000` for waits when using agent-browser
  * Validate JSON before processing - use try/catch and salvage techniques for malformed responses
  * Consider processing in chunks: extract IDs first, then fetch details individually
  * **Pitfall**: When saving raw JSON responses to files, validate the JSON structure before writing to avoid decode errors - use proper JSON serialization methods

- **Session Validated (June 1, 2026)**: See references/reddit_scraping_lessons_june_1_2026.md for detailed lessons on Reddit scraping in automated environments.
- **Session Validated (June 1, 2026)**: In automated environments (cron jobs, execute_code blocks), browser automation for YouTube transcript extraction consistently failed due to blocking, validating that yt-dlp flat-playlist mode is more reliable for YouTube scraping in automated contexts. See references/youtube_extraction_lessons_may_2026.md and references/skill_updates_session_june_1_2026.md in the youtube-content skill for detailed learnings.
- **Session Learning (June 2, 2026)**: In automated environments (cron job execution), Reddit scraping using .json endpoints with proper User-Agent headers encountered JSON decode errors, indicating potential blocking or rate limiting by Reddit. This validates that:
          * Reddit scraping in automated environments may require additional anti-bot mitigation strategies beyond standard User-Agent headers
          * Consider implementing retry logic with exponential backoff for Reddit API requests
          * May need to use alternative approaches such as cached data or reducing request frequency

### Reddit Blocking Mitigation (June 2026)
**Session learned (June 3, 2026)**: In automated environments, both .json endpoints and agent-browser were blocked by Cloudflare/js_challenge anti-bot measures when scraping Reddit. This validates that:
  * Reddit scraping in automated environments requires advanced anti-bot mitigation beyond standard User-Agent headers
  * Consider implementing request throttling with 30-60s delays between requests
  * Consider using Reddit's official API with OAuth for more reliable access
  * May need to use alternative data sources (Pushshift, RSS feeds, cached data) when blocking persists
  * Implement challenge detection in responses to automatically switch strategies
  * See references/reddit_blocking_lessons_june_2026.md in the autonomous-business-system skill for detailed patterns

## Example: Search and Extract

```bash
agent-browser open https://www.google.com
agent-browser snapshot -i --json
# AI identifies search box @e1
agent-browser fill @e1 "AI agents"
agent-browser press Enter
agent-browser wait --load networkidle
agent-browser snapshot -i --json
# AI identifies result refs
agent-browser get text @e3 --json
agent-browser get attr @e4 "href" --json
```

## Example: Multi-Session Testing

```bash
# Admin session
agent-browser --session admin open app.com
agent-browser --session admin state load admin-auth.json
agent-browser --session admin snapshot -i --json

# User session (simultaneous)
agent-browser --session user open app.com
agent-browser --session user state load user-auth.json
agent-browser --session user snapshot -i --json
```

## Installation

```bash
npm install -g agent-browser
agent-browser install                     # Download Chromium
agent-browser install --with-deps         # Linux: + system deps
```

## Credits

Skill created by Yossi Elkrief ([@MaTriXy](https://github.com/MaTriXy))

agent-browser CLI by [Vercel Labs](https://github.com/vercel-labs/agent-browser)
