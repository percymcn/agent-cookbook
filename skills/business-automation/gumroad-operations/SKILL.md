---
name: gumroad-operations
description: "Manage Purse's Gumroad store through the local Gumroad CLI and MCP server: products, sales, offer codes, subscribers, licenses, webhooks, reports, and guarded mutations."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  created_by: agent
  project: /Users/pharma6/hermes-gumroad-mcp
---

# Gumroad Operations

Use this skill when Purse asks to manage Gumroad products, sales, subscriptions/subscribers, offer codes, licenses, webhooks, analytics, daily reports, or agent/MCP integration.

## Project paths

- Project root: `/Users/pharma6/hermes-gumroad-mcp`
- CLI wrapper: `/Users/pharma6/bin/gumroad`
- MCP wrapper: `/Users/pharma6/hermes-gumroad-mcp/scripts/run-mcp.sh`
- Webhook receiver: `/Users/pharma6/hermes-gumroad-mcp/scripts/run-webhook.sh`
- Daily report: `/Users/pharma6/hermes-gumroad-mcp/scripts/daily-report.sh`
- Runbook: `/Users/pharma6/hermes-gumroad-mcp/README.md`
- Secrets: `/Users/pharma6/hermes-gumroad-mcp/.env` — never read or expose values.

## Installed integrations

- Hermes MCP server: `gumroad`; test with `hermes mcp test gumroad`.
- Claude Code local MCP server: `gumroad`; test with `claude mcp list` from project root.
- Cursor project config: `/Users/pharma6/hermes-gumroad-mcp/.cursor/mcp.json`.
- Daily Hermes cron exists: job ID `d2a0d729d1e1`. It can be resumed/running once `/Users/pharma6/hermes-gumroad-mcp/.env` has a real `GUMROAD_ACCESS_TOKEN`.

Restart Hermes/new session required for MCP tools to appear in active chats.

## CLI commands

```bash
export PATH="/opt/homebrew/bin:/Users/pharma6/bin:$PATH"
gumroad doctor --json
gumroad user get --json
gumroad products list --json
# IMPORTANT: products are paginated. If output has next_page_key, keep fetching:
gumroad request GET /products --query '{"page_key":"NEXT_PAGE_KEY"}' --json
gumroad products get PRODUCT_ID --json
gumroad sales list --limit 5 --json
gumroad sales summary --after YYYY-MM-DD --before YYYY-MM-DD --json
gumroad offer-codes list PRODUCT_ID --json
gumroad subscribers list --product-id PRODUCT_ID --json
gumroad webhooks list --json
gumroad webhooks list --resource-name sale --json
gumroad licenses verify --product-permalink PERMALINK --license-key LICENSE_KEY --json
```

Mutation commands require both:

1. `.env` has `GUMROAD_ALLOW_MUTATIONS=true`
2. command has exact confirmation, e.g. `--confirm offer-codes.create`

Examples:

```bash
gumroad offer-codes create PRODUCT_ID --name LAUNCH50 --amount-off 50 --offer-type percent --confirm offer-codes.create --json
gumroad products disable PRODUCT_ID --confirm products.disable --json
gumroad sales refund SALE_ID --amount-cents 500 --confirm sales.refund --json
```

Refunds and product changes are money/business-impacting. Confirm with Purse in-session before executing unless he explicitly gave the exact action and confirmation.

## MCP tools

The MCP server exposes 24 tools, prefixed `gumroad_`, including:

- user/products/sales: `gumroad_get_user`, `gumroad_list_products`, `gumroad_get_product`, `gumroad_list_sales`, `gumroad_sales_summary`, `gumroad_get_sale`
- offer codes: `gumroad_list_offer_codes`, `gumroad_create_offer_code`, `gumroad_update_offer_code`, `gumroad_delete_offer_code`
- subscribers/licenses: `gumroad_list_subscribers`, `gumroad_get_subscriber`, `gumroad_verify_license`, `gumroad_license_action`
- webhooks: `gumroad_list_webhooks`, `gumroad_create_webhook`, `gumroad_delete_webhook`
- future-proof: `gumroad_raw_request`

Use read-only tools first. Mutating tools have internal env/confirm gates.

## Token setup

If live calls fail with missing token, ask Purse for the Gumroad access token. Store it only in `/Users/pharma6/hermes-gumroad-mcp/.env` as `GUMROAD_ACCESS_TOKEN=...`; never hardcode it into configs or messages.

## Verification after token

```bash
gumroad doctor --json
gumroad user get --json
gumroad products list --json
gumroad sales list --limit 5 --json
gumroad sales summary --limit 50 --json
gumroad webhooks list --json
hermes mcp test gumroad
```

Then test Claude Code:

```bash
cd /Users/pharma6/hermes-gumroad-mcp
claude -p "Use gumroad MCP. Call gumroad_doctor, gumroad_list_products, gumroad_list_sales limit 5, and gumroad_sales_summary. Summarize results. Do not mutate anything."
```

## Webhooks

Local receiver is verified:

