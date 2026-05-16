#!/usr/bin/env python
"""Python version helper: detect & recommend best Python interpreter"""
import sys
import subprocess
from pathlib import Path

# Minimum Python version for modern packages
REQUIRED_VERSION = (3, 11)

def get_version_tuple(version_str: str):
    parts = version_str.split(".")
    try:
        return tuple(int(p) for p in parts[:3])
    except:
        return (0, 0, 0)

def check_current():
    """Check if current Python meets requirements"""
    v = sys.version_info
    if v >= REQUIRED_VERSION:
        return {"ok": True, "version": f"{v.major}.{v.minor}.{v.micro}", "interpreter": sys.executable}
    return {"ok": False, "version": f"{v.major}.{v.minor}.{v.micro}", "interpreter": sys.executable}

def find_best_python():
    """Find the best available Python on this system"""
    candidates = ["python", "python", "python3.11", "python3.12", "python3.13"]
    best = None
    best_version = (0, 0, 0)
    
    for cmd in candidates:
        try:
            r = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
            ver_str = r.stdout.strip() or r.stderr.strip()
            # Parse "Python 3.11.9" 
            for part in ver_str.split():
                if part[0].isdigit():
                    v = get_version_tuple(part)
                    if v >= REQUIRED_VERSION and v > best_version:
                        best_version = v
                        best = cmd
                        break
        except:
            pass
    
    return {"best": best, "version": ".".join(str(x) for x in best_version) if best_version > (0,0,0) else None}

def run_with_best_python(script_path: str, *args):
    """Run a script with the best available Python"""
    info = find_best_python()
    if not info["best"]:
        # Fallback to current
        return subprocess.run([sys.executable, script_path, *args], capture_output=True, text=True)
    return subprocess.run([info["best"], script_path, *args], capture_output=True, text=True)

if __name__ == "__main__":
    current = check_current()
    best = find_best_python()
    print(f"Current: Python {current['version']} at {current['interpreter']}")
    print(f"Best:    Python {best['version']} via '{best['best']}'")
    print(f"Status:  {'OK' if current['ok'] else 'NEED UPGRADE'}")
