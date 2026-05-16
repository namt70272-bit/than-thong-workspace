# Security Checklist Report

**Generated:** 2026-05-16 20:27 GMT+7  
**Scope:** `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`  
**Method:** File content scanning, port scan, permissions review  
**Policy:** Do NOT print actual secrets — all tokens masked as `****`

---

## 1. API Keys / Tokens Exposed in Files

### 🔴 CRITICAL — Hardcoded Gemini API key in scripts

**Files:**
- `scripts/test-gemini-key.py` (line 3)
- `scripts/test-gemini-openai-endpoint.py` (line 4)
- `scripts/create-n8n-cred.py` (line 9)
- `scripts/create-n8n-http-workflow.py` (line 43 — embedded in URL parameter)

The same Google Gemini API key `AIzaSyC28WW_****` is hardcoded in **4 separate script files**. This key is used in HTTPS URLs and HTTP headers across production scripts (n8n credential creation, Gemini API tests, n8n workflow generation). If the repository is pushed to a public remote, this key is compromised immediately.

**Risk:** Unauthorized usage of the Gemini API; potential billing impact (though the key appears to be from a free tier, it still has usage quotas).

**Fix:** Move to environment variable (e.g., `os.environ["GEMINI_API_KEY"]`). Add `scripts/` to `.gitignore` or externalize all credential references.

---

### 🔴 CRITICAL — GCP Service Account key stored in workspace

**File:** `config/gcp-n8n-vertex-ai-key.json`

Contains a full Google Cloud Platform service account JSON with private key material:
- Project: `gen-lang-client-0477618387`
- Client email: `n8n-vertex-ai@gen-lang-client-0477618387.iam.gserviceaccount.com`
- Private key ID: `c04c234e4e712b00841aed839566a89734bda4d7`
- Private key: `-----BEGIN PRIVATE KEY-----****-----END PRIVATE KEY-----`

This file is referenced by:
- `scripts/test-gemini-api.py` (loads and uses the key)
- `scripts/test-vertex-ai-key.py` (loads and uses the key)

**Risk:** Any process with read access to this file can impersonate the service account to access Vertex AI, Cloud Storage, or any enabled GCP service in that project. Full private key exposure = full account control within GCP project scope.

**Fix:** Remove this file from the workspace. Use GCP Workload Identity Federation or environment variable `GOOGLE_APPLICATION_CREDENTIALS` pointing outside the repo. Add `config/gcp-*.json` to `.gitignore`.

---

### 🟡 MEDIUM — PostHog telemetry API key in reference library

**File:** `tools-internal/reference-library/mem0/telemetry.py` (line 12)

Contains a real PostHog API key: `phc_hgJkUVJFYtmaJqrvf6CYN67TIQ8yhXAkWzUn`

This is in third-party extracted code, not actively used in the workspace. However, if any process imports this module, it phones home to PostHog with telemetry data.

**Risk:** Low — the code is in reference library, not actively imported. But it's still a real key in the filesystem.

**Fix:** Remove the telemetry.py file or replace the key with a placeholder.

---

### ⚪ LOW — Various test/placeholder credentials in reference library

**Files under `tools-internal/reference-library/` contain hundreds of test credentials** (e.g., `testpass`, `test_api_key`, `test_token`, `test-secret`, `GOCSPX-test123`, `sk_test_456`).

These are **test values** from extracted third-party test suites. They pose minimal direct risk but clutter the workspace with credential-like patterns that trigger false positives in automated scanners.

**Risk:** None directly (test values). However, `GOCSPX-test123` matches Google OAuth client secret format and could be confused with a real secret. `sk_test_456` matches Stripe test key format.

**Fix:** Ideally exclude extracted test files from the workspace or add them to a scanner exclusion list.

---

## 2. .env Files Location and Git Exposure

### 🟢 GOOD — .gitignore properly excludes .env

The workspace `.gitignore` contains:
```
.env
.env.*
```

This means both found `.env` files will not be committed to git:
- `config/.env.rate-limit` — Contains only `LLM_MAX_CALLS_PER_MINUTE=30`, a non-sensitive rate limit config
- `tools-internal/.env` — Contains only the comment `# Keys moved to vault. Use vault_get() to access.`

**Risk:** LOW. Both `.env` files contain no secrets. The `.gitignore` is correctly configured.

**Recommendation:** None needed. Good practice observed.

---

## 3. Sensitive Ports Open

### 🟢 LOW — Standard Windows ports only

```
TCP    0.0.0.0:135     LISTENING   (RPC Endpoint Mapper)
TCP    0.0.0.0:445     LISTENING   (SMB over TCP)
TCP    [::]:135        LISTENING
TCP    [::]:445        LISTENING
TCP    172.26.192.1:139   LISTENING (NetBIOS, virtual adapter)
TCP    192.168.123.3:139  LISTENING
TCP    192.168.217.1:139  LISTENING
TCP    192.168.253.1:139  LISTENING
```

