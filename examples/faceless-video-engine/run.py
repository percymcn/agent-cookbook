#!/usr/bin/env python3
"""Dry-run of the faceless-video-engine workflow.

Produces a JSON production plan for one Short: script beats, voice spec,
image prompts, b-roll prompts, assembly plan. No real API calls — the
"model" outputs are deterministic fixtures so the script is reproducible.

In production this script would be replaced by orchestrator calls to:
  - Claude (script + visual prompts)
  - ElevenLabs (TTS)
  - Kie nano-banana (stills) / Veo3 (b-roll)
  - ffmpeg or remotion (assembly)
  - Blotato (publishing)
"""
from __future__ import annotations

import argparse
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOPIC = "Why some people remember dreams every single night"


def build_plan(topic: str) -> dict:
    beats = [
        {"t": "0-2s",  "kind": "hook",  "line": f"{topic.split(' ')[0]} 9 out of 10 people forget — here's the 1 thing they do differently."},
        {"t": "2-15s", "kind": "beat1", "line": "Your brain replays the day in REM. If you wake mid-cycle, the script is still loaded."},
        {"t": "15-30s","kind": "beat2", "line": "Sleep researchers found 90-minute cycles. Wake on the boundary, not in the middle."},
        {"t": "30-50s","kind": "beat3", "line": "Three habits do most of the work: stable bedtime, no alcohol, journal within 60s of waking."},
        {"t": "50-58s","kind": "cta",   "line": "Try the journal trick tonight. Comment what you dreamed."},
    ]
    return {
        "topic": topic,
        "channel": "BuzzMind",
        "target_length_s": 58,
        "voice": {"engine": "elevenlabs", "voice_id": "Will", "stability": 0.4},
        "beats": beats,
        "stills": [
            {"beat": "hook",  "prompt": "soft-lit bedroom at dawn, blue palette, dreamy bokeh"},
            {"beat": "beat1", "prompt": "diagram of REM cycle, neon outline, dark background"},
            {"beat": "beat2", "prompt": "alarm clock, 90-min sleep cycle infographic"},
            {"beat": "beat3", "prompt": "journal + pen on nightstand, morning light"},
        ],
        "broll": [
            {"beat": "beat1", "prompt": "slow zoom into a sleeping eye, REM flutter"},
            {"beat": "beat2", "prompt": "clock face speed-ramp through one night"},
            {"beat": "beat3", "prompt": "hand writing in journal, top-down"},
        ],
        "assembly": {
            "tool": "ffmpeg",
            "captions": "whisper-burned",
            "outro_pad_s": 5,
            "aspect": "9:16",
        },
        "publishing": {
            "platforms": ["youtube_shorts", "tiktok", "instagram_reels"],
            "scheduled_for": f"{date.today().isoformat()}T17:00:00-05:00",
            "dry_run": True,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", default=True,
                    help="Always on for this example.")
    ap.add_argument("--topic", default=TOPIC)
    ap.add_argument("--out", default=str(HERE / "out" / "plan.json"))
    args = ap.parse_args()

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    plan = build_plan(args.topic)
    out.write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"[dry-run] wrote production plan for: {plan['topic']!r}")
    print(f"[dry-run] beats={len(plan['beats'])} stills={len(plan['stills'])} broll={len(plan['broll'])}")
    print(f"[dry-run] artifact: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
