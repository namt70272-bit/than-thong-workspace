"""Tests for automation_helper.py"""

import pytest
import sys
import os

scripts_dir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    "tools-internal", "scripts"
)
sys.path.insert(0, scripts_dir)

import automation_helper as ah


class TestStackCheck:
    def test_check_stack_returns_all_keys(self):
        results = ah.check_stack()
        expected_keys = {"playwright", "pywinauto", "uiautomation",
                         "pyautogui", "docker", "opencv", "pillow"}
        assert expected_keys.issubset(set(results.keys()))

    def test_check_stack_all_ok(self):
        results = ah.check_stack()
        for name, status in results.items():
            assert not str(status).startswith("FAIL"), f"{name}: {status}"

    def test_docker_info(self):
        results = ah.check_stack()
        assert results["docker"].startswith("OK")
        assert "containers" in results["docker"].lower() or "v" in results["docker"]


class TestRunInSandbox:
    def test_run_hello_in_sandbox(self):
        code = "print('hello from sandbox')"
        rc, stdout, stderr = ah.run_in_sandbox(code, timeout=30)
        assert rc == 0
        assert "hello from sandbox" in stdout