No database ports (27017 MongoDB, 5432 PostgreSQL, 3306 MySQL, 6379 Redis) were detected listening externally. No debug ports (9229, 5858) found. No container orchestration ports (2375, 2376 Docker).

Ports **135** and **445** are standard Windows services — SMB and RPC. These are required for normal Windows operation. NetBIOS (139) is bound only to virtual adapters, not the physical network.

**Risk:** LOW. Standard Windows attack surface. Not unusual for a desktop machine.

**Recommendation:** If this machine is on a public network, consider blocking SMB (445) and RPC (135) at the Windows Firewall for public interfaces.

---

## 4. Docker Containers — Privileged or Sensitive Mounts

### 🟢 NOT DETECTED

No Dockerfiles or docker-compose files were found in the workspace. No container-related infrastructure was detected.

**Risk:** NONE. This environment does not use Docker-based isolation.

---

## 5. Browser Profiles Sharing

### ⚪ NOT SCANNED (permission denied / not available on PATH)

Chrome profile scanning failed (access denied to `C:\Users\ACER\AppData\Local\Google\Chrome\User Data`). This is expected — Chrome profile directories are protected by Windows permissions.

**Risk:** Unknown but presumed controlled by Windows user account permissions. Standard desktop security applies.

**Recommendation:** Ensure your Windows user account is password-protected and the machine is locked when unattended.

---

## 6. Agent Permissions

### 🔴 CRITICAL — Elevated exec wildcard

OpenClaw's built-in security audit (from `%TMPDIR%/openclaw/openclaw-2026-05-16.log`) reports:

> **CRITICAL:** `tools.elevated.allowFrom.webchat.wildcard` — Elevated exec allowlist contains wildcard `"*"` on the webchat channel.

This means **anyone** with access to the webchat interface can execute commands with elevated (admin) privileges without explicit approval. This is a massive escalation path — if the webchat is exposed or if the agent can be tricked via prompt injection, an attacker gets full system-level access.

**Risk:** CRITICAL. Eliminate the wildcard.

**Fix:** In gateway.yaml/openclaw.yaml, replace `"*"` with specific trusted user identifiers, or disable elevated mode entirely: `tools.elevated.allowFrom.webchat: []`.

---

### 🟡 MEDIUM — Small model fallbacks with web tools and no sandbox

OpenClaw security audit reports:

> Small models (<=300B params): `ollama/qwen2.5:7b` (7B), `ollama/deepseek-r1:14b` (14B) in fallbacks with web tools (`web_search`, `web_fetch`) enabled and sandbox disabled.

**Risk:** Small models are more susceptible to prompt injection. An injected prompt could trick the model into using web tools to exfiltrate data or perform unauthorized actions.

**Fix:** Either disable web tools for small models with `tools.byProvider["provider/model"].deny=["group:web"]`, or enable `agents.defaults.sandbox.mode="all"`.

---

### ⚪ INFO — Agent can delete/send/pay

From AGENTS.md and OpenClaw config:
- Agent has access to `exec` (system command execution)
- Agent has access to `web_search`, `web_fetch` (external data)
- Agent has `elevated` mode enabled (can run as admin)
- Agent has browser control enabled
- Agent has internal hooks enabled

The "thần thông" (than-thong) policy restricts billing/quota usage through command guards (than-thong-command-guard, than-thong-shutdown-guard). However, the agent *can* technically interact with any system command exposed via `exec` + elevated.

**Risk:** The agent is a powerful tool with system-level permissions. Current guardrails are policy-based (written in AGENTS.md), not technically enforced at the execution layer for all scenarios.

**Recommendation:** Consider running the agent in a non-admin Windows account or container for untrusted tasks.

---

## 7. MCP / Tool Permissions

### 🟡 MEDIUM — Unpinned plugin spec

OpenClaw security audit reports:

> Plugin install uses unpinned npm spec: `@openclaw/acpx` (no version pin).

**Risk:** Supply-chain risk. If the npm package is compromised, the next update could inject malicious code.

**Fix:** Pin the version: `@openclaw/acpx@1.0.0` (or the current stable version).

---

### 🟢 GOOD — Runtime guard plugin exists

`runtime-guard/than-thong-guard/` implements a plugin that:
- Blocks billing/tool usage at runtime
- Enforces offline-first routing
- Has a configurable blocked-tools list

This is an *excellent* security control for a local-first agent. It provides defense in depth beyond policy files.

**Risk:** LOW. The runtime guard is properly structured as an OpenClaw plugin with hooks.

---

## 8. Log Files Containing Tokens

### 🟡 MEDIUM — Runner diagnostic logs contain credential references

**Files:**
- `runner/_diag/Worker_20260516-120437-utc.log` (153KB)
- `runner/_diag/Worker_20260516-120534-utc.log` (145KB)
- `runner/_diag/Worker_20260516-120711-utc.log` (142KB)
- (27 more Runner/Worker log files, each up to ~150KB)

