"""Service — Windows Service wrapper."""
import sys, os, time, threading
from pathlib import Path
from than_thong.engine import engine
from than_thong.logger import log


class ThanThongService:
    """Wrapper để chạy dưới dạng Windows Service."""

    def __init__(self):
        self._running = False

    def start(self):
        log.info("Service starting...")
        engine.start()
        self._running = True
        log.info("Service started")
        while self._running:
            time.sleep(5)

    def stop(self):
        log.info("Service stopping...")
        self._running = False
        engine.stop()
        log.info("Service stopped")

    def install(self):
        """Install as Windows Service using pywin32."""
        try:
            import win32serviceutil
            import servicemanager
            import win32service
        except ImportError:
            log.error("pywin32 required for service support. pip install pywin32")
            return False

        # This would be expanded with actual service class
        log.info("Service installation requires pywin32 ServiceFramework class")
        return False

    @staticmethod
    def cmd_install():
        svc = ThanThongService()
        return svc.install()

    @staticmethod
    def cmd_remove():
        log.info("Service removal not yet implemented")
