#!/usr/bin/env python3
"""Gemini Webhook — thay the n8n workflow Gemini 3 Flash (HTTP)"""
import json, sys, os
from http.server import HTTPServer, BaseHTTPRequestHandler
import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
if not GEMINI_API_KEY:
    print("ERROR: Set GEMINI_API_KEY env var")
    exit(1)
MODEL = "gemini-3-flash-preview"
PORT = 5678

class GeminiHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/webhook/gemini":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'{"error":"not found"}')
            return
        
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        
        try:
            data = json.loads(body)
            prompt = data.get("prompt", "Say hello")
        except:
            prompt = "Say hello"
        
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"
        payload = {"contents": [{"parts": [{"text": prompt}]}]}
        
        try:
            r = requests.post(url, json=payload, timeout=60)
            result = r.json()
            text = result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception as e:
            text = f"Error: {e}"
        
        response = {"response": text}
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(response, ensure_ascii=False).encode("utf-8"))
    
    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
    
    def log_message(self, format, *args):
        sys.stderr.write(f"[GeminiWebhook] {args[0]} {args[1]} {args[2]}\n")

if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", PORT), GeminiHandler)
    print(f"Gemini Webhook running on port {PORT}")
    print(f"POST http://localhost:{PORT}/webhook/gemini")
    server.serve_forever()
