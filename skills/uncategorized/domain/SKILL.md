---
name: domain
description: "Use when performing passive domain reconnaissance — subdomain discovery via crt.sh, SSL certificate inspection, WHOIS lookups, DNS record queries, domain availability checks, and bulk multi-domain analysis. Python stdlib only, no API keys required."
---

# Domain Intelligence

Passive domain reconnaissance using only Python stdlib and public data sources.

## When to use

- Finding subdomains for a target domain.
- Inspecting SSL/TLS certificates (expiry, SANs, cipher, TLS version).
- Running WHOIS lookups across 100+ TLDs via direct TCP.
- Querying DNS records (A, AAAA, MX, NS, TXT, CNAME).
- Checking domain availability (DNS + WHOIS + SSL signals).
- Bulk analyzing up to 20 domains in parallel.

## Data sources

- **crt.sh** — Certificate Transparency logs for subdomain discovery.
- **WHOIS servers** — Direct TCP to authoritative TLD servers.
- **Google DNS-over-HTTPS** — MX/NS/TXT/CNAME resolution.
- **System DNS** — A/AAAA records.

## Notes

- Zero dependencies, zero API keys — works out of the box.
- All techniques are passive; no active scanning or intrusive probes.
- Rate-limit awareness: crt.sh and WHOIS servers may throttle under heavy use.
