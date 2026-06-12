# Micro-SaaS Portfolio Plan

## 1. Ranked Opportunities

| Rank | Product | Speed | Revenue Potential | Competition | Skill Fit | Score |
|------|---------|-------|-------------------|-------------|-----------|-------|
| 1 | AI Visibility Checker | 3-4 days | $29-49/mo, high volume | Low (new category) | High (API chaining, scraping) | 9.2 |
| 2 | MCP Context Optimization Server | 1-2 weeks | $10-30/mo, dev niche | Medium (early market) | Very High (already running MCPs) | 8.7 |
| 3 | WhatsApp/Telegram MCP Server | 2-3 weeks | $15-49/mo | Low-Medium | Very High (Telegram bot experience) | 8.1 |
| 4 | Codebase-to-Tutorial SaaS | 2-3 weeks | $10-29/mo | Medium | Medium | 7.0 |
| 5 | Boring Compliance SaaS | 4-6 weeks | $50-100/mo, slower growth | High (established players) | Low (domain expertise needed) | 5.8 |

### Scoring Rationale

**AI Visibility Checker wins because:**
- Fastest to ship (3-4 days = revenue this week)
- Novel category with viral potential ("see who AI recommends instead of you")
- Every business owner with a website is a customer (massive TAM)
- No MCP expertise needed from buyer = broader market
- High perceived value = premium pricing justified
- Perfect for Product Hunt launch (visual, shareable results)

---

## 2. #1 Pick: AI Visibility Checker — Full Build Spec

### Concept
"Who does ChatGPT recommend instead of you?" — Enter your brand/product, get a report showing how visible you are across AI models (ChatGPT, Claude, Gemini, Perplexity) and who gets recommended instead.

### Tech Stack
- **Frontend**: Next.js 14 (App Router) + Tailwind + shadcn/ui
- **Backend**: Next.js API routes + Bull queue (Redis)
- **Database**: PostgreSQL (Supabase free tier to start)
- **AI APIs**: OpenAI API, Anthropic API, Google Gemini API
- **Payments**: Stripe (checkout + subscriptions)
- **Email**: Resend (already have)
- **Hosting**: Vercel (frontend) + Railway or Docker on pharma6 (queue workers)
- **Domain**: aivisibility.co or brandradar.ai

### MVP Features (ship in 3-4 days)
1. **Brand Scan** — User enters brand name + category (e.g., "Notion" + "project management")
2. **Multi-Model Query** — System asks ChatGPT, Claude, Gemini: "What are the best [category] tools?" in 10 prompt variations
3. **Visibility Score** — 0-100 score based on mention frequency, position, sentiment
4. **Competitor Map** — Who gets mentioned instead, how often, in what context
5. **PDF Report** — Downloadable branded report (shareable = viral)
6. **Weekly Monitoring** — Track score changes over time (subscription hook)

### Prompt Engineering (Core IP)
```
Prompts to fire per scan (10 variations):
- "What are the best {category} tools in 2026?"
- "I need a {category} solution, what do you recommend?"
- "Compare the top {category} platforms"
- "{brand} vs competitors"
- "What's better than {brand}?"
- "Recommend a {category} tool for small business"
- "What {category} tool has the best reviews?"
- "I'm switching from {brand}, what should I use?"
- "{category} tools ranked"
- "Which {category} tool is most popular?"
```

### Pricing
| Plan | Price | Includes |
|------|-------|----------|
| Single Scan | $9 one-time | 1 brand, 1 report, PDF download |
| Pro | $29/mo | 3 brands, weekly monitoring, alerts, historical trends |
| Agency | $49/mo | 10 brands, white-label reports, API access |

### Landing Page Copy Outline

**Headline**: "Is AI Recommending Your Competitors Instead of You?"

**Subhead**: "Find out exactly what ChatGPT, Claude, and Gemini say when customers ask for products like yours."

