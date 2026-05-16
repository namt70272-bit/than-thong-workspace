"""Analyze current config"""
import json

with open(r'C:\Users\ACER\.openclaw\openclaw.json', 'r') as f:
    cfg = json.load(f)

# Compaction
comp = cfg.get('agents', {}).get('defaults', {}).get('compaction', {})
print('=== COMPACTION ===')
for k, v in comp.items():
    key = str(k)
    val = str(v)
    print(f'  {key}: {val}')

# Bootstrap
boot = cfg.get('agents', {}).get('defaults', {})
print('\n=== BOOTSTRAP / CONTEXT ===')
for k in ['bootstrapMaxChars', 'bootstrapTotalMaxChars', 'contextInjection']:
    val = str(boot.get(k, 'N/A'))
    print(f'  {k}: {val}')

# Models
models = cfg.get('agents', {}).get('defaults', {}).get('model', {})
print('\n=== MODELS ===')
print(f'  Primary: {models.get("primary", "N/A")}')
fallbacks = models.get('fallbacks', [])
print(f'  Fallbacks ({len(fallbacks)}):')
for f in fallbacks:
    print(f'    - {f}')

# Session
session = cfg.get('session', {})
print('\n=== SESSION ===')
print(json.dumps(session, indent=2))
