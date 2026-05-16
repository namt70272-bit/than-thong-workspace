---
name: web-search
description: "Unified web & content search skill covering blog/RSS feed monitoring (blogwatcher), Gemini CLI for AI-powered Q&A and summaries, GIF search (gifgrep), URL/video/PDF summarization (summarize), and Google Places search (goplaces)."
---
# Web Search & Content Discovery

This skill covers all web search and content discovery tools: RSS/blog feed monitoring via blogwatcher, Gemini CLI for AI Q&A and generation, GIF search via gifgrep, URL/video/document summarization via summarize, and Google Places search via goplaces.

---

## 1. blogwatcher — Blog & RSS/Atom Feed Monitor

**Requires:** `blogwatcher` binary  
**Install:** `go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest`  
**Docs:** https://github.com/Hyaxia/blogwatcher

### Common Commands

```bash
# Add a blog or RSS/Atom feed
blogwatcher add "My Blog" https://example.com

# List tracked blogs
blogwatcher blogs

# Scan for new articles
blogwatcher scan

# List articles (new and read)
blogwatcher articles

# Mark an article as read
blogwatcher read 1

# Mark all articles read
blogwatcher read-all

# Remove a blog
blogwatcher remove "My Blog"

# Help for any command
blogwatcher <command> --help
```

### Example Output

```
$ blogwatcher blogs
Tracked blogs (1):

  xkcd
    URL: https://xkcd.com

$ blogwatcher scan
Scanning 1 blog(s)...

  xkcd
    Source: RSS | Found: 4 | New: 4

Found 4 new article(s) total!
```

---

## 2. Gemini CLI — AI-Powered Q&A and Generation

**Requires:** `gemini` binary  
**Install:** `brew install gemini-cli`  
**Docs:** https://ai.google.dev/

Use Gemini in one-shot mode with a positional prompt. Avoid interactive mode.

### Common Commands

```bash
# One-shot Q&A or generation
gemini "Answer this question..."

# Use a specific model
gemini --model <name> "Prompt..."

# Request JSON output
gemini --output-format json "Return JSON describing..."

# List available extensions
gemini --list-extensions

# Manage extensions
gemini extensions <command>
```

**Notes:**
- If auth is required, run `gemini` once interactively to complete the login flow.
- Avoid `--yolo` flag for safety.
- Best for one-shot tasks: summaries, Q&A, structured generation, and quick lookups.

---

## 3. gifgrep — GIF Search

**Description:** Search for GIFs by keyword using the `gifgrep` CLI, which queries GIF providers (e.g. Giphy, Tenor) and returns matching results.

**Requirements:** `gifgrep` binary installed and API key configured.

### Common Commands

```bash
# Search for GIFs by keyword
gifgrep "celebration"

# Limit results
gifgrep "reaction" --limit 5

# Output URLs only
gifgrep "funny cat" --urls-only
```

**Notes:**
- Requires a Giphy or Tenor API key configured in the environment or config file.
- Returns URLs or local previews of matching GIFs.

---

## 4. summarize — URL, Video & Document Summarizer

**Requires:** `summarize` binary  
**Install:** `brew install steipete/tap/summarize`  
**Docs:** https://summarize.sh

### When to Use

Use this skill immediately when the user asks:
- "summarize this URL/article"
- "what's this link/video about?"
- "transcribe this YouTube/video"
- "use summarize.sh"

### Quick Start

```bash
summarize "https://example.com" --model google/gemini-3-flash-preview
summarize "/path/to/file.pdf" --model google/gemini-3-flash-preview
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto
```

### YouTube: Summary vs Transcript

```bash
# Best-effort transcript extraction (no yt-dlp needed)
summarize "https://youtu.be/dQw4w9WgXcQ" --youtube auto --extract-only
```

If transcript is large, return a tight summary first, then ask which section/time range to expand.

### Useful Flags

```
--length short|medium|long|xl|xxl|<chars>
--max-output-tokens <count>
--extract-only          (URLs only; no LLM summarization)
--json                  (machine-readable output)
--firecrawl auto|off|always   (fallback extraction for blocked sites)
--youtube auto          (Apify fallback if APIFY_API_TOKEN set)
```

### Model & API Keys

Default model: `google/gemini-3-flash-preview`

Set the API key for your chosen provider:
- OpenAI: `OPENAI_API_KEY`
- Anthropic: `ANTHROPIC_API_KEY`
- xAI: `XAI_API_KEY`
- Google: `GEMINI_API_KEY` (aliases: `GOOGLE_GENERATIVE_AI_API_KEY`, `GOOGLE_API_KEY`)

### Config

Optional config file `~/.summarize/config.json`:
```json
{ "model": "openai/gpt-5.2" }
```

Optional service keys:
- `FIRECRAWL_API_KEY` — for blocked/paywalled sites
- `APIFY_API_TOKEN` — for YouTube transcript fallback

---

## 5. goplaces — Google Places Search

**Requires:** `goplaces` binary + `GOOGLE_PLACES_API_KEY` env var  
**Install:** `brew install steipete/tap/goplaces`  
**Docs:** https://github.com/steipete/goplaces

### Common Commands

```bash
# Text search
goplaces search "coffee" --open-now --min-rating 4 --limit 5

# Location-biased search
goplaces search "pizza" --lat 40.8 --lng -73.9 --radius-m 3000

# Paginate results
goplaces search "pizza" --page-token "NEXT_PAGE_TOKEN"

# Resolve a place name to ID(s)
goplaces resolve "Soho, London" --limit 5

# Get place details (with reviews)
goplaces details <place_id> --reviews

# JSON output for scripts
goplaces search "sushi" --json
```

### Notes

- `GOOGLE_PLACES_API_KEY` is required. Set it in your environment.
- Optional: `GOOGLE_PLACES_BASE_URL` for testing or proxying.
- `--no-color` or `NO_COLOR=1` disables ANSI color output.
- Price levels: 0 (free) to 4 (very expensive).
- Type filter: only the first `--type` value is sent (API accepts one type at a time).
- Human-readable output by default; use `--json` for scripting.
