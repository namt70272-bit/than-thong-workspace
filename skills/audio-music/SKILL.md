---
name: audio-music
description: "All audio, speech, and music tools. Covers ElevenLabs cloud TTS (sag), offline local TTS (sherpa-onnx-tts), local Whisper speech-to-text (openai-whisper), cloud Whisper transcription (openai-whisper-api), audio spectrograms (songsee), and Spotify terminal playback (spotify-player)."
---

# Audio & Music

Consolidated skill covering text-to-speech, speech-to-text, audio visualization, and music playback.

---

## sag — ElevenLabs Text-to-Speech

Use `sag` for ElevenLabs TTS with local playback.

**Requires:** `sag` binary, `ELEVENLABS_API_KEY`
**Install:** `brew install steipete/tap/sag`
**Homepage:** https://sag.sh

### API key (required)
- `ELEVENLABS_API_KEY` (preferred)
- `SAG_API_KEY` also supported by the CLI

### Quick start

```bash
sag "Hello there"
sag speak -v "Roger" "Hello"
sag voices
sag prompting     # model-specific tips
```

### Model notes
- Default: `eleven_v3` (expressive)
- Stable: `eleven_multilingual_v2`
- Fast: `eleven_flash_v2_5`

### Pronunciation + delivery rules
- First fix: respell (e.g. "key-note"), add hyphens, adjust casing.
- Numbers/units/URLs: `--normalize auto` (or `off` if it harms names).
- Language bias: `--lang en|de|fr|...` to guide normalization.
- v3: SSML `<break>` not supported; use `[pause]`, `[short pause]`, `[long pause]`.
- v2/v2.5: SSML `<break time="1.5s" />` supported; `<phoneme>` not exposed in `sag`.

### v3 audio tags (put at the entrance of a line)
- `[whispers]`, `[shouts]`, `[sings]`
- `[laughs]`, `[starts laughing]`, `[sighs]`, `[exhales]`
- `[sarcastic]`, `[curious]`, `[excited]`, `[crying]`, `[mischievously]`
- Example: `sag "[whispers] keep this quiet. [short pause] ok?"`

### Voice defaults
- Set `ELEVENLABS_VOICE_ID` or `SAG_VOICE_ID` for default voice.
- Confirm voice + speaker before long output.

### Chat voice responses

When the user asks for a "voice" reply (e.g., "crazy scientist voice"):

```bash
# Generate audio file
sag -v Clawd -o /tmp/voice-reply.mp3 "Your message here"
# Then include: MEDIA:/tmp/voice-reply.mp3
```

Voice character tips:
- Crazy scientist: Use `[excited]` tags, dramatic pauses `[short pause]`, vary intensity
- Calm: Use `[whispers]` or slower pacing
- Dramatic: Use `[sings]` or `[shouts]` sparingly

Default voice for Clawd: `lj2rcrvANS3gaWWnczSX` (or just `-v Clawd`)

---

## sherpa-onnx-tts — Local Offline Text-to-Speech

Local TTS using the sherpa-onnx offline CLI. No API key needed.

**Requires:** `SHERPA_ONNX_RUNTIME_DIR`, `SHERPA_ONNX_MODEL_DIR` env vars
**Platforms:** macOS, Linux, Windows

### Install

1. Download the runtime for your OS (extracts into `$OPENCLAW_STATE_DIR/tools/sherpa-onnx-tts/runtime`, default `~/.openclaw/tools/sherpa-onnx-tts/runtime`)
2. Download a voice model (extracts into `$OPENCLAW_STATE_DIR/tools/sherpa-onnx-tts/models`)

Resolve the active state directory:
```bash
STATE_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}"
```

Configure in `~/.openclaw/openclaw.json`:
```json5
{
  skills: {
    entries: {
      "sherpa-onnx-tts": {
        env: {
          SHERPA_ONNX_RUNTIME_DIR: "/path/to/state-dir/tools/sherpa-onnx-tts/runtime",
          SHERPA_ONNX_MODEL_DIR: "/path/to/state-dir/tools/sherpa-onnx-tts/models/vits-piper-en_US-lessac-high",
        },
      },
    },
  },
}
```

### Usage

```bash
{baseDir}/bin/sherpa-onnx-tts -o ./tts.wav "Hello from local TTS."

# Add wrapper to PATH
export PATH="{baseDir}/bin:$PATH"
```

