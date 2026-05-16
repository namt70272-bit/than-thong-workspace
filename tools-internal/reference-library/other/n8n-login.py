#!/usr/bin/env python3
"""
n8n Login Tool — login UI cho n8n, support Docker
Usage:
  python n8n-login.py http://localhost:5678 admin@n8n.local N8nadmin123!
"""
import sys, os, json, requests
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

N8N_URL = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("N8N_URL", "http://localhost:5678")
EMAIL = sys.argv[2] if len(sys.argv) > 2 else "admin@n8n.local"
PASSWORD = sys.argv[3] if len(sys.argv) > 3 else "N8nadmin123!"

class LoginHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            html = f"""
            <!DOCTYPE html>
            <html>
            <head><meta charset="utf-8"><title>n8n Login</title>
            <style>
                body {{ font-family: sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }}
                input, button {{ width: 100%; padding: 10px; margin: 8px 0; box-sizing: border-box; }}
                button {{ background: #4CAF50; color: white; border: none; cursor: pointer; }}
                .error {{ color: red; }} .success {{ color: green; }}
            </style></head>
            <body>
            <h2>n8n Login</h2>
            <form method="POST">
                <label>n8n URL:</label>
                <input type="text" name="url" value="{N8N_URL}" required>
                <label>Email:</label>
                <input type="text" name="email" value="{EMAIL}" required>
                <label>Password:</label>
                <input type="password" name="password" value="{PASSWORD}" required>
                <button type="submit">Login & Save Cookie</button>
            </form>
            <div id="result"></div>
            </body></html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode()
        params = parse_qs(body)
        url = params.get("url", [N8N_URL])[0]
        email = params.get("email", [EMAIL])[0]
        pwd = params.get("password", [PASSWORD])[0]

        # Attempt setup + login
        result_html = ""
        s = requests.Session()
        try:
            # Try owner setup first
            r1 = s.post(f"{url}/rest/owner/setup", json={
                "firstName": "Admin", "lastName": "n8n",
                "email": email, "password": pwd
            }, timeout=10)
            if r1.status_code == 200:
                result_html += f'<p class="success">Owner setup OK</p>'
        except:
            pass

        try:
            r2 = s.post(f"{url}/rest/login", json={
                "emailOrLdapLoginId": email, "password": pwd
            }, timeout=10)
            if r2.status_code == 200:
                n8n_auth = s.cookies.get("n8n-auth", "")
                if n8n_auth:
                    cookie_path = os.path.expanduser("~/.n8n-cookie.txt")
                    with open(cookie_path, "w") as f:
                        f.write(f"Cookie: n8n-auth={n8n_auth}")
                    result_html += f'<p class="success">Login OK! Cookie saved.</p>'
                    result_html += f'<pre>Cookie: {n8n_auth[:50]}...</pre>'
            else:
                result_html += f'<p class="error">Login failed: {r2.text[:200]}</p>'
        except Exception as e:
            result_html += f'<p class="error">Error: {e}</p>'

        html = f"""<!DOCTYPE html>
        <html><head><meta charset="utf-8"></head>
        <body style="font-family:sans-serif;max-width:600px;margin:20px auto">
        <h3>Login Result</h3>
        {result_html}
        <a href="/">Back</a>
        </body></html>"""
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, format, *args):
        pass

if __name__ == "__main__":
    from sys import argv, stderr
    port = int(os.environ.get("N8N_LOGIN_PORT", 8888))
    server = HTTPServer(("0.0.0.0", port), LoginHandler)
    print(f"n8n Login Tool: http://localhost:{port}")
    print(f"Target: {N8N_URL}")
    print(f"Default: {EMAIL} / {PASSWORD}")
    server.serve_forever()
