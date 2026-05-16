---
name: code-development
description: "Consolidated development toolkit: GitNexus code analysis (index/explore/debug/impact/PR review/refactor/wiki), local AI code review from diffs, skill creation/packaging, coding agent delegation (Codex/Claude Code/OpenCode/Pi via background processes), and safe external repo extraction. Use when: indexing or analyzing a codebase, tracing errors, understanding architecture, blast radius analysis, refactoring, reviewing PRs, creating/editing skills, delegating build tasks to coding agents, or extracting code from external repos safely."
---

# Code Development Toolkit

Unified skill covering all code analysis and development workflows:

| Section | When to Use |
|---------|-------------|
| [GitNexus - Code Analysis](#gitnexus---code-analysis) | Index repos, explore architecture, debug errors, impact analysis, safe refactoring, generate wikis |
| [Code Review](#code-review) | AI-structured review of local diffs, PR comments |
| [Skill Creator](#skill-creator) | Create, edit, tidy, review, or package SKILL.md files |
| [Coding Agent](#coding-agent-sub-process-delegation) | Delegate build/refactor/PR tasks to Codex, Claude Code, OpenCode, or Pi |
| [Khai Thác](#khai-thác---external-code-analysis) | Safely extract and reuse code from external repos |

---

## GitNexus - Code Analysis

### CLI Commands

All commands via `npx` — no global install needed:

```bash
npx gitnexus analyze          # Build/refresh the knowledge graph index
npx gitnexus analyze --force  # Force full re-index
npx gitnexus analyze --embeddings  # Enable semantic search
npx gitnexus status           # Check index freshness
npx gitnexus clean            # Delete the index (--force to skip prompt, --all for all repos)
npx gitnexus wiki             # Generate docs from the graph (requires API key)
npx gitnexus list             # List all indexed repos
```

**Wiki flags:** `--force`, `--model <model>`, `--base-url <url>`, `--api-key <key>`, `--concurrency <n>`, `--gist`

**When to run analyze:** First time in a project, after major code changes, or when context warns "Index is stale". In Claude Code, a PostToolUse hook runs it automatically after `git commit` / `git merge`.

**Troubleshooting:**
- "Not inside a git repository": Run from inside a git repo
- Stale after re-analyze: Restart Claude Code to reload MCP server
- Embeddings slow: Omit `--embeddings` or set `OPENAI_API_KEY`

---

### Always Start Here

For any code task (exploring, debugging, impact, refactoring):

1. `READ gitnexus://repo/{name}/context` — codebase overview + staleness check
2. Match task to workflow below
3. If stale → `npx gitnexus analyze` first

---

### Exploring Architecture

**Trigger:** "How does X work?", "Show me the auth flow", "What's the project structure?"

**Workflow:**
```
1. READ gitnexus://repos                            → Discover indexed repos
2. READ gitnexus://repo/{name}/context              → Overview, staleness
3. gitnexus_query({query: "<concept>"})             → Find execution flows
4. gitnexus_context({name: "<symbol>"})             → Deep dive a symbol
5. READ gitnexus://repo/{name}/process/{name}       → Full execution trace
6. Read source files for implementation details
```

**Checklist:**
- [ ] READ context resource
- [ ] gitnexus_query for the concept
- [ ] gitnexus_context on key symbols
- [ ] Read process resources for full traces

**Example — "How does payment processing work?"**
```
1. READ gitnexus://repo/my-app/context → 918 symbols, 45 processes
2. gitnexus_query({query: "payment processing"})
   → CheckoutFlow, RefundFlow
3. gitnexus_context({name: "processPayment"})
   → Incoming: checkoutHandler, webhookHandler
   → Outgoing: validateCard, chargeStripe, saveTransaction
4. Read src/payments/processor.ts
```

---

### Debugging Errors

**Trigger:** "Why is X failing?", "Trace this error", "This endpoint returns 500"

**Workflow:**
```
1. gitnexus_query({query: "<error or symptom>"})    → Find related flows
2. gitnexus_context({name: "<suspect>"})            → Callers/callees/processes
3. READ gitnexus://repo/{name}/process/{name}       → Trace execution
4. gitnexus_cypher({query: "MATCH path..."})        → Custom traces if needed
```

**Debugging Patterns:**

| Symptom | Approach |
|---------|----------|
| Error message | `gitnexus_query` for error text → `context` on throw sites |
| Wrong return value | `context` → trace callees for data flow |
| Intermittent failure | `context` → look for external calls, async deps |
| Performance issue | `context` → find symbols with many callers (hot paths) |
| Recent regression | `detect_changes` to see what changes affect |

**Example — "Payment endpoint returns 500 intermittently"**
```
1. gitnexus_query({query: "payment error handling"})
   → validatePayment, handlePaymentError
2. gitnexus_context({name: "validatePayment"})
   → Outgoing: verifyCard, fetchRates (external API!)
3. READ gitnexus://repo/my-app/process/CheckoutFlow
   → Step 3: validatePayment → calls fetchRates (external, no timeout)
4. Root cause: fetchRates missing timeout
```

---

### Impact Analysis

**Trigger:** "What breaks if I change X?", "Is it safe to change this?", "Blast radius?"

**Workflow:**
```
1. gitnexus_impact({target: "X", direction: "upstream"})   → What depends on this
2. READ gitnexus://repo/{name}/processes                    → Affected execution flows
3. gitnexus_detect_changes()                               → Pre-commit check
4. Assess risk and report
```

**Risk Levels:**

| Depth | Risk | Meaning |
|-------|------|---------|
| d=1 | **WILL BREAK** | Direct callers/importers |
| d=2 | LIKELY AFFECTED | Indirect dependencies |
| d=3 | MAY NEED TESTING | Transitive effects |

**Risk Assessment:**

| Affected | Risk |
|----------|------|
| <5 symbols, few processes | LOW |
| 5-15 symbols, 2-5 processes | MEDIUM |
| >15 symbols or many processes | HIGH |
| Critical path (auth, payments) | CRITICAL |

**Example:**
```
gitnexus_impact({target: "validateUser", direction: "upstream"})
→ d=1: loginHandler, apiMiddleware (WILL BREAK)
→ d=2: authRouter, sessionManager (LIKELY AFFECTED)
→ Risk: 2 direct callers, 2 processes = MEDIUM
```

---

### Refactoring

**Trigger:** "Rename this function", "Extract into a module", "Split this service", "Move to a new file"

**Workflow:**
```
1. gitnexus_impact({target: "X", direction: "upstream"})   → Map dependents
2. gitnexus_query({query: "X"})                            → Find execution flows
3. gitnexus_context({name: "X"})                           → All incoming/outgoing refs
4. Plan update order: interfaces → implementations → callers → tests
```

**Rename Symbol checklist:**
- [ ] `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` — preview
- [ ] Review graph edits (high confidence) and ast_search edits (review carefully)
- [ ] Apply: `gitnexus_rename({..., dry_run: false})`
- [ ] `gitnexus_detect_changes()` — verify only expected files changed
- [ ] Run tests for affected processes

**Extract Module checklist:**
- [ ] `gitnexus_context` — all incoming/outgoing refs
- [ ] `gitnexus_impact` upstream — external callers
- [ ] Define new module interface
- [ ] Extract code, update imports
- [ ] `gitnexus_detect_changes()` — verify scope
- [ ] Run tests for affected processes

**Risk Rules:**

| Risk Factor | Mitigation |
|-------------|------------|
| Many callers (>5) | Use gitnexus_rename for automated updates |
| Cross-area refs | detect_changes after to verify scope |
| String/dynamic refs | gitnexus_query to find them |
| External/public API | Version and deprecate properly |

**Example — Rename `validateUser` to `authenticateUser`:**
```
1. gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: true})
   → 12 edits: 10 graph (safe), 2 ast_search (review)
2. Review ast_search edits (config.json: dynamic reference!)
3. gitnexus_rename({..., dry_run: false}) → Applied 12 edits
4. gitnexus_detect_changes() → Affected: LoginFlow, TokenRefresh → run tests
```

---

### GitNexus Tools & Resources Reference

**MCP Tools:**

| Tool | What it gives you |
|------|------------------|
| `gitnexus_query` | Process-grouped flows related to a concept |
| `gitnexus_context` | 360° symbol view — callers, callees, processes |
| `gitnexus_impact` | Blast radius — dependents at depth 1/2/3 with confidence |
| `gitnexus_detect_changes` | Git-diff impact — what current changes affect |
| `gitnexus_rename` | Multi-file coordinated rename with confidence-tagged edits |
| `gitnexus_cypher` | Raw graph queries (read schema resource first) |
| `list_repos` | Discover indexed repos |

**MCP Resources (lightweight ~100-500 tokens):**

| Resource | Content |
|----------|---------|
| `gitnexus://repo/{name}/context` | Stats, staleness check |
| `gitnexus://repo/{name}/clusters` | Functional areas with cohesion scores |
| `gitnexus://repo/{name}/cluster/{name}` | Area members with file paths |
| `gitnexus://repo/{name}/processes` | All execution flows |
| `gitnexus://repo/{name}/process/{name}` | Step-by-step trace |
| `gitnexus://repo/{name}/schema` | Graph schema for Cypher queries |

**Graph Schema:**
- **Nodes:** File, Function, Class, Interface, Method, Community, Process
- **Edges (CodeRelation.type):** CALLS, IMPORTS, EXTENDS, IMPLEMENTS, DEFINES, MEMBER_OF, STEP_IN_PROCESS

```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: "myFunc"})
RETURN caller.name, caller.filePath
```

---

## Code Review

Generate structured PR/staged review feedback from local diffs — no GitHub auth required.

### Usage

```
/review <path>         # Review changes in path
/review <path> --post  # Post review (when GitHub available)
```

### What this does

1. **Reads diff/changes** from specified path
2. **Architectural review**: Questions design decisions, checks scope
3. **Analyzes changes**: security, testing, design patterns, code quality
4. **Generates structured feedback**: Specific suggestions with file/line references
5. **Educational focus**: Explains "why" behind each recommendation
6. **Balanced**: Acknowledges good practices alongside improvements

### Review checklist

- [ ] Architecture/design decisions aligned with project goals
- [ ] Security: input validation, secrets, permissions
- [ ] Testing: coverage, edge cases, integration
- [ ] Code quality: KISS, DRY, SOLID, YAGNI
- [ ] Dependencies: necessary? versions pinned?
- [ ] Documentation: README, comments, changelog

> Works fully local. No external API required. Uses OpenClaw built-in tools for file/diff analysis.

---

## Skill Creator

Create, edit, improve, tidy, review, audit, or restructure AgentSkills and SKILL.md files.

### Core Principles

- **Concise is key**: Context window is shared. Only add what Codex doesn't already know. Every token must justify its cost.
- **Default assumption**: Codex is smart. Challenge each sentence: "Does this justify its token cost?"
- **Progressive disclosure**: metadata (always) → SKILL.md body (on trigger) → bundled resources (as needed)

### Skill Structure

```
skill-name/
├── SKILL.md (required)
│   ├── YAML frontmatter: name + description (required)
│   └── Markdown instructions
└── Optional resources:
    ├── scripts/     # Executable code (Python/Bash)
    ├── references/  # Docs loaded into context as needed
    └── assets/      # Output files (templates, images, fonts)
```

**SKILL.md body:** Keep under 500 lines. Split to references/ when approaching limit.

**scripts/**: Use when the same code gets rewritten repeatedly or when deterministic reliability matters.

**references/**: For schemas, API docs, domain knowledge loaded only when needed. Prefer over SKILL.md body for detailed material.

**assets/**: Templates, images, fonts — not loaded into context, used in output.

**DO NOT create:** README.md, INSTALLATION_GUIDE.md, CHANGELOG.md, QUICK_REFERENCE.md — these are clutter.

### Creation Process

1. **Understand** the skill with concrete examples
2. **Plan** reusable contents (scripts, references, assets)
3. **Initialize**: `python scripts/init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets]`
4. **Edit** SKILL.md and add resources
5. **Package**: `python scripts/package_skill.py <path/to/skill-folder>`
6. **Iterate** based on real usage

### Writing SKILL.md

**Frontmatter:**
- `name`: hyphen-case, under 64 chars, verb-led preferred (e.g., `gh-address-comments`)
- `description`: primary trigger mechanism — include BOTH what it does AND when to use it. No "When to Use" section in body (body loads after trigger, so it won't help).

**Body:** Use imperative/infinitive form. Keep essential procedural instructions here; move detailed schemas/examples to references/.

### Progressive Disclosure Patterns

**Pattern 1 — High-level guide with references:**
```markdown
## Advanced features
- **Form filling**: See [FORMS.md](FORMS.md)
- **API reference**: See [REFERENCE.md](REFERENCE.md)
```

**Pattern 2 — Domain organization:** Separate references per domain (finance.md, sales.md) so only relevant context loads.

**Pattern 3 — Conditional details:** Show basics in SKILL.md, link to advanced files only when needed.

### Packaging

```bash
python scripts/package_skill.py <path/to/skill-folder>
python scripts/package_skill.py <path/to/skill-folder> ./dist
```

Packaging auto-validates: YAML frontmatter, naming conventions, description quality, file organization. Symlinks are rejected.

### Scripts location

`skills/skill-creator/` in the OpenClaw npm package contains:
- `init_skill.py` — Create new skill from template
- `package_skill.py` — Package skill → `.skill` file (zip)
- `quick_validate.py` — Quick validation check

---

## Coding Agent (Sub-process Delegation)

Delegate coding tasks to Codex, Claude Code, OpenCode, or Pi as background processes.

**Use for:** Building/creating features, reviewing PRs in temp clones, large refactors, iterative file exploration.
**NOT for:** Simple one-line fixes (just edit), reading code (use read tool), or any work in `~/.openclaw/` workspace.

### ⚠️ Critical Rules

1. **Always use `background:true`** — never foreground
2. **PTY mode:**
   - Codex / Pi / OpenCode: `pty:true` required
   - Claude Code: use `--print --permission-mode bypassPermissions` (NO PTY)
3. **Require completion notification** via `openclaw message send` — never rely on heartbeat or `openclaw system event`
4. **Never start Codex inside `~/.openclaw/`** — it'll read soul docs and behave strangely
5. **Never checkout branches in `~/Projects/openclaw/`** — that's the live OpenClaw instance
6. **Capture notify route before spawning**: channel, target, account, reply_to, thread_id

### Mandatory Pattern

Every run:
1. Capture notification route (channel, target, account, reply_to, thread_id)
2. Start CLI with `background:true`
3. Inject completion notification snippet into worker prompt
4. Monitor with `process action:log` / `poll`
5. If worker needs input or fails before notifying, handle explicitly

### Completion Prompt Snippet (inject in every worker prompt)

```text
Notification route for completion:
- channel: <notifyChannel>
- target: <notifyTarget>
- account: <notifyAccount or omit>
- reply_to: <notifyReplyTo or omit>
- thread_id: <notifyThreadId or omit>

When the task is completely finished, send exactly one completion message back to the user with:
  openclaw message send --channel <channel> --target '<target>' --message 'Done: <brief summary>'
If the task fails fatally, send one failure message instead.
Do not use openclaw system event. Do not rely on heartbeat.
```

### Codex

```bash
# Scratch work — create temp git repo first (Codex needs a trusted git dir)
SCRATCH=$(mktemp -d) && cd "$SCRATCH" && git init

# Build/create (background, PTY)
exec pty:true workdir:$SCRATCH background:true command:"codex exec --full-auto 'Your task here. <inject completion snippet>'"

# More autonomy
exec pty:true workdir:~/project background:true command:"codex --yolo 'Refactor the auth module. <inject completion snippet>'"
```

**Codex flags:** `exec "prompt"` (one-shot), `--full-auto` (sandboxed auto-approve), `--yolo` (no sandbox, no approvals)
**Default model:** `gpt-5.2-codex` (set in `~/.codex/config.toml`)

### Claude Code

```bash
exec workdir:~/project background:true command:"claude --permission-mode bypassPermissions --print 'Your task. <inject completion snippet>'"
```
No PTY. No `--dangerously-skip-permissions`.

### OpenCode

```bash
exec pty:true workdir:~/project background:true command:"opencode run 'Your task. <inject completion snippet>'"
```

### Pi Coding Agent

```bash
exec pty:true workdir:~/project background:true command:"pi 'Your task. <inject completion snippet>'"
exec pty:true workdir:~/project background:true command:"pi -p 'Non-interactive task'"
exec pty:true workdir:~/project background:true command:"pi --provider openai --model gpt-4o-mini -p 'Task'"
```

### PR Reviews

```bash
# Never review in OpenClaw's own project folder — always use temp clone or worktree
REVIEW_DIR=$(mktemp -d)
git clone https://github.com/user/repo.git $REVIEW_DIR
cd $REVIEW_DIR && gh pr checkout 130
exec pty:true workdir:$REVIEW_DIR background:true command:"codex review --base origin/main"

# Or worktree
git worktree add /tmp/pr-130-review pr-130-branch
exec pty:true workdir:/tmp/pr-130-review background:true command:"codex review --base main"
```

### Parallel Issues with git worktrees

```bash
git worktree add -b fix/issue-78 /tmp/issue-78 main
git worktree add -b fix/issue-99 /tmp/issue-99 main

exec pty:true workdir:/tmp/issue-78 background:true command:"codex --yolo 'Fix issue #78: <desc>. Commit and push. <inject completion snippet>'"
exec pty:true workdir:/tmp/issue-99 background:true command:"codex --yolo 'Fix issue #99: <desc>. Commit and push. <inject completion snippet>'"

process action:list
process action:log sessionId:XXX
```

### Process Tool Actions

| Action | Description |
|--------|-------------|
| `list` | List all running/recent sessions |
| `poll` | Check if session is still running |
| `log` | Get session output (offset/limit supported) |
| `write` | Send raw data to stdin |
| `submit` | Send data + newline (like typing Enter) |
| `send-keys` | Send key tokens or hex bytes |
| `paste` | Paste text (optional bracketed mode) |
| `kill` | Terminate the session |

### Progress Updates

- Send 1 short message when starting: what is running and where
- Update only when something changes: milestone, worker question, error, or finish
- If you kill a session, say why immediately
- If worker will self-notify via `openclaw message send`, say that clearly upfront

---

## Khai Thác - External Code Analysis

Safely review, extract, and reuse content from external directories/repos **without importing entire trees**.

Use when: reading before importing to E, taking only what's needed, avoiding duplicates, state pollution, config conflicts, or breaking the running system.

### Hard Rules

- ❌ Do NOT copy an entire repo/directory into E and figure it out later
- ❌ Do NOT overwrite active files without diff, backup, and clear purpose
- ❌ Do NOT import runtime state, caches, DBs, vector indexes, or auto-generated files into production
- ✅ Create minimal new files from selected content instead of copying whole clusters
- ✅ Follow: **inventory → read → select → build minimal candidate → isolated test → only then consider connecting to real system**

### Standard Process

**1) Inventory first**
- Count files/dirs and total size
- Build 2-3 level directory map
- Label each zone:
  - docs, config, executable/plugin, runtime state/data, vendor, examples/assets
- Flag for isolation: `.db`, `.sqlite`, `.pkl`, `.kuzu`, `.json` state files, `.cache`, `dist`, `build`, `node_modules`

**2) Read in hot-order**
1. README / architecture docs / limitations
2. Sample configs
3. Plugin manifest / install scripts
4. Execution entrypoints
5. Core logic
6. Vendor / generated / state (last)

**3) Select content to extract**

Choose one of three extraction types:
1. **Ideas/rules** → distill into a new file in E
2. **Sample config** → convert to minimal patch for existing config
3. **Useful source code** → copy individual files or blocks with intent; never bring a whole module unless needed

**4) Build minimal candidate in E**

- Place in a separate `review/candidate` directory, NOT connected to live runtime
- For small logic: extract to a new file
- For config: create the smallest possible diff/patch
- For state data: exclude unless specifically testing that state

**5) Check for conflicts**

Before bringing anything into E:
- Any filename conflicts?
- Does it overwrite active config/tool/plugin?
- Does it pull in ports/services/dependencies already running?
- Does it touch memory backend, auth, gateway, cron, or plugin hooks?

**6) Isolated test before connecting**

- Read/inspect/test in the candidate first
- Only connect to real config/runtime when it passes
- If restart risk exists, say so explicitly upfront

### Required Output

Always return:
- Short directory map
- High-risk zones
- Files worth extracting
- Files to leave behind
- Minimal import path to E
- Risks if connected directly

### Trigger Phrases

- "Extract safely from this directory"
- "Build map, read carefully, take only what's needed"
- "Don't bring the whole repo, just extract the useful parts"
- "Build a minimal candidate before importing to E"

---

## Quick Reference

| Task | Tool/Command |
|------|-------------|
| Index a repo | `npx gitnexus analyze` |
| Check index freshness | `npx gitnexus status` |
| Explore architecture | `gitnexus_query` + `gitnexus_context` |
| Debug an error | `gitnexus_query` for error text → `gitnexus_context` on suspect |
| Blast radius before change | `gitnexus_impact({target, direction: "upstream"})` |
| Pre-commit impact check | `gitnexus_detect_changes({scope: "staged"})` |
| Rename symbol everywhere | `gitnexus_rename({symbol_name, new_name, dry_run: true})` then apply |
| Generate wiki | `npx gitnexus wiki` |
| Review local diff | `/review <path>` |
| Create new skill | `python init_skill.py <name> --path <dir>` |
| Package skill | `python package_skill.py <skill-dir>` |
| Delegate build task | `exec pty:true background:true command:"codex exec --full-auto 'task'"` |
| PR review in temp dir | Clone → `exec pty:true background:true command:"codex review --base origin/main"` |
| Extract from external repo | Inventory → read → select → build candidate → test → connect |
