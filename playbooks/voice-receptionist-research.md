# Voice AI Receptionist - Research & Architecture

**Date**: 2026-05-05
**Goal**: Build a voice AI receptionist system under $0.03/min total cost
**Services**: Foundation for Service 1, 7, 8

---

## 1. Open-Source Voice AI Frameworks

### Tier 1 (Production-Ready, Actively Maintained)

| Framework | License | Language | Phone Support | Notes |
|-----------|---------|----------|---------------|-------|
| **Pipecat** | BSD-2 | Python | Twilio, Telnyx via WebSocket | Daily.co backed. 40+ AI service plugins. Best for rapid prototyping. |
| **LiveKit Agents** | Apache 2.0 | Python/Go | Native SIP (GA since 2025) | WebRTC-based. Lowest latency. Built-in phone numbers. v1.5.x as of 2026. |

### Tier 2 (Viable but Caveats)

| Framework | Status | Notes |
|-----------|--------|-------|
| **Vocode** | Stalled (2026) | Was good, active dev stopped. Avoid for new projects. |
| **AIReceptionist** (kirklandsig) | Active | OpenAI Realtime API only. Cost: $0.04-0.20/min. Not cheap enough. |
| **Dograh** | Newer entrant | Dashboard-first, less flexible. |

### Recommendation: **Pipecat**
- Most flexible provider choices (swap STT/LLM/TTS freely)
- Twilio + WebSocket integration is well-documented
- Zero framework fees (open source)
- Can self-host entirely on Mac mini
- Large community, NVIDIA backing

---

## 2. Phone Number & Inbound Calls (Cheapest Options)

| Provider | Number Cost | Inbound/min | Outbound/min | SIP Support | Notes |
|----------|-------------|-------------|--------------|-------------|-------|
| **Telnyx** | $1/mo | $0.002/min | $0.010/min | Yes (Elastic SIP) | Best price. Channel billing option for unlimited inbound. |
| **Twilio** | $1.15/mo | $0.0085/min | $0.014/min | Yes | Most documented. ConversationRelay supports Claude directly. |
| **Plivo** | $0.80/mo | $0.0085/min | $0.010/min | Yes | Simple APIs, predictable spend. |
| **Vonage** | $1/mo | $0.0084/min | $0.012/min | Yes | Good fraud prevention. |
| **LiveKit Phone** | Varies | Included in LiveKit | - | Native | Simplest if using LiveKit Agents. |

### Recommendation: **Telnyx** (cheapest) or **Twilio** (best docs + Claude integration)

For our target: Telnyx at $0.002/min inbound is unbeatable.

---

## 3. Speech-to-Text (STT) Options

| Provider | Cost/min | Streaming | Latency | Self-Hosted | Notes |
|----------|----------|-----------|---------|-------------|-------|
| **Self-hosted Whisper (whisper.cpp)** | $0.00 | Yes | ~100ms on M-series | Yes | FREE. Mac mini can do real-time easily (10x+ real-time on M2 Pro). |
| **Self-hosted faster-whisper** | $0.00 | Yes | ~100ms | Yes (needs GPU) | 4x faster than OpenAI Whisper. CTranslate2 backend. |
| **Deepgram Nova-3** | $0.0077/min | Yes | <300ms | No | Best accuracy. $200 free credits (~26K minutes). |
| **OpenAI gpt-4o-mini-transcribe** | $0.003/min | Limited | ~500ms | No | Cheapest cloud. Good accuracy. |
| **OpenAI gpt-4o-transcribe** | $0.006/min | Limited | ~500ms | No | Better accuracy, 2x price. |
| **AssemblyAI** | $0.0065/min | Yes | <500ms | No | Good streaming, higher cost. |

### Recommendation: **Self-hosted whisper.cpp on Mac mini** ($0.00/min)
- Apple Silicon Metal acceleration works out of the box
- large-v3-turbo model: 10x real-time on M2 Pro
- Pipecat has a local Whisper plugin
- Fallback: Deepgram at $0.0077/min (excellent streaming, free $200 credit)

