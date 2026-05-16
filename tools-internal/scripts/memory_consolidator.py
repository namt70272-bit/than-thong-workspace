#!/usr/bin/env python3
"""
memory_consolidator.py -- Memory pipeline for Thần Thú Thời Thượng Cổ

Scans daily notes, generates INDEX.md, consolidation report, and suggests MEMORY.md updates.

Usage:
  python memory_consolidator.py         # full run
  python memory_consolidator.py --report  # show only, no writes
  python memory_consolidator.py --cron   # cron-friendly short output
"""

import os, re, json, sys, datetime
from pathlib import Path
from collections import defaultdict

# -- Config ------------------------------------------------------------------
WORKSPACE = Path(os.environ.get(
    "OPENCLAW_WORKSPACE",
    r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
))
MEMORY_DIR = WORKSPACE / "memory"
MEMORY_MD  = WORKSPACE / "MEMORY.md"
INDEX_MD   = MEMORY_DIR / "INDEX.md"
STATE_JSON = MEMORY_DIR / ".consolidator-state.json"

# Files to skip during scan
SKIP_PATTERNS = [r"consolidation-", r"INDEX\.md", r"README\.md", r"^\."]

DECISION_PATTERNS = [
    r"(?i)^##?\s*(quy.t d.nh|ch.t l.i|decision)",
    r"(?i)^- \*\*decision|^# .+ decision",
    r"(?i)(?:da )?(ch.t l.i|quy.t d.nh) r.ng",
    r"(?i)(rule|policy) (m.i|chinh th.c|update|new|modified)",
]
EVENT_PATTERNS = [
    r"(?i)(?:da )?(hoan thanh|hoan tat|done|completed|finished)",
    r"(?i)(?:da )?(chay|test|fix|va|apply) (?:thanh cong|ok|pass|xong)",
    r"(?i)(?:da )?(xoa|go|removed|deleted|import|cai|dung|xay|them)",
]
BLOCKER_PATTERNS = [
    r"(?i)(?:^##?\s*)?(blocker|ch.a hoan thanh|ton .ong|stuck|pending)(?:$|[.:])",
    r"(?i)(c.n tiep|phai lam tiep|can .u.c)",
    r"(?i)(?:con|still) .{0,20}(?:blocker|v.ng|pending|stuck)",
]
STATE_PATTERNS = [
    r"(?i)^##?\s*(trang thai|status|current state|readiness)",
    r"(?i)(san sang|ready|du de|current readiness)",
    r"(?i)(hien tai|dang chay|dang hoat d.ng)",
]

