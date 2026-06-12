---
name: media-asset-tools
description: "Media asset tools umbrella: GIF search/download, AI song/music generation prompts, HeartMuLa generation, audio feature/spectrogram analysis, and lightweight media utilities. Use for small media assets and audio/music workflows that do not require the full video-production or YouTube pipelines."
---

# Media Asset Tools

Use this umbrella for small media and audio/music tasks. Keep full video production and YouTube monitoring pipelines separate when their dedicated project-specific package is needed.

## GIF search

Use Tenor-style search/download flows when the user wants a reaction GIF or animated media asset. Search first, pick a relevant result, download if needed, and deliver as native media when the target platform supports it.

Typical pattern:

```bash
curl -s "https://tenor.googleapis.com/v2/search?q=<query>&key=$TENOR_API_KEY&limit=10" | jq
```

## Songwriting and AI music prompts

For songs, separate craft from generation:

1. Clarify genre, mood, tempo, language, singer perspective, and structure.
2. Draft lyrics with sections (`[Verse]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`).
3. Provide compact model tags/style prompts for Suno-like generators.
4. Avoid overstuffed tags; prioritize the musical identity and vocal direction.

## HeartMuLa generation

Use HeartMuLa when the task is direct song/audio generation from lyrics and tags. Verify provider credentials/tool availability before promising generated output. Save returned media and deliver with `MEDIA:/path` when local.

## Audio feature analysis via SongSee

Use SongSee-style spectrogram/feature tools for mel, chroma, MFCC, or audio visualization tasks. Prefer concrete outputs: image files, feature summaries, or CSV/JSON artifacts.

## AudioCraft

Use AudioCraft/MusicGen/AudioGen patterns when generating music or sound effects locally from text prompts. Check model availability and hardware constraints before running heavy inference.

## Reporting

For media work, report:

- Source or generation tool used.
- Output file path/URL.
- Any licensing or attribution concerns.
- Whether output was verified by opening/analyzing/listing the file.
