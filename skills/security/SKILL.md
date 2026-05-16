---
name: security
description: "Secrets and credential management via 1Password CLI (op). Sign in, read/inject secrets, and manage vaults securely."
---
# Security — 1Password CLI

Use the 1Password CLI (`op`) to sign in, read secrets, inject credentials into processes, and manage vaults.

**Requires:** `op` binary  
**Install:** `brew install 1password-cli`  
**Docs:** https://developer.1password.com/docs/cli/get-started/

---

## References

- `references/get-started.md` — install + app integration + sign-in flow
- `references/cli-examples.md` — real `op` examples

---

## Workflow

1. Check OS + shell.
2. Verify CLI present: `op --version`
3. Confirm desktop app integration is enabled (per get-started) and the app is unlocked.
4. **REQUIRED:** Create a fresh tmux session for all `op` commands (no direct `op` calls outside tmux).
5. Sign in / authorize inside tmux: `op signin` (expect app prompt).
6. Verify access inside tmux: `op whoami` (must succeed before any secret read).
7. If multiple accounts: use `--account` or `OP_ACCOUNT`.

---

## REQUIRED tmux Session (T-Max)

The shell tool uses a fresh TTY per command. To avoid re-prompts and failures, always run `op` inside a dedicated tmux session with a fresh socket/session name.

```bash
SOCKET_DIR="${OPENCLAW_TMUX_SOCKET_DIR:-${TMPDIR:-/tmp}/openclaw-tmux-sockets}"
mkdir -p "$SOCKET_DIR"
SOCKET="$SOCKET_DIR/openclaw-op.sock"
SESSION="op-auth-$(date +%Y%m%d-%H%M%S)"

tmux -S "$SOCKET" new -d -s "$SESSION" -n shell
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op signin --account my.1password.com" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op whoami" Enter
tmux -S "$SOCKET" send-keys -t "$SESSION":0.0 -- "op vault list" Enter
tmux -S "$SOCKET" capture-pane -p -J -t "$SESSION":0.0 -S -200
tmux -S "$SOCKET" kill-session -t "$SESSION"
```

---

## Common `op` Commands

```bash
# Check CLI version
op --version

# Sign in
op signin
op signin --account my.1password.com

# Verify current session
op whoami

# List vaults
op vault list

# List items in a vault
op item list --vault "Personal"

# Get a specific item
op item get "Login name or UUID"

# Get a specific field from an item
op item get "Login name" --fields username
op item get "Login name" --fields password

# Read a secret by reference
op read "op://vault-name/item-name/field-name"

# Inject secrets into environment variables and run a command
op run --env-file .env -- your-command

# Inject secrets from a template file
op inject --in-file template.env --out-file .env

# Create a new item
op item create --category login --title "My Service" \
  --url "https://example.com" \
  --generate-password

# Edit an item field
op item edit "Login name" username=newuser@example.com

# Delete an item
op item delete "Login name"

# List accounts
op account list

# Add an additional account
op account add

# Sign out
op signout
```

---

## Guardrails

- **Never** paste secrets into logs, chat, or code.
- Prefer `op run` / `op inject` over writing secrets to disk.
- If sign-in without app integration is needed, use `op account add`.
- If a command returns "account is not signed in", re-run `op signin` inside tmux and authorize in the app.
- **Do not run `op` outside tmux**; stop and ask if tmux is unavailable.
- Use `op read` for one-off secret reads; use `op run` to inject secrets into subprocesses without exposing them in environment.

---

## Tips

- Use `--format json` for scripting: `op item get "My Login" --format json`
- Secret references follow the pattern: `op://vault/item/field`
- For CI/CD: use service accounts (`op service-account create`) instead of user credentials
- The desktop app integration (biometric unlock) is the recommended auth method; it avoids storing master passwords
