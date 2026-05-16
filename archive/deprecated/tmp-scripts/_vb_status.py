"""Check VoiceBox status."""
import json, urllib.request

BASE = "http://127.0.0.1:17493"

def get(path, timeout=5):
    try:
        r = urllib.request.urlopen(f"{BASE}{path}", timeout=timeout)
        return json.loads(r.read().decode())
    except Exception as e:
        return {"error": str(e)}

print("=== VOICEBOX STATUS ===")
print("Health:", json.dumps(get("/health"), indent=2))
print()

models = get("/models/status").get("models", [])
print("Models:")
for m in models:
    d = "DN" if m["downloaded"] else "  "
    l = "LD" if m["loaded"] else "  "
    print(f"  [{d}{l}] {m['model_name']:30s} {m['display_name']}")

print()
print("Active tasks:", json.dumps(get("/tasks/active"), indent=2))