**Hero CTA**: "Scan My Brand Free" (limited free scan = lead gen)

**Social Proof Section**: Show example reports (anonymized or self-generated)

**Pain Points**:
- "40% of product research now starts with AI, not Google"
- "You can't optimize what you can't measure"
- "Your competitors might already be gaming AI visibility"

**How It Works** (3 steps):
1. Enter your brand + category
2. We query major AI models with real user prompts
3. Get your Visibility Score + actionable recommendations

**Pricing Section**: Plans above

**FAQ**:
- "How is this different from SEO tools?" — AI models don't use Google rankings
- "Can I improve my score?" — Yes, we provide specific recommendations
- "How often are results updated?" — Weekly for Pro/Agency plans

### Day-by-Day Build Plan
- **Day 1**: Next.js scaffold, Stripe integration, landing page, database schema
- **Day 2**: Core scan engine (multi-model queries, parsing, scoring algorithm)
- **Day 3**: Results dashboard, PDF generation, email delivery
- **Day 4**: Polish, free tier limit logic, deploy, test end-to-end

---

## 3. #2 Pick: MCP Context Optimization Server — Brief Spec

### Concept
A hosted MCP server that intelligently manages context windows for Claude Code / Cursor / Windsurf users. Automatically summarizes, prioritizes, and rotates context to maximize LLM output quality.

### Key Features (MVP)
- Connect via MCP protocol to any compatible IDE
- Auto-summarize long files before injecting into context
- Priority queue: most relevant files ranked by recency + relevance
- Context budget manager: visual indicator of token usage
- "Memory" layer: persist important facts across sessions

### Tech Stack
- TypeScript MCP server (Node.js)
- Redis for session state
- Stripe for billing
- Docker image for self-host option

### Timeline: 10 days
- Days 1-3: MCP server scaffold, protocol compliance, basic context routing
- Days 4-6: Summarization engine, priority algorithm, memory persistence
- Days 7-8: Dashboard UI (usage stats, config)
- Days 9-10: Stripe billing, docs, launch prep

### Pricing: $10/mo (indie), $25/mo (team), $99/mo (enterprise self-host license)

---

## 4. #3 Pick: WhatsApp/Telegram MCP Server — Brief Spec

### Concept
MCP server that gives Claude Code / AI agents the ability to send and receive WhatsApp and Telegram messages programmatically. Enables AI-powered customer support, notifications, and conversational workflows.

### Key Features (MVP)
- MCP tools: send_message, read_messages, list_chats, send_media
- WhatsApp Business API integration (via official Cloud API)
- Telegram Bot API integration (already have experience)
- Message queue with retry logic
- Webhook receiver for incoming messages
- Rate limiting and audit log

### Tech Stack
- TypeScript MCP server
- WhatsApp Cloud API + Telegram Bot API
- PostgreSQL (message log)
- Bull queue (delivery)
- Docker deployment

### Timeline: 14 days
- Days 1-4: MCP protocol server, Telegram integration (known territory)
- Days 5-9: WhatsApp Business API integration, webhook handling
- Days 10-12: Dashboard (message logs, analytics, config)
- Days 13-14: Billing, docs, launch

### Pricing: $15/mo (1 channel, 1K msgs), $35/mo (both channels, 10K msgs), $49/mo (unlimited + priority)

---

## 5. Distribution Strategy

### Launch Sequence (per product)

**Week -1 (Pre-launch)**:
- Build in public on Twitter/X (daily progress screenshots)
- Collect 50+ emails via waitlist on landing page
- Write "Show HN" draft

**Launch Day**:
- Product Hunt launch (schedule for Tuesday 12:01 AM PT)
- Hacker News "Show HN" post
- Reddit: r/SaaS, r/Entrepreneur, r/ChatGPT (for AI Visibility Checker), r/LocalLLaMA, r/ClaudeAI (for MCP products)
- Twitter/X thread with demo video

