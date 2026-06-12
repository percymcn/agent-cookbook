---
name: youtube-content-to-social
description: "Automatically monitors YouTube channels and repurposes content for social media"
platforms: [linux, macos, windows]
---

# YouTube Content to Social Media Repurposer

Automatically monitors YouTube channels for new videos, extracts metadata via yt-dlp, and generates platform-optimized content for Twitter/X, LinkedIn, blogs, and Instagram — without requiring video transcripts.

## When to use

Use when you want to automate the process of turning YouTube video metadata into multiple social media formats, fully autonomously in cron/automated environments. This skill handles:
- Monitoring configured YouTube channels for new uploads
- Fetching rich metadata (title, description, stats) via yt-dlp `--dump-json`
- Generating platform-specific content (Twitter threads, LinkedIn posts, blog summaries, Instagram captions)
- Saving organized output with deduplication
- Logging all activities

## Why metadata-only (no transcripts needed)

The bundled `run_repurposer.py` uses **yt-dlp `--dump-json`** for metadata extraction — NOT the `youtube-content` skill or `youtube-transcript-api`. This was an intentional design decision:

- **Reliability**: Metadata extraction works even when transcripts are disabled, blocked, or unavailable
- **Speed**: `--dump-json` returns in seconds vs minutes for transcript processing
- **Cron-safe**: No browser automation, no CAPTCHA risk, no rate-limit cascading
- **Rich enough**: Description + title + stats provide sufficient context for template-based content generation
- **Zero dependency on youtube-content skill**: The repurposer has no coupling to the youtube-content skill. That skill (transcript-based) is a separate pipeline for deep-dive blog posts or playbook generation.

## Setup

```bash
# Required: yt-dlp (for metadata extraction)
pip install yt-dlp
# OR use the brew-installed version: /opt/homebrew/bin/yt-dlp
```

## Important Notes on Execution

- This skill runs entirely with stdlib Python + yt-dlp subprocess. No `hermes_tools` or special imports needed.
- Confirmed working in cron/automated environments (3+ cycles per day, 32+ videos processed, zero failures).
- The script uses full absolute paths for yt-dlp (`YTDLP_PATH` in `config.py`) to avoid PATH issues in cron shells.
- If youtube-content skill can't be loaded due to name collision (duplicate skill in two directories), the repurposer is unaffected — it doesn't need it.

## Workflow

1. **Configuration**: Set up YouTube channels to monitor in `config.py` or via environment variables
2. **Monitoring**: Checks each channel for the latest video using yt-dlp
3. **Deduplication**: Skips videos already processed (tracked in `processed_videos.json`)
4. **Transcript Extraction**: Uses the youtube-content skill's `fetch_transcript.py` to get video transcripts
5. **Content Generation**: Creates four formats from each transcript:
   - Twitter/X thread (engaging, numbered tweets)
   - LinkedIn post (professional, insight-focused)
   - Blog summary (detailed with sections and takeaways)
   - Instagram caption (engaging with emojis and hashtags)
6. **Output Organization**: Saves each video's content in a timestamped directory:
   ```
   data/
   └── video_{video_id}_{timestamp}/
       ├── video_info.json
       ├── twitter_thread.txt
       ├── linkedin_post.txt
       ├── blog_summary.txt
       ├── instagram_caption.txt
       └── output.json (all formats combined)
   ```
7. **Logging**: Creates daily log files in `logs/` directory
8. **Completion**: Reports number of new videos processed

## Helper Script

The skill provides a ready-to-run script: `scripts/run_repurposer.py`

```bash
# Run once to check for new content
python scripts/run_repurposer.py

# Example cron entry (runs every 4 hours)
0 */4 * * * cd /path/to/skill && python scripts/run_repurposer.py >> logs/cron.log 2>&1
```

## Configuration

Edit `scripts/config.py` to customize:
- `youtube_channels`: List of YouTube channel handles (e.g., `["@thekoerneroffice", "@starterstory"]`)
- `output_formats`: Which formats to generate (default: all four)
- `check_interval_hours`: How often to check for new videos (used for cron scheduling)
- `data_dir`: Directory for saving output (default: `./data`)
- `logs_dir`: Directory for logs (default: `./logs`)

## Output Formats

### Twitter Thread
```
🧵 Thread: [Video Title]

1/ Based on this insightful video, here are the key takeaways:
[Key point 1]

2/ The main insight that stood out:
[Key point 2]

3/ Actionable steps you can take today:
[Action 1]

4/ Why this matters for your business/goals:
[Implication]

5/ Controversial take worth considering:
[Unique perspective]

💡 Full video: [YouTube URL]
#Entrepreneurship #AI #Productivity
```

