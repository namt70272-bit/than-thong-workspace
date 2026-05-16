import json, uuid, os

api_key = os.environ.get("GEMINI_API_KEY", "")
if not api_key:
    print("ERROR: Set GEMINI_API_KEY env var")
    exit(1)

workflow = {
    "id": str(uuid.uuid4()),
    "name": "Gemini 3 Flash (HTTP)",
    "nodes": [
        {
            "id": str(uuid.uuid4()),
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [250, 300],
            "parameters": {
                "httpMethod": "POST",
                "path": "gemini",
                "responseMode": "lastNode"
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Call Gemini API",
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.2,
            "position": [550, 300],
            "parameters": {
                "method": "POST",
                "url": f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3-flash-preview:generateContent?key={api_key}",
                "authentication": "none",
                "sendBody": True,
                "bodyParameters": {
                    "parameters": [
                        {
                            "name": "contents",
                            "value": "={{ [{ \"parts\": [{ \"text\": $json.body.prompt }] }] }}"
                        }
                    ]
                },
                "options": {
                    "response": {
                        "responseFormat": "json"
                    }
                }
            }
        },
        {
            "id": str(uuid.uuid4()),
            "name": "Parse & Respond",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1,
            "position": [800, 300],
            "parameters": {
                "respondWith": "json",
                "responseBody": "={{ { \"response\": $json.candidates[0].content.parts[0].text } }}"
            }
        }
    ],
    "connections": {
        "Webhook": {
            "main": [[{"node": "Call Gemini API", "type": "main", "index": 0}]]
        },
        "Call Gemini API": {
            "main": [[{"node": "Parse & Respond", "type": "main", "index": 0}]]
        }
    },
    "settings": {},
    "pinData": {}
}

with open(r"C:\Users\ACER\AppData\Local\Temp\n8n-gemini-http-workflow.json", "w") as f:
    json.dump([workflow], f, indent=2)
print("Workflow created:", workflow["id"])
