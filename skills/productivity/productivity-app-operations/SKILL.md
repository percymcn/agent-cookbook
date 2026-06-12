---
name: productivity-app-operations
description: "Productivity app operations umbrella: Airtable, Google Workspace, Maps/geocoding/routes, Notion, Teams meeting pipeline, and document-adjacent app automation. Use for CRUD/search/export operations across productivity SaaS and office workflows."
---

# Productivity App Operations

Use this umbrella for operating productivity tools and lightweight SaaS workflows. Verify credentials/tool availability before claiming access.

## Airtable

Use Airtable REST API for bases/tables/records: list, filter, create, update, delete, and upsert. Prefer explicit base ID, table name/ID, field names, and `filterByFormula` for targeted reads. For mutations, confirm scope and show affected record IDs.

## Google Workspace

Use `gws`/Google API bridge workflows for Gmail, Calendar, Drive, Docs, and Sheets. Before destructive changes, confirm target account and object IDs. For Gmail search, use Gmail's native query syntax; for Sheets, prefer batch reads/writes over cell-by-cell loops.

## Maps, geocoding, routes, and time zones

Use OSM/Nominatim/OSRM-style tools for geocoding, POI lookup, routing, distances, and timezone lookups. Always include assumptions: travel mode, origin/destination normalization, and timestamp when time-sensitive.

## Notion

Use Notion API/CLI for pages, databases, blocks, search, and markdown conversion. Remember that Notion block structures are nested; inspect schemas before writing database records and preserve property types.

## Teams meeting pipeline

Use the Teams meeting pipeline for meeting summary jobs, Microsoft Graph subscriptions, replaying jobs, and pipeline status checks. Prefer pipeline commands over ad-hoc Graph calls when the local pipeline already owns state.

## Documents and presentations

For documents, OCR, PDFs, and PowerPoint, choose the dedicated document skill when the task is file-format-heavy. Use this umbrella only for routing and app-level operations.

## Mutation discipline

- Read/inspect before write.
- Confirm destructive or external-facing actions.
- Report IDs/URLs of changed objects.
- Verify by re-reading after mutation when possible.