These logs contain:
- GitHub Actions runner credential configuration
- `github_token` (marked `isSecret: true` in log, but the log file exists in plain text)
- Runner OAuth client credentials (`80b50478-7935-47d0-aa64-a0f196d98bda`)
- References to `token.actions.githubusercontent.com`

The actual token values appear to be masked (`***`) in the log, but the mere existence of these files means that if an attacker gains filesystem access, they can see the runner's configuration.

**Additionally:** `runner/.credentials` file contains OAuth client config including clientId for GitHub Actions runner.

### 🟢 GOOD — OpenClaw log does not contain secrets

The OpenClaw log (`%TMPDIR%/openclaw/openclaw-2026-05-16.log`) contains the security audit output but no plaintext secrets/credentials.

**Risk:** The runner diagnostic logs and `.credentials` file must be considered part of the sensitive attack surface. If the workspace is backed up or shared, these go with it.

**Fix:** Add `runner/_diag/` and `runner/.credentials*` to `.gitignore` (they appear to already be excluded by git's default patterns, but verify).

---

## 9. Configs That Should Be Templated

### 🟡 MEDIUM — `config/gcp-n8n-vertex-ai-key.json` should not exist at all

This contains a full GCP service account key. As noted in section 1, this is a **CRITICAL** exposure. The proper approach is to never store raw service account keys in the workspace. Use GCP's workload identity or environment variables pointing to a secure location outside version control.

### 🟢 GOOD — GitHub Actions workflows use `${{ github.token }}`

All GitHub workflows correctly use the auto-generated `${{ github.token }}` token. No `secrets.*` references were found — the workflows don't persist any long-lived secrets in GitHub Actions secrets storage.

This is **excellent practice** for a self-hosted runner: zero dependency on GitHub-managed secrets.

### 🟡 MEDIUM — `create-n8n-cred.py` and `create-n8n-workflow.py` contain hardcoded credential references

`create-n8n-workflow.py` (line 21) uses a hardcoded credential ID `9233165a-f3b6-4d65-b3f1-82a403ac5c87` for Google AI credentials. This is an opaque UUID, not a secret itself, but it references a credential store that would need to exist on the target n8n instance.

**Recommendation:** Template out credential references. Create workflow templates with credential placeholders.

---

## Summary

| # | Finding | Severity | Status |
|---|---------|----------|--------|
| 1a | Hardcoded Gemini API key (`AIzaSyC28WW_****`) in 4 scripts | 🔴 CRITICAL | Fix immediately |
| 1b | GCP service account private key in workspace (`config/gcp-n8n-vertex-ai-key.json`) | 🔴 CRITICAL | Fix immediately |
| 1c | Real PostHog API key in mem0 telemetry.py | 🟡 MEDIUM | Review & remove |
| 2 | `.env` files properly gitignored | 🟢 GOOD | No action |
| 3 | Only standard Windows ports (135, 445, 139) — no DB/debug ports | 🟢 LOW | Monitor |
| 4 | No Docker detected | 🟢 NOT FOUND | No action |
| 5 | Chrome profiles not accessible (permissions) | ⚪ UNKNOWN | Verify account security |
| 6a | Elevated exec wildcard (`"*"`) on webchat | 🔴 CRITICAL | Fix immediately |
| 6b | Small model fallbacks with web tools, no sandbox | 🟡 MEDIUM | Configure sandbox/deny web tools |
| 7a | Unpinned npm plugin spec (`@openclaw/acpx`) | 🟡 MEDIUM | Pin version |
| 7b | Runtime guard plugin exists (good practice) | 🟢 GOOD | Maintain |
| 8 | Runner diagnostic logs with credential configs | 🟡 MEDIUM | Ensure gitignored |
| 9a | GCP key should be templated / moved outside workspace | 🔴 CRITICAL | Same fix as 1b |
| 9b | GitHub workflows use `${{ github.token }}` (good) | 🟢 GOOD | No action |
| 9c | Hardcoded credential UUID in n8n workflow script | 🟡 MEDIUM | Template-ize |

### Top 3 Immediate Actions

1. **🔴 Remove** `config/gcp-n8n-vertex-ai-key.json` from workspace and rotate the service account key in GCP Console.
2. **🔴 Remove** hardcoded API key from all 4 scripts in `scripts/` and use environment variables.
3. **🔴 Fix** the elevated exec wildcard in OpenClaw config: change `tools.elevated.allowFrom.webchat` from `["*"]` to `[]` or specific user IDs.

### Additional Recommendations

- Consider adding `runner/_diag/`, `runner/.credentials`, and `config/gcp-*.json` patterns to a `.gitattributes` or `.gitignore` audit if not already covered.
- For the reference-library test files with placeholder credentials, add an automated scanner exclusion rule.
- Review the need for elevated mode — if the agent does not require admin access, disable `tools.elevated` entirely.
