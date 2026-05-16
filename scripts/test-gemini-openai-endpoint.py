import requests, os

# Test the OpenAI-compatible endpoint for Gemini
api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("ERROR: Set GEMINI_API_KEY env var")
    exit(1)

# Method 1: Bearer token
headers1 = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
payload = {
    "model": "gemini-3-flash-preview",
    "messages": [{"role": "user", "content": "Say hello in 5 words"}]
}
r1 = requests.post("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", json=payload, headers=headers1)
print(f"Method 1 (Bearer): {r1.status_code}")
if r1.status_code == 200:
    print(f"  Response: {r1.json()['choices'][0]['message']['content']}")
else:
    print(f"  Error: {r1.text[:200]}")

# Method 2: x-goog-api-key header
headers2 = {
    "x-goog-api-key": api_key,
    "Content-Type": "application/json"
}
r2 = requests.post("https://generativelanguage.googleapis.com/v1beta/openai/chat/completions", json=payload, headers=headers2)
print(f"\nMethod 2 (x-goog-api-key): {r2.status_code}")
if r2.status_code == 200:
    print(f"  Response: {r2.json()['choices'][0]['message']['content']}")
else:
    print(f"  Error: {r2.text[:200]}")

# Method 3: query parameter key
r3 = requests.post(f"https://generativelanguage.googleapis.com/v1beta/openai/chat/completions?key={api_key}", json=payload)
print(f"\nMethod 3 (query param): {r3.status_code}")
if r3.status_code == 200:
    print(f"  Response: {r3.json()['choices'][0]['message']['content']}")
else:
    print(f"  Error: {r3.text[:200]}")
