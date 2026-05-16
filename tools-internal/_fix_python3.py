#!/usr/bin/env python
"""Fix python3 -> python in all thần thông scripts"""
import os, re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

T = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
SCR = os.path.join(T, 'scripts')

all_targets = []

# Scan all .py files in scripts/ and tools-internal root
for root, dirs, files in os.walk(T):
    for f in files:
        if not f.endswith('.py'): continue
        if f.startswith('_ext_') or f.startswith('_ext'): continue
        fp = os.path.join(root, f)
        try:
            c = open(fp, 'rb').read().decode('utf-8', errors='replace')
            if '"python"' in c or "'python'" in c:
                all_targets.append((fp, c))
        except: pass

print(f"Found {len(all_targets)} files with hardcoded 'python'")

# Fix each file
fixed = 0
shebang_fixed = 0
for fp, c in all_targets:
    original = c
    
    # Fix shebang
    c = c.replace('#!/usr/bin/env python', '#!/usr/bin/env python')
    if c != original: shebang_fixed += 1
    
    # Fix subprocess calls: "python" -> sys.executable or "python"
    # For scripts that are in the SCRIPTS dir and call each other
    rel = os.path.relpath(fp, T)
    
    if os.path.dirname(fp) == SCR:
        # Scripts that call other scripts -> use sys.executable
        # But we'll use "python" which points to 3.11
        c = c.replace('"python"', '"python"')
        c = c.replace("'python'", "'python'")
    else:
        c = c.replace('"python"', '"python"')
        c = c.replace("'python'", "'python'")
    
    if c != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(c)
        fixed += 1
        if fixed <= 10:
            print(f"  Fixed: {rel}")

print(f"\nResults:")
print(f"  Shebangs fixed: {shebang_fixed}")
print(f"  Subprocess calls fixed: {fixed}")

# Verify the fix
print(f"\nVerifying: checking for remaining 'python' hardcode...")
remaining = []
for root, dirs, files in os.walk(T):
    for f in files:
        if not f.endswith('.py'): continue
        fp = os.path.join(root, f)
        try:
            c = open(fp, 'rb').read().decode('utf-8', errors='replace')
            if '"python"' in c or "'python'" in c:
                remaining.append(os.path.relpath(fp, T))
        except: pass

if remaining:
    print(f"  REMAINING: {len(remaining)} files")
    for f in remaining:
        print(f"    {f}")
else:
    print(f"  NONE - all clean!")
