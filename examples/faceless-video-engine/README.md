# Example: faceless-video-engine (dry-run)

Mirrors [`workflows/faceless-video-engine.md`](../../workflows/faceless-video-engine.md).
Produces the JSON production plan a real run would hand to ElevenLabs / Kie /
ffmpeg. No network, no credentials, no media generated.

## Run

```bash
python3 run.py
```

## Expected output

```
[dry-run] wrote production plan for: 'Why some people remember dreams every single night'
[dry-run] beats=5 stills=4 broll=3
[dry-run] artifact: .../examples/faceless-video-engine/out/plan.json
```

The plan lands at `out/plan.json` with five script beats, voice spec, still
prompts, b-roll prompts, assembly config, and a dry-run publishing block.

## What a real deployment replaces

| Dry-run                                        | Production                                    |
| ---------------------------------------------- | --------------------------------------------- |
| Hard-coded beats / prompts                     | Claude script + visual-prompt generation      |
| `voice.engine = "elevenlabs"` (spec only)      | ElevenLabs TTS call returning .mp3            |
| `stills` / `broll` (prompt only)               | Kie nano-banana + Veo3 generations            |
| `assembly.tool = "ffmpeg"` (spec only)         | Actual ffmpeg / remotion stitch + whisper SRT |
| `publishing.dry_run = true`                    | Blotato scheduled post across YT / TikTok / IG |
