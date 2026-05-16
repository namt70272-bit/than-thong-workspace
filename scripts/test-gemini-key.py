import json, requests, os

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("ERROR: Set GEMINI_API_KEY env var or create .env file")
    exit(1)

# Test with correct model name - gemini-3-flash-preview
models_to_test = [
    "gemini-3-flash-preview",
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite", 
    "gemini-2.5-pro",
]

for model in models_to_test:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    payload = {"contents": [{"parts": [{"text": "Say hello in 3 words"}]}]}
    r = requests.post(url, json=payload)
    if r.status_code == 200:
        text = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        print(f"[OK] {model}: {text}")
    else:
        err = r.json().get("error", {}).get("message", "unknown")
        print(f"[--] {model}: {err[:80]}")
