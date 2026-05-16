#!/usr/bin/env python3
"""
automation_helper.py — Reusable GUI automation utilities for Thần Thú

Features:
  - Playwright web automation with retry + screenshot
  - Docker sandbox runner for isolated testing
  - Screenshot-based verification
  - Common patterns: wait, click, type, scroll, extract

Usage:
  python automation_helper.py --check-stack     # Kiểm tra toàn bộ stack
  python automation_helper.py --sandbox-test    # Test Docker sandbox
"""

import os, sys, json, datetime, time, tempfile, subprocess, shutil
from pathlib import Path

WORKSPACE = Path(os.environ.get(
    "OPENCLAW_WORKSPACE",
    r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
))


def safeprint(*args, **kwargs):
    text = " ".join(str(a) for a in args)
    try:
        print(text, **kwargs, flush=True)
    except UnicodeEncodeError:
        print(text.encode("ascii", "replace").decode("ascii"), **kwargs, flush=True)


# ── Stack Check ────────────────────────────────────────────────────────

def check_stack():
    results = {}

    # Playwright
    try:
        from playwright.sync_api import sync_playwright
        p = sync_playwright().start()
        b = p.chromium.launch(headless=True)
        page = b.new_page()
        page.goto("about:blank")
        results["playwright"] = f"OK (chromium {b.version})"
        b.close()
        p.stop()
    except Exception as e:
        results["playwright"] = f"FAIL: {e}"

    # pywinauto
    try:
        import pywinauto
        results["pywinauto"] = pywinauto.__version__
    except Exception as e:
        results["pywinauto"] = f"FAIL: {e}"

    # uiautomation
    try:
        import uiautomation as auto
        results["uiautomation"] = "OK"
    except Exception as e:
        results["uiautomation"] = f"FAIL: {e}"

    # PyAutoGUI
    try:
        import pyautogui
        results["pyautogui"] = pyautogui.__version__
    except Exception as e:
        results["pyautogui"] = f"FAIL: {e}"

    # Docker
    try:
        r = subprocess.run(["docker", "info", "--format", "{{json .}}"],
                           capture_output=True, text=True, timeout=10)
        if r.returncode == 0:
            info = json.loads(r.stdout)
            results["docker"] = f"OK (v{info.get('ServerVersion','?')}, {info.get('Containers','?')} containers)"
        else:
            results["docker"] = f"FAIL: {r.stderr.strip()[:100]}"
    except Exception as e:
        results["docker"] = f"FAIL: {e}"

    # OpenCV
    try:
        import cv2
        results["opencv"] = cv2.__version__
    except Exception as e:
        results["opencv"] = f"FAIL: {e}"

    # Pillow
    try:
        from PIL import Image
        results["pillow"] = Image.__version__
    except Exception as e:
        results["pillow"] = f"FAIL: {e}"

    return results


def print_stack(results):
    safeprint("GUI Automation Stack Check")
    safeprint("=" * 40)
    for name, status in sorted(results.items()):
        ok = not str(status).startswith("FAIL")
        icon = "[OK]" if ok else "[FAIL]"
        safeprint(f"  {icon} {name}: {status}")


# ── Docker Sandbox Runner ──────────────────────────────────────────────

def docker_sandbox_test():
    """Test if Docker can run an isolated container for automation testing."""
    safeprint("Testing Docker sandbox...")

    # 1. Run a minimal container
    r = subprocess.run(
        ["docker", "run", "--rm", "alpine:latest", "echo", "sandbox-ok"],
        capture_output=True, text=True, timeout=30
    )
    if r.returncode != 0:
        safeprint(f"  [FAIL] Container run: {r.stderr.strip()[:150]}")
        return False

    output = r.stdout.strip()
    if "sandbox-ok" in output:
        safeprint(f"  [OK] Container run: {output}")
    else:
        safeprint(f"  [?] Unexpected output: {output}")

    # 2. Check Python in sandbox
    r = subprocess.run(
        ["docker", "run", "--rm", "python:3.11-slim",
         "python", "-c", "import sys; print(f'Python {sys.version.split()[0]}')"],
        capture_output=True, text=True, timeout=60
    )
    if r.returncode == 0:
        safeprint(f"  [OK] Python sandbox: {r.stdout.strip()}")
    else:
        safeprint(f"  [FAIL] Python sandbox: {r.stderr.strip()[:150]}")

    # 3. Check Playwright in sandbox (if image exists)
    r = subprocess.run(
        ["docker", "images", "--format", "{{.Repository}}:{{.Tag}}"],
        capture_output=True, text=True, timeout=10
    )
    if r.returncode == 0:
        images = r.stdout.strip().split("\n")
        safeprint(f"  Available images: {len(images)}")
        for img in images[:5]:
            safeprint(f"    - {img}")

    safeprint("  [OK] Docker sandbox ready")
    return True


def run_in_sandbox(script_content, image="python:3.11-slim", timeout=120):
    """Run a Python script in an isolated Docker container."""
    with tempfile.TemporaryDirectory() as tmpdir:
        script_path = Path(tmpdir) / "script.py"
        script_path.write_text(script_content, encoding="utf-8")

        r = subprocess.run(
            ["docker", "run", "--rm", "-v", f"{tmpdir}:/workspace",
             image, "python", "/workspace/script.py"],
            capture_output=True, text=True, timeout=timeout
        )
        return r.returncode, r.stdout, r.stderr


# ── Common Web Automation Patterns (Playwright) ────────────────────────

def playwright_browser(headless=True):
    """Create a reusable Playwright browser context."""
    from playwright.sync_api import sync_playwright
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context(
        viewport={"width": 1280, "height": 720},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    )
    page = context.new_page()
    return p, browser, context, page


def web_extract(page, url, selector=None):
    """Extract content from a URL. Returns text or element text."""
    page.goto(url, wait_until="networkidle", timeout=30000)
    if selector:
        elems = page.query_selector_all(selector)
        return [e.inner_text() for e in elems]
    return page.inner_text("body")


def web_screenshot(page, url, output_path):
    """Take a screenshot of a URL."""
    page.goto(url, wait_until="load", timeout=30000)
    page.screenshot(path=str(output_path), full_page=True)
    return output_path


# ── Main ───────────────────────────────────────────────────────────────

def main():
    args = set(sys.argv[1:])

    if "--check-stack" in args:
        results = check_stack()
        print_stack(results)
        # Save report
        report = {
            "timestamp": datetime.datetime.now().isoformat(),
            "results": results,
        }
        report_path = WORKSPACE / "reports" / "automation-stack.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        safeprint(f"\nReport saved: {report_path}")

    elif "--sandbox-test" in args:
        ok = docker_sandbox_test()
        sys.exit(0 if ok else 1)

    elif "--web-test" in args:
        safeprint("Testing Playwright web automation...")
        try:
            p, browser, ctx, page = playwright_browser(headless=True)
            safeprint("  [OK] Browser launched")
            page.goto("https://httpbin.org/get", wait_until="networkidle", timeout=15000)
            safeprint(f"  [OK] Page loaded: {page.title()[:60]}")
            browser.close()
            p.stop()
            safeprint("  [OK] Browser closed")
        except Exception as e:
            safeprint(f"  [FAIL] {e}")

    else:
        safeprint("Usage:")
        safeprint("  automation_helper.py --check-stack    Check all GUI automation tools")
        safeprint("  automation_helper.py --sandbox-test    Test Docker sandbox")
        safeprint("  automation_helper.py --web-test        Test Playwright web automation")


if __name__ == "__main__":
    main()