Windows:
```bash
node {baseDir}\bin\sherpa-onnx-tts -o tts.wav "Hello from local TTS."
```

### Notes
- Pick a different model from the sherpa-onnx `tts-models` release for other voices.
- If the model dir has multiple `.onnx` files, set `SHERPA_ONNX_MODEL_FILE` or pass `--model-file`.
- You can also pass `--tokens-file` or `--data-dir` to override defaults.

---

## openai-whisper — Local Speech-to-Text (Whisper CLI)

Use `whisper` to transcribe audio locally. No API key required.

**Requires:** `whisper` CLI
**Install:** `brew install openai-whisper`
**Homepage:** https://openai.com/research/whisper

### Quick start

```bash
whisper /path/audio.mp3 --model medium --output_format txt --output_dir .
whisper /path/audio.m4a --task translate --output_format srt
```

### Notes
- Models download to `~/.cache/whisper` on first run.
- `--model` defaults to `turbo` on this install.
- Use smaller models for speed, larger for accuracy.

---

## openai-whisper-api — Cloud Speech-to-Text (OpenAI API)

Transcribe an audio file via OpenAI's `/v1/audio/transcriptions` endpoint.

**Requires:** `curl`, `OPENAI_API_KEY`
**Install:** `brew install curl`
**Homepage:** https://platform.openai.com/docs/guides/speech-to-text

### Quick start

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a
```

Defaults: Model `whisper-1`, output `<input>.txt`

### Useful flags

```bash
{baseDir}/scripts/transcribe.sh /path/to/audio.ogg --model whisper-1 --out /tmp/transcript.txt
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --language en
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --prompt "Speaker names: Peter, Daniel"
{baseDir}/scripts/transcribe.sh /path/to/audio.m4a --json --out /tmp/transcript.json
```

### API key setup

Set `OPENAI_API_KEY`, or configure in `~/.openclaw/openclaw.json`:

```json5
{
  skills: {
    "openai-whisper-api": {
      apiKey: "OPENAI_KEY_HERE",
    },
  },
}
```

Optionally set `OPENAI_BASE_URL` (e.g. `http://127.0.0.1:51805/v1`) to use an OpenAI-compatible proxy.

---

## songsee — Audio Spectrograms & Visualizations

Generate spectrograms and feature-panel visualizations from audio files.

**Requires:** `songsee`
**Install:** `brew install steipete/tap/songsee`
**Homepage:** https://github.com/steipete/songsee

### Quick start

```bash
songsee track.mp3                                            # Basic spectrogram
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux  # Multi-panel
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg    # Time slice
cat track.mp3 | songsee - --format png -o out.png            # Stdin
```

### Common flags
- `--viz` list (repeatable or comma-separated)
- `--style` palette: `classic`, `magma`, `inferno`, `viridis`, `gray`
- `--width` / `--height` output size
- `--window` / `--hop` FFT settings
- `--min-freq` / `--max-freq` frequency range
- `--start` / `--duration` time slice
- `--format` `jpg|png`

### Notes
- WAV/MP3 decode native; other formats use ffmpeg if available.
- Multiple `--viz` renders a grid.

---

## spotify-player — Terminal Spotify Playback

Use `spogo` (preferred) or `spotify_player` for Spotify playback and search.

**Requires:** Spotify Premium, `spogo` or `spotify_player`
**Install:** `brew install steipete/tap/spogo` or `brew install spotify_player`
**Homepage:** https://www.spotify.com

### spogo setup

```bash
spogo auth import --browser chrome   # Import cookies
```

### spogo commands (preferred)

```bash
spogo search track "query"           # Search
spogo play                           # Start playback
spogo pause                          # Pause
spogo next                           # Next track
spogo prev                           # Previous track
spogo device list                    # List devices
spogo device set "<name|id>"         # Set active device
spogo status                         # Current playback status
```

### spotify_player commands (fallback)

```bash
spotify_player search "query"
spotify_player playback play|pause|next|previous
spotify_player connect
spotify_player like
```

### Notes
- Config folder: `~/.config/spotify-player` (e.g., `app.toml`).
- For Spotify Connect integration, set a user `client_id` in config.
- TUI shortcuts available via `?` in the app.
