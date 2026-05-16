---
name: utilities
description: "Utility tools: weather forecasts (wttr.in), Trello board/card management, GitHub issues/PR/CI via gh CLI, gh-issues auto-fix orchestrator, and Things 3 todos on macOS."
---

# Utilities

Consolidated skill covering five tools: **weather** (wttr.in forecasts), **trello** (REST API board/card management), **github** (gh CLI for PRs/issues/CI), **gh-issues** (auto-fix GitHub issues with sub-agents), and **things-mac** (Things 3 todos on macOS).

---

## Part 1 — Weather

Get current weather conditions and forecasts. Uses wttr.in — no API key required.

### Requirements
- Binary: `curl`
- Install: `brew install curl`

### When to Use

✅ Use for: current conditions, rain forecasts, temperature, week forecast, travel weather checks.

❌ Don't use for: historical weather data, climate analysis, hyper-local microclimate, aviation/marine weather (use METAR etc.).

### Commands

**Current weather:**
```bash
# One-line summary
curl "wttr.in/London?format=3"

# Detailed current conditions
curl "wttr.in/London?0"

# Specific city
curl "wttr.in/New+York?format=3"
```

**Forecasts:**
```bash
# 3-day forecast
curl "wttr.in/London"

# Week forecast
curl "wttr.in/London?format=v2"

# Specific day (0=today, 1=tomorrow, 2=day after)
curl "wttr.in/London?1"
```

**Format options:**
```bash
# One-liner with multiple fields
curl "wttr.in/London?format=%l:+%c+%t+%w"

# JSON output
curl "wttr.in/London?format=j1"

# PNG image
curl "wttr.in/London.png"
```

**Format codes:** `%c` condition emoji · `%t` temperature · `%f` feels like · `%w` wind · `%h` humidity · `%p` precipitation · `%l` location

**Quick responses:**
```bash
# "What's the weather?"
curl -s "wttr.in/London?format=%l:+%c+%t+(feels+like+%f),+%w+wind,+%h+humidity"

# "Will it rain?"
curl -s "wttr.in/London?format=%l:+%c+%p"

# "Weekend forecast"
curl "wttr.in/London?format=v2"
```

### Notes
- No API key needed (uses wttr.in)
- Rate limited; don't spam requests
- Supports airport codes: `curl wttr.in/ORD`

---

## Part 2 — Trello

Manage Trello boards, lists, and cards via the Trello REST API.

### Requirements
- Binary: `jq`
- Env vars: `TRELLO_API_KEY`, `TRELLO_TOKEN`
- Install: `brew install jq`
- Homepage: https://developer.atlassian.com/cloud/trello/rest/

### Setup

1. Get your API key: https://trello.com/app-key
2. Generate a token (click "Token" link on that page)
3. Set environment variables:
   ```bash
   export TRELLO_API_KEY="your-api-key"
   export TRELLO_TOKEN="your-token"
   ```

### Commands

**List boards:**
```bash
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

**List lists in a board:**
```bash
curl -s "https://api.trello.com/1/boards/{boardId}/lists?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id}'
```

**List cards in a list:**
```bash
curl -s "https://api.trello.com/1/lists/{listId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, id, desc}'
```

**Create a card:**
```bash
curl -s -X POST "https://api.trello.com/1/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={listId}" \
  -d "name=Card Title" \
  -d "desc=Card description"
```

**Move a card to another list:**
```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "idList={newListId}"
```

**Add a comment to a card:**
```bash
curl -s -X POST "https://api.trello.com/1/cards/{cardId}/actions/comments?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "text=Your comment here"
```

**Archive a card:**
```bash
curl -s -X PUT "https://api.trello.com/1/cards/{cardId}?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" \
  -d "closed=true"
```

### Examples

```bash
# Get all boards
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN&fields=name,id" | jq

# Find a specific board by name
curl -s "https://api.trello.com/1/members/me/boards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | select(.name | contains("Work"))'

