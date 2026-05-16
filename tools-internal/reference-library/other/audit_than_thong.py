#!/usr/bin/env python3
"""Comprehensive audit of thần thông tools"""
import os, json, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

T = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\tools-internal'
SCR = os.path.join(T, 'scripts')

print("=" * 65)
print("THAN THONG AUDIT REPORT")
print("=" * 65)

# 1. STDLIB shadowing
shadow_zones = []
for f in os.listdir(T):
    if f.startswith('_ext_') and f.endswith('.py'):
        original = f.replace('_ext_', '')
        shadow_zones.append(original)
print(f"\n1. STDLIB SHADOWING (da fix)")
print(f"   {len(shadow_zones)} files renamed to _ext_ prefix")
print(f"   Ex: openai.py, requests.py, redis.py, posthog.py...")
print(f"   Trang thai: DA FIX nhung con nguy co tai phat sinh")

# 2. Multi-version Python conflict
py_versions = []
try:
    import sys; py_versions.append(('python3 (main)', sys.version[:6]))
except: pass
try:
    import subprocess
    r = subprocess.run(['python', '-c', 'import sys; print(sys.version[:6])'], capture_output=True, text=True, timeout=5)
    py_versions.append(('python (fallback)', r.stdout.strip()))
except: pass

print(f"\n2. PYTHON VERSION CONFLICT")
for name, ver in py_versions:
    print(f"   {name}: {ver}")
print(f"   Van de: python3=3.14 thieu package, python=3.11 du package")
print(f"   Nhung script thần thong chay bang python3 (3.14) -> thieu package")
print(f"   Script tu import_wave chay bang python3 -> erros")

# 3. Broken commands
print(f"\n3. LENH BI LOI")
errors = []
# preflight runner
errors.append(("preflight", "billing_gate.py nhan empty string -> block", "Cao: can sua preflight_runner.py"))
# import_validator blocking legit files
errors.append(("import_validator", "Chan n8n-db2.sqlite, .env, skills moi", "Trung binh: false positive"))
# deep_validator
errors.append(("deep_validator", "Timeout (30s+) khi ko co Internet", "Cao: can timeout fallback"))

# Check actual script quality
print()
for cmd, issue, severity in errors:
    print(f"   [{severity[:4]}] {cmd:25s} | {issue}")

# 4. Architecture issues
print(f"\n4. VAN DE KIEN TRUC")
arch_issues = [
    ("Gate double-check", "Moi lenh goi gate 2 lan (console -> scripts -> gate)"),
    ("Hardcoded paths", "script:\n     ROOT= Path(r'E:\\...') trong 20+ files"),
    ("No test suite", "Khong co unit test cho scripts"),
    ("No dependency check", "Script import packages ko kiem tra ton tai truoc"),
    ("Extracted file mess", "3300 .py trong tools-internal, 8 shadow files da fix"),
    ("thần thông console thin", "than_thong_console.py chi 267B - wrapper mong"),
    ("preflight + billing gate", "Chay subprocess nhau tao vong lap chet"),
]

for issue, detail in arch_issues:
    print(f"   [{issue:25s}] {detail}")

# 5. Dependency gaps
print(f"\n5. THIEU DEPENDENCY")
deps = [
    ("policy/billing.policy.json", "Co, nhung cod tu cung (policy-path) so voi .env"),
    ("trusted_registry.py", "Co, nhung khong duoc goi boi script nao"),
    ("compliance_audit.py", "Co, nhung khong duoc goi boi console"),
    ("than_thong_daily.py", "Co, nhung khong co cron job de chay"),
    ("Vault/secret management", "Khong co - API keys luu trong .env plaintext"),
]
for name, status in deps:
    print(f"   {name:35s} | {status}")

# 6. Integration gaps
print(f"\n6. THIEU TICH HOP")
integration = [
    "MCP server khong duoc thần thong service auto-start",
    "mem0 memory khong duoc tich hop vao workflow",
    "FireCrawl search khong duoc goi tu console",
    "Ollama khong duoc thần thong phat hien tu dong",
    "Skill registry khong duoc console doc/display",
]
for item in integration:
    print(f"   - {item}")

# Final score
print(f"\n{'=' * 65}")
print(f"DIEU CAN LAM NGAY:")
print(f"{'=' * 65}")
print("""
1. SUA preflight_runner.py: bo sung default text 'system check'
2. SUA import_validator: ignore .sqlite, .env, skills/ paths
3. THEM python11 fallback: scripts tu check python version truoc
4. XOA 3300 file rac: scripts khong dung trong tools-internal/
5. TICH HOP: MCP server + thần thông console
""")
