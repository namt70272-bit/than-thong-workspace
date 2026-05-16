---
name: connectivity
description: "Device pairing, remote control, MCP servers, communication, food delivery, and PDF editing. Covers OpenClaw Android/iOS/macOS node pairing and diagnostics (node-connect), tmux session remote control (tmux), MCP server management (mcporter), voice calls (voice-call), Foodora order tracking (ordercli), and natural-language PDF editing (nano-pdf)."
---

# Connectivity & Utilities

Consolidated skill for device connectivity, remote control, MCP server management, and general CLI utilities.

---

## node-connect — Pair Android/iOS/macOS Nodes

Diagnose OpenClaw Android, iOS, or macOS node pairing: QR/setup code, route, auth, and connection failures.

### Topology first

Decide which case you are in before proposing fixes:
- Same machine / emulator / USB tunnel
- Same LAN / local Wi-Fi
- Same Tailscale tailnet
- Public URL / reverse proxy

Do not mix them. Ask for clarification if the setup is unclear.

### Canonical checks

```bash
openclaw config get gateway.mode
openclaw config get gateway.bind
openclaw config get gateway.tailscale.mode
openclaw config get gateway.remote.url
openclaw config get gateway.auth.mode
openclaw config get gateway.auth.allowTailscale
openclaw config get plugins.entries.device-pair.config.publicUrl
openclaw qr --json
openclaw devices list
openclaw nodes status
```

If pointed at a remote gateway:
```bash
openclaw qr --remote --json
```

If Tailscale is involved:
```bash
tailscale status --json
```

### Reading `openclaw qr --json` results

- `gatewayUrl`: the actual endpoint the app should use.
- `urlSource`: which config path won.

Common good sources:
- `gateway.bind=lan`: same Wi-Fi / LAN
- `gateway.bind=tailnet`: direct tailnet access
- `gateway.tailscale.mode=serve` or `funnel`: Tailscale route
- `plugins.entries.device-pair.config.publicUrl`: explicit public/reverse-proxy route
- `gateway.remote.url`: remote gateway route

### Root-cause map

**`Gateway is only bound to loopback`:**
- Same LAN: use `gateway.bind=lan`
- Same tailnet: prefer `gateway.tailscale.mode=serve` or `gateway.bind=tailnet`
- Public internet: set `plugins.entries.device-pair.config.publicUrl` or `gateway.remote.url`

**App says `pairing required`:**
```bash
openclaw devices list
openclaw devices approve --latest
```

**App says `bootstrap token invalid or expired`:**
- Generate a fresh setup code and rescan (do after any URL/auth fix).

**App says `unauthorized`:**
- Wrong token/password, or Tailscale expectation mismatch.
- For Tailscale Serve, `gateway.auth.allowTailscale` must match the intended flow.

### Fast heuristics
- Same Wi-Fi + gateway advertises `127.0.0.1`/loopback: wrong.
- Remote setup + manual uses private LAN IP: wrong.
- Tailnet setup + gateway advertises LAN IP instead of MagicDNS: wrong.
- `openclaw devices list` shows pending: stop changing network config and approve first.

---

## tmux — Remote-Control tmux Sessions

Remote-control tmux sessions for interactive CLIs by sending keystrokes and scraping pane output.

**Requires:** `tmux`
**Install:** `brew install tmux`
**Platforms:** macOS, Linux

### When to use
✅ Monitoring Claude/Codex sessions in tmux, sending input to interactive TUI apps, scraping long-running process output.
❌ Don't use for one-off shell commands (use `exec`), new background processes (use `exec background:true`), or non-interactive scripts.

### List sessions

```bash
tmux list-sessions
tmux ls
```

### Capture output

```bash
# Last 20 lines of pane
tmux capture-pane -t shared -p | tail -20

# Entire scrollback
tmux capture-pane -t shared -p -S -

# Specific pane in window
tmux capture-pane -t shared:0.0 -p
```

### Send keys

```bash
tmux send-keys -t shared "hello"         # Send text (no Enter)
tmux send-keys -t shared "y" Enter       # Send text + Enter
tmux send-keys -t shared Enter           # Enter only
tmux send-keys -t shared Escape
tmux send-keys -t shared C-c             # Ctrl+C
tmux send-keys -t shared C-d             # Ctrl+D (EOF)
tmux send-keys -t shared C-z             # Ctrl+Z (suspend)
```

### Window/pane navigation

```bash
tmux select-window -t shared:0
tmux select-pane -t shared:0.1
tmux list-windows -t shared
```

### Session management

```bash
tmux new-session -d -s newsession
tmux kill-session -t sessionname
tmux rename-session -t old new
```

### Sending input safely (for TUIs)

```bash
tmux send-keys -t shared -l -- "Please apply the patch in src/foo.ts"
sleep 0.1
tmux send-keys -t shared Enter
```

### Claude Code session patterns

```bash
# Check if session needs input
tmux capture-pane -t worker-3 -p | tail -10 | grep -E "❯|Yes.*No|proceed|permission"

# Approve prompt
tmux send-keys -t worker-3 'y' Enter

# Check all sessions
for s in shared worker-2 worker-3 worker-4 worker-5 worker-6 worker-7 worker-8; do
  echo "=== $s ==="
  tmux capture-pane -t $s -p 2>/dev/null | tail -5
done

# Send task to session
tmux send-keys -t worker-4 "Fix the bug in auth.js" Enter
```