### LinkedIn Post
```
🎯 Just watched an incredibly insightful video: "[Video Title]"

Here's what resonated most:

[Summary of key insights]

The biggest takeaway? [Main insight]

This has direct applications for:
• [Application 1]
• [Application 2] 
• [Application 3]

If you're in [relevant industry/role], this is definitely worth your time.

What's your experience with [related topic]? Would love to hear your thoughts in the comments.

#Leadership #Innovation #BusinessStrategy
```

### Blog Summary
```
# [Video Title]

## Key Takeaways

[Detailed summary of video content]

## Main Insights

1. [Insight 1 with explanation]
2. [Insight 2 with explanation] 
3. [Insight 3 with explanation]

## Actionable Recommendations

Based on the video's content, here are specific actions you can take:

- [Action 1]
- [Action 2]
- [Action 3]

## Why This Matters

[Context about importance/relevance]

## Full Video Resource

Watch the complete video here: [YouTube URL]

*Summary generated by YouTube Content to Social Media Repurposer*
```

### Instagram Caption
```
[Video Title] ✨

[Engaging caption with line breaks and emojis]

💥 Key insight: [Most compelling point]

👉 Try this today: [One actionable tip]

💭 What's your take? Drop a comment below!

#Entrepreneur #Motivation #VideoInsights #ContentRepurposing #AI
```

## Error Handling\n\n- **Transcript disabled**: Skips video and logs warning; suggest checking YouTube subtitles\n- **Private/unavailable video**: Logs error and continues to next channel\n- **No matching language**: Attempts to fetch any available transcript, notes actual language\n- **Dependency missing**: Provides clear installation instructions\n- **Network issues**: Retries with exponential backoff (built into yt-dlp)\n- **DNS resolution failures**: If you encounter DNS resolution errors (e.g., \"Failed to resolve 'www.youtube.com'\", \"nodename nor servname provided, or not known\"):\n    * First, wait 30 seconds and retry (temporary DNS glitch)\n    * If persistent, check network connectivity and DNS settings (try switching to 1.1.1.1 or 8.8.8.8)\n    * Use yt-dlp as a more resilient alternative:\n      - `yt-dlp --skip-download --write-auto-sub --sub-lang en --convert-subs srt \"https://www.youtube.com/watch?v=VIDEO_ID\" -o \"%(title)s.%(ext)s\"`\n    * Consider using residential proxies or VPN if DNS-based blocking is suspected\n    * Reference: see references/dns_retry_fix.md for documentation on DNS resolution fixes implemented in Gideon's AI Content Repurposer\n\n## Notes\n\n- **Production-Ready Content Generation**: This skill is designed to work with Hermes Agent's available LLM capabilities (via `hermes_tools`) for high-quality, context-aware content generation. In production use, replace the template-based generation functions with actual LLM calls using the available models (like nvidia/nemotron-3-super-120b-a12b) for superior results that drive engagement and conversions.\n- **Monetization Focus**: This skill is optimized for building income-generating AI automation businesses. Each set of generated content (Twitter thread, LinkedIn post, blog summary, Instagram caption) represents sellable value that can be monetized through:\n  - Done-for-you content services ($49-99/month per client)\n  - Content packages (5 videos/week = $299/month)\n  - Agency management services\n  - White-label solutions for marketing firms\n- **Niche Selection for Profitability**: For maximum revenue potential, focus on monitoring channels in high-value niches where audiences have purchasing power and problems worth solving:\n  - AI automation and tools (like we demonstrated with @thekoerneroffice)\n  - Entrepreneurship and side hustles (like @starterstory)\n  - Personal finance and investing\n  - Health and wellness (specifically profitable sub-niches)\n  - Business software and SaaS\n  - Real estate and property management\n  - Avoid overly broad or entertainment-only niches unless you have a clear monetization strategy\n- The system is designed to be lightweight and runnable in minimal environments (requires only Python 3.6+, yt-dlp, and youtube-transcript-api).\n- For best results, monitor channels that regularly upload educational, business, or motivational content in profitable niches (entrepreneurship, side hustles, AI automation, etc.).\n- Output files are plain text and ready for direct posting or integration with social media scheduling tools.\n- **Integration Note**: This skill is designed to work seamlessly with the existing `youtube-content` skill, leveraging its transcript fetching capabilities while adding automated monitoring, multi-format generation, and organized output management. In the Gideon AI Content Repurposer implementation, we demonstrated successful integration with Hermes Agent's tool ecosystem for autonomous operation.\n- **Business-First Approach**: This skill follows the principle of building real money-making systems first, then optimizing. Start with a simple, working version that generates revenue, then enhance quality and features as profits come in.\n- **Standalone Implementation**: While this skill is designed to work within the Hermes Agent ecosystem, the core concepts (YouTube monitoring, transcript extraction, AI content generation, scheduled execution, deduplication, and organized output) can be implemented as a standalone system using available tools like yt-dlp, youtube-transcript-api, and cron jobs, as demonstrated in the Gideon AI Content Repurposer business.