---
name: notes-knowledge
description: "Unified notes and knowledge management skill covering Notion (API), Obsidian (vault + obsidian-cli), Apple Notes, Bear Notes, and Apple Reminders."
---
# Notes & Knowledge Management

This skill covers all note-taking and knowledge management tools: Notion via REST API, Obsidian vaults via obsidian-cli and direct Markdown editing, Apple Notes, Bear Notes, and Apple Reminders.

---

## 1. Notion — Pages, Databases & Blocks

**Requires:** `NOTION_API_KEY` environment variable  
**Docs:** https://developers.notion.com

### Setup

1. Create an integration at https://notion.so/my-integrations
2. Copy the API key (starts with `ntn_` or `secret_`)
3. Store it:
```bash
mkdir -p ~/.config/notion
echo "ntn_your_key_here" > ~/.config/notion/api_key
```
4. Share target pages/databases with your integration: click "..." → "Connect to" → your integration name.

### API Basics

All requests need:
```bash
NOTION_KEY=$(cat ~/.config/notion/api_key)
curl -X GET "https://api.notion.com/v1/..." \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json"
```

> **Note:** `Notion-Version: 2025-09-03` header is required. In this version, databases are called "data sources" in the API.

### Common Operations

**Search for pages and data sources:**
```bash
curl -X POST "https://api.notion.com/v1/search" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"query": "page title"}'
```

**Get page:**
```bash
curl "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**Get page content (blocks):**
```bash
curl "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03"
```

**Create page in a data source (database):**
```bash
curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"database_id": "xxx"},
    "properties": {
      "Name": {"title": [{"text": {"content": "New Item"}}]},
      "Status": {"select": {"name": "Todo"}}
    }
  }'
```

**Query a data source:**
```bash
curl -X POST "https://api.notion.com/v1/data_sources/{data_source_id}/query" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"property": "Status", "select": {"equals": "Active"}},
    "sorts": [{"property": "Date", "direction": "descending"}]
  }'
```

**Create a data source (database):**
```bash
curl -X POST "https://api.notion.com/v1/data_sources" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "parent": {"page_id": "xxx"},
    "title": [{"text": {"content": "My Database"}}],
    "properties": {
      "Name": {"title": {}},
      "Status": {"select": {"options": [{"name": "Todo"}, {"name": "Done"}]}},
      "Date": {"date": {}}
    }
  }'
```

**Update page properties:**
```bash
curl -X PATCH "https://api.notion.com/v1/pages/{page_id}" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{"properties": {"Status": {"select": {"name": "Done"}}}}'
```

**Add blocks to page:**
```bash
curl -X PATCH "https://api.notion.com/v1/blocks/{page_id}/children" \
  -H "Authorization: Bearer $NOTION_KEY" \
  -H "Notion-Version: 2025-09-03" \
  -H "Content-Type: application/json" \
  -d '{
    "children": [
      {"object": "block", "type": "paragraph", "paragraph": {"rich_text": [{"text": {"content": "Hello"}}]}}
    ]
  }'
```

### Property Types

Common property formats for database items:
- **Title:** `{"title": [{"text": {"content": "..."}}]}`
- **Rich text:** `{"rich_text": [{"text": {"content": "..."}}]}`
- **Select:** `{"select": {"name": "Option"}}`
- **Multi-select:** `{"multi_select": [{"name": "A"}, {"name": "B"}]}`
- **Date:** `{"date": {"start": "2024-01-15", "end": "2024-01-16"}}`
- **Checkbox:** `{"checkbox": true}`
- **Number:** `{"number": 42}`
- **URL:** `{"url": "https://..."}`
- **Email:** `{"email": "a@b.com"}`
- **Relation:** `{"relation": [{"id": "page_id"}]}`

### Key Differences in API version 2025-09-03

- **Databases → Data Sources:** Use `/data_sources/` endpoints for queries and retrieval
- **Two IDs:** Each database has both a `database_id` and a `data_source_id`
  - Use `database_id` when creating pages (`parent: {"database_id": "..."}`)
  - Use `data_source_id` when querying (`POST /v1/data_sources/{id}/query`)
- **Search results:** Databases return as `"object": "data_source"` with their `data_source_id`
- **Parent in responses:** Pages show `parent.data_source_id` alongside `parent.database_id`

### Rate Limits & Limits

- Rate limit: ~3 requests/second average; `429 rate_limited` uses `Retry-After`
- Append block children: up to 100 children per request, up to 2 nesting levels per append
- Payload size: up to 1000 block elements and 500KB overall
- Use `is_inline: true` when creating data sources embedded in pages
- The API cannot set database view filters (UI-only)

---

## 2. Obsidian — Markdown Vault

**Requires:** `obsidian-cli` binary  
**Install:** `brew install yakitrak/yakitrak/obsidian-cli`  
**Docs:** https://help.obsidian.md

### Vault Structure

An Obsidian vault is a normal folder on disk:
- Notes: `*.md` (plain Markdown; edit with any editor)
- Config: `.obsidian/` (workspace + plugin settings — don't touch from scripts)
- Canvases: `*.canvas` (JSON)
- Attachments: configured in Obsidian settings

### Find Active Vault(s)

Obsidian desktop tracks vaults at:  
`~/Library/Application Support/obsidian/obsidian.json`

```bash
# If a default is set:
obsidian-cli print-default --path-only

