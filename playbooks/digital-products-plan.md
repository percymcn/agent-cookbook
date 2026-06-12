# Digital Products & Courses — Revenue Stream Plan

## 1. Top 3 Product Ideas (Ranked: Effort vs Revenue)

| Rank | Product | Effort | Revenue Potential | Why |
|------|---------|--------|-------------------|-----|
| 1 | **AI Agency Blueprint** | Medium | $5-15K/mo | Highest demand, broadest audience, Nick Saraev proving the model at $250K/mo. Purse has real receipts (Fluxio, OneGo, TradeFlow). |
| 2 | Trading Automation Course + Templates | Medium-High | $3-8K/mo | Niche but high-ticket buyers. Leverages TradeFlow, webhook-to-broker, TradingView expertise. Smaller TAM. |
| 3 | n8n/Claude Workflow Templates Marketplace | Low | $1-3K/mo | Easy to produce, but low ticket ($19-49 per template). Better as a lead magnet or upsell funnel entry. |

**Winner: AI Agency Blueprint**

Rationale: The "build an AI agency" market is exploding. Purse has actual running businesses (not theory). The audience on Twitter/YouTube already follows for AI + automation content. This product has the widest funnel and highest perceived value.

---

## 2. Product Outline — "AI Agency Blueprint"

### Course Title
**"Ship & Scale: Build a Profitable AI Agency in 30 Days"**

### Modules

| Module | Title | Content |
|--------|-------|---------|
| 0 | Foundations | What an AI agency actually sells, market positioning, who pays $2-10K/mo for AI work |
| 1 | Your Tech Stack | Claude Code + MCP servers, n8n, Docker, Telegram bots — the exact stack Purse uses |
| 2 | First Client in 7 Days | Outreach templates, pricing frameworks, proposal docs, how to close without a portfolio |
| 3 | Delivery System | SOPs for client onboarding, project management, using AI to 10x delivery speed |
| 4 | Automation Builds (Live) | 3 real builds: Telegram bot, n8n webhook workflow, Chrome automation with MCP |
| 5 | Productize & Scale | Turning custom work into repeatable packages, hiring contractors, building SaaS from client work |
| 6 | Case Studies | TradeFlow (trading SaaS from scratch), OneGo (ride-hailing MVP), Fluxio (agency ops) |
| Bonus | Template Vault | n8n workflows, proposal templates, client onboarding docs, Claude prompts library |

### Pricing Tiers

| Tier | Price | Includes |
|------|-------|----------|
| Self-Paced | $197 | All modules, template vault, community access |
| Pro | $497 | + 2 group coaching calls/month, private Discord channel, code reviews |
| Done-With-You | $1,997 | + 4x 1:1 calls, custom stack setup, first client acquisition support |

### Platform
**Primary: Whop** (handles payments, community, course hosting, no-code setup, built-in affiliate system)
- Alternative: Skool ($99/mo but strong community features)
- Templates/digital downloads mirror on Gumroad for SEO discovery

---

## 3. Launch Strategy

### Phase 1: Pre-Launch (Days 1-14)
- [ ] Twitter thread series: "How I built 3 businesses with AI in 12 months" (use Blotato to schedule)
- [ ] YouTube video: "My Exact AI Agency Stack (Full Breakdown)" — screen recording of real tools
- [ ] Lead magnet: Free PDF "5 AI Automations That Sell for $2K+" (collect emails via Gumroad free product)
- [ ] DM existing TradeFlow users who've asked about automation consulting
- [ ] Build waitlist landing page on Whop

### Phase 2: Launch (Days 15-21)
- [ ] Open cart with 48-hour early bird ($147 instead of $197)
- [ ] Twitter thread: "I'm launching the course. Here's everything inside."
- [ ] YouTube launch video with walkthrough of Module 1 (free preview)
- [ ] Email blast to waitlist + TradeFlow user base
- [ ] Telegram channel announcement

