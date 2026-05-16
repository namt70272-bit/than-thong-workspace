import urllib.request, json

# Test SearXNG
try:
    r = urllib.request.urlopen("http://localhost:8888/", timeout=5)
    print("SearXNG running: HTTP", r.getcode())
except Exception as e:
    print("SearXNG NOT running:", str(e)[:80])

# Test search API
url = "http://localhost:8888/search?q=openclaw+ai&format=json"
req = urllib.request.Request(url)
req.add_header("Accept", "application/json")
try:
    r2 = urllib.request.urlopen(req, timeout=10)
    data = json.loads(r2.read().decode())
    results = data.get("results", [])
    print("Search results:", len(results))
    for res in results[:3]:
        print(" -", res.get("title", "?"))
        print("   ", res.get("url", "?"))
except Exception as e:
    print("Search failed:", str(e)[:120])