---

## 4. Text-to-Speech (TTS) Options

| Provider | Cost/min | Latency | Quality | Self-Hosted | Notes |
|----------|----------|---------|---------|-------------|-------|
| **Piper TTS** | $0.00 | <200ms | Good (not ElevenLabs tier) | Yes | CPU-only, runs on Raspberry Pi. ONNX models. |
| **Coqui TTS** | $0.00 | ~300ms | Good | Yes | 17 languages. Voice cloning from 6 sec. |
| **gpt-4o-mini-tts** | $0.015/min | ~300ms | Excellent | No | Best price/quality ratio in cloud. 13 voices. |
| **Deepgram Aura** | $0.015/min | <250ms | Very Good | No | Low latency streaming TTS. |
| **OpenAI tts-1** | ~$0.015/min | ~400ms | Good | No | Standard OpenAI voices. |
| **Cartesia Sonic** | ~$0.03/min | <100ms | Excellent | No | Fastest first-byte. Premium price. |
| **ElevenLabs** | ~$0.05/min | ~300ms | Best | No | Too expensive for target. |

### Recommendation: **Piper TTS self-hosted** ($0.00/min) for budget
- Runs on Mac mini CPU easily
- Pipecat has native Piper integration
- Quality is acceptable for phone calls (8kHz codec)
- Upgrade path: gpt-4o-mini-tts at $0.015/min for premium quality

---

## 5. LLM Options for Voice Agent

| Provider | Cost (est/min conversation) | Latency | Notes |
|----------|----------------------------|---------|-------|
| **Claude Haiku 4.5** | ~$0.002/min | Fast | $1/$5 per 1M tokens. Best value. |
| **Claude Sonnet 4.6** | ~$0.008/min | Medium | $3/$15 per 1M tokens. Better reasoning. |
| **GPT-4o-mini** | ~$0.002/min | Fast | Comparable to Haiku. |
| **Self-hosted Llama 3.2 3B** | $0.00 | ~500ms | Free but lower quality. Runs on Mac mini. |
| **Self-hosted Llama 3.1 8B** | $0.00 | ~1-2s | Free, good quality. Needs Mac mini RAM. |
| **Groq (Llama)** | ~$0.001/min | <200ms | Fastest inference. Very cheap. |

### Recommendation: **Claude Haiku 4.5** (~$0.002/min)
- Best quality/cost for conversation
- Tool use (function calling) for booking, transfers, etc.
- Fallback: self-hosted Llama 3.2 for $0.00 if cost is critical

---

## 6. Total Cost Per Minute Breakdown

### Budget Stack (Target: $0.00-0.01/min)

| Component | Provider | Cost/min |
|-----------|----------|----------|
| Phone (inbound) | Telnyx | $0.002 |
| STT | Self-hosted whisper.cpp | $0.000 |
| LLM | Claude Haiku 4.5 | $0.002 |
| TTS | Self-hosted Piper | $0.000 |
| Framework | Pipecat (open source) | $0.000 |
| **TOTAL** | | **$0.004/min** |

### Quality Stack (Target: under $0.03/min)

| Component | Provider | Cost/min |
|-----------|----------|----------|
| Phone (inbound) | Telnyx | $0.002 |
| STT | Deepgram Nova-3 | $0.008 |
| LLM | Claude Haiku 4.5 | $0.002 |
| TTS | gpt-4o-mini-tts | $0.015 |
| Framework | Pipecat (open source) | $0.000 |
| **TOTAL** | | **$0.027/min** |

### Comparison to Competitors

| Platform | Cost/min |
|----------|----------|
| Vapi | $0.05 |
| Retell AI | $0.07-0.10 |
| Bland.ai | $0.09 |
| **Our Budget Stack** | **$0.004** |
| **Our Quality Stack** | **$0.027** |

---

## 7. Architecture

