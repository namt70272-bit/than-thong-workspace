---
name: communication
description: "Unified communication skill covering email (Himalaya IMAP/SMTP, Gmail/Google Workspace via gog), Discord, Slack, BlueBubbles, iMessage, WhatsApp (wacli), and Twitter/X (xurl)."
---
# Communication

This skill covers all messaging and communication channels: IMAP/SMTP email via Himalaya CLI, Google Workspace (Gmail/Calendar/Drive/Contacts/Sheets/Docs) via gog, Discord, Slack, BlueBubbles, iMessage, WhatsApp (wacli), and Twitter/X (xurl).

---

## 1. Himalaya — IMAP/SMTP Email CLI

**Requires:** `himalaya` binary  
**Install:** `brew install himalaya`  
**Docs:** https://github.com/pimalaya/himalaya

### Configuration Setup

Run interactive wizard:
```bash
himalaya account configure
```

Or create `~/.config/himalaya/config.toml` manually:
```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"
```

### Common Operations

**List folders:**
```bash
himalaya folder list
```

**List emails:**
```bash
himalaya envelope list
himalaya envelope list --folder "Sent"
himalaya envelope list --page 1 --page-size 20
```

**Search emails:**
```bash
himalaya envelope list from john@example.com subject meeting
```

**Read an email:**
```bash
himalaya message read 42
himalaya message export 42 --full   # raw MIME
```

**Reply / forward:**
```bash
himalaya message reply 42
himalaya message reply 42 --all
himalaya message forward 42
```

**Write new email:**
```bash
himalaya message write
# Or send directly:
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

**Move / copy / delete:**
```bash
himalaya message move 42 "Archive"
himalaya message copy 42 "Important"
himalaya message delete 42
```

**Flags:**
```bash
himalaya flag add 42 --flag seen
himalaya flag remove 42 --flag seen
```

**Attachments:**
```bash
himalaya attachment download 42
himalaya attachment download 42 --dir ~/Downloads
```

**Multiple accounts:**
```bash
himalaya account list
himalaya --account work envelope list
```

**Output format:**
```bash
himalaya envelope list --output json
himalaya envelope list --output plain
```

**Debug:**
```bash
RUST_LOG=debug himalaya envelope list
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

---

## 2. gog — Google Workspace CLI

**Requires:** `gog` binary  
**Install:** `brew install steipete/tap/gogcli`  
**Docs:** https://gogcli.sh

### Auth Setup (once)
```bash
gog auth credentials /path/to/client_secret.json
gog auth add you@gmail.com --services gmail,calendar,drive,contacts,docs,sheets
gog auth list
```
Set default account: `export GOG_ACCOUNT=you@gmail.com`

### Gmail

```bash
# Search (by thread)
gog gmail search 'newer_than:7d' --max 10

# Search (per message, not thread)
gog gmail messages search "in:inbox from:ryanair.com" --max 20 --account you@example.com

# Send plain text
gog gmail send --to a@b.com --subject "Hi" --body "Hello"

# Send multi-line (body-file or stdin)
gog gmail send --to a@b.com --subject "Hi" --body-file ./message.txt
gog gmail send --to a@b.com --subject "Hi" --body-file -

# Send HTML
gog gmail send --to a@b.com --subject "Hi" --body-html "<p>Hello</p>"

# Draft
gog gmail drafts create --to a@b.com --subject "Hi" --body-file ./message.txt
gog gmail drafts send <draftId>

# Reply
gog gmail send --to a@b.com --subject "Re: Hi" --body "Reply" --reply-to-message-id <msgId>
```

**Email formatting tips:**
- Prefer plain text. Use `--body-file` for multi-paragraph messages.
- `--body` does not unescape `\n`. Use heredoc or `$'Line 1\n\nLine 2'` for inline newlines.
- HTML tags: `<p>`, `<br>`, `<strong>`, `<em>`, `<a href="url">`, `<ul>/<li>`

