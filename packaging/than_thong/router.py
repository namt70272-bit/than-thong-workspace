"""Router — route lệnh tới internal tool đúng. Tự động dùng inline khi standalone."""
import subprocess, shutil, os, sys, json
from pathlib import Path
from than_thong.gate import check_tool, check_billing
from than_thong.logger import log
from than_thong.config import config


# === Inline command handlers (no subprocess needed) ===
from than_thong.inline_commands import (
    cmd_trang_thai,
    cmd_don_dep,
    cmd_kiem_tra_bao_mat,
    cmd_thong_tin,
    cmd_kiem_tra_cong,
    cmd_hoi,
    cmd_ai,
    cmd_sao_chep,
    cmd_di_chuyen,
    cmd_dong_bo,
    cmd_kiem_tra_file,
    cmd_checksum,
    cmd_so_sanh_checksum,
    cmd_wsl_export,
    cmd_wsl_xoa,
)

# Tieng Viet + English aliases
INLINE_COMMANDS = {
    # Tieng Viet
    "kiem-tra-cong": cmd_kiem_tra_cong,
    "trang-thai": cmd_trang_thai,
    "thong-tin": cmd_thong_tin,
    "don-dep": cmd_don_dep,
    "kiem-tra-bao-mat": cmd_kiem_tra_bao_mat,
    "don-rac": cmd_don_dep,
    # English (tuong thich nguoc)
    "gate-test": cmd_kiem_tra_cong,
    "status": cmd_trang_thai,
    "info": cmd_thong_tin,
    "win-cleanup": cmd_don_dep,
    "win-audit": cmd_kiem_tra_bao_mat,
    "cleanup": cmd_don_dep,
    "audit": cmd_kiem_tra_bao_mat,
    # Hoi / chat / AI
    "hoi": cmd_hoi,
    "chat": cmd_hoi,
    "ask": cmd_hoi,
    "ai": cmd_ai,
    "model": cmd_ai,
    # File tools
    "sao-chep": cmd_sao_chep,
    "copy": cmd_sao_chep,
    "di-chuyen": cmd_di_chuyen,
    "move": cmd_di_chuyen,
    "dong-bo": cmd_dong_bo,
    "sync": cmd_dong_bo,
    "kiem-tra-file": cmd_kiem_tra_file,
    "file-info": cmd_kiem_tra_file,
    "checksum": cmd_checksum,
    "so-sanh": cmd_so_sanh_checksum,
    "wsl-export": cmd_wsl_export,
    "wsl-xoa": cmd_wsl_xoa,
    # Tieng noi
}


# Inline commands with arguments
INLINE_WITH_ARGS = {
    "hoi": cmd_hoi,
    "chat": cmd_hoi,
    "ask": cmd_hoi,
    "sao-chep": cmd_sao_chep,
    "copy": cmd_sao_chep,
    "di-chuyen": cmd_di_chuyen,
    "move": cmd_di_chuyen,
    "dong-bo": cmd_dong_bo,
    "sync": cmd_dong_bo,
    "kiem-tra-file": cmd_kiem_tra_file,
    "file-info": cmd_kiem_tra_file,
    "checksum": cmd_checksum,
    "so-sanh": cmd_so_sanh_checksum,
    "wsl-export": cmd_wsl_export,
    "wsl-xoa": cmd_wsl_xoa,
    # Tieng noi
}


# === Legacy subprocess (chỉ dùng trong dev mode) ===
def _get_scripts_dir():
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "scripts"
    return Path(__file__).resolve().parent.parent.parent / "tools-internal" / "scripts"


SCRIPTS_DIR = _get_scripts_dir()


def resolve_python():
    for name in ["python3", "python"]:
        exe = shutil.which(name)
        if exe:
            return exe
    return sys.executable


def run_script(script_name: str, *args) -> dict:
    """Run script via subprocess. Only used when inline not available."""
    if getattr(sys, "frozen", False):
        return {"success": False, "error": "Subprocess not available in standalone mode. Inline version needed."}

    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        return {"success": False, "error": f"Script not found: {script_path}"}

    python = resolve_python()
    cmd = [python, str(script_path)] + list(args)

    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        return {
            "success": r.returncode == 0,
            "stdout": r.stdout[-2000:] if r.stdout else "",
            "stderr": r.stderr[-2000:] if r.stderr else "",
            "returncode": r.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Timeout (120s)"}
    except Exception as e:
        return {"success": False, "error": str(e)}


LEGACY_SUBPROCESS = {
    "full-dashboard": ["than_thong_console.py", "full-dashboard"],
    "win-data-map": ["than_thong_console.py", "win-data-map"],
    "domains": ["ops_console.py", "domains"],
    "dashboard": ["ops_console.py", "dashboard"],
    "inventory": ["ops_console.py", "inventory"],
    "junk": ["ops_console.py", "junk"],
}


def route(command: str, *args) -> dict:
    """Route lệnh qua gate -> inline handler -> fallback subprocess."""
    tool_check = f"cmd:{command}"
    if not check_tool(tool_check):
        return {
            "success": False,
            "blocked": True,
            "reason": f"Command '{command}' blocked by policy",
        }

    if command.startswith(("api:", "web:", "cloud:")):
        if not check_billing("external"):
            return {"success": False, "blocked": True, "reason": "Billing blocked"}

    # 1. Try inline handler first
    if command in INLINE_WITH_ARGS:
        try:
            text = " ".join(args) if args else ""
            result = INLINE_WITH_ARGS[command](text)
            log.info("Inline command '%s' succeeded", command)
            return result
        except Exception as e:
            log.error("Inline command '%s' failed: %s", command, e)
            return {"success": False, "error": str(e)}
    if command in INLINE_COMMANDS:
        try:
            result = INLINE_COMMANDS[command]()
            log.info("Inline command '%s' succeeded", command)
            return result
        except Exception as e:
            log.error("Inline command '%s' failed: %s", command, e)
            return {"success": False, "error": str(e)}

    # 2. Fallback to legacy subprocess
    if command in LEGACY_SUBPROCESS:
        script_cmd = LEGACY_SUBPROCESS[command]
        res = run_script(*script_cmd, *args)
        if not res.get("success"):
            res["note"] = "Subprocess mode. Run with Python installed for full functionality."
        return res

    # 3. Unknown
    all_cmds = sorted(INLINE_COMMANDS.keys()) + sorted(LEGACY_SUBPROCESS.keys())
    return {
        "success": False,
        "error": f"Unknown command: '{command}'. Available: {all_cmds}",
    }
