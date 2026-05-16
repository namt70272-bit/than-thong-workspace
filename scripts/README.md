# scripts/README.md

Runnable helper scripts for local workflows.

## Current inventory

### Top level

| Script | Purpose |
| --- | --- |
| `browser.py` | Lightweight Playwright browser opener and inspector |
| `model_usage.py` | Summarize CodexBar local usage/cost data by model |
| `play_song.py` | Open YouTube search results and play the first match |

### Subdirectories

| Folder | Files | Purpose |
| --- | --- | --- |
| `tmux/` | `find-sessions.sh`, `wait-for-text.sh` | tmux discovery and pane-text waiting helpers |
| `video/` | `frame.sh` | Extract frames from video via ffmpeg |
| `whisper/` | `transcribe.sh` | Whisper transcription helper |

## Placement rule

Put something in `scripts/` when it is meant to be run directly. If it is primarily imported by other Python code, it probably belongs in `utils/` instead.

## Notes

- Some scripts depend on local tools already being installed (`playwright`, `ffmpeg`, `tmux`, `codexbar`, Whisper tooling).
- Keep script names descriptive and task-oriented.
- If usage becomes non-obvious, add a short header comment or usage block.
