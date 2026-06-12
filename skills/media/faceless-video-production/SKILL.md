---
name: faceless-video-production
description: "Produce faceless/narrated videos end-to-end: script, voiceover, stills, local animation, captions, vertical shorts, verification, and Telegram/media delivery."
---

# Faceless Video Production

Use this skill when the user asks to resume, build, finish, caption, cut down, or deliver faceless/narrated videos for YouTube, Shorts, TikTok, Reels, psychology channels, listicles, explainers, or similar content.

## Core workflow

1. **Resume state first**
   - Read the project/resume notes and locate existing assets, scripts, task IDs, and partial outputs.
   - Avoid regenerating assets that already exist unless they are corrupt, missing, or explicitly rejected.

2. **Check external-generation prerequisites without stalling**
   - If the workflow references paid/external generators (Kie, Higgsfield, FAL, ElevenLabs, etc.), check whether credentials/task status are actually available.
   - If external credentials/credits are unavailable, do not stop unless the user specifically required that provider. Switch to a local or available fallback and clearly label the fallback.

3. **Generate or recover the missing assets**
   - Voiceover: use existing project VO first. If none exists, try local Supertonic TTS before paid/API TTS when the goal is cost-sensitive drafting or batch production:
     `cd /Users/pharma6/ai-team && source .venvs/supertonic/bin/activate && supertonic tts '<script>' -o vo.wav --voice M1 --steps 5 --lang en`.
     Use paid/premium TTS only when quality materially affects public launch/revenue or the user requests that provider.
   - Stills: use configured image generation if available; otherwise create local cinematic stills using PIL/ffmpeg-friendly 16:9 art, gradients, silhouettes, scene labels, and consistent palette.
   - If the user rejects the visuals as “programmatic,” “not saying anything,” generic, or specifically asks for Kie/Nano Banana/Higgsfield-quality imagery, stop treating local/PIL stills as acceptable final art. Generate real AI visual assets through the preferred provider or a working delegated MCP/Claude Code provider path, then rebuild the video and label the provider path honestly.
   - When Kie/Nano Banana credits are available, use Kie as the preferred rebuild path for Purse-facing proof videos: generate 5-8 vertical Nano Banana beats, generate ElevenLabs voice through Kie when quality matters, assemble locally with motion/captions, then contact-sheet QA before delivery. See `references/kie-ai-production-rebuild.md`.
   - Keep assets in the project folder with stable names (`script_full.txt`, `vo_full.mp3`, `s02.jpg`, etc.).
   - For Purse-facing faceless/documentary videos, bias toward engagement: use many more short visual beats instead of a few long static scenes. As a default for 8–12 minute documentaries, target ~45–80 visuals/segments, ~8–14 seconds per visual, varied props/maps/symbolic overlays, and motion on every still. If the first cut feels static or scenes do not communicate the story, rebuild an enhanced cut with clearer visual concepts rather than merely explaining the limitation.

4. **Assemble the long video**
   - Use ffmpeg to animate stills with slow zoom/pan (Ken Burns), concat segments, mux the voiceover, and fade audio in/out.
   - Add documentary-style movement where possible: alternating pan directions, subtle zooms, film grain/scratches, map overlays, light pulses, and faster cuts for hook sections.
   - Output a normal landscape master first.

5. **Add captions**
   - Extract audio, transcribe with Whisper/faster-whisper when available, generate SRT, then burn captions using a libass-capable ffmpeg.
   - If the default ffmpeg lacks the `subtitles` filter, search for another installed ffmpeg (for example `~/bin/ffmpeg`) before giving up.

6. **Create the short**
   - Trim a strong 30–45s hook segment.
   - Reframe to 9:16 with blurred background + centered foreground.
   - Burn larger centered captions suitable for Shorts/Reels/TikTok.

7. **Verify before reporting**
   - Run `ffprobe` on final outputs.
   - Extract a contact sheet and visually QA it before sending Purse-facing drafts; technical validity alone is not enough.
   - If this model cannot inspect frames directly, delegate the contact sheet to Claude Code/Felix for visual QA before delivery.
   - Report: path, duration, file size, resolution, whether audio exists, and whether visual QA passed.
   - Deliver media files directly in Telegram using `MEDIA:/absolute/path.mp4` when requested.

8. **Score hooks and stage distribution safely**
   - If using Higgsfield `virality_predictor`, score <=16s hook cuts rather than full 40s Shorts when the provider enforces a short input cap.
   - For weak hooks, try no-spend local improvements first: 0–3s pattern-interrupt overlays, animated stingers, and 15s re-score cuts.
   - Build an approval matrix before publishing: exact files, accounts, visibility, captions, hashtags, schedule, exclusions, and publish gate.
   - Use read-only/list checks for distribution tools first. Do not create public posts, schedules, paid generation, or money-moving actions without direct in-session approval.

## Pharma6 local factory

