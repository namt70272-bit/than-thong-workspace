"""App — main entry point for the than-thong desktop application.

Usage:
  python -m than_thong              # Start tray app
  python -m than_thong --cli        # CLI mode (console)
  python -m than_thong console      # Interactive console
  python -m than_thong <command>    # Run one command
"""
import sys, os, json, argparse
from pathlib import Path

# Uu tien print() dung duoc tieng Viet
try:
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
except Exception:
    pass


def ensure_deps():
    """Báo nếu thiếu dependency."""
    missing = []
    try:
        import pystray
    except ImportError:
        missing.append("pystray")
    try:
        from PIL import Image
    except ImportError:
        missing.append("Pillow")
    try:
        import winshell
    except ImportError:
        missing.append("winshell")
    if missing:
        print("[WARN] Thieu goi: %s" % ', '.join(missing))
        print("   pip install %s" % ' '.join(missing))
        return False
    return True


def main():
    parser = argparse.ArgumentParser(description="Than Thong - Cong Kiem Soat May Tinh")
    parser.add_argument("mode", nargs="?", default="gui",
                        help="gui (mac dinh) | cli | console | <lenh>")
    parser.add_argument("args", nargs="*", help="Tham so cho lenh")
    args = parser.parse_args()

    mode = args.mode
    extra = args.args

    if mode in ("cli", "--cli"):
        from than_thong.engine import engine
        from than_thong.tray import TrayApp
        app = TrayApp()
        app._cli_mode()

    elif mode in ("console", "--console", "dieu-khien"):
        from than_thong.console import run_interactive
        run_interactive()

    elif mode in ("gui", "--gui", ""):
        if not ensure_deps():
            sys.exit(1)
        from than_thong.tray import TrayApp
        app = TrayApp()
        app.run()

    elif mode == "service":
        from than_thong.service import ThanThongService
        svc = ThanThongService()
        if extra and extra[0] in ("install", "cai-dat"):
            svc.install()
        else:
            svc.start()

    else:
        from than_thong.console import run_once
        sys.exit(run_once(mode, *extra))


if __name__ == "__main__":
    main()