```
                    INBOUND CALL FLOW

    Caller ──► Telnyx/Twilio SIP ──► WebSocket ──► Pipecat Server (Mac mini)
                                                         │
                                         ┌───────────────┼───────────────┐
                                         │               │               │
                                         ▼               ▼               ▼
                                   whisper.cpp      Claude API       Piper TTS
                                   (local STT)     (Haiku 4.5)     (local TTS)
                                         │               │               │
                                         └───────────────┼───────────────┘
                                                         │
                                                         ▼
                                                  Audio Response
                                                  back via WebSocket
                                                         │
                                                         ▼
                                              Caller hears response
```

### Connection Flow (Technical)

1. **Caller dials phone number** (Telnyx/Twilio DID)
2. **Telephony provider** hits webhook on our server
3. **Server responds** with WebSocket upgrade (Twilio ConversationRelay or Telnyx Media Streaming)
4. **Audio streams in** via WebSocket (8kHz mu-law PCM)
5. **Pipecat pipeline** processes: audio → whisper.cpp (STT) → Claude Haiku (LLM) → Piper (TTS) → audio
6. **Audio streams back** via same WebSocket
7. **Caller hears AI response** with <1-2s latency

### Key Protocol Details

- **SIP**: Session Initiation Protocol handles call setup/teardown
- **WebSocket**: Bidirectional real-time audio streaming after call connects
- **Codec**: G.711 mu-law (8kHz) standard for telephony
- **Interruption handling**: Pipecat handles barge-in natively

---

## 8. What Runs on Mac Mini (pharma6)

### Can Run Locally (FREE)

| Component | Resource Usage | Notes |
|-----------|---------------|-------|
| Pipecat server | ~0.5 CPU per concurrent call | 10 CPU machine = ~20 concurrent calls |
| whisper.cpp (STT) | GPU (Metal) + ~2GB RAM | large-v3-turbo model, real-time on Apple Silicon |
| Piper TTS | CPU only, minimal | ONNX models, very lightweight |
| Llama 3.2 3B (optional LLM) | ~4GB RAM | If you want fully local, no API costs |
| FastAPI/WebSocket server | Minimal | Handles Twilio/Telnyx webhooks |

### Must Use Cloud APIs

| Component | Why |
|-----------|-----|
| Claude Haiku | Quality + tool use. Self-hosted Llama is fallback. |
| Phone number (Telnyx) | Need a real DID number. $1/mo. |
| Deepgram (optional STT upgrade) | If whisper.cpp latency is too high for streaming. |
| gpt-4o-mini-tts (optional TTS upgrade) | If Piper quality isn't sufficient. |

### Mac Mini Requirements

- macOS (already have it)
- Python 3.11+
- whisper.cpp compiled with Metal support
- Piper installed (single binary + voice model)
- Pipecat installed via pip
- Public endpoint (Cloudflare tunnel already in place)

---

## 9. Recommended Production Stack

### Phase 1: MVP (Get it working)

```
Twilio + Pipecat + Deepgram STT + Claude Haiku + gpt-4o-mini-tts
Cost: ~$0.027/min
```

Why: Twilio has the best Claude ConversationRelay docs. Deepgram and gpt-4o-mini-tts are reliable cloud services with low latency. Ship fast, optimize later.

### Phase 2: Optimize (Reduce cost)

```
Telnyx + Pipecat + whisper.cpp (local) + Claude Haiku + Piper TTS (local)
Cost: ~$0.004/min
```

Why: Replace cloud STT/TTS with local inference. Only pay for phone + LLM.

### Phase 3: Scale (High volume)

```
Telnyx (channel billing) + Pipecat + whisper.cpp + Claude Haiku (cached) + Piper TTS
Cost: ~$0.002/min at volume
```

Why: Channel billing = unlimited inbound minutes flat fee. Prompt caching reduces Claude costs by 90%.

---

## 10. Key Implementation Resources

### Tutorials & Repos