Purse already has a faceless-video factory on this Mac at `/Users/pharma6/ai-team`.

Read these before producing or distributing BuzzMind/Hype Loop content:

- `/Users/pharma6/ai-team/HERMES_HANDOFF.md`
- `/Users/pharma6/ai-team/POSTING_PACKAGE.md`
- `/Users/pharma6/ai-team/research_validated_topics.md`
- `/Users/pharma6/.claude/scheduled-tasks/daily-video-production/SKILL.md`

Confirmed stack:

- Hermes native MCP has `blotato` working directly from `/Users/pharma6/.hermes/config.yaml` using `${BLOOTATO_API_KEY}` from `/Users/pharma6/.hermes/.env`; use Hermes-native Blotato tools for account listing, upload URLs, staging, schedules, and post status instead of routing through Claude Code quota.
- Hermes native MCP has `kie` working through the local proxy `http://127.0.0.1:3010/${KIE_PROXY_URL_SECRET}/mcp`; the Kie launchd service should keep upstream `127.0.0.1:3000` and proxy `127.0.0.1:3010` alive.
- Kie native tools expected: `elevenlabs_tts`, `nano_banana_image`, `veo3_generate_video`, `get_task_status`, `wait_for_task`, and `list_tasks`.
- Higgsfield is configured for Hermes OAuth but may need one browser approval in Hermes; Claude Code's managed OAuth token is separate and should not be assumed portable.
- Kie MCP/env exists at `/Users/pharma6/.config/kie-mcp/.env`; helper exists at `/Users/pharma6/ai-team/kie_fetch.sh`.
- Existing scripts include `assemble_video.sh`, `add_captions.sh`, `make_short.sh`, `factory_assemble_one.py`, and `hook_loop/adapters/higgsfield.py`.
- Existing outputs include long MP4s, `_CAPTIONED.mp4`, `_SHORT.mp4`, thumbnails, hook cuts, and virality test clips under `/Users/pharma6/ai-team`.
- Content-engine brain lives at `/Users/pharma6/ai-team/content_engine/`; read `CONTENT_ENGINE_SOURCE_OF_TRUTH.md`, `state/*.json`, and `backlog/topics_ranked.md` before taking over BuzzMind/Hype Loop scheduling or production state.
- For paid Skool/content-creation courses, do not stop at written material: build a module/video inventory, transcribe/analyze lesson videos, and extract channel-specific SOPs. See `references/skool-course-video-ingestion.md`.
- Posting guardrail for BuzzMind/Hype Loop: social scheduling/captioning/hashtagging/retiming/media swaps are autonomous, but always inspect Blotato schedules first and never blind-create duplicates. YouTube long-forms stay private with notify off until Purse directly says to make them public. Money/Stripe/billing, DNS, tunnels, OAuth, deployments, service create/remove, or irreversible infra changes require direct in-session operator confirmation every time. Always exclude Onego and TradeFlow unless explicitly selected, and obey the 12–24h cadence rule.

Recommended first action for this factory: verify existing files with `ffprobe`, run/read virality results, list Blotato accounts, build the posting matrix, upload/stage, then request the single publish gate.

## Local fallback pattern

When image generation is unavailable but the user wants the video completed now:

- Use PIL to generate a coherent sequence of 1920×1080 cinematic stills.
- Use gradients, vignettes, film grain, faceless silhouettes, subtle symbolic props, and short scene labels.
- Use ffmpeg `zoompan` to create slow movement from stills.
- This is acceptable as a completion fallback, but state that premium external-generated assets were not used.

## SOP-to-production test runs

When Purse asks to start production from completed SOP/course resources, do not ask for a topic or stop with a plan. Pick 1-2 reviewable test cuts from the validated backlog/SOPs, render actual vertical MP4s locally, verify them with `ffprobe`, extract a contact sheet, and visually QA the frames before sending to Telegram as `MEDIA:/absolute/path.mp4`. Use local PIL/ffmpeg/TTS drafts for speed if premium Kie/Nano Banana/Higgsfield visuals would block the first proof, but do not send placeholder/wireframe/programmatic-looking visuals as if they are production quality. If local fallback is used, label it honestly and hold it back until it passes contact-sheet QA. After the files exist, inspect Blotato/Kie readiness and keep the explicit publish gate. See `references/sop-to-production-test-run.md` and `references/pre-delivery-visual-qa-gate.md`.

## Pitfalls

