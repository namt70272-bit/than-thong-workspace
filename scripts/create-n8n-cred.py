import uuid, os

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("ERROR: Set GEMINI_API_KEY env var")
    exit(1)

cred = [
  {
    "id": str(uuid.uuid4()),
    "name": "Google AI - Gemini 3 Flash",
    "type": "googleAi",
    "data": {
      "apiKey": api_key
    }
  }
]

import json
with open(r"C:\Users\ACER\AppData\Local\Temp\n8n-google-ai-cred.json", "w") as f:
    json.dump(cred, f, indent=2)
print("Created cred with ID:", cred[0]["id"])