# Get all cards on a board
curl -s "https://api.trello.com/1/boards/{boardId}/cards?key=$TRELLO_API_KEY&token=$TRELLO_TOKEN" | jq '.[] | {name, list: .idList}'
```

### Notes
- Board/List/Card IDs can be found in the Trello URL or via the list commands
- API key and token provide full access to your account — keep them secret!
- Rate limits: 300 requests per 10 seconds per API key; 100 requests per 10 seconds per token; `/1/members` limited to 100 requests per 900 seconds

---

## Part 3 — GitHub (gh CLI)

Use the `gh` CLI to interact with GitHub repositories, issues, PRs, and CI.

### Requirements
- Binary: `gh`
- Install: `brew install gh` or `apt install gh`

### When to Use

✅ Use for: PR status/reviews/merge readiness, CI/workflow run status and logs, creating/closing/commenting on issues, creating/merging PRs, querying GitHub API for repo data, listing repos/releases/collaborators.

❌ Don't use for: local git operations (commit, push, pull, branch) → use `git` directly; non-GitHub repos; cloning → use `git clone`; reviewing actual code changes → use `coding-agent`.

### Setup

```bash
# Authenticate (one-time)
gh auth login

# Verify
gh auth status
```

### Common Commands

**Pull Requests:**
```bash
# List PRs
gh pr list --repo owner/repo

# Check CI status
gh pr checks 55 --repo owner/repo

# View PR details
gh pr view 55 --repo owner/repo

# Create PR
gh pr create --title "feat: add feature" --body "Description"

# Merge PR
gh pr merge 55 --squash --repo owner/repo
```

**Issues:**
```bash
# List issues
gh issue list --repo owner/repo --state open

# Create issue
gh issue create --title "Bug: something broken" --body "Details..."

# Close issue
gh issue close 42 --repo owner/repo
```

**CI/Workflow Runs:**
```bash
# List recent runs
gh run list --repo owner/repo --limit 10

# View specific run
gh run view <run-id> --repo owner/repo

# View failed step logs only
gh run view <run-id> --repo owner/repo --log-failed

# Re-run failed jobs
gh run rerun <run-id> --failed --repo owner/repo
```

**API Queries:**
```bash
# Get PR with specific fields
gh api repos/owner/repo/pulls/55 --jq '.title, .state, .user.login'

# List all labels
gh api repos/owner/repo/labels --jq '.[].name'

# Get repo stats
gh api repos/owner/repo --jq '{stars: .stargazers_count, forks: .forks_count}'
```

### JSON Output

```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
gh pr list --json number,title,state,mergeable --jq '.[] | select(.mergeable == "MERGEABLE")'
```

### Templates

**PR Review Summary:**
```bash
PR=55 REPO=owner/repo
echo "## PR #$PR Summary"
gh pr view $PR --repo $REPO --json title,body,author,additions,deletions,changedFiles \
  --jq '"**\(.title)** by @\(.author.login)\n\n\(.body)\n\n📊 +\(.additions) -\(.deletions) across \(.changedFiles) files"'
gh pr checks $PR --repo $REPO
```

**Issue Triage:**
```bash
gh issue list --repo owner/repo --state open --json number,title,labels,createdAt \
  --jq '.[] | "[\(.number)] \(.title) - \([.labels[].name] | join(", ")) (\(.createdAt[:10]))"'
```

### Notes
- Always specify `--repo owner/repo` when not in a git directory
- Use URLs directly: `gh pr view https://github.com/owner/repo/pull/55`
- Rate limits apply; use `gh api --cache 1h` for repeated queries

---

## Part 4 — gh-issues (Auto-Fix GitHub Issues with Parallel Sub-agents)

Fetch GitHub issues, delegate fixes to sub-agents, open PRs, and watch for review comments. Uses curl + GitHub REST API exclusively (not the `gh` CLI).

### Requirements
- Binaries: `curl`, `git`, `gh`
- Env var: `GH_TOKEN` (injected by OpenClaw)
- Install: `brew install gh`

### Invocation

```
/gh-issues [owner/repo] [flags]
```

**Flags:**
| Flag | Default | Description |
|------|---------|-------------|
| `--label` | _(none)_ | Filter by label (e.g. `bug`) |
| `--limit` | 10 | Max issues to fetch per poll |
| `--state` | open | Issue state: open, closed, all |
| `--fork` | _(none)_ | Fork repo to push branches to |
| `--watch` | false | Keep polling for new issues |
| `--interval` | 5 | Minutes between polls (with `--watch`) |
| `--dry-run` | false | Fetch and display only — no sub-agents |
| `--yes` | false | Skip confirmation |
| `--reviews-only` | false | Only handle PR review comments |
| `--cron` | false | Fire-and-forget cron-safe mode |
| `--model` | _(none)_ | Model for sub-agents (e.g. `glm-5`) |
| `--notify-channel` | _(none)_ | Telegram channel ID for final PR summary |

