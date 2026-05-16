import json

# Read E: config
cfg_path = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\openclaw.json'
with open(cfg_path, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

# Read .env
env_path = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\.env'
with open(env_path, 'r') as f:
    env_content = f.read()

# Extract all keys
providers = cfg.get('models', {}).get('providers', {})
for name, p in providers.items():
    k = p.get('apiKey', '')
    print('%s apiKey: len=%d val=%s' % (name, len(k), repr(k)))

# Gateway auth
auth = cfg.get('gateway', {}).get('auth', {})
print('gateway auth token: %s' % repr(auth.get('token', '')))
print('gateway auth mode: %s' % auth.get('mode', ''))

# Telegram
tele = cfg.get('channels', {}).get('telegram', {})
for aname, ainfo in tele.get('accounts', {}).items():
    bt = ainfo.get('botToken', '')
    print('telegram %s botToken: len=%d val=%s' % (aname, len(bt), repr(bt)))

# .env content
print()
print('.env content:')
print(env_content)