### Phase 3: Evergreen (Day 22+)
- [ ] Weekly free content on Twitter/YouTube drives to lead magnet
- [ ] Lead magnet email sequence (5 emails over 7 days) → course offer
- [ ] Affiliate program on Whop (30% commission) — recruit other AI creators
- [ ] Monthly live build sessions (recorded, added to course) to keep content fresh

---

## 4. Funnel Architecture

```
FREE CONTENT (Twitter threads, YouTube videos, Blotato posts)
    |
    v
LEAD MAGNET — "5 AI Automations That Sell for $2K+" (free PDF, email capture)
    |
    v
LOW-TICKET — n8n Template Pack or Single Workflow ($27-49 on Gumroad)
    |
    v
MID-TICKET — AI Agency Blueprint Self-Paced ($197)
    |
    v
HIGH-TICKET — Pro ($497) or Done-With-You ($1,997)
```

Each tier qualifies the buyer for the next. Low-ticket buyers get upsell emails. Pro buyers get pitched DWY on coaching calls.

---

## 5. Tools & Platforms

| Purpose | Tool | Cost |
|---------|------|------|
| Course hosting + community | Whop | Free (they take a cut) |
| Digital downloads / templates | Gumroad | Free tier |
| Email list + sequences | Resend (already have) or ConvertKit | Free-$29/mo |
| Content scheduling | Blotato (already running) | Existing |
| Promotion | Twitter, YouTube, Telegram | Free |
| Affiliate management | Whop built-in | Included |
| Payment processing | Whop / Gumroad (Stripe under hood) | % per sale |

---

## 6. Revenue Targets — $3-5K/mo in 60 Days

### Conservative Model
- 15 Self-Paced sales/mo x $197 = $2,955
- 3 Pro sales/mo x $497 = $1,491
- 1 DWY sale/mo x $1,997 = $1,997
- **Total: $6,443/mo**

### Minimum Viable (hitting $3K)
- 10 Self-Paced x $197 = $1,970
- 2 Pro x $497 = $994
- Template sales (Gumroad): ~$200
- **Total: $3,164/mo**

### Required traffic to hit minimum:
- Landing page conversion: 3-5%
- Need ~300 landing page visits/mo
- Twitter (5K+ followers) + YouTube + email list should clear this easily with consistent posting via Blotato

---

## 7. Creating the Product with AI (Speed-Ship Method)

### Curriculum & Written Content
1. Use Claude to outline each module (already done above)
2. For each lesson: prompt Claude with "Write a 1500-word lesson on [topic] for someone technical who wants to ship fast. Include code examples and real scenarios."
3. Export as Notion pages or Markdown → upload to Whop

### Video Content (Pick one or combine)
- **Screen recordings** (fastest): Record real builds in OBS. No face needed. 10-20 min per lesson.
- **AI voiceover**: Write script with Claude → ElevenLabs or use your own voice. Layer over screen recordings.
- **Loom-style**: Talk through the build live. Unedited is fine for this audience (they value substance over polish).

### Templates & Deliverables
- n8n workflows: Export as JSON, package in a zip
- Claude prompts: Markdown files in a GitHub repo or Notion database
- Proposal/SOPs: Claude writes first draft, Purse edits from real experience

### Production Timeline
| Week | Deliverable |
|------|-------------|
| 1 | Module 0-2 written + recorded. Lead magnet PDF done. Whop set up. |
| 2 | Module 3-4 written + recorded. Landing page live. Waitlist open. |
| 3 | Module 5-6 + Bonus done. Email sequence written. Pre-launch content goes out. |
| 4 | Launch week. Cart open. Daily content push. |

### Key Principle
Ship Module 0-3 first, sell access, then build the rest live with early buyers watching. This creates urgency AND reduces risk of building something nobody wants.

---

## Next Actions (This Week)

1. Set up Whop creator account and configure course shell
2. Write lead magnet PDF using Claude (2 hours max)
3. Record 1 YouTube video: "My AI Agency Stack" (screen recording, 15 min)
4. Schedule 5 Twitter threads via Blotato for the next 2 weeks
5. Build Gumroad free product page for lead magnet (email capture)