### Notes
- Target format: `session:window.pane` (e.g., `shared:0.0`)
- Use `capture-pane -p` to print to stdout (essential for scripting)
- `-S -` captures entire scrollback history
- Sessions persist across SSH disconnects

---

## mcporter — MCP Server Management

List, configure, authenticate, call, and inspect MCP servers/tools over HTTP or stdio.

**Requires:** `mcporter`
**Install:** `npm install -g mcporter`
**Homepage:** http://mcporter.dev

### Quick start

```bash
mcporter list
mcporter list <server> --schema
mcporter call <server.tool> key=value
```

### Call tools

```bash
# Selector style
mcporter call linear.list_issues team=ENG limit:5

# Function syntax
mcporter call "linear.create_issue(title: \"Bug\")"

# Full URL
mcporter call https://api.example.com/mcp.fetch url:https://example.com

# Stdio (local server)
mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com

# JSON payload
mcporter call <server.tool> --args '{"limit":5}'
```

### Auth + config

```bash
mcporter auth <server | url> [--reset]    # OAuth auth
mcporter config list|get|add|remove|import|login|logout
```

### Daemon

```bash
mcporter daemon start|status|stop|restart
```

### Code generation

```bash
mcporter generate-cli --server <name>          # Generate CLI wrapper
mcporter generate-cli --command <url>
mcporter inspect-cli <path> [--json]           # Inspect generated CLI
mcporter emit-ts <server> --mode client|types  # TypeScript emit
```

### Notes
- Config default: `./config/mcporter.json` (override with `--config`).
- Prefer `--output json` for machine-readable results.

---

## voice-call — Voice Calls via OpenClaw Plugin

Start voice calls via the OpenClaw voice-call plugin (Twilio, Telnyx, Plivo, or mock).

**Requires:** `plugins.entries.voice-call.enabled` in config

### CLI

```bash
openclaw voicecall call --to "+15555550123" --message "Hello from OpenClaw"
openclaw voicecall status --call-id <id>
```

### Tool actions (`voice_call`)

- `initiate_call` (message, to?, mode?)
- `continue_call` (callId, message)
- `speak_to_user` (callId, message)
- `end_call` (callId)
- `get_status` (callId)

### Provider config (in `plugins.entries.voice-call.config`)

- **Twilio:** `provider: "twilio"` + `twilio.accountSid/authToken` + `fromNumber`
- **Telnyx:** `provider: "telnyx"` + `telnyx.apiKey/connectionId` + `fromNumber`
- **Plivo:** `provider: "plivo"` + `plivo.authId/authToken` + `fromNumber`
- **Dev fallback:** `provider: "mock"` (no network)

---

## ordercli — Foodora Order Tracking

Check past orders and track active order status on Foodora (Deliveroo WIP).

**Requires:** `ordercli`
**Install:** `brew install steipete/tap/ordercli` or `go install github.com/steipete/ordercli/cmd/ordercli@latest`
**Homepage:** https://ordercli.sh

### Quick start (Foodora)

```bash
ordercli foodora countries
ordercli foodora config set --country AT
ordercli foodora login --email you@example.com --password-stdin
ordercli foodora orders
ordercli foodora history --limit 20
ordercli foodora history show <orderCode>
```

### Orders

```bash
ordercli foodora orders                                   # Active list (arrival/status)
ordercli foodora orders --watch                           # Watch live
ordercli foodora order <orderCode>                        # Active order detail
ordercli foodora history show <orderCode> --json          # History detail JSON
```

### Reorder (adds to cart)

```bash
ordercli foodora reorder <orderCode>                      # Preview
ordercli foodora reorder <orderCode> --confirm            # Confirm
ordercli foodora reorder <orderCode> --confirm --address-id <id>
```

### Cloudflare / bot protection

```bash
ordercli foodora login --email you@example.com --password-stdin --browser
# Reuse browser profile:
ordercli foodora login --email you@example.com --password-stdin \
  --browser-profile "$HOME/Library/Application Support/ordercli/browser-profile"
# Import Chrome cookies:
ordercli foodora cookies chrome --profile "Default"
```

### Session import (no password)

```bash
ordercli foodora session chrome --url https://www.foodora.at/ --profile "Default"
ordercli foodora session refresh --client-id android
```

### Notes
- Use `--config /tmp/ordercli.json` for testing.
- Confirm before any reorder or cart-changing action.
- Deliveroo WIP: requires `DELIVEROO_BEARER_TOKEN` (optional `DELIVEROO_COOKIE`).

---

## nano-pdf — Natural-Language PDF Editing

Edit PDFs with natural-language instructions using the nano-pdf CLI.

**Requires:** `nano-pdf`
**Install:** `uv install nano-pdf`
**Homepage:** https://pypi.org/project/nano-pdf/

### Quick start

```bash
nano-pdf edit deck.pdf 1 "Change the title to 'Q3 Results' and fix the typo in the subtitle"
```

### Notes
- Page numbers may be 0-based or 1-based depending on the tool's version/config; if result is off by one, retry with the other.
- Always sanity-check the output PDF before sending it out.
