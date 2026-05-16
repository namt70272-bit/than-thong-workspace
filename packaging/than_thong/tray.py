"""Tray — system tray icon with right-click menu (tieng Viet)."""
import threading, sys, os, json
from pathlib import Path
from than_thong.config import config
from than_thong.logger import log
from than_thong.engine import engine
from than_thong.notifier import notifier
from than_thong.console import run_once, run_interactive


ICON_PATH = Path(__file__).parent / "resources" / "icon.png"


class TrayApp:
    """System tray icon với pystray."""

    def __init__(self):
        self._icon = None
        self._icon_image = self._load_icon()

    def _load_icon(self):
        try:
            from PIL import Image
            p = ICON_PATH
            if p.exists():
                return Image.open(p)
            img = Image.new("RGBA", (64, 64), (15, 23, 42, 255))
            return img
        except ImportError:
            return None

    def run(self):
        try:
            import pystray
        except ImportError:
            log.warning("thieu pystray; chay che do CLI")
            self._cli_mode()
            return

        if self._icon_image is None:
            log.warning("Khong co icon; chay CLI")
            self._cli_mode()
            return

        menu = pystray.Menu(
            pystray.MenuItem("Than Thong", None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Trang thai", self._action_status),
            pystray.MenuItem("Kiem tra cong", self._action_gate_test),
            pystray.MenuItem("Don dep Windows", self._action_cleanup),
            pystray.MenuItem("Mo dieu khien", self._action_console),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Cai dat",
                pystray.Menu(
                    pystray.MenuItem("Bat/Tat thong bao", self._toggle_notifications),
                    pystray.MenuItem("Khoi dong cung Windows", self._toggle_auto_start),
                    pystray.MenuItem("Xem cau hinh", self._action_config),
                ),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Khoi dong lai Engine", self._action_restart),
            pystray.MenuItem("Thoat", self._action_exit),
        )

        self._icon = pystray.Icon("than-thong", self._icon_image, "Than Thong", menu)
        engine.start()
        log.info("Tray app da chay")
        self._icon.run()

    def _cli_mode(self):
        """Fallback: khong co tray."""
        engine.start()
        print("Than Thong - che do CLI (khong co system tray)")
        print("   Ctrl+C de thoat\n")
        try:
            while True:
                import time
                time.sleep(1)
        except KeyboardInterrupt:
            engine.stop()

    def _action_status(self, icon=None, item=None):
        status = engine.get_status()
        msg = (
            f"Engine: {status['engine']}\n"
            f"Thoi gian chay: {status['uptime_seconds']}s\n"
            f"Da chan: {status['stats']['blocked']}\n"
            f"Da cho qua: {status['stats']['passed']}\n"
            f"Loi: {status['stats']['errors']}"
        )
        notifier.notify("Than Thong - Trang thai", msg, duration=5)

    def _action_gate_test(self, icon=None, item=None):
        from than_thong.router import route
        result = route("gate-test")
        ok = result.get("success", False)
        msg = "Cong OK" if ok else "Cong LOI: " + result.get('error', 'khong ro')
        notifier.notify("Kiem tra cong", msg, duration=3)

    def _action_cleanup(self, icon=None, item=None):
        notifier.notify("Don dep", "Dang don dep Windows...", duration=2)
        threading.Thread(target=self._run_cleanup, daemon=True).start()

    def _run_cleanup(self):
        result = engine.run_command("win-cleanup")
        if result.get("success"):
            freed = result.get("total_freed_mb", 0)
            notifier.notify("Don dep xong", "Da giai phong %.1f MB" % freed)
        else:
            notifier.notify("Don dep that bai", result.get("error", "khong ro"))

    def _action_console(self, icon=None, item=None):
        """Mo terminal moi voi console."""
        import subprocess
        python = sys.executable
        subprocess.Popen(
            [python, "-m", "than_thong", "console"],
            creationflags=subprocess.CREATE_NEW_CONSOLE,
        )

    def _toggle_notifications(self, icon=None, item=None):
        current = config.get("enable_notifications", True)
        config.set("enable_notifications", not current)
        icon.update_menu()
        notifier.notify("Thong bao", "BAT" if not current else "TAT", duration=2)

    def _toggle_auto_start(self, icon=None, item=None):
        current = config.get("auto_start", False)
        config.set("auto_start", not current)
        self._update_auto_start(not current)
        icon.update_menu()
        notifier.notify("Khoi dong cung Windows", "BAT" if not current else "TAT", duration=2)

    def _update_auto_start(self, enable: bool):
        """Them/xoa Startup shortcut."""
        import winshell
        from win32com.client import Dispatch
        startup = winshell.startup()
        link_path = Path(startup) / "Than Thong.lnk"
        if enable:
            exe = sys.executable
            ws = Dispatch("WScript.Shell")
            shortcut = ws.CreateShortcut(str(link_path))
            shortcut.TargetPath = str(exe)
            shortcut.Arguments = "-m than_thong"
            shortcut.WorkingDirectory = str(Path.cwd())
            shortcut.Description = "Than Thong - Cong kiem soat may tinh"
            shortcut.Save()
        else:
            if link_path.exists():
                link_path.unlink()

    def _action_config(self, icon=None, item=None):
        os.startfile(str(config.CONFIG_PATH))

    def _action_restart(self, icon=None, item=None):
        engine.stop()
        engine.start()
        notifier.notify("Engine", "Da khoi dong lai")

    def _action_exit(self, icon=None, item=None):
        engine.stop()
        if self._icon:
            self._icon.stop()
