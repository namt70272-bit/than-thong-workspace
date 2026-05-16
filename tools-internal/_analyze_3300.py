#!/usr/bin/env python3
"""Phan tich chi tiet 3300 files trong tools-internal"""
import os, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

T = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
all_py = [f for f in os.listdir(T) if f.endswith('.py') and not f.startswith('_') and not f.startswith('_ext')]

# Size
tiny = sum(1 for f in all_py if os.path.getsize(os.path.join(T,f)) < 1024)
small = sum(1 for f in all_py if 1024 <= os.path.getsize(os.path.join(T,f)) < 5120)
med = sum(1 for f in all_py if 5120 <= os.path.getsize(os.path.join(T,f)) < 20480)
large = sum(1 for f in all_py if 20480 <= os.path.getsize(os.path.join(T,f)) < 102400)
xlarge = sum(1 for f in all_py if os.path.getsize(os.path.join(T,f)) >= 102400)

print("=== SIZE ===")
print(f"  <1KB (tiny/empty):   {tiny}")
print(f"  1-5KB (small util):  {small}")
print(f"  5-20KB (medium):     {med}")
print(f"  20-100KB (large):    {large}")
print(f"  >=100KB (xlarge):    {xlarge}")

# Find files with real logic
has_logic = []
empty_files = []
test_only = []
for f in all_py:
    sz = os.path.getsize(os.path.join(T,f))
    if sz < 100:
        empty_files.append(f)
        continue
    try:
        c = open(os.path.join(T,f), 'rb').read().decode('utf-8', errors='replace')
        if 'def ' in c or 'class ' in c or ('import ' in c and ';' not in c[:20]):
            has_logic.append(f)
        else:
            test_only.append(f)
    except:
        empty_files.append(f)

print()
print("=== REAL CONTENT ===")
print(f"  Co logic that (def/class/import): {len(has_logic)}")
print(f"  Empty/rung (<100 bytes):          {len(empty_files)}")
print(f"  Test/data/other:                  {len(test_only)}")
print(f"  TOTAL:                            {len(all_py)}")

# Kiem tra xem co bao nhieu file test_* that su co gia tri
test_with_logic = [f for f in all_py if f.startswith('test_') and f in has_logic]
test_empty = [f for f in all_py if f.startswith('test_') and f in empty_files]
print()
print(f"  Trong 923 test_* files:")
print(f"    Co logic that:  {len(test_with_logic)}")
print(f"    Rong (<100B):   {len(test_empty)}")

# Show examples of valuable files
print()
print("=== 10 FILE CO GIA TRI NHAT (lon + logic) ===")
valuable = [(os.path.getsize(os.path.join(T,f)), f) for f in has_logic]
valuable.sort(reverse=True)
for sz, f in valuable[:10]:
    kb = sz // 1024
    print(f"  {kb:5d}KB  {f}")

# Show garbage examples
print()
print("=== 10 FILE RAC VI ENH (nho, test, vo dung) ===")
for f in sorted(empty_files)[:10]:
    sz = os.path.getsize(os.path.join(T,f))
    print(f"  {sz:5d}B  {f}")

# Final verdict
print()
print("=== KET LUAN ===")
print(f"  GIA TRI THUC: {len(has_logic)} files (co the dung lai)")
print(f"  RAC/RUNG:     {len(empty_files)} files (xoa duoc)")
print(f"  TEST FILES:   {len(test_only)} files (da co logic can giu, con lai xoa)")
print()
print(f"  De xuat: Giu {len(has_logic)} file co gia tri, xoa ~{len(empty_files) + len(test_only) - 200} file rac")
