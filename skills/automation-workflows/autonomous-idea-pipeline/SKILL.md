---
name: autonomous-idea-pipeline
description: Build and operate fully autonomous systems for continuously discovering, validating, and preparing business opportunities from multiple data sources without manual intervention.
---
# Autonomous Idea Pipeline

## Overview

Create self-operating systems that continuously scan for business opportunities, validate them against predefined criteria, and generate actionable plans—all without manual intervention. This skill covers the design, implementation, and maintenance of autonomous idea generation pipelines.

## When to Use

Use this skill when you want to:
- Build systems that run autonomously on schedules (e.g., every 6 hours, daily)
- Continuously monitor multiple sources for opportunities (YouTube, Reddit, forums, etc.)
- Automatically validate and score business ideas based on revenue potential, simplicity, etc.
- Generate ready-to-execute business plans for top opportunities
- Operate without manual intervention once deployed

## Core Components

An autonomous idea pipeline consists of:

1. **Source Scrapers** - Modules that extract data from target sources
2. **Validation Engine** - System that scores and ranks opportunities
3. **Idea Generator** - Creates business models from validated pain points
4. **Plan Builder** - Generates actionable implementation steps
5. **Delivery System** - Sends results to desired output channels
6. **Scheduler/Orchestrator** - Controls when and how often the pipeline runs
7. **Logging & Monitoring** - Tracks performance and system health

## Implementation Workflow

### 1. Define Sources and Triggers

Identify what sources to monitor and how often to scan them:

```text
SOURCES:
- YouTube: @thekoerneroffice, @starterstory (business model videos)
- Reddit: r/Entrepreneur, r/SideHustle, r/smallbusiness (pain points)
- Additional: Product Hunt, Indie Hackers, Google Trends (optional)

TRIGGER: Schedule-based (e.g., every 6 hours)
```

### 2. Build Scraper Modules

Create specialized scrapers for each source type:

**YouTube Scraper:**
- Navigate to channel videos page
- Extract video titles, descriptions, view counts, upload dates
- Identify business models with revenue claims
- Structure data for validation

**Reddit Scraper:**
- Monitor target subreddits
- Extract posts with pain point language ("I wish", "Anyone know how to")
- Filter by engagement (upvotes, comments) and recency
- Structure pain points for ideation

### 3. Design Validation Criteria

Create a scoring system that evaluates opportunities:

```text
SCORING FRAMEWORK (0-100 points):

Revenue Potential (0-30):
- Explicit revenue claims in source: 15pts
- Market size indicators: 10pts  
- Monetization clarity: 5pts

Simplicity (0-25):
- Implementation complexity: 10pts
- Required skills/knowledge: 5pts
- Dependencies/barriers: 5pts
- Time to first revenue: 5pts

Automation Feasibility (0-20):
- Can be built with available tools: 10pts
- Requires minimal custom code: 5pts
- Has automatable delivery: 5pts

Validation Signals (0-15):
- Multiple sources mention similar ideas: 5pts
- Evidence of willingness to pay: 5pts
- Low competition indicators: 5pts

Actionability (0-10):
- Clear next steps identifiable: 5pts
- MVP scope definable: 5pts
```

### 4. Implement Idea Generation

Transform validated pain points into business models:

**Pattern Matching Approach:**
- Map pain points to known business model templates
- Apply successful models from source materials
- Generate variations based on context

**Template Library:**
- Digital Product Funnel (Google Drive links, courses)
- Service Arbitrage/Middleman
- Subscription/Community Models
- Automated Service Businesses
- Marketplace/Aggregator Models

### 5. Build Execution Plans

Convert scored ideas into actionable plans:

**Plan Components:**
- Problem statement (from pain point)
- Proposed solution (business model)
- Revenue model explanation
- Step-by-step implementation guide
- Required tools/resources from available skills
- Estimated timeline and effort
- First 30-day action plan
- Success metrics to track

### 6. Set Up Autonomous Operation

Configure the system to run without intervention:

**Scheduler Options:**
- Cron jobs (every 6h, daily, weekly)
- Cloud schedulers (if deploying externally)
- Internal orchestrators with retry logic

