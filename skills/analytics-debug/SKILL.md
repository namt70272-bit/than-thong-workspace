---
name: analytics-debug
description: "Analytics and debugging tools: CodexBar model cost logs (model-usage), session log search (session-logs), and oracle CLI for bundling prompts/files for second-model debugging."
---

# Analytics & Debug

Consolidated skill covering three tools: **model-usage** (CodexBar cost logs), **session-logs** (search session JSONL files), and **oracle** (bundle prompts/files for external model debugging).

---

## Part 1 — model-usage (CodexBar Cost Logs)

Get per-model usage cost from CodexBar's local cost logs. Supports "current model" (most recent daily entry) or "all models" summaries for Codex or Claude.

### Requirements
- Binary: `codexbar`
- Install: `brew install steipete/tap/codexbar`
- OS: macOS

### Quick Start

```bash
python {baseDir}/scripts/model_usage.py --provider codex --mode current
python {baseDir}/scripts/model_usage.py --provider codex --mode all
python {baseDir}/scripts/model_usage.py --provider claude --mode all --format json --pretty
```

### Current Model Logic

- Uses the most recent daily row with `modelBreakdowns`.
- Picks the model with the highest cost in that row.
- Falls back to the last entry in `modelsUsed` when breakdowns are missing.
- Override with `--model <name>` when you need a specific model.

### Inputs

```bash
# Default: runs codexbar automatically
python {baseDir}/scripts/model_usage.py --provider codex --mode all

# From a saved file
codexbar cost --provider codex --format json > /tmp/cost.json
python {baseDir}/scripts/model_usage.py --input /tmp/cost.json --mode all

# From stdin
cat /tmp/cost.json | python {baseDir}/scripts/model_usage.py --input - --mode current
```

### Output

- Text (default) or JSON (`--format json --pretty`).
- Values are cost-only per model; tokens are not split by model in CodexBar output.

### References

- Read `references/codexbar-cli.md` for CLI flags and cost JSON fields.

---

## Part 2 — session-logs (Search Session JSONL Files)

Search your complete conversation history stored in session JSONL files. Use when a user references older/parent conversations or asks what was said before.

### Requirements
- Binaries: `jq`, `rg` (ripgrep)
- Install: `brew install jq` / `brew install ripgrep`

### Location

Session logs live under:
`$OPENCLAW_STATE_DIR/agents/<agentId>/sessions/` (default: `~/.openclaw/agents/<agentId>/sessions/`)

Use the `agent=<id>` value from the system prompt Runtime line.

- **`sessions.json`** — Index mapping session keys to session IDs
- **`<session-id>.jsonl`** — Full conversation transcript per session

### Structure

Each `.jsonl` file contains messages with:
- `type`: "session" (metadata) or "message"
- `timestamp`: ISO timestamp
- `message.role`: "user", "assistant", or "toolResult"
- `message.content[]`: Text, thinking, or tool calls (filter `type=="text"` for human-readable content)
- `message.usage.cost.total`: Cost per response

### Common Queries

**List all sessions by date and size:**
```bash
AGENT_ID="<agentId>"
SESSION_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/agents/$AGENT_ID/sessions"
for f in "$SESSION_DIR"/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  size=$(ls -lh "$f" | awk '{print $5}')
  echo "$date $size $(basename $f)"
done | sort -r
```

**Find sessions from a specific day:**
```bash
AGENT_ID="<agentId>"
SESSION_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/agents/$AGENT_ID/sessions"
for f in "$SESSION_DIR"/*.jsonl; do
  head -1 "$f" | jq -r '.timestamp' | grep -q "2026-01-06" && echo "$f"
done
```

**Extract user messages from a session:**
```bash
jq -r 'select(.message.role == "user") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl
```

**Search for keyword in assistant responses:**
```bash
jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text' <session>.jsonl | rg -i "keyword"
```

**Get total cost for a session:**
```bash
jq -s '[.[] | .message.usage.cost.total // 0] | add' <session>.jsonl
```

**Daily cost summary:**
```bash
AGENT_ID="<agentId>"
SESSION_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/agents/$AGENT_ID/sessions"
for f in "$SESSION_DIR"/*.jsonl; do
  date=$(head -1 "$f" | jq -r '.timestamp' | cut -dT -f1)
  cost=$(jq -s '[.[] | .message.usage.cost.total // 0] | add' "$f")
  echo "$date $cost"
done | awk '{a[$1]+=$2} END {for(d in a) print d, "$"a[d]}' | sort -r
```

**Count messages and tokens in a session:**
```bash
jq -s '{
  messages: length,
  user: [.[] | select(.message.role == "user")] | length,
  assistant: [.[] | select(.message.role == "assistant")] | length,
  first: .[0].timestamp,
  last: .[-1].timestamp
}' <session>.jsonl
```

**Tool usage breakdown:**
```bash
jq -r '.message.content[]? | select(.type == "toolCall") | .name' <session>.jsonl | sort | uniq -c | sort -rn
```

**Search across ALL sessions for a phrase:**
```bash
AGENT_ID="<agentId>"
SESSION_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/agents/$AGENT_ID/sessions"
rg -l "phrase" "$SESSION_DIR"/*.jsonl
```