- **Pipecat + Twilio**: https://docs.cerebrium.ai/v4/examples/twilio-voice-agent
- **Pipecat quickstart**: https://docs.pipecat.ai/getting-started/quickstart
- **Pipecat GitHub**: https://github.com/pipecat-ai/pipecat
- **LiveKit telephony**: https://docs.livekit.io/telephony/
- **LiveKit Agents GitHub**: https://github.com/livekit/agents
- **AIReceptionist (reference)**: https://github.com/kirklandsig/AIReceptionist
- **Twilio + Claude ConversationRelay**: https://www.twilio.com/en-us/blog/integrate-anthropic-twilio-voice-using-conversationrelay
- **Twilio + Claude function calling**: https://www.twilio.com/en-us/blog/developers/tutorials/product/function-calling-twilio-voice-anthropic-claude-integration
- **whisper.cpp**: https://github.com/ggerganov/whisper.cpp
- **Piper TTS**: https://github.com/rhasspy/piper
- **Modal low-latency voice bot**: https://modal.com/blog/low-latency-voice-bot

### Pipecat Pipeline Example (Conceptual)

```python
from pipecat.pipeline import Pipeline
from pipecat.services.whisper import WhisperSTTService
from pipecat.services.anthropic import AnthropicLLMService
from pipecat.services.piper import PiperTTSService
from pipecat.transports.twilio import TwilioTransport

pipeline = Pipeline([
    TwilioTransport(websocket),       # Audio in/out
    WhisperSTTService(model="large-v3-turbo"),  # Local STT
    AnthropicLLMService(model="claude-haiku-4-5-20241022"),  # LLM
    PiperTTSService(voice="en_US-lessac-medium"),  # Local TTS
])
```

---

## 11. Latency Budget

Target: < 2 seconds end-to-end (caller speaks → hears response)

| Step | Target | Notes |
|------|--------|-------|
| Audio capture + network | 200ms | WebSocket overhead |
| STT (whisper.cpp local) | 200-400ms | Depends on utterance length |
| LLM (Claude Haiku) | 300-800ms | First token, then streaming |
| TTS (Piper local) | 100-200ms | First audio chunk |
| Audio delivery + network | 200ms | WebSocket back |
| **Total** | **1000-1800ms** | Acceptable for phone |

---

## 12. Risks & Mitigations

| Risk | Mitigation |
|------|-----------|
| whisper.cpp streaming latency | Fall back to Deepgram ($0.008/min) |
| Piper voice quality complaints | Upgrade to gpt-4o-mini-tts ($0.015/min) |
| Mac mini overload (many calls) | Scale to 2nd Mac or move STT/TTS to cloud |
| Twilio/Telnyx WebSocket drops | Implement reconnection logic in Pipecat |
| Claude API latency spikes | Cache common responses, use prompt caching |
| Phone compliance (STIR/SHAKEN) | Telnyx/Twilio handle this for inbound |

---

## 13. Decision Matrix

**For Service 1, 7, 8 voice AI:**

| Decision | Choice | Reason |
|----------|--------|--------|
| Framework | Pipecat | Open source, most flexible, Claude support |
| Phone provider | Telnyx (prod), Twilio (dev) | Cheapest inbound; Twilio for prototyping |
| STT | whisper.cpp local → Deepgram fallback | Free → $0.008/min |
| LLM | Claude Haiku 4.5 | $0.002/min, tool use, quality |
| TTS | Piper local → gpt-4o-mini-tts upgrade | Free → $0.015/min |
| Hosting | Mac mini (pharma6) | Already available, Apple Silicon = fast inference |
| Tunnel | Cloudflare Tunnel | Already configured for webhooks |

---

## Bottom Line

**You can build a production voice AI receptionist for $0.004-0.027/min** — that's 2-12x cheaper than Vapi/Retell/Bland. The Mac mini can handle all local inference (STT + TTS) for free, leaving only phone costs ($0.002/min) and LLM costs ($0.002/min) as recurring expenses.

Next step: Install Pipecat, set up whisper.cpp with Metal, test Piper voices, get a Telnyx number, wire up the pipeline.