**Autonomous Features:**
- Error handling and recovery
- State persistence between runs
- Duplicate detection (don't process same opportunity twice)
- Performance metrics logging
- Self-healing capabilities

### 7. Implement Delivery System

Get results to where they're needed:

**Output Options:**
- Direct chat/message delivery (Telegram, Slack, etc.)
- Email summaries/reports
- File saves to specific directories
- Dashboard updates
- API/webhook notifications

## Best Practices

### Design for Autonomy:
- Assume no human will be available during execution
- Include comprehensive error handling
- Log everything for post-run analysis
- Make all steps idempotent where possible
- Validate inputs and outputs at each stage
- **Bias toward action**: When in doubt, execute rather than seek clarification
- **Human-in-the-loop only for complex decisions**: Seek approval only for:
  - Financial transactions/payments
  - Major strategic pivots
  - Legal/compliance issues
  - Explicit user requests for input
- Default to "go ahead" unless the user has explicitly said to wait for approval on a specific matter
- **Bias toward action**: When in doubt, execute rather than seek clarification
- **Human-in-the-loop only for complex decisions**: Seek approval only for:
  - Financial transactions/payments
  - Major strategic pivots
  - Legal/compliance issues
  - Explicit user requests for input
- Default to "go ahead" unless the user has explicitly said to wait for approval on a specific matter
- **Bias toward action**: When in doubt, execute rather than seek clarification
- **Human-in-the-loop only for complex decisions**: Seek approval only for:
  - Financial transactions/payments
  - Major strategic pivots
  - Legal/compliance issues
  - Explicit user requests for input
- Default to "go ahead" unless the user has explicitly said to wait for approval on a specific matter

### Validation Tuning:\n- Start with broad criteria, narrow based on results\n- Track false positives/negatives to improve scoring\n- Adjust weights based on actual outcomes\n- Incorporate feedback loops when possible\n\n### Security and Ethics:\n- Respect robots.txt and terms of service\n- Implement reasonable request throttling\n- Don't scrape personally identifiable information without consent\n- Clearly identify your bot/user agent\n\n## SESSION-SPECIFIC LEARNINGS AND USER PREFERENCES (GIDEON EDITION)\n\nBased on implementation in this session with user Gideon, these patterns emerged as critical for successful autonomous operation:\n\n### STRONG BIAS TOWARD ACTION\nUser explicitly stated: \"just go ahead\" and \"you do everything\" - systems should default to execution unless explicitly told to wait for approval on a specific matter.\n\n### HUMAN-IN-THE-LOOP TRIGGERS\nSeek user input ONLY for:\n- Financial transactions/payments (Stripe invoicing)\n- Prospect responses requiring conversation/negotiation\n- Major strategic pivots (user-defined)\n- Legal/compliance issues\n- Explicit user requests for input on specific matters\n\n### ACCOMMODATING DRIVING CONSTRAINTS\nWhen user indicates they cannot read (driving, etc.):\n- PRIMARY: Audio responses via text-to-speech for updates and alerts\n- SECONDARY: Very concise text summaries when audio not feasible\n- ALERT ONLY: For action-required situations (prospect responses, payments, decisions)\n- SILENT OPERATION: All background processes run without notification\n- USER-INITIATED CHECKS: User can request status via simple voice commands\n\n### PROVEN AUTONOMOUS SYSTEMS FROM THIS SESSION\nThese patterns work reliably based on implementation:\n- **Content Repurposing Pipeline**: YouTube → transcript → 4 formats (Twitter, LinkedIn, Blog, Instagram) every 4 hours\n- **Prospect Research**: Automated identification of leads across niches every 2 hours\n- **Personalized Outreach**: Automated initial contact + follow-up sequences (day 2, 4, 7)\n- **Response Monitoring**: Automated checking for replies with instant audio alerting\n- **Business Opportunity Scanning**: Continuous discovery from multiple sources every 4-6 hours\n\n### INTERNET ACCESS CAPABILITIES\nAutonomous systems can access the internet through:\n- **Headless Browser Automation**: browser_navigate, browser_snapshot, browser_type, browser_click\n- **Direct HTTP Requests**: Via terminal using curl/wget for API calls\n- **Specialized Skills**: Web search, financial data, YouTube content, social media\n- **Agent Delegation**: For parallel work, delegate to subagents with same capabilities\n\n### CROSS-SESSION LEARNING\nUse memory for storing durable facts about user preferences and system state that persist across conversations.

## Common Pitfalls and Fixes

| Problem | Solution |
|---------|----------|
| Getting blocked by sources | Add delays, rotate user agents, respect rate limits |
| Low signal-to-noise ratio | Improve filtering criteria, add validation steps |
| Duplicate processing | Implement opportunity deduplication using hashes/IDs |
| Schema changes breaking scrapers | Add flexible parsing, error recovery, version detection |
| Analysis paralysis from too many ideas | Implement strong scoring, limit outputs to top N |
| Automation fatigue | Design for true autonomy - set and forget for weeks |

## Available Tools in Hermes Ecosystem\n\nLeverage these built-in capabilities:\n\n**Scraping & Data Collection:**\n- `browser_navigate`, `browser_snapshot`, `browser_type`, `browser_click`\n- `execute_code` for custom parsing logic\n- `search_files` and `read_file` for local data\n- `youtube-content` for extracting video transcripts (proven effective)\n\n**Processing & Analysis:**\n- `execute_code` for Python-based analysis\n- `write_file` for saving intermediate results\n- `memory` for cross-session learning\n- `session_search` for referencing past discoveries\n\n**Automation & Orchestration:**\n- `cronjob` for scheduling pipeline runs (proven reliable for autonomous operation)\n- `delegate_task` for parallel processing (analyze multiple ideas simultaneously)\n- `skill_view` for loading domain-specific expertise\n- `plan` for documenting workflows before execution\n\n**Delivery & Communication:**\n- `send_message` for chat/Telegram delivery\n- `write_file` for saving reports/plans\n- `text_to_speech` for audio summaries (if needed)\n- `image_generate` for visual reports/diagrams\n\n## Proven Tool Combinations\n\nBased on implementation experience, these tool combinations work particularly well:\n\n**For YouTube Content Extraction:**\n- `youtube-content` skill + `execute_code` for parsing = Reliable transcript extraction\n- Alternative: `browser_navigate` to video page + `browser_snapshot` + `execute_code` for DOM parsing\n\n**For Reddit/Web Scraping:**\n- `agent-browser` skill (provides `browser_*` tools) + `execute_code` for data extraction\n- Pattern: Navigate → Extract HTML/JSON → Parse with Python → Structure data\n\n**For Autonomous Operation:**\n- `cronjob` (every 4-6h) + dedicated directory + timestamped files = Persistent autonomous system\n- Adding `memory` for cross-session learning improves accuracy over time\n\n**For Idea Validation:**\n- `execute_code` for scoring algorithms + `write_file` for saving scored opportunities\n- Combining multiple data sources (YouTube + Reddit) increases signal quality\n\n## Implementation Patterns\n\n### Data Flow Optimization\n```\n[Scheduler] → [Specialized Scrapers] → [Data Normalization] → [Validation Engine] → [Idea Generation] → [Plan Builder] → [Delivery]\n```\n\n### Error Handling Patterns\n1. **Source Failures**: Implement exponential backoff and fallback sources\n2. **Parsing Errors**: Use try/catch with logging and skip rather than halt\n3. **Rate Limiting**: Respect robots.txt, add delays between requests, rotate user agents\n4. **Schema Changes**: Implement flexible parsing with fallback selectors\n\n### State Management\n- Use timestamped files in dedicated directories for historical analysis\n- Implement opportunity deduplication using content hashes\n- Track processed IDs to avoid duplicate work across runs\n- Store intermediate results for debugging and re-processing\n\n### Delivery Optimization\n- Format results as readable Markdown for Telegram/chat consumption\n- Include actionable next steps and required tools\n- Provide summary statistics (total scanned, ideas found, top opportunities)\n- Consider attaching detailed JSON for programmatic consumption\n\n## Common Pitfalls and Fixes\n\n| Problem | Solution |\n|---------|----------|\n| Getting blocked by sources | Add delays, rotate user agents, respect rate limits, use yt-dlp alternative for YouTube |\n| Low signal-to-noise ratio | Improve filtering criteria, add validation steps, require multiple source confirmation |\n| Duplicate processing | Implement opportunity deduplication using content hashes + similarity detection |\n| Schema changes breaking scrapers | Add flexible parsing with CSS selector fallbacks, error recovery, version detection |\n| Analysis paralysis from too many ideas | Implement strong scoring, limit outputs to top N, use tiered scoring (quick filter → deep analysis) |\n| Automation fatigue | Design for true autonomy - set and forget for weeks, include self-healing capabilities |\n| Incomplete data extraction | Validate extracted data, implement retry mechanisms for partial failures |\n| Processing bottlenecks | Use delegate_task for parallel source analysis, implement caching for repeated operations |\n| Delivery failures | Implement multiple delivery channels (chat + file save + email fallback) |\n\n## Enhanced Validation Framework\n\nBased on implementation learnings, enhance the scoring system with:\n\n```text\nENHANCED SCORING FRAMEWORK (0-100 points):\n\nRevenue Potential (0-25):\n- Explicit revenue claims with proof: 10pts\n- Market size/TAM indicators: 8pts\n- Monetization clarity and path: 7pts\n\nSimplicity & Execution (0-20):\n- Implementation complexity with available tools: 8pts\n- Required skills/knowledge assessment: 6pts\n- Time to first revenue/prototype: 6pts\n\nAutomation Potential (0-20):\n- % of process automatable with Hermes tools: 10pts\n- Need for external APIs/services: 5pts\n- Maintenance/oversight required: 5pts\n\nValidation Strength (0-15):\n- Multiple independent source confirmation: 5pts\n- Evidence of willingness to pay (pre-orders, etc.): 5pts\n- Low competition/market gap indicators: 5pts\n\nActionability & Clarity (0-10):\n- Clear MVP scope definition: 5pts\n- Immediate next steps identifiable: 5pts\n\nBonus: AI/LLM Leverage (0-10)\n- Degree to which AI eliminates manual work: up to 10pts\n```\n\n## Maintenance & Evolution\n\n### Weekly Review Checklist\n1. **Pipeline Health**: Review logs for errors, success rates, processing times\n2. **Source Quality**: Evaluate signal-to-noise ratio for each source, consider additions/removals\n3. **Idea Quality**: Sample 5-10 generated ideas, assess actionability and novelty\n4. **Performance Metrics**: Track ideas processed per run, scoring distribution, delivery success\n5. **Tool Updates**: Check for new Hermes skills/tools that could enhance pipeline\n\n### Monthly Enhancement Cycle\n1. **Scoring Refinement**: Adjust weights based on any implemented ideas' actual performance\n2. **Source Expansion**: Test new sources (newsletters, forums, product sites) for signal quality\n3. **Template Library**: Add new business model templates based on observed patterns\n4. **Automation Deep Dive**: Identify manual steps in pipeline that could be automated further\n5. **Feedback Integration**: If available, incorporate outcomes from tested/implemented ideas\n\n## Success Indicators\n\nAn autonomous idea pipeline is working well when:\n- It runs consistently without manual intervention for 4+ weeks\n- >60% of generated ideas pass initial manual review for plausibility\n- Top 3 ideas each run show increasing actionability and specificity\n- The system introduces novel combinations or variations not seen in source materials\n- Maintenance time decreases over time as the system stabilizes\n\n## Example: AI-Focused Variant\n\nFollowing the pattern from our implementation, an AI/automation-focused variant would:\n\n1. **Source Filtering**: Prioritize YouTube videos with AI/automation keywords in titles/descriptions\n2. **Transcript Analysis**: Extract full transcripts and scan for implementation steps, tools used, revenue models\n3. **Pain Point Detection**: Scan Reddit for posts mentioning manual work that could be automated with AI\n4. **AI-Specific Scoring**: Add weights for:\n   - AI tool availability in Hermes ecosystem\n   - Degree of human-in-the-loop elimination\n   - Scalability of AI solution\n   - Data/API availability for training/operation\n\nThis approach led to the discovery of opportunities like AI content repurposing, automated lead enrichment, and AI-powered niche SaaS wrappers that can be built primarily with existing Hermes tools.

## Example Implementation

The system we just built includes:
- YouTube channel scraper for @thekoerneroffice and @starterstory
- Reddit pain point miner for Entrepreneur, SideHustle, smallbusiness, WorkOnline
- Scoring system based on revenue claims, simplicity, automation potential
- Idea generation using business model templates
- Plan creation with implementation steps
- Cron job scheduler (every 6 hours)
- Results delivery back to chat
- Logging and state persistence

This represents a working autonomous idea pipeline that operates continuously without manual intervention.

## Maintenance Checklist

**Weekly:**
- Review pipeline logs for errors or patterns
- Check source availability and response times
- Review a sample of generated ideas for quality
- Update scraper selectors if sources changed
- Verify delivery system is working

**Monthly:**
- Evaluate overall ROI - are ideas actionable and valuable?
- Consider adding/removing sources based on signal quality
- Refine scoring criteria based on any implemented ideas
- Check for new available tools/skills that could enhance pipeline
- Archive old results and maintain clean storage

## Next-Level Enhancements

Once the basic pipeline is stable, consider:
- Adding predictive modeling for idea success
- Implementing A/B testing of different validation criteria
- Building a rejection analysis system (why ideas were filtered out)
- Creating cross-pipeline idea combination (mixing elements from different sources)
- Adding automated prototyping for top ideas (landing pages, basic MVPs)
- Building a feedback loop from implemented ideas to improve scoring
## SESSION-SPECIFIC LEARNINGS AND USER PREFERENCES (GIDEON EDITION)

Based on implementation in this session with user Gideon (Purse), these patterns emerged as critical for successful autonomous operation:

### STRONG BIAS TOWARD ACTION
User explicitly stated: "just go ahead" and "you do everything" - systems should default to execution unless explicitly told to wait for approval on a specific matter.

### HUMAN-IN-THE-LOOP TRIGGERS
Seek user input ONLY for:
- Financial transactions/payments (Stripe invoicing)
- Prospect responses requiring conversation/negotiation
- Major strategic pivots (user-defined)
- Legal/compliance issues
- Explicit user requests for input on specific matters

### ACCOMMODATING DRIVING CONSTRAINTS
When user indicates they cannot read (driving, etc.):
- PRIMARY: Audio responses via text-to-speech for updates and alerts
- SECONDARY: Very concise text summaries when audio not feasible
- ALERT ONLY: For action-required situations (prospect responses, payments, decisions)
- SILENT OPERATION: All background processes run without notification
- USER-INITIATED CHECKS: User can request status via simple voice commands

### PROVEN AUTONOMOUS SYSTEMS FROM THIS SESSION
These patterns work reliably based on implementation:
- **Content Repurposing Pipeline**: YouTube → transcript → 4 formats (Twitter, LinkedIn, Blog, Instagram) every 4 hours
- **Prospect Research**: Automated identification of leads across niches every 2 hours
- **Personalized Outreach**: Automated initial contact + follow-up sequences (day 2, 4, 7)
- **Response Monitoring**: Automated checking for replies with instant audio alerting
- **Business Opportunity Scanning**: Continuous discovery from multiple sources every 4-6 hours (using youtube-content skill with metadata fallback when transcripts blocked)

### INTERNET ACCESS CAPABILITIES
Autonomous systems can access the internet through:
- **Headless Browser Automation**: browser_navigate, browser_snapshot, browser_type, browser_click
- **Direct HTTP Requests**: Via terminal using curl/wget for API calls
- **Specialized Skills**: Web search, financial data, YouTube content, social media
- **Agent Delegation**: For parallel work, delegate to subagents with same capabilities

### CROSS-SESSION LEARNING
Use memory for storing durable facts about user preferences and system state that persist across conversations.
    Autonomous systems can access the internet through:
    - **Headless Browser Automation**: browser_navigate, browser_snapshot, browser_type, browser_click
    - **Direct HTTP Requests**: Via terminal using curl/wget for API calls
    - **Specialized Skills**: Web search, financial data, YouTube content, social media
    - **Agent Delegation**: For parallel work, delegate to subagents with same capabilities
    
    ### CROSS-SESSION LEARNING
    Use memory for storing durable facts about user preferences and system state that persist across conversations.