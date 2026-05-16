"""Quick test for than-thong AI integration"""
import subprocess, sys, json

exe = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\packaging\dist\than-thong.exe"

for cmd in ["ai", "kiem-tra-cong"]:
    print(f"\n=== {cmd} ===")
    try:
        r = subprocess.run([exe, cmd], capture_output=True, text=True, timeout=15)
        print("STDOUT:", r.stdout[:2000] if r.stdout else "(empty)")
        print("STDERR:", r.stderr[:500] if r.stderr else "(none)")
    except subprocess.TimeoutExpired:
        print("TIMEOUT after 15s")
    except Exception as e:
        print(f"ERROR: {e}")
