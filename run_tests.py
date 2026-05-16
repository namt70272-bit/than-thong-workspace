#!/usr/bin/env python3
"""
Run all tests for the workspace.

Usage:
  python run_tests.py              # Run all tests
  python run_tests.py --unit       # Unit tests only (no Docker)
  python run_tests.py --docker     # Docker sandbox tests
  python run_tests.py --verbose    # Verbose output
"""

import sys
import os
import subprocess

WORKSPACE = os.environ.get(
    "OPENCLAW_WORKSPACE",
    r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace"
)
TESTS_DIR = os.path.join(WORKSPACE, "tests")


def run_pytest(args, label):
    """Run pytest with given args."""
    # Run from workspace root, tests/ is found by pytest discovery
    cmd = [sys.executable, "-m", "pytest"] + args
    print(f"[{label}] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    return result.returncode


def main():
    args = set(sys.argv[1:])
    verbose = "--verbose" in args
    docker = "--docker" in args
    unit = "--unit" in args

    exit_code = 0

    # 1. Unit tests (no Docker)
    if unit or not docker:
        pytest_args = ["-v"] if verbose else []
        pytest_args += ["tests/"]
        rc = run_pytest(pytest_args, "UNIT")
        if rc != 0:
            exit_code = rc

    # 2. Docker sandbox test (explicit)
    if docker or (not unit and not args - {"--verbose", "--docker"}):
        print("[DOCKER] Testing sandbox isolation...")
        rc_docker = subprocess.run([
            sys.executable,
            os.path.join(WORKSPACE, "tools-internal", "scripts", "automation_helper.py"),
            "--sandbox-test"
        ], capture_output=True, text=True, timeout=120)
        if rc_docker.stdout:
            print(rc_docker.stdout)
        if rc_docker.returncode != 0:
            print(f"[DOCKER] FAIL (exit {rc_docker.returncode})")
            exit_code = rc_docker.returncode
        else:
            print("[DOCKER] Sandbox test: OK")

    if exit_code == 0:
        print("\n[OK] All tests passed")
    else:
        print(f"\n[FAIL] Some tests failed (exit {exit_code})")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
