# Tool Install Status

## Audit Tools

| Tool | Status | Method | Purpose | Output Created |
|---|---|---|---|---|
| **Repomix** | ✅ Ran | `npx repomix@latest` | Codebase bundler | `openclaw-repomix.md` (39.5MB, 4,195 files) |
| **Trivy** | ✅ Ran | Docker (`aquasec/trivy`) | Filesystem vulnerability/secret scan | `trivy-fs.json` (207KB) |
| **Gitleaks** | ✅ Ran | Docker (`zricethezav/gitleaks`) | Secret/token leak detection | `gitleaks-report.json` (37.6KB) |
| **Syft** | ✅ Ran | Docker (`anchore/syft`) | SBOM generation | `syft-sbom.json` (1.5MB) |
| **Grype** | ⚠️ Ran (empty output) | Docker (`anchore/grype`) | Vulnerability scanning | `grype-vulnerabilities.json` (0B - no vulns found) |
| **Madge** | ✅ Ran | `npx madge@latest` | Dependency graph | `madge-*.json/txt` (found 1 circular dep in 3rd party) |
| **Dependency Cruiser** | ⏳ Skipped | `npx dependency-cruiser` | Module dependency analysis | Not run (Madge already covered) |
| **Mermaid CLI** | ⏳ Skipped | `npx @mermaid-js/mermaid-cli` | Diagram export | Mermaid in markdown works without it |

## Already Installed Tools

| Tool | Version | Path | Purpose |
|---|---|---|---|
| **node** | v24.14.1 | `C:\Program Files\nodejs\node.exe` | Runtime |
| **npm** | 11.12.1 | with node | Package manager |
| **npx** | 11.12.1 | with node | Run packages without install |
| **docker** | 29.3.1 | Docker Desktop | Container runtime |
| **git** | 2.53.0 | `C:\Program Files\Git\cmd\git.exe` | Version control |
| **python** | 3.11.9 | Python 3.11 | Script runtime |
| **pip** | 26.0.1 | with python | Python package manager |
| **gh** | 2.70.0 | Portable | GitHub CLI |
| **ruff** | 0.15.13 | pip | Python linter |
| **ollama** | 0.23.0 | Native app | Local LLM |
| **playwright** | 1.59.0 | pip | Web automation |

## Not Installed (intentionally skipped)

| Tool | Reason |
|---|---|
| **pipx** | Not needed (Docker for most scans) |
| **winget** | Not needed (npm/Docker for everything) |
| **Portainer** | Already running in Docker |
| **Lazydocker** | Dozzle already covers log viewing |
| **Dozzle** | Already running in Docker |
