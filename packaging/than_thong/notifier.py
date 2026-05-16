"""Thong bao — toast notification Windows, tieng Viet."""
import threading, time
from than_thong.config import config
from than_thong.logger import log


class Notifier:
    """Thong bao he thong. In ra console neu khong co GUI."""

    def __init__(self):
        self._enabled = config.get("enable_notifications", True)
        self._notify = None
        self._try_init()

    def _try_init(self):
        try:
            import plyer.platforms.win.notification  # force load platform
            from plyer import notification
            self._notify = notification.notify
        except Exception as e:
            log.warning("Khong the tai plyer: %s; thu win10toast...", e)
            try:
                from win10toast import ToastNotifier
                self._toaster = ToastNotifier()
                self._notify = self._win10toast_wrapper
            except (ImportError, ModuleNotFoundError) as e2:
                log.warning("Khong co thu vien thong bao (%s); dung print", e2)
                self._notify = self._print_fallback

    def _win10toast_wrapper(self, title, message, duration=5, **kw):
        try:
            self._toaster.show_toast(title, message, duration=duration, threaded=True)
        except Exception:
            self._print_fallback(title, message)

    def _print_fallback(self, title, message, **kw):
        log.info("[THONG BAO] %s: %s", title, message)

    def thong_bao(self, tieu_de: str, noi_dung: str, thoi_gian: int = 5):
        if not self._enabled:
            return
        try:
            self._notify(title=tieu_de, message=noi_dung, timeout=thoi_gian)
        except Exception as e:
            log.warning("Thong bao that bai: %s", e)

    def canh_bao_chan(self, cong_cu: str):
        self.thong_bao(
            "Than Thong - Da chan",
            "Cong cu '%s' bi chan theo chinh sach" % cong_cu,
            thoi_gian=3,
        )

    def canh_bao_qua_cong(self, lenh: str):
        self.thong_bao(
            "Than Thong - Cho qua",
            "Lenh '%s' da qua cong" % lenh,
            thoi_gian=2,
        )


notifier = Notifier()
