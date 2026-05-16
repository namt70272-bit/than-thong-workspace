# 11-Venice-AI - Skill Summary
> Nguon: E:\skill\11-Venice-AI
> Ngay: 2026-05-13
> Dong bo vao mang 07-Tich-hop-API

Tong SKILL.md: 20

- **my-venice-skill**: One or two sentences describing exactly when an agent should load this skill and what it covers. Mention the specific en
  - `template\SKILL.md`
- **venice-api-keys**: Manage Venice API keys. Covers GET/POST/PATCH/DELETE /api_keys, GET /api_keys/{id}, GET /api_keys/rate_limits, GET /api_
  - `skills\venice-api-keys\SKILL.md`
- **venice-api-overview**: High-level map of the Venice.ai API - base URL, authentication modes, endpoint categories, response headers, pricing mod
  - `skills\venice-api-overview\SKILL.md`
- **venice-audio-music**: Async music / audio-track generation via Venice. Covers the /audio/quote + /audio/queue + /audio/retrieve + /audio/compl
  - `skills\venice-audio-music\SKILL.md`
- **venice-audio-speech**: Generate speech from text via POST /audio/speech. Covers TTS models (Kokoro, Qwen 3, xAI, Inworld, Chatterbox, Orpheus, 
  - `skills\venice-audio-speech\SKILL.md`
- **venice-audio-transcription**: Transcribe audio files to text via POST /audio/transcriptions. Covers supported models (Parakeet, Whisper, Wizper, Scrib
  - `skills\venice-audio-transcription\SKILL.md`
- **venice-augment**: Venice augmentation endpoints for agent pipelines. Covers POST /augment/text-parser (extract text from PDF/DOCX/XLSX/pla
  - `skills\venice-augment\SKILL.md`
- **venice-auth**: Authenticate to the Venice API with a Bearer API key or with an x402 / SIWE wallet. Covers header formats, the SIWE mess
  - `skills\venice-auth\SKILL.md`
- **venice-billing**: Venice billing and usage analytics - GET /billing/balance, GET /billing/usage (paginated per-request ledger, JSON or CSV
  - `skills\venice-billing\SKILL.md`
- **venice-characters**: Discover and use Venice public characters (persona-driven system prompts with a bound model). Covers GET /characters (se
  - `skills\venice-characters\SKILL.md`
- **venice-chat**: Call POST /chat/completions on Venice. Covers the OpenAI-compatible request shape, Venice-only venice_parameters (web se
  - `skills\venice-chat\SKILL.md`
- **venice-crypto-rpc**: Use Venice as a pay-per-call JSON-RPC proxy to 20+ EVM and Starknet networks. Covers GET /crypto/rpc/networks, POST /cry
  - `skills\venice-crypto-rpc\SKILL.md`
- **venice-embeddings**: Call POST /embeddings on Venice. Covers request shape (input, model, encoding_format, dimensions, user), OpenAI compatib
  - `skills\venice-embeddings\SKILL.md`
- **venice-errors**: Handle Venice API errors correctly. Covers the StandardError / DetailedError / ContentViolationError / X402InferencePaym
  - `skills\venice-errors\SKILL.md`
- **venice-image-edit**: Transform existing images with Venice. Covers POST /image/edit (prompt-driven single-image edit), /image/multi-edit (com
  - `skills\venice-image-edit\SKILL.md`
- **venice-image-generate**: Generate images with Venice. Covers POST /image/generate (Venice-native), POST /images/generations (OpenAI-compatible), 
  - `skills\venice-image-generate\SKILL.md`
- **venice-models**: Discover Venice models, their capabilities, constraints, and pricing. Covers GET /models (with ?type filter), /models/tr
  - `skills\venice-models\SKILL.md`
- **venice-responses**: Use Venice's Alpha POST /responses endpoint - an OpenAI-compatible Responses API with typed output blocks (reasoning, me
  - `skills\venice-responses\SKILL.md`
- **venice-video**: Generate and transcribe videos via Venice. Covers the async /video/quote + /video/queue + /video/retrieve + /video/compl
  - `skills\venice-video\SKILL.md`
- **venice-x402**: Manage Venice x402 wallet credits. Covers POST /x402/top-up (payment discovery + signed USDC settlement), GET /x402/bala
  - `skills\venice-x402\SKILL.md`