### API Auth Pattern

```bash
curl -s -H "Authorization: Bearer $GH_TOKEN" -H "Accept: application/vnd.github+json" ...
```

### Phases

1. **Parse Arguments** — detect `owner/repo` from git remote if omitted
2. **Fetch Issues** — GitHub Issues API, filter out pull requests
3. **Present & Confirm** — markdown table, user confirmation (unless `--yes`)
4. **Pre-flight Checks** — dirty tree, base branch, remote access, existing PRs/branches
5. **Spawn Sub-agents** — parallel (up to 8), each fixes one issue, commits, pushes, opens PR
6. **PR Review Handler** — check open `fix/issue-*` PRs for review comments, spawn fix sub-agents

### Examples

```bash
# Dry run: see what issues would be processed
/gh-issues owner/repo --dry-run

# Auto-process all open bug issues
/gh-issues owner/repo --label bug --yes

# Watch mode: poll every 5 minutes
/gh-issues owner/repo --watch --interval 5

# Cron mode: fire-and-forget one issue at a time
/gh-issues owner/repo --cron

# Only handle review comments on open PRs
/gh-issues owner/repo --reviews-only
```

---

## Part 5 — Things 3 (macOS)

Add, update, list, search, or inspect Things 3 todos, inbox, today, projects, areas, and tags on macOS.

### Requirements
- Binary: `things` (things3-cli)
- OS: macOS only
- Install: `GOBIN=/opt/homebrew/bin go install github.com/ossianhempel/things3-cli/cmd/things@latest`
- Homepage: https://github.com/ossianhempel/things3-cli

### Setup

- If DB reads fail: grant **Full Disk Access** to the calling app (Terminal or `OpenClaw.app`).
- Optional: set `THINGSDB` (or pass `--db`) to point at your `ThingsData-*` folder.
- Optional: set `THINGS_AUTH_TOKEN` to avoid passing `--auth-token` for update ops.

### Read-Only (DB)

```bash
things inbox --limit 50
things today
things upcoming
things search "query"
things projects
things areas
things tags
```

### Write (URL Scheme)

```bash
# Safe preview (prints URL, does not open Things)
things --dry-run add "Title"

# Add basic todo
things add "Buy milk"

# Add with notes
things add "Buy milk" --notes "2% + bananas"

# Add to a project/area
things add "Book flights" --list "Travel"

# Add to a project heading
things add "Pack charger" --list "Travel" --heading "Before"

# Add with tags
things add "Call dentist" --tags "health,phone"

# Add with checklist
things add "Trip prep" --checklist-item "Passport" --checklist-item "Tickets"

# Add with deadline
things add "Submit report" --when today --deadline 2026-01-02

# Bring Things to front
things --foreground add "Title"

# From STDIN (multi-line => title + notes)
cat <<'EOF' | things add -
Title line
Notes line 1
Notes line 2
EOF
```

### Modify a Todo (Needs Auth Token)

```bash
# Get the ID (UUID column) first
things search "milk" --limit 5

# Update title
things update --id <UUID> --auth-token <TOKEN> "New title"

# Replace notes
things update --id <UUID> --auth-token <TOKEN> --notes "New notes"

# Append/prepend notes
things update --id <UUID> --auth-token <TOKEN> --append-notes "..."
things update --id <UUID> --auth-token <TOKEN> --prepend-notes "..."

# Move to list/heading
things update --id <UUID> --auth-token <TOKEN> --list "Travel" --heading "Before"

# Replace or add tags
things update --id <UUID> --auth-token <TOKEN> --tags "a,b"
things update --id <UUID> --auth-token <TOKEN> --add-tags "a,b"

# Complete or cancel
things update --id <UUID> --auth-token <TOKEN> --completed
things update --id <UUID> --auth-token <TOKEN> --canceled

# Safe preview
things --dry-run update --id <UUID> --auth-token <TOKEN> --completed
```

### Delete a Todo?

Not supported by `things3-cli` (no delete/trash write command; `things trash` is read-only).
Options: use Things UI to delete/trash, or mark as `--completed` / `--canceled` via `things update`.

### Notes
- macOS-only
- `--dry-run` prints the URL and does not open Things
