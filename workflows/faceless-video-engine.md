# Faceless Video Engine

A daily pipeline for producing YouTube Shorts, TikToks, and IG Reels without
showing your face. Used in production for the BuzzMind and Hype Loop channels.

## Stages

1. **Ideation** — pull current-day trends from a vertical-specific feed (Reddit, X, niche newsletters). One topic per channel per day.
2. **Script** — Claude writes a 60-90s script with a hook, 3 beats, and a CTA.
3. **Voice** — ElevenLabs TTS, single voice per channel for consistency.
4. **Stills + B-roll** — Kie nano-banana for images; Veo3 for moving b-roll.
5. **Assembly** — ffmpeg or remotion stitches voice + visuals + captions.
6. **Captioning** — auto-srt with whisper, burned in with style tokens.
7. **Publish** — Blotato schedules across YouTube/TikTok/IG/FB.

## Skills used

- `creative/*` — script + visual prompt generation.
- `media/*` — TTS, image, video tooling.
- `social-media/*` — platform publishing wrappers.

## Cost knobs

- Veo3 b-roll is the largest line item — cap at 3 shots per video.
- Nano-banana stills are cheap; over-generate and select.
- ElevenLabs: cache voice samples by hash so re-renders cost nothing.

## Failure modes seen in prod

- Kie polling-shape change broke the pipeline silently — always check the
  poll response schema in CI.
- Captions drift if the TTS audio gets re-rendered without re-running whisper.
- TikTok rejects clips under 35s — pad with a 5s outro.

## Quality bar (45% retention gate for Shorts)

- Hook lands in first 1.5 seconds.
- Face-equivalent motion (mouth-on-character, kinetic typography) every 2-3s.
- High contrast between consecutive frames.
