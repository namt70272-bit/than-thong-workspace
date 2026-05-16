import json, uuid

workflow_id = str(uuid.uuid4())
webhook_id = str(uuid.uuid4())
gemini_id = str(uuid.uuid4())
respond_id = str(uuid.uuid4())

workflow = {
    "id": workflow_id,
    "name": "Gemini 3 Flash Test",
    "nodes": [
        {
            "id": webhook_id,
            "name": "Webhook",
            "type": "n8n-nodes-base.webhook",
            "typeVersion": 2,
            "position": [250, 300],
            "parameters": {
                "httpMethod": "POST",
                "path": "gemini-test",
                "responseMode": "lastNode"
            }
        },
        {
            "id": gemini_id,
            "name": "Gemini 3 Flash",
            "type": "@n8n/n8n-nodes-langchain.lmChatGoogleAi",
            "typeVersion": 1,
            "position": [550, 300],
            "credentials": {
                "googleAi": "9233165a-f3b6-4d65-b3f1-82a403ac5c87"
            },
            "parameters": {
                "model": "gemini-3-flash-preview",
                "text": "={{ $json.body.prompt || 'Say hello' }}",
                "options": {
                    "maxTokens": 500,
                    "temperature": 0.7
                }
            }
        },
        {
            "id": respond_id,
            "name": "Respond",
            "type": "n8n-nodes-base.respondToWebhook",
            "typeVersion": 1.1,
            "position": [850, 300],
            "parameters": {
                "respondWith": "json",
                "responseBody": "={{ $json }}"
            }
        }
    ],
    "connections": {
        "Webhook": {
            "main": [[{"node": "Gemini 3 Flash", "type": "main", "index": 0}]]
        },
        "Gemini 3 Flash": {
            "main": [[{"node": "Respond", "type": "main", "index": 0}]]
        }
    },
    "settings": {
        "executionOrder": "v1"
    },
    "active": False,
    "pinData": {}
}

with open(r"C:\Users\ACER\AppData\Local\Temp\n8n-gemini-workflow.json", "w") as f:
    json.dump([workflow], f, indent=2)
print("Workflow ID:", workflow_id)
