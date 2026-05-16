import json, requests, sys
from google.oauth2 import service_account
from google.auth.transport.requests import Request as AuthRequest

key_path = r'E:\KY-DATA\OpenClaw\runtime-mirror\.openclaw\workspace\config\gcp-n8n-vertex-ai-key.json'

creds = service_account.Credentials.from_service_account_file(
    key_path,
    scopes=["https://www.googleapis.com/auth/cloud-platform"]
)
creds.refresh(AuthRequest())
token = creds.token
print("[OK] Token obtained:", creds.service_account_email)

# Direct generateContent test for Gemini 3 Flash
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
test_url = "https://us-central1-aiplatform.googleapis.com/v1/projects/gen-lang-client-0477618387/locations/us-central1/publishers/google/models/gemini-3-flash:generateContent"
payload = {"contents": [{"parts": [{"text": "Say hello in 5 words"}]}]}

r = requests.post(test_url, json=payload, headers=headers)
if r.status_code == 200:
    result = r.json()
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    print("[OK] Gemini 3 Flash responds:", text)
else:
    print(f"[FAIL] Status {r.status_code}: {r.text[:500]}")
