"""Test VoiceBox module."""
import sys, os, json, time
sys.path.insert(0, r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace")
from utils.voicebox import VoiceBox

vb = VoiceBox()

# 1. Check health
print("=== TEST VOICEBOX ===")
health = vb.health()
print(f"\n1. Health: {json.dumps(health, indent=2)}")

# 2. List models
models = vb.list_models()
print(f"\n2. Available models: {len(models)}")
for m in models:
    status = "DOWNL" if m.get('downloaded') else "     "
    status += " LOAD" if m.get('loaded') else "     "
    print(f"   [{status}] {m['model_name']} ({m['display_name']})")

# 3. Setup LuxTTS (CPU-friendly)
import time
import json

print("\n3. Trying setup with luxtts...")
t0 = time.time()
ok = vb.setup("luxtts")
print(f"   Result: {ok} ({time.time()-t0:.0f}s)")

if ok:
    # 4. Generate speech
    print("\n4. Generating speech...")
    t0 = time.time()
    try:
        result = vb.generate("Xin chao, toi la tro ly AI cua ban. Rat vui duoc gap ban!")
        print(f"   Result: {json.dumps(result, indent=2)[:500]}")
        gen_id = result.get('generation_id')
        if gen_id:
            # Save audio
            audio_dir = os.path.join(r"E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace", "media", "voicebox")
            os.makedirs(audio_dir, exist_ok=True)
            path = vb.save_audio(gen_id, os.path.join(audio_dir, "test_generation.wav"))
            print(f"   Audio saved to: {path}")
        print(f"   Time: {time.time()-t0:.1f}s")
    except Exception as e:
        print(f"   Error: {e}")

print("\n=== TEST COMPLETE ===")
