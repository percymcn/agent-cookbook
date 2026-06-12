---
name: tradeflow-pipeline
description: Automates discovery, extraction, validation, and storage of trading ideas for TradeFlow.
category: trading
---
# TradeFlow Discovery Pipeline

This skill automates the end-to-end process of discovering trading ideas from YouTube/Reddit, extracting content (with metadata fallback for blocked transcripts), validating via deep research, and saving structured playbooks and JSON data for the TradeFlow system.

## Steps

1. **Discover**: Run `autonomous-business-system` to fetch recent trading‑idea videos/posts from configured sources (YouTube channels, Reddit communities).
2. **Extract**: For each URL, attempt transcript extraction via `youtube-content`. If blocked or unavailable, automatically fall back to metadata extraction (title, description, upload date, channel) using `yt-dlp` – this approach has been validated to produce useful business opportunity analyses.
3. **Validate**: Feed the extracted text (transcript or metadata) into `deep-research-pro` to enrich with market context, competition, risk factors, and opportunity scoring.
4. **Save**: Store the validated result as:
   - JSON: `~/playbooks/tradeflow/YYYY-MM-DD/<uuid>.json`
   - Markdown playbook: `~/playbooks/tradeflow/YYYY-MM-DD/<uuid>.md`
5. **Notify**: Optionally send a Telegram summary via `hermes_comms` (requires Felix).

## Key Learnings from Session\n\n- **Metadata Fallback Effectiveness**: When YouTube transcript APIs are blocked (common in automated environments), extracting metadata (title, description) via `yt-dlp` and analyzing it for business signals provides sufficient context for meaningful opportunity scoring (validated at 15/25+ points across 5+ test videos).\n- **Reliable Discovery in Automated Environments**: Use `yt-dlp --flat-playlist` for robust YouTube video listing in cron jobs/automated contexts (avoids browser automation issues).\n- **Extraction Priority**: Try `youtube-content` first for transcripts, but expect fallback to metadata extraction in ~30% of cases due to blocking/Javascript requirements.\n- **Pipeline Validation**: End-to-end processing time of ~3-4 minutes per video is acceptable for 6-hourly scheduled runs in automated environments.\n- **Manual Execution Workflow**: When API validation fails (e.g., NVIDIA API 404 errors), discovery and extraction steps can still complete successfully. Save extracted content (transcripts or metadata) manually and retry validation once API issues are resolved.\n- **Manual Execution Workflow**: When API validation fails (e.g., NVIDIA API 404 errors), discovery and extraction steps can still complete successfully. Save extracted content (transcripts or metadata) manually and retry validation once API issues are resolved.\n- **Manual Execution Workflow**: When API validation fails (e.g., NVIDIA API 404 errors), discovery and extraction steps can still complete successfully. Save extracted content (transcripts or metadata) manually and retry validation once API issues are resolved.

## References
- See `references/metadata_fallback_validation_may_2026.md` for detailed validation results and recommendations from the May 2026 session.
- See `references/api_failure_troubleshooting_may_2026.md` for troubleshooting NVIDIA API 404 errors encountered during validation.

## Usage

### As a standalone command (for testing)

```bash
hermes run tradeflow-pipeline --query "crypto trading strategy" --limit 5
```

### As a cron job (recommended)

```bash
hermes cron create \
  --name "tradeflow-discovery-pipeline" \
  --schedule "every 6h" \
  --prompt "Run the TradeFlow discovery pipeline for crypto trading ideas" \
  --skills tradeflow-pipeline autonomous-business-system youtube-content deep-research-pro \
  --deliver telegram \
  --model provider=nvidia model=nemotron-3-super-120b-a12b
```

## Configuration

- `--query`: Search term for the discovery step (default: `"trading strategy"`)
- `--limit`: Number of URLs to process per run (default: `10`)
- Output directory: `~/playbooks/tradeflow/YYYY-MM-DD/` (created automatically)
- Each run creates a new sub‑folder for the date; files inside are UUID‑named to avoid collisions.

## Example Output

```
~/playbooks/tradeflow/2026-05-24/
├── 3f1a2b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c.json
├── 3f1a2b4c-5d6e-7f8a-9b0c-1d2e3f4a5b6c.md
└── ...
```

## Notes

- The skill assumes you have the `autonomous-business-system`, `youtube-content`, and `deep-research-pro` skills available (they are part of your current toolkit).
- If transcript extraction fails, the metadata‑fallback strategy (title, description, upload date, channel) is used automatically – this has been validated to produce useful business‑opportunity analyses.
- For best results, pair this pipeline with the `tradeflow-paper` worker (already running) which will back‑test any new strategies that appear in the generated playbooks.
- **API Failure Handling**: If the NVIDIA API returns errors (like 404) during the validation step, the pipeline can still complete discovery and extraction. Save the extracted content manually and retry validation once API issues are resolved. See `references/api_failure_troubleshooting_may_2026.md` for detailed troubleshooting.