- For paid-course/Skool ingestion, do not only process the flashiest or highest-ROI later videos. Build a canonical course-order map and use it as the primary full-ingestion path so foundations and dependencies are not skipped.
- Do not stop at “credentials missing” if a local fallback can produce a useful draft/master.
- Do not claim external paid assets were regenerated if they were replaced with local fallbacks.
- Do not publish publicly or spend paid generation credits at scale unless the user has approved it.
- When staging via Blotato, distinguish platform submission status from public visibility: YouTube private uploads can return `status: published`; TikTok `SELF_ONLY`/draft submissions can also return `published` and a profile URL. Record submitted privacy fields and state the distinction clearly.
- Do not auto-run Instagram/Reels for a non-public staging request unless a draft/private field is available and verified; hold Instagram rows in the posting matrix until explicit public-post approval.
- Do not submit full-length Shorts to hook-only virality tools when they enforce a short input cap; trim a private 15s hook cut and score that.
- Do not treat a provider-side scoring error as a permanent limitation. Retry with a fresh upload, capture exact request/error IDs, then continue with the best verified local output if blocked.
- Do not finish with a plan only. Produce real media files and verify them.
- Do not send placeholder/wireframe/geometric/local-programmatic visuals as a Purse-facing production draft just because the video rendered. Extract/review a contact sheet first and rebuild if the frames look like debug art.
- Do not trust cloud AI renders blindly. Blotato/Kie/FAL/etc. outputs can be technically valid but still contain garbled AI text, fake logos, watermarks, recognizable IP, broken captions, or off-tone frames; reject and rebuild before delivery.
- Do not assume Kie temporary asset URLs are broken if Python `urllib` gets HTTP 403. Retry downloads with `curl -L --retry 3 --max-time 120 -A 'Mozilla/5.0'` and verify file size before rerendering.
- Do not leave debug footers, internal labels, or “fallback/reviewed” metadata in delivered frames.
- Do not dump long ffmpeg logs in the final answer; summarize verified outputs.

## References

- `templates/course-lesson-sop.json` — canonical SOP JSON template for course video lessons. Copy and fill when generating SOPs from transcripts.
- `references/skool-course-video-ingestion.md` — paid Skool/course workflow: check existing authenticated Chrome session before declaring bad credentials blocked, inventory modules first, create `transcript_queue.json`, then transcribe Skool-native videos into SOP/playbook outputs.
- `references/course-order-content-engine-ingestion.md` — canonical course-order ingestion pattern: maintain `course_sequence.json`, `MASTER_COURSE_SEQUENCE.md`, and `course_order_transcript_queue.json`; use priority queues only for fast wins, not the main production-engine build.
- `references/skool-notebooklm-ingestion.md` — proven Skool → NotebookLM ingestion workflow: authenticated browser inventory, NotebookLM copied-text UI fallback, Mux audio extraction with headers, Whisper transcripts, SOP JSONs, and token-redaction pitfalls.
- `references/course-ingestion-completion-verification.md` — finalization checklist for course ingestion: canonical course-order queues, transcript-to-SOP parity, SOP schema normalization, NotebookLM UI verification, and concise evidence-based reporting.
- `references/local-fallback-video1.md`
- `references/local-fallback-video1.md` — concrete session pattern for finishing a stalled faceless psychology video using local PIL stills, TTS, ffmpeg assembly, captions, and Shorts export.
- `references/engagement-rebuild-pattern.md` — how to rebuild a too-static long faceless/documentary cut with many more visual beats, richer motion, QA sheets, and verified outputs.
- `references/virality-and-distribution-gates.md` — hook-scoring workaround, no-spend hook iteration pattern, Blotato/distribution approval matrix, and publish-gate checklist.
- `references/hermes-native-media-mcps.md` — how to port/use Blotato, Kie, and Higgsfield as Hermes-native MCPs, including local Kie proxy launchd persistence and gateway reload pitfalls.
- `references/blotato-staging-semantics.md` — durable Blotato upload/staging semantics: presigned PUT workflow, YouTube private uploads returning `published`, TikTok SELF_ONLY/draft handling, Instagram non-public hold rule, and run-package checklist.
- `references/ai-visual-rebuild-after-placeholder-rejection.md` — when a completed faceless/documentary video is rejected for weak/programmatic visuals, switch to real AI visual assets, rebuild, verify, and deliver contact sheets.
- `references/sop-to-production-test-run.md` — immediate SOP-to-production workflow: choose 1-2 validated topics, render local vertical proof cuts, ffprobe-verify, send MP4s to Telegram, then inspect premium visual/posting readiness while preserving the publish gate.
- `references/pre-delivery-visual-qa-gate.md` — mandatory Purse-facing visual QA gate: contact sheets, Claude/Felix frame review when needed, rejection criteria for placeholder visuals/cloud AI artifacts/debug metadata, and send-only-after-pass delivery rule.
- `references/kie-ai-production-rebuild.md` — Kie/Nano Banana + Kie ElevenLabs rebuild workflow for turning rejected placeholder/stock drafts into reviewed Purse-facing vertical MP4s, including robust URL download, contact-sheet QA, and ElevenLabs 500 local-say fallback.
- `references/multi-video-parallel-production-batch.md` — producing multiple vertical shorts from different Niches/SOPs in a single run: single-builder script with per-video metadata dicts, shared scene-prep pipeline, caption timing algorithm, and output structure.