**Week +1 (Amplification)**:
- Indie Hackers post with revenue numbers
- Dev.to / Hashnode technical article
- YouTube short demo (< 2 min)
- Cold DM 20 relevant Twitter accounts for feedback/RT

**Ongoing**:
- SEO content: "How to improve AI visibility" blog posts
- Affiliate program (20% recurring for MCP products)
- Integration partnerships (list on MCP directories, AI tool aggregators)

### Channel Priority by Product
| Product | Primary Channel | Secondary |
|---------|----------------|-----------|
| AI Visibility Checker | Product Hunt + Twitter | Reddit r/SEO, r/marketing |
| MCP Context Server | Hacker News + r/ClaudeAI | Dev.to, MCP registries |
| Telegram/WA MCP | MCP registries + r/LocalLLaMA | Product Hunt |

---

## 6. Cross-Sell from TradeFlow

### Existing Assets
- 60+ active users (traders = high-income, tool-buyers)
- Email list with established open rates
- Telegram notification channel (direct push)

### Cross-Sell Plays

1. **AI Visibility Checker for Trading Educators**
   - TradeFlow users who also run courses/communities → "See if AI recommends your trading course"
   - In-app banner + email blast

2. **MCP Server for TradeFlow Power Users**
   - TradeFlow already uses Claude → offer context optimization as upgrade
   - "Make your TradeFlow AI assistant smarter with MCP Context Pro"

3. **Bundle Discount**
   - "TradeFlow Pro users get 30% off any micro-SaaS product"
   - Increases perceived value of TradeFlow subscription

4. **Referral Loop**
   - Each micro-SaaS has "Powered by the TradeFlow team" footer
   - Drives discovery back to TradeFlow for trader audience

---

## 7. Revenue Projection: Path to $5K MRR

### Month 1 (AI Visibility Checker launch)
- 200 single scans at $9 = $1,800 one-time
- 30 Pro signups at $29/mo = $870 MRR
- **Total MRR: $870**

### Month 2 (MCP Context Server launch + AVC growth)
- AVC: 50 Pro + 5 Agency = $1,695 MRR
- MCP Context: 40 indie + 5 team = $525 MRR
- **Total MRR: $2,220**

### Month 3 (Telegram/WA MCP launch + organic growth)
- AVC: 80 Pro + 10 Agency = $2,810 MRR
- MCP Context: 70 indie + 10 team = $950 MRR
- Telegram/WA MCP: 25 base + 10 pro = $725 MRR
- **Total MRR: $4,485**

### Month 4 (optimization + content marketing kicks in)
- AVC: 100 Pro + 15 Agency = $3,635 MRR
- MCP Context: 90 indie + 15 team = $1,275 MRR
- Telegram/WA MCP: 40 base + 15 pro = $1,125 MRR
- **Total MRR: $6,035**

### Key Assumptions
- 3-5% monthly churn (typical for low-ticket SaaS)
- Product Hunt launch drives 500+ signups per product
- 5-8% free-to-paid conversion
- No paid ads in first 4 months (organic only)

### Milestone Targets
| Milestone | Target Date | Revenue |
|-----------|-------------|---------|
| First dollar | Week 1 | $9 (single scan) |
| $1K MRR | Month 1.5 | AI Visibility Checker alone |
| $3K MRR | Month 2.5 | AVC + MCP Context |
| $5K MRR | Month 3.5 | Full portfolio |

---

## Next Actions (This Week)

1. **Today**: Register domain (aivisibility.co), scaffold Next.js project
2. **Day 1-2**: Core scan engine + Stripe + landing page
3. **Day 3-4**: Dashboard, PDF reports, deploy to Vercel
4. **Day 5**: Beta test with 10 TradeFlow users, collect feedback
5. **Day 6**: Product Hunt listing prep (screenshots, description, maker comment)
6. **Day 7**: Launch on PH + HN + Reddit simultaneously