```bash
./scripts/run-webhook.sh
curl http://127.0.0.1:8787/health
```

Logs: `/Users/pharma6/hermes-gumroad-mcp/logs/webhooks.jsonl`

Gumroad requires `resource_name` when querying resource subscriptions. The wrapper queries all supported names by default (`sale`, `refund`, `dispute`, `cancellation`, `subscription_updated`) and supports `gumroad webhooks list --resource-name sale --json` for a single resource.

Do not create public Gumroad webhook subscriptions until there is an HTTPS URL/tunnel/domain and `GUMROAD_WEBHOOK_SECRET` is set.

## Storefront/homepage redesign

When Purse says the Gumroad homepage/profile is blank, newsletter-only, or needs redesign, use `references/storefront-redesign-workflow.md` before acting. Key points: inspect the public page with browser rendering, not only curl; compare public output against `gumroad user get --json` and paginated product listings; profile/homepage edits are dashboard/browser work because `PUT/PATCH/POST /user` returned 404; never publish drafts or change prices during a redesign unless explicitly instructed.

**Gumroad cannot host custom-designed landing pages** — no custom CSS, hero images, font choices, or layout controls. The storefront is locked to Gumroad's template (headline, bio, featured products, subscribe form). If Purse wants a custom design:

1. Build a self-contained HTML page locally
2. **Show Purse a full-page screenshot BEFORE deploying** — use agent-browser to render the HTML file locally and screenshot it
3. Only deploy once approved
4. Deploy externally (Vercel, Netlify, GitHub Pages) — not on Gumroad
5. Link "Buy Now" CTAs to individual Gumroad product checkout URLs
6. Optionally point a custom domain (e.g. store.fluxio.ai) at the hosted page

**Custom landing page structure:** Self-contained HTML with CDN-loaded CSS (Tailwind, Google Fonts), no build step. Product CTAs link directly to gumroad.com/l/PERMALINK pages.

### Custom landing page — deploy workflow

Once Purse approves the screenshot:

1. **Verify all Gumroad links** in the HTML resolve to real product pages
2. **Copy the HTML to `index.html`** (required by most static hosts): `cp "page.html" index.html`
3. **Deploy on Vercel:**
   ```bash
   # From the directory with index.html:
   npx vercel --prod
   ```
   - If `npx vercel` asks to set up a new project, say yes
   - The project name auto-creates (e.g. `fluxio-ai-storefront`)
4. **Toggle off Vercel Deployment Protection** (SSO) — this blocks public custom domains:
   - Project Dashboard → Settings → Deployment Protection → toggle OFF
   - Without this, visitors see a 401 login wall
5. **Add a custom domain** if Purse owns one (e.g. `store.fluxio.ai`):
   - Run: `npx vercel domains add DOMAIN`
   - At the DNS provider (GoDaddy, Cloudflare, etc.), add a CNAME record:
     - Name: `store`
     - Target: `cname.vercel-dns.com`
   - Wait up to 30 min for DNS propagation
6. **Verify live URL** loads with all Gumroad CTAs clickable
7. **Important:** Do NOT change Gumroad product prices, publish drafts, or refund during a landing page deploy — this is strictly a front-end change

**Claude Code alternative:** If `npx vercel` is slow or fails, delegate to Claude Code:
```python
from call_claude_code import call_claude_code
call_claude_code("Deploy /path/to/index.html to Vercel: cp to temp dir, run `npx vercel --prod`, return the live URL. Do not change anything else.", timeout=600)
```

## Product readiness / draft publishing

When Purse asks to audit drafts, publish more products, verify that products deliver value, or make the store more purchase-ready, use `references/product-readiness-verification.md`. Key points: paginate product listings, treat non-empty `file_info`/`files` as the sellable-deliverable gate, verify public pages with rendered snapshots, and keep products offline if they only have covers/copy but no attached fulfillment file.

## Reporting

Manual report:

```bash
./scripts/daily-report.sh
```

Reports write to `/Users/pharma6/hermes-gumroad-mcp/reports/`.

After publishing or storefront cleanup, include a compact sales sanity check from the API (`gumroad sales summary --json` and/or `gumroad sales list --limit 5 --json`) so Purse gets both storefront readiness and real revenue status. Report it as “sales verified via API,” not as a guessed outcome.

Cron `d2a0d729d1e1` can be resumed after token is installed.

## Guardrails

- Never expose Gumroad tokens or webhook secrets.
- Do not mutate products, refunds, offer codes, webhooks, or licenses without explicit business approval.
- Use read-only commands for analysis/reporting by default.
- If an official endpoint is missing, use `gumroad_raw_request`/`gumroad request`, but keep the same mutation guardrails.
- In active Hermes chats, MCP tools may not inherit `.env` mutation flags even when `gumroad doctor --json` from the project shows `mutations_enabled: true`. If an explicitly approved raw mutation is blocked by MCP env, run the CLI from `/Users/pharma6/hermes-gumroad-mcp` instead, e.g. `gumroad request PUT /products/PRODUCT_ID --body '{"name":"..."}' --form --confirm request.PUT --json`.
