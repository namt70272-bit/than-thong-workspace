"""Test hoi with proper encoding at all levels"""
import subprocess, sys, json, time, os

exe = r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\packaging\dist\than-thong.exe"

def out(data):
    try:
        os.write(1, (data + '\n').encode('utf-8'))
    except:
        print(data)

print("=== hoi (may in bi loi) ===")
t0 = time.time()
try:
    r = subprocess.run(
        [exe, "hoi", "xin chao, ban la ai?"],
        capture_output=True, text=False, timeout=30,
    )
    elapsed = time.time() - t0
    out(f"Time: {elapsed:.1f}s")
    stdout = r.stdout.decode('utf-8', errors='replace')
    stderr = r.stderr.decode('utf-8', errors='replace')
    out("=== STDOUT ===")
    out(stdout[:4000] if stdout else "(empty)")
    out("=== STDERR ===")
    out(stderr[:500] if stderr else "(none)")
except subprocess.TimeoutExpired:
    out(f"TIMEOUT after {time.time()-t0:.0f}s")
except Exception as e:
    out(f"ERROR: {e}")
