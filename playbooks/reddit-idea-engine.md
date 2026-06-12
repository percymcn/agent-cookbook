# Reddit Business Idea Engine - Felix Playbook

## What This Is
Automated system where Felix scrapes Reddit, identifies validated pain points, generates micro-SaaS/service ideas, and adds them to the build pipeline. Runs on existing tools - no API keys needed beyond what we have.

## The Playbook (5-Stage Funnel)

### Stage 1: Wide Scan (100+ raw ideas)
**Source:** Y Combinator RFS, a16z theses, Starter Story, IndieHackers
**Felix does:** Scrape trending posts, feed to Claude via `claude -p`, generate 100+ ideas filtered through Purse's skills (trading, crypto, Jamaica market, AI automation)

### Stage 2: Reddit Pain Mining (narrow to 25)
**Subreddits to monitor:**
- r/smallbusiness, r/SaaS, r/Entrepreneur (general)
- r/webdev, r/sysadmin, r/devops (technical)
- r/DigitalMarketing, r/PPC, r/seo (marketing)
- r/ecommerce, r/shopify (commerce)
- r/cryptocurrency, r/algotrading (trading/crypto)
- r/Jamaica, r/Caribbean (local market)

**Method:**
1. Scrape posts with keywords: "frustrated", "wish there was", "anyone know a tool", "paying for", "hate that", "looking for alternative"
2. Feed comments to Claude: "Rank recurring complaints, identify feature gaps, estimate willingness to pay"
3. Output: Clustered pain patterns with pricing signals

### Stage 3: Competitor Review Mining (prioritize to 10)
**Source:** G2, Capterra, TrustRadius 1-2 star reviews
**Method:**
1. Scrape competitor low-rating reviews
2. Summarize with Claude: missing integrations, hidden fees, poor support
3. Extract: feature roadmap + marketing copy

### Stage 4: Outreach Validation (3-5 ideas)
**Method:**
1. Filter for businesses with low ratings on Google Business
2. Generate personalized outreach quoting their own review pain
3. Example: "Hi Sarah, 3 reviewers mentioned slow response at your dental office. I build AI assistants that cut reply time from hours to minutes."

### Stage 5: Build Decision (1 launch candidate)
**Criteria:**
- Can Felix build it autonomously? (no human coding needed)
- $29-199/mo price point?
- <500 lines of code for MVP?
- Pain validated in 3+ Reddit posts?

---

## Top 10 Ideas We Can Build NOW

### Tier A: Felix Can Build Solo (no new APIs needed)

| # | Idea | Revenue | Effort | Source |
|---|------|---------|--------|--------|
| 1 | **AI Search Visibility Tracker** - Monitor brand presence in ChatGPT/Perplexity/Gemini | $79-199/mo | 2 days | r/seo |
| 2 | **Google Algorithm Drop Forensics** - Diagnose traffic losses from updates | $49/mo + $199 audit | 3 days | r/seo |
| 3 | **Automated SOP Generator** - Turn Loom videos + docs into SOPs | $50-200/mo | 2 days | r/smallbusiness |
| 4 | **Vendor/Subscription Optimizer** - Find duplicate/unused SaaS subscriptions | $20-100/mo | 1 day | r/smallbusiness |
| 5 | **Agency Contract Analyzer** - AI reviews contracts for red flags | $19-49/analysis | 2 days | r/DigitalMarketing |

### Tier B: Felix + Existing Skills

| # | Idea | Revenue | Effort | Source |
|---|------|---------|--------|--------|
| 6 | **Crypto Trading Alert Service** - Telegram signals from AlphaEar | $50-200/mo sub | 1 day | r/algotrading |
| 7 | **E-commerce Review Analyzer** - Scrape + sentiment analysis for stores | $19-79/mo | 2 days | r/ecommerce |
| 8 | **SEO Content Generator** - Research + write optimized blog posts | $6K/mo agency | ongoing | r/seo |
| 9 | **Cold Outreach Personalization** - AI writes emails from prospect research | $500-1K/client | 1 day | r/DigitalMarketing |
| 10 | **Market Research Reports** - Auto-generate industry reports from Reddit/web | $500-3K/report | 3 days | r/Entrepreneur |

---

## Felix Automation Schedule

```
DAILY (via autonomous driver):
- Scrape 5 target subreddits for new pain points
- Score + rank new opportunities
- Add top finds to task_pool.json

WEEKLY:
- Generate "Reddit Opportunities Report" saved to brain/research/
- Cross-reference with existing build capabilities
- Update this playbook with new validated ideas

MONTHLY:
- Full competitor review sweep (G2/Capterra)
- Revenue potential re-ranking
- Prune dead ideas, promote validated ones
```

## Tools Used (all existing, no new costs)
- `deep-research-pro` skill for web research
- `alphaear-search` / `alphaear-sentiment` for market analysis
- `apify-lead-generation` for scraping
- `cold-outreach` skill for validation outreach
- `claude -p` for analysis (uses existing Max subscription)
- Telegram bot for notifications

## Sources
- [30 Micro SaaS Ideas Reddit Is Begging You to Build](https://www.greensighter.com/blog/micro-saas-ideas)
- [50 Micro-SaaS Opportunities from Reddit](https://www.saasniche.com/blog/50-micro-saas-opportunities-from-reddit-in-2026)
- [How I Use Reddit + AI to Find Winning Startup Ideas](https://blog.alexanderfyoung.com/how-i-use-reddit-and-ai-to-find-winning-startup-ideas-2025-tutorial/)
- [10 OpenClaw Side Hustles](https://growwstacks.com/blog/openclaw-side-hustles)
- [Using AI to Find Business Ideas with Reddit and n8n](https://www.youtube.com/watch?v=D2Y9FKvVUig)
- [AI Automation to Find Validated Startup Ideas](https://www.youtube.com/watch?v=N4Oh06BvGRM)
- [Best Way to Start AI Automation Agency 2026](https://www.youtube.com/watch?v=m-uQJ8AseMw)
