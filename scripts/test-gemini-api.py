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
print("[OK] Token from SA:", creds.service_account_email)

# Test: Gemini API (generativelanguage) - try with SA token
import urllib.request

url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent"
req_data = json.dumps({"contents": [{"parts": [{"text": "Say hello in 5 words"}]}]}).encode()
req = urllib.request.Request(url, data=req_data, headers={
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
})

try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    print("[OK] Gemini API via SA token:", text)
except urllib.error.HTTPError as e:
    body = json.loads(e.read())
    print(f"[FAIL] Gemini API: {e.code}")
    print(json.dumps(body, indent=2))

# Alternative: test with API key approach
print("\n--- Alternative: Gemini API with API key ---")
api_key_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash:generateContent"
print(f"If using API key: GET {api_key_url}?key=YOUR_API_KEY")
print("Get free API key at: https://aistudio.google.com/app/apikey")
