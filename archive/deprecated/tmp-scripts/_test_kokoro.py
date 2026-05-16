"""Test VoiceBox with Kokoro (already downloaded, CPU-friendly)."""
import sys, os, json, time
sys.path.insert(0, r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
from utils.voicebox import VoiceBox

BASE = "http://127.0.0.1:17493"
vb = VoiceBox()

# Kokoro is already downloaded (82M params, CPU-friendly)
MODEL = "kokoro"
print(f"=== VOICEBOX TEST WITH {MODEL} ===")

# 1. Just load kokoro (no download needed)
print(f"\n1. Loading {MODEL}...")
t0 = time.time()
try:
    result = vb.load_model(MODEL)
    print(f"   Load result: {json.dumps(result, indent=2)[:300]}")
    print(f"   Time: {time.time()-t0:.1f}s")
except Exception as e:
    print(f"   Error loading: {e}")
    # Maybe already loading
    pass

# 2. Check if loaded
print(f"\n2. Checking model status...")
for _ in range(30):
    m = vb.list_models()
    target = next((x for x in m if x["model_name"] == MODEL), None)
    if target and target.get("loaded"):
        print(f"   {MODEL} is LOADED!")
        break
    time.sleep(2)
else:
    print(f"   {MODEL} not loaded after 60s")
    # Try without loading (maybe auto-loads on request)
    pass

# 3. Generate speech
print(f"\n3. Generating speech...")
t0 = time.time()
try:
    result = vb.generate("Hello! I am your AI assistant. Nice to meet you!")
    print(f"   Result keys: {list(result.keys())}")
    print(f"   Result: {json.dumps(result, indent=2)[:500]}")

    gen_id = result.get("generation_id")
    if gen_id:
        audio_dir = os.path.join(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace", "media", "voicebox")
        os.makedirs(audio_dir, exist_ok=True)
        path = vb.save_audio(gen_id, os.path.join(audio_dir, "kokoro_test.wav"))
        print(f"   Audio saved: {path}")
        print(f"   File size: {os.path.getsize(path)} bytes")

    print(f"   Time: {time.time()-t0:.1f}s")
except Exception as e:
    print(f"   Error: {e}")

# 4. Check health
print(f"\n4. Post-generation health:")
h = vb.health()
print(f"   Model loaded: {h.get('model_loaded')}")
print(f"   Backend: {h.get('backend_type')} / {h.get('backend_variant')}")

print(f"\n=== TEST COMPLETE ===")