**Plain text via stdin example:**
```bash
gog gmail send --to recipient@example.com \
  --subject "Meeting Follow-up" \
  --body-file - <<'EOF'
Hi Name,

Thanks for meeting today. Next steps:
- Item one
- Item two

Best regards,
Your Name
EOF
```

### Calendar

```bash
gog calendar events <calendarId> --from <iso> --to <iso>
gog calendar create <calendarId> --summary "Title" --from <iso> --to <iso>
gog calendar create <calendarId> --summary "Title" --from <iso> --to <iso> --event-color 7
gog calendar update <calendarId> <eventId> --summary "New Title" --event-color 4
gog calendar colors
```

**Calendar color IDs (from `gog calendar colors`):**
- 1: #a4bdfc  2: #7ae7bf  3: #dbadff  4: #ff887c  5: #fbd75b  6: #ffb878
- 7: #46d6db  8: #e1e1e1  9: #5484ed  10: #51b749  11: #dc2127

### Drive & Contacts

```bash
gog drive search "query" --max 10
gog contacts list --max 20
```

### Sheets

```bash
gog sheets get <sheetId> "Tab!A1:D10" --json
gog sheets update <sheetId> "Tab!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED
gog sheets append <sheetId> "Tab!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS
gog sheets clear <sheetId> "Tab!A2:Z"
gog sheets metadata <sheetId> --json
```

### Docs

```bash
gog docs export <docId> --format txt --out /tmp/doc.txt
gog docs cat <docId>
```

**Notes:**
- Confirm before sending mail or creating events.
- For scripting, prefer `--json` plus `--no-input`.
- `gog gmail search` = one row per thread; use `gog gmail messages search` for individual emails.

---

## 3. Discord

**Requires:** `channels.discord.token` in OpenClaw config  
**Tool:** Use the `message` tool with `channel: "discord"`

### Key Rules
- Always set `"channel": "discord"` on every action.
- Respect gating: `channels.discord.actions.*` (roles, moderation, presence, channels may be off by default).
- Prefer explicit IDs: `guildId`, `channelId`, `messageId`, `userId`.
- Multi-account: use optional `accountId`.
- No Markdown tables in Discord messages.
- Mention users as `<@USER_ID>`.
- Prefer Discord components v2 (`components`) for rich UI; use legacy `embeds` only when required.
- Do NOT combine `components` with `embeds`.

### Send / Read

**Send message:**
```json
{
  "action": "send",
  "channel": "discord",
  "to": "channel:123",
  "message": "hello",
  "silent": true
}
```

**Send with attachment:**
```json
{
  "action": "send",
  "channel": "discord",
  "to": "channel:123",
  "message": "see attachment",
  "media": "file:///tmp/example.png"
}
```

**Send with components v2 (rich UI):**
```json
{
  "action": "send",
  "channel": "discord",
  "to": "channel:123",
  "message": "Status update",
  "components": "[Carbon v2 components]"
}
```

**Read messages:**
```json
{
  "action": "read",
  "channel": "discord",
  "to": "channel:123",
  "limit": 20
}
```

### Edit / Delete / React

```json
{ "action": "edit", "channel": "discord", "channelId": "123", "messageId": "456", "message": "fixed typo" }
{ "action": "delete", "channel": "discord", "channelId": "123", "messageId": "456" }
{ "action": "react", "channel": "discord", "channelId": "123", "messageId": "456", "emoji": "✅" }
```

### Polls, Pins, Threads, Search

**Poll:**
```json
{
  "action": "poll",
  "channel": "discord",
  "to": "channel:123",
  "pollQuestion": "Lunch?",
  "pollOption": ["Pizza", "Sushi", "Salad"],
  "pollMulti": false,
  "pollDurationHours": 24
}
```

**Pin:**
```json
{ "action": "pin", "channel": "discord", "channelId": "123", "messageId": "456" }
```

**Create thread:**
```json
{ "action": "thread-create", "channel": "discord", "channelId": "123", "messageId": "456", "threadName": "bug triage" }
```

