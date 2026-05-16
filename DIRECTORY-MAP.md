# DIRECTORY-MAP.md

Visual map of the current workspace structure.

**Root:** `E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace`
**Last mapped:** 2026-05-12

## 1) Top-level map

```text
workspace/
├── .git/                          Git metadata
├── .gitignore                     Ignore rules for cache/runtime artifacts
├── .openclaw/                     Runtime state for this workspace
├── archive/                       Safe holding area for deprecated files
│   └── deprecated/
├── config/                        Shared config templates
├── examples/                      Reusable workflow examples
├── khai-thac/                     External-source analysis notes
├── memory/                        Daily memory logs
├── references/                    Imported reference material
├── reports/                       Generated audits and analysis reports
├── scripts/                       Runnable helper scripts
├── skills/                        Custom skills and skill tooling
├── utils/                         Shared Python utilities
├── AGENTS.md                      Workspace operating rules
├── HEARTBEAT.md                   Proactive-check checklist
├── IDENTITY.md                    Agent identity
├── README.md                      Quick landing page
├── RESTRUCTURE-PLAN.md            Restructure plan
├── SKILL-REGISTRY.md              Master skills inventory
├── SOUL.md                        Personality and values
├── TOOLS.md                       Local environment notes
├── USER.md                        Human preferences
└── WORKSPACE.md                   Full workspace guide
```

## 2) Expanded structure

```text
workspace/
├── archive/
│   └── deprecated/
│       ├── __init__.py
│       ├── engram-folder-map-2026-05-11.md
│       ├── test_package_skill.py
│       ├── test_quick_validate.py
│       └── test_search.py
├── config/
│   └── prompts-template.yaml
├── examples/
│   ├── inbox-triage.lobster
│   └── pr-intake.lobster
├── khai-thac/
│   ├── Agent365-devTools-plan.md
│   └── openclaw-source-report.md
├── memory/
│   ├── 2026-05-11.md
│   └── 2026-05-12-awesome-skills-intake.md
├── references/
│   ├── 1password/
│   │   ├── cli-examples.md
│   │   └── get-started.md
│   ├── awesome-skills-catalog/
│   │   ├── CONTRIBUTING.md
│   │   ├── INDEX.md
│   │   ├── README-VN.md
│   │   ├── README.md
│   │   └── USAGE.md
│   ├── himalaya/
│   │   ├── configuration.md
│   │   └── message-composition.md
│   └── model-usage/
│       └── codexbar-cli.md
├── reports/
│   ├── engram-candidate-gap-report-2026-05-11.md
│   ├── engram-deep-review-2026-05-11.md
│   ├── engram-extraction-findings-2026-05-11.md
│   ├── engram-file-manifest-2026-05-11.json
│   ├── engram-import-plan-2026-05-11.md
│   ├── engram-staged-readiness-2026-05-11.md
│   ├── openclaw-c-legacy-inventory-2026-05-11.md
│   ├── openclaw-canonicalization-2026-05-11.md
│   └── openclaw-infra-audit-2026-05-09.md
├── scripts/
│   ├── browser.py
│   ├── model_usage.py
│   ├── play_song.py
│   ├── tmux/
│   │   ├── find-sessions.sh
│   │   └── wait-for-text.sh
│   ├── video/
│   │   └── frame.sh
│   └── whisper/
│       └── transcribe.sh
├── skills/
│   ├── billing-guard/
│   │   └── SKILL.md
│   ├── khai-thac/
│   │   ├── references/
│   │   └── SKILL.md
│   ├── review-code/
│   │   └── SKILL.md
│   └── skill-creator/
│       ├── init_skill.py
│       ├── package_skill.py
│       └── quick_validate.py
└── utils/
    ├── prompt_utils.py
    └── rate_limiter.py
```

## 3) Functional zones

### Core identity and behavior
- `AGENTS.md`
- `SOUL.md`
- `IDENTITY.md`
- `USER.md`
- `TOOLS.md`
- `HEARTBEAT.md`

### Operational code
- `skills/`
- `utils/`
- `scripts/`
- `config/`

### Knowledge and records
- `references/`
- `reports/`
- `memory/`
- `archive/`
- `khai-thac/`

### Root-level legacy summary docs
- `OPTIMIZATION-REPORT.md`
- `BÁO-CÁO-TỐI-ƯU-HÓA.md`
- `RESTRUCTURE-COMPLETE.md`
- `HOÀN-THÀNH.md`
- `TÓM-TẮT-NGẮN.md`

These are useful historical summaries, but they overlap and should not be treated as the only source of truth.

## 4) Quick orientation

- Start at `README.md` for the short overview.
- Use `WORKSPACE.md` for the full guide.
- Use `QUICK-START.md` if you are onboarding.
- Use `SKILL-REGISTRY.md` to find usable skills fast.
- Use `REFERENCE-INDEX.md` to find imported reference material.

## 5) Current counts

Audited on 2026-05-12 after follow-up fixes.

- Whole workspace: 118 files / 43 directories / ~655 KB
- Excluding `.git` and `__pycache__`: 78 files / 24 directories / ~507 KB
- `skills/`: 4 subdirectories, 11 files total before `__pycache__`
- `utils/`: 2 Python utilities (+ `README.md`, `__pycache__`)
- `scripts/`: 8 runnable scripts across 4 subdirectories (+ `README.md`, `__pycache__`)
- `references/`: 11 reference files across 4 collections
- `reports/`: 11 files including `README.md`
- `examples/`: 2 example workflows (+ `README.md`)
- `memory/`: 2 dated note files (+ `README.md`)
- `archive/`: 5 deprecated files (+ `README.md`)