**Fast text-only hint (low noise):**
```bash
AGENT_ID="<agentId>"
SESSION_DIR="${OPENCLAW_STATE_DIR:-$HOME/.openclaw}/agents/$AGENT_ID/sessions"
jq -r 'select(.type=="message") | .message.content[]? | select(.type=="text") | .text' "$SESSION_DIR"/<id>.jsonl | rg 'keyword'
```

### Tips

- Sessions are append-only JSONL (one JSON object per line)
- Large sessions can be several MB — use `head`/`tail` for sampling
- The `sessions.json` index maps chat providers (discord, whatsapp, etc.) to session IDs
- Deleted sessions have `.deleted.<timestamp>` suffix

---

## Part 3 — oracle (Bundle Prompt + Files for Second-Model Debugging)

Oracle bundles your prompt + selected files into one "one-shot" request so another model can answer with real repo context (API or browser automation). Treat output as advisory: verify against code + tests.

### Requirements
- Binary: `oracle`
- Install: `npm install -g @steipete/oracle` (or `npx -y @steipete/oracle --help` without install)
- Homepage: https://askoracle.dev

### Main Use Case (Browser, GPT‑5.2 Pro)

Default workflow: `--engine browser` with GPT‑5.2 Pro in ChatGPT. This is the common "long think" path: ~10 minutes to ~1 hour is normal; expect a stored session you can reattach to.

Recommended defaults:
- Engine: browser (`--engine browser`)
- Model: GPT‑5.2 Pro (`--model gpt-5.2-pro` or `--model "5.2 Pro"`)

### Golden Path

1. Pick a tight file set (fewest files that still contain the truth).
2. Preview payload + token spend (`--dry-run` + `--files-report`).
3. Use browser mode for the usual GPT‑5.2 Pro workflow; use API only when you explicitly want it.
4. If the run detaches/timeouts: reattach to the stored session (don't re-run).

### Commands

**Help:**
```bash
oracle --help
# If not installed:
npx -y @steipete/oracle --help
```

**Preview (no tokens spent):**
```bash
oracle --dry-run summary -p "<task>" --file "src/**" --file "!**/*.test.*"
oracle --dry-run full -p "<task>" --file "src/**"
```

**Token sanity check:**
```bash
oracle --dry-run summary --files-report -p "<task>" --file "src/**"
```

**Browser run (main path; long-running is normal):**
```bash
oracle --engine browser --model gpt-5.2-pro -p "<task>" --file "src/**"
```

**Manual paste fallback:**
```bash
oracle --render --copy -p "<task>" --file "src/**"
# Note: --copy is a hidden alias for --copy-markdown
```

### Attaching Files (`--file`)

`--file` accepts files, directories, and globs. Pass it multiple times; entries can be comma-separated.

```bash
# Include
--file "src/**"
--file src/index.ts
--file docs --file README.md

# Exclude
--file "src/**" --file "!src/**/*.test.ts" --file "!**/*.snap"
```

Default-ignored dirs: `node_modules`, `dist`, `coverage`, `.git`, `.turbo`, `.next`, `build`, `tmp`. Files > 1 MB rejected.

### Engines (API vs Browser)

- **Auto-pick**: `api` when `OPENAI_API_KEY` is set; otherwise `browser`.
- **Browser** supports GPT + Gemini only; use `--engine api` for Claude/Grok/Codex or multi-model runs.
- **Browser attachments**: `--browser-attachments auto|never|always`
- **Remote browser host**:
  ```bash
  # Host:
  oracle serve --host 0.0.0.0 --port 9473 --token <secret>
  # Client:
  oracle --engine browser --remote-host <host:port> --remote-token <secret> -p "<task>" --file "src/**"
  ```

### Sessions + Slugs

- Stored under `~/.oracle/sessions` (override with `ORACLE_HOME_DIR`).
- If the CLI times out, reattach — don't re-run:
  ```bash
  oracle status --hours 72
  oracle session <id> --render
  ```
- Use `--slug "<3-5 words>"` to keep session IDs readable.
- Use `--force` only when you truly want a fresh run (duplicate prompt guard exists).

### Prompt Template (High Signal)

Oracle starts with **zero** project knowledge. Include:
- Project briefing (stack + build/test commands + platform constraints)
- "Where things live" (key directories, entrypoints, config files, boundaries)
- Exact question + what you tried + the error text (verbatim)
- Constraints ("don't change X", "must keep public API", etc.)
- Desired output ("return patch plan + tests", "give 3 options with tradeoffs")

### Safety

- Don't attach secrets by default (`.env`, key files, auth tokens). Redact aggressively.

### "Exhaustive Prompt" Restoration Pattern

For long investigations, write a standalone prompt + file set so you can rerun days later:
- 6–30 sentence project briefing + the goal
- Repro steps + exact errors + what you tried
- Attach all context files needed (entrypoints, configs, key modules, docs)

Oracle runs are one-shot; the model doesn't remember prior runs. "Restoring context" means re-running with the same prompt + `--file …` set (or reattaching a still-running stored session).