def safeprint(*args, **kwargs):
    text = " ".join(str(a) for a in args)
    try:
        print(text, **kwargs, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"), **kwargs, flush=True)

def load_state():
    if STATE_JSON.exists():
        try: return json.loads(STATE_JSON.read_text(encoding="utf-8"))
        except: return {}
    return {}

def save_state(state):
    STATE_JSON.parent.mkdir(parents=True, exist_ok=True)
    STATE_JSON.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")

# -- Scan ----------------------------------------------------------------

def should_skip(name):
    for pat in SKIP_PATTERNS:
        if re.search(pat, name):
            return True
    return False


def scan_notes():
    notes = []
    if not MEMORY_DIR.exists():
        safeprint("[!] memory/ does not exist")
        return notes
    for f in sorted(MEMORY_DIR.glob("*.md")):
        if should_skip(f.name):
            continue
        try:
            content = f.read_text(encoding="utf-8", errors="replace")
        except Exception as e:
            safeprint(f"  [!] Cannot read {f.name}: {e}")
            continue
        dm = re.match(r"(\d{4}-\d{2}-\d{2})", f.name)
        date = dm.group(1) if dm else f.stem
        sections = re.split(r"\n(?=##\s)", content)
        sections = [s.strip() for s in sections if s.strip()]
        notes.append({"filename": f.name, "date": date, "size": len(content),
                       "content": content, "sections": sections})
    return notes

def extract_items(notes, patterns):
    items = []
    for note in notes:
        for section in note["sections"]:
            lines = section.split("\n")
            for i, line in enumerate(lines):
                for pat in patterns:
                    if re.search(pat, line):
                        start, end = max(0, i-1), min(len(lines), i+3)
                        context = "\n".join(lines[start:end]).strip()
                        items.append({"date": note["date"], "file": note["filename"],
                                       "line": line.strip(), "context": context})
                        break
    return items

def extract_topic_snapshot(notes):
    topics = defaultdict(list)
    for note in notes:
        for section in note["sections"]:
            lines = section.split("\n")
            title = lines[0].replace("##", "").strip() if lines else "General"
            topics[title].append({"date": note["date"],
                                   "body": "\n".join(lines[1:]).strip() if len(lines) > 1 else ""})
    return dict(topics)

# -- Generate ------------------------------------------------------------

def generate_index(notes):
    lines = [
        "# Memory Index",
        "",
        f"_Auto-updated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}_",
        "",
        "## Daily Notes",
        "",
    ]
    for note in notes:
        titles = []
        for sec in note["sections"]:
            t = sec.split("\n")[0].replace("##", "").strip()
            if t: titles.append(t)
        ts = f" -- {' | '.join(titles[:5])}" if titles else ""
        lines.append(f"- [{note['filename']}]({note['filename']}) ({note['size']}B){ts}")

    lines.append("")
    lines.append("## Stats")
    lines.append(f"- Total notes: {len(notes)}")
    fr = notes[0]["date"] if notes else "N/A"
    to_ = notes[-1]["date"] if notes else "N/A"
    lines.append(f"- Range: {fr} -> {to_}")
    lines.append("")
    return "\n".join(lines)

def generate_report(notes):
    decisions = extract_items(notes, DECISION_PATTERNS)
    events    = extract_items(notes, EVENT_PATTERNS)
    blockers  = extract_items(notes, BLOCKER_PATTERNS)
    states    = extract_items(notes, STATE_PATTERNS)
    topics    = extract_topic_snapshot(notes)

    lines = [
        "# Memory Consolidation Report",
        "",
        f"_Generated: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} GMT+7_",
        f"_Scanned: {len(notes)} daily notes_",
        "",
    ]

    # Decisions
    if decisions:
        lines.extend(["## Decisions", ""])
        for d in decisions:
            lines.append(f"- [{d['date']}] {d['line'][:120]}")
        lines.append("")

    # Blockers
    if blockers:
        lines.extend(["## Blockers & Pending", ""])
        for b in blockers:
            lines.append(f"- [{b['date']}] {b['line'][:150]}")
        lines.append("")

    # Topic snapshots
    lines.extend(["## Topic Snapshots", ""])
    for topic, entries in sorted(topics.items()):
        if topic == "General": continue
        latest = max(entries, key=lambda x: x["date"])
        lines.append(f"### {topic}")
        lines.append(f"_Last: {latest['date']}_")
        body = latest["body"][:300]
        if body: lines.append(body)
        lines.append("")

    # Suggestions
    lines.extend(["## Suggested MEMORY.md Updates", ""])
    for d in decisions:
        lines.append(f"- [{d['date']}] {d['line'][:100]}")
    lines.append("")

    return "\n".join(lines)

def suggest_updates(notes):
    decisions = extract_items(notes, DECISION_PATTERNS)
    if not decisions: return None
    current = MEMORY_MD.read_text(encoding="utf-8") if MEMORY_MD.exists() else ""
    suggestions = []
    for d in decisions:
        if d["line"][:80] not in current:
            suggestions.append(f"- [{d['date']}]: {d['line'][:120]}")
    return suggestions if suggestions else None

# -- Main -------------------------------------------------------------------

def main():
    args = set(sys.argv[1:])
    cron_mode = "--cron" in args
    report_only = "--report" in args

    notes = scan_notes()
    if not notes:
        safeprint("[!] No daily notes found.")
        return

    # 1. INDEX.md
    idx = generate_index(notes)
    if not report_only:
        INDEX_MD.write_text(idx, encoding="utf-8")
        if cron_mode:
            safeprint(f"[memory] INDEX.md updated: {len(notes)} notes")
        else:
            safeprint(f"[OK] INDEX.md updated ({len(notes)} notes)")

    # 2. Consolidation report
    report = generate_report(notes)
    today = datetime.date.today().isoformat()
    report_file = MEMORY_DIR / f"consolidation-{today}.md"
    if not report_only:
        for old in MEMORY_DIR.glob(f"consolidation-{today}*.md"):
            old.unlink()
        report_file.write_text(report, encoding="utf-8")
        if cron_mode:
            safeprint(f"[memory] Report -> {report_file}")
        else:
            safeprint(f"[OK] Report -> {report_file}")

    # 3. MEMORY.md suggestions
    suggestions = suggest_updates(notes)
    if suggestions:
        safeprint(f"\n[!] MEMORY.md needs updates ({len(suggestions)} items):")
        for s in suggestions:
            safeprint(f"    {s}")
    elif not cron_mode:
        safeprint("[OK] MEMORY.md is synced with daily notes")

    # 4. State
    state = {
        "last_run": datetime.datetime.now().isoformat(),
        "notes_count": len(notes),
        "latest_note": notes[-1]["date"] if notes else None,
        "suggested_updates": len(suggestions) if suggestions else 0,
    }
    save_state(state)

    if cron_mode:
        blk = extract_items(notes, BLOCKER_PATTERNS)
        dec = extract_items(notes, DECISION_PATTERNS)
        safeprint(f"[memory] {len(notes)} files | {len(dec)} decisions | {len(blk)} blockers | OK")

if __name__ == "__main__":
    main()
