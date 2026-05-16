#!/usr/bin/env python3
"""Ops Console — main entry for thần thông commands"""
import os, sys, json, subprocess
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# === Dynamic path detection ===
_POSSIBLE = [Path.cwd(), Path(__file__).resolve().parent.parent.parent, Path(__file__).resolve().parent.parent]
WORKSPACE = next((p for p in _POSSIBLE if (p/"AGENTS.md").exists()), Path(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"))
SCRIPTS = WORKSPACE / "tools-internal" / "scripts"

COMMANDS = {
    "preflight": "preflight_runner.py",
    "inventory": "workspace_inventory.py",
    "domains": "index_domains.py",
    "junk": "find_junk.py",
    "duplicate": "duplicate_checker.py",
    "canonical": "canonical_checker.py",
    "track": "domain_tracker.py",
    "drift": "drift_checker.py",
    "waves": "wave_manager.py",
    "dashboard": "ops_dashboard.py",
    "win-audit": "top_win_audit.py",
    "win-cleanup": "top_win_cleanup.py",
    "win-process": "top_win_process_audit.py",
    "win-data": "top_win_data_map.py",
    "win-dashboard": "top_win_dashboard.py",
    "win-env": "top_win_env_audit.py",
    "win-svc": "top_win_svc_audit.py",
    "win-startup": "top_win_startup_audit.py",
    "win-disk": "top_win_disk_health.py",
    "win-restore": "top_win_system_restore.py",
    "win-tighten": "top_win_tighten.py",
    "win-full": "top_win_full_dashboard.py",
    "win-repair-printer": "top_win_repair_printer.py",
    "win-repair-spooler": "top_win_repair_spooler.py",
    "win-repair-usb": "top_win_repair_usb.py",
    "win-repair-audio": "top_win_repair_audio.py",
    "win-events": "win_event_correlator.py",
    "local-search": "local_search_index.py",
    "docs-miner": "local_docs_miner.py",
    "local-qa": "local_knowledge_qa.py",
    "scan-G": "top_scan_G_source.py",
    "daily": "than_thong_daily.py",
}

def run_script(script_name, *args):
    """Run a script and return output"""
    script = SCRIPTS / script_name
    task = f"internal ops console command {script_name}"
    
    # Gate first (lightweight)
    gate = subprocess.run(
        [sys.executable, str(SCRIPTS / "billing_gate.py"), task],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10
    )
    gate_result = json.loads(gate.stdout) if gate.stdout else {}
    
    # Run target script
    out = subprocess.run(
        [sys.executable, str(script), *args],
        capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60
    )
    result = gate_result
    result["output"] = out.stdout[:5000] if out.stdout else out.stderr[:500]
    result["exit_code"] = out.returncode
    return result

def main():
    if len(sys.argv) < 2:
        print(json.dumps({"commands": list(COMMANDS.keys())}, ensure_ascii=False, indent=2))
        return 0
    cmd = sys.argv[1]
    if cmd not in COMMANDS:
        print(json.dumps({"error": f"unknown command: {cmd}"}, ensure_ascii=False, indent=2))
        return 2
    args = sys.argv[2:]
    result = run_script(COMMANDS[cmd], *args)
    # Don't re-print gate, just output
    if result.get("output"):
        print(result["output"])
    return result.get("exit_code", 0)

if __name__ == "__main__":
    raise SystemExit(main())
