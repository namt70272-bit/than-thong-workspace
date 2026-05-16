# Dependency Map

## Runtime Summary

| Runtime | Version | Purpose |
|---|---|---|
| **Node.js** | v24.14.1 | OpenClaw core + npm/npx tools |
| **Python** | 3.11.9 | All scripts, testing, AI pipeline |
| **Docker** | 29.3.1 | Services (Qdrant, n8n, Dozzle, Portainer) |
| **Ollama** | 0.23.0 | Local LLM serving |

## Key Python Packages

| Package | Version | Purpose |
|---|---|---|
| **playwright** | 1.59.0 | Web automation |
| **pywinauto** | 0.6.9 | Windows GUI automation |
| **qdrant-client** | latest | Vector DB client |
| **pytest** | 9.0.3 | Testing framework |
| **opencv-python** | 4.13.0 | Computer vision |
| **pillow** | 11.3.0 | Image processing |
| **numpy** | 2.4.5 | Numerical computing |
| **ruff** | 0.15.13 | Python linter |
| **docker** (CLI) | 29.3.1 | Container management |

## Key Node Packages (via npx)

| Package | Purpose |
|---|---|
| **repomix** | Codebase bundler for AI analysis |
| **madge** | JavaScript dependency graph |
| **@mermaid-js/mermaid-cli** | Diagram generation |

## AI/ML Stack

| Component | Model/Version | Size | Purpose |
|---|---|---|---|
| **Ollama** | v0.23.0 | - | Local LLM runtime |
| **bge-m3** | latest | 1.2 GB | Text embeddings |
| **gemma3:1b-it-qat** | latest | 1.0 GB | Lightweight inference |
| **qwen2.5-coder:7b** | latest | 4.7 GB | Code generation/review |
| **Qdrant** | v1.18.0 | - | Vector database |

## Docker Images (9 total)

| Image | Size | Purpose |
|---|---|---|
| qdrant/qdrant:latest | ~200MB | Vector database |
| n8nio/n8n:latest | 2.27GB | Workflow automation (restarting) |
| n8n-pipeline-python-worker:latest | 1.34GB | n8n Python worker |
| amir20/dozzle:latest | 89MB | Docker log viewer |
| portainer/portainer-ce:latest | 242MB | Docker UI management |
| postgres:16-alpine | 396MB | PostgreSQL database |
| python:3.11-slim | 188MB | Python sandbox container |
| alpine:latest | 13MB | Minimal Linux base |
| vimagick/tinyproxy:latest | 9MB | HTTP proxy |
| ghcr.io/langfuse/langfuse:latest | 1.37GB | LLM observability |

## Git Workflows (12 total)

All in `.github/workflows/` - see WORKFLOW_MAP.md for details.

## Potential Issues

1. **n8n** container keeps restarting - may be misconfigured
2. **langfuse** image is pulled but no container running - unused resource
3. **n8n-pipeline-python-worker** image exists but no container - unused
4. **pip conflicts**: 3 remaining (diffusers, hf-gradio, rembg - all AI niche)
5. **No requirements.txt**: Dependencies managed ad-hoc via pip, not locked