# Otherwise read the config and use the vault entry with "open": true
```

> Do not hardcode vault paths in scripts. Read config or use `print-default`.

### obsidian-cli Quick Start

```bash
# Set a default vault (once)
obsidian-cli set-default "<vault-folder-name>"

# Print default vault info
obsidian-cli print-default
obsidian-cli print-default --path-only

# Search note names
obsidian-cli search "query"

# Search note contents (shows snippets + line numbers)
obsidian-cli search-content "query"

# Create a new note
obsidian-cli create "Folder/New note" --content "..." --open

# Move / rename a note (updates wikilinks and Markdown links across vault)
obsidian-cli move "old/path/note" "new/path/note"

# Delete a note
obsidian-cli delete "path/note"
```

**Notes:**
- Direct file edits (open `.md` and edit) work fine; Obsidian picks up changes automatically.
- Avoid creating notes in hidden dot-folders via URI; Obsidian may refuse them.
- `obsidian-cli move` is the safe way to rename/move notes — it updates all internal links.

---

## 3. Apple Notes

**Description:** Manage notes in Apple's Notes app on macOS and iOS. Integration is via AppleScript on macOS.

**Requirements:** macOS with Notes app. No third-party CLI required for basic operations.

### Common AppleScript Operations

**Create a note:**
```applescript
tell application "Notes"
  tell account "iCloud"
    make new note at folder "Notes" with properties {name: "My Note", body: "Note content here"}
  end tell
end tell
```

**Search notes:**
```applescript
tell application "Notes"
  set matchingNotes to notes whose name contains "search term"
  repeat with n in matchingNotes
    log name of n
  end repeat
end tell
```

**Append to a note:**
```applescript
tell application "Notes"
  set targetNote to first note whose name is "My Note"
  set body of targetNote to (body of targetNote) & "<br>Appended content"
end tell
```

**Notes:**
- Notes body is HTML; use `<br>` for line breaks, `<b>` for bold, etc.
- Use `osascript -e '...'` or an `.applescript` file to run from CLI.
- iCloud vs local accounts: specify `account "iCloud"` or `account "On My Mac"`.

---

## 4. Bear Notes

**Description:** Bear is a Markdown note-taking app for macOS and iOS. It supports x-callback-url and a CLI via the `bear` scheme for automation.

**Requirements:** Bear app installed on macOS.

### Bear x-callback-url Actions (via `open` command)

```bash
# Create a new note
open "bear://x-callback-url/create?title=My%20Note&text=Content%20here"

# Open/search notes
open "bear://x-callback-url/search?term=keyword"

# Add text to existing note by title
open "bear://x-callback-url/add-text?title=My%20Note&text=Appended%20text"

# Open a specific note by ID
open "bear://x-callback-url/open-note?id=NOTE-ID"
```

**Notes:**
- URL-encode all parameters (spaces → `%20`, newlines → `%0A`).
- Bear supports tags: add `#tag` in note text to tag notes.
- Export notes via File → Export in the app UI (no CLI export).
- Bear Pro required for export and sync features.

---

## 5. Apple Reminders

**Description:** Manage reminders and to-do lists in Apple's Reminders app on macOS and iOS. Accessible via AppleScript on macOS.

**Requirements:** macOS with Reminders app.

### Common AppleScript Operations

**Create a reminder:**
```applescript
tell application "Reminders"
  tell list "Reminders"
    make new reminder with properties {name: "Buy groceries", due date: date "Thursday, June 1, 2024 at 9:00 AM"}
  end tell
end tell
```

**List all reminders:**
```applescript
tell application "Reminders"
  set incompleteReminders to reminders whose completed is false
  repeat with r in incompleteReminders
    log name of r
  end repeat
end tell
```

**Complete a reminder:**
```applescript
tell application "Reminders"
  set r to first reminder whose name is "Buy groceries"
  set completed of r to true
end tell
```

**List reminder lists:**
```applescript
tell application "Reminders"
  set allLists to name of every list
  log allLists
end tell
```

**Notes:**
- Use `osascript -e '...'` or an `.applescript` file to run AppleScript from CLI.
- iCloud sync: reminders sync across devices when iCloud Reminders is enabled.
- Supports due dates, priorities (0–9), and recurring reminders via the app UI.