**Search:**
```json
{
  "action": "search",
  "channel": "discord",
  "guildId": "999",
  "query": "release notes",
  "channelIds": ["123", "456"],
  "limit": 10
}
```

**Set presence (gated):**
```json
{ "action": "set-presence", "channel": "discord", "activityType": "playing", "activityName": "with fire", "status": "online" }
```

---

## 4. Slack

**Requires:** `channels.slack` configured in OpenClaw  
**Tool:** Use the `slack` tool (or `message` tool with Slack channel)

### Action Groups

| Action group | Default | Notes                  |
|-------------|---------|------------------------|
| reactions   | enabled | React + list reactions |
| messages    | enabled | Read/send/edit/delete  |
| pins        | enabled | Pin/unpin/list         |
| memberInfo  | enabled | Member info            |
| emojiList   | enabled | Custom emoji list      |

### Message Operations

**Send:**
```json
{ "action": "sendMessage", "to": "channel:C123", "content": "Hello from OpenClaw" }
```

**Read recent:**
```json
{ "action": "readMessages", "channelId": "C123", "limit": 20 }
```

**Edit:**
```json
{ "action": "editMessage", "channelId": "C123", "messageId": "1712023032.1234", "content": "Updated text" }
```

**Delete:**
```json
{ "action": "deleteMessage", "channelId": "C123", "messageId": "1712023032.1234" }
```

### Reactions

```json
{ "action": "react", "channelId": "C123", "messageId": "1712023032.1234", "emoji": "✅" }
{ "action": "reactions", "channelId": "C123", "messageId": "1712023032.1234" }
```

### Pins

```json
{ "action": "pinMessage", "channelId": "C123", "messageId": "1712023032.1234" }
{ "action": "unpinMessage", "channelId": "C123", "messageId": "1712023032.1234" }
{ "action": "listPins", "channelId": "C123" }
```

### Member Info & Emoji

```json
{ "action": "memberInfo", "userId": "U123" }
{ "action": "emojiList" }
```

**Notes:**
- `messageId` in Slack = timestamp, e.g. `1712023032.1234`
- React with ✅ to mark completed tasks; pin key decisions or weekly status updates.

---

## 5. BlueBubbles (iMessage via BlueBubbles server)

**Description:** Interact with iMessage through a running BlueBubbles server instance. Enables sending and reading iMessages from non-Apple devices or remote machines.

**Requirements:**
- BlueBubbles server running on a Mac
- BlueBubbles server URL and password configured in OpenClaw channels config (`channels.bluebubbles`)

**Typical actions** (via `message` tool with `channel: "bluebubbles"`):
- Send iMessage to a phone number or Apple ID
- Read recent messages from a chat
- List conversations

---

## 6. iMessage (imsg)

**Description:** Send and receive iMessages directly on macOS using the `imsg` CLI tool or AppleScript integration. Works natively on Mac without a BlueBubbles server.

**Requirements:**
- macOS with Messages app
- `imsg` binary or AppleScript access

**Typical usage:**
- Send iMessage: `imsg send --to "+15551234567" --body "Hello"`
- Read recent messages from a conversation

---

## 7. WhatsApp (wacli)

**Description:** Send and receive WhatsApp messages via `wacli`, a CLI tool that interfaces with WhatsApp Web protocol.

**Requirements:**
- `wacli` binary installed
- WhatsApp account linked (scan QR code on first run)

**Typical commands:**
- `wacli send --to "+15551234567" --message "Hello from CLI"`
- `wacli list-chats`
- `wacli history --contact "+15551234567" --limit 20`

---

## 8. Twitter/X (xurl)

**Description:** Post tweets, read timelines, search tweets, and manage Twitter/X interactions via `xurl` CLI.

**Requirements:**
- `xurl` binary installed
- Twitter/X API credentials configured (OAuth tokens)

**Typical commands:**
- Post tweet: `xurl tweet --text "Hello from CLI"`
- Read timeline: `xurl timeline --limit 20`
- Search: `xurl search --query "keyword" --limit 10`
- Reply: `xurl reply --to <tweet_id> --text "My reply"